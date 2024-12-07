from trosnoth import qtreactor

qtreactor.declare_this_module_requires_asyncio_reactor()

from asgiref.sync import sync_to_async
import datetime
import functools
from hashlib import sha1
import logging
import os
import random
import string
import sys
import uuid
import webbrowser

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from django.contrib.auth import authenticate
from django.core import management
import simplejson
from twisted.internet import reactor, defer
from twisted.internet.error import CannotListenError
from twisted.internet.protocol import (
    Factory, ProcessProtocol, DatagramProtocol,
)
from twisted.internet.ssl import PrivateCertificate, KeyPair, DistinguishedName
from twisted.protocols import amp
from twisted.python.failure import Failure

from trosnoth import dbqueue, version
from trosnoth.dbqueue import run_in_synchronous_thread, in_synchronous_thread
from trosnoth.const import MULTICAST_PROTOCOL_NAME
from trosnoth.djangoapp.models import (
    User, TrosnothUser, TrosnothArena, TrosnothServerSettings,
)
from trosnoth.network import authcommands
from trosnoth.network.networkDefines import (
    multicastGroup, multicastPort,
)
from trosnoth.server import arenaamp
from trosnoth.utils.aio import return_deferred
from trosnoth.utils.event import Event
from trosnoth.utils.utils import initLogging
from trosnoth.web.server import startWebServer

log = logging.getLogger(__name__)

MAX_GAMES = 1
USERNAME_CHARACTERS = string.ascii_lowercase + string.digits


def startManhole(*args, **kwargs):
    # Manhole is non-essential so don't explode if we're using a Twisted version that doesn't have it
    try:
        from trosnoth.network.manhole import startManhole as realStart
    except ImportError as e:
        log.warning('Error starting manhole: %s', e)
        return
    realStart(*args, **kwargs)


class AuthenticationProtocol(amp.AMP):
    '''
    Trosnoth authentication server which is used when running a game server
    which keeps track of users.
    '''

    def connectionMade(self):
        super(AuthenticationProtocol, self).connectionMade()
        self.user = None
        self.token = None
        log.info('New connection.')

    def connectionLost(self, reason):
        log.info('Connection lost.')

    @authcommands.GetServerInfo.responder
    def get_server_info(self):
        settings = run_in_synchronous_thread(TrosnothServerSettings.get)
        return {
            'name': settings.serverName,
            'version': version.version,
        }

    @authcommands.ListGames.responder
    @return_deferred
    async def list_games(self):
        result = {
            'games': [{
                'id': arena.id,
                'name': arena.name,
            } async for arena in TrosnothArena.objects.all() if arena.enabled]
        }
        return result

    @authcommands.ConnectToGame.responder
    @defer.inlineCallbacks
    def connectToGame(self, game_id, spectate):
        if self.user is None and not spectate:
            raise authcommands.NotAuthenticated()

        try:
            arena_proxy = yield self.factory.getArena(game_id, start=True)
        except (TrosnothArena.DoesNotExist, GameIsDisabled):
            raise authcommands.GameDoesNotExist()

        if self.user is None:
            defer.returnValue({'port': arena_proxy.port})
        else:
            auth_tag = random.randrange(2**64)
            yield arena_proxy.amp.callRemote(
                arenaamp.RegisterAuthTag,
                username=self.user.username, auth_tag=auth_tag)
            nick = self.user.getNick()

            defer.returnValue({
                'port': arena_proxy.port,
                'auth_tag': auth_tag,
                'nick': nick,
            })

    @authcommands.GetAuthSettings.responder
    def get_auth_settings(self):
        return {
            'account_creation': self.are_new_users_allowed(),
        }

    def are_new_users_allowed(self):
        # TODO: make this a setting in the web interface
        return True

    @authcommands.PasswordAuthenticate.responder
    @defer.inlineCallbacks
    def password_authenticate(self, username, password):
        try:
            user = yield self.factory.authManager.authenticate_user(username, password)
        except Exception as e:
            log.info(f'Error while authenticating: {e}')
            return {'result': False, 'token': b''}
        self.user = user
        return {
            'result': True,
            'token': self.factory.build_token(username),
        }

    @authcommands.TokenAuthenticate.responder
    def token_authenticate(self, username, token):
        try:
            user = self.factory.check_token(username, token)
        except Exception as e:
            log.info(f'Error while checking token: {e}')
            user = None

        if user is None:
            return {'result': False, 'token': b''}

        self.user = user
        return {'result': True, 'token': self.factory.build_token(username)}

    @authcommands.LocalUsername.responder
    def gotClientUsername(self, username):
        user = self.factory.authManager.noteClientUsername(username)
        if user:
            self.user = user
        return {}

    @authcommands.CreateUserWithPassword.responder
    def create_user_with_password(self, username, password):
        if not self.are_new_users_allowed():
            return {'error': 'This is a private server', 'token': b''}

        nick = username
        username = username.lower()

        auth_manager = self.factory.authManager
        if auth_manager.checkUsername(username):
            return {'error': 'That username is taken.', 'token': b''}
        try:
            self.user = auth_manager.createUser(username, password, nick)
        except ValueError as e:
            return {'error': str(e), 'token': b''}
        return {
            'error': '',
            'token': self.factory.build_token(username),
        }


class AuthManager(object):
    '''
    Manages user accounts on the system.
    '''

    def __init__(self):
        self.tags = {}      # auth tag -> user id

    def checkUsername(self, username):
        '''
        Returns True or False, depending on whether the given username is
        already in use.
        '''
        try:
            TrosnothUser.from_user(username=username)
        except User.DoesNotExist:
            return False
        return True

    def noteClientUsername(self, username):
        '''
        Do nothing, unless the "Trust client usernames" setting is switched on.
        Returns a Trosnoth user, or None.
        '''
        settings = run_in_synchronous_thread(TrosnothServerSettings.get)
        if not settings.trustClientUsernames:
            return None

        return self.get_or_create_by_username(username)

    def get_or_create_by_username(self, username):
        username = username.lower()
        try:
            trosnothUser = TrosnothUser.from_user(username=username)
        except User.DoesNotExist:
            user = self.createUser(username, None)
        else:
            if not trosnothUser.user.is_active:
                return None
            user = AuthenticatedUser(self, username)

        user.seen()
        return user

    @return_deferred
    async def authenticate_user(self, username, password):
        '''
        If a username exists with the given password, returns the user,
        otherwise raises an exception.
        '''
        username = username.lower()
        try:
            trosnothUser = TrosnothUser.from_user(username=username)
        except User.DoesNotExist:
            raise

        if not trosnothUser.oldPasswordHash:
            # Just use Django auth
            try:
                djangoUser = await sync_to_async(authenticate)(
                    username=username, password=password)
            except Exception as e:
                log.exception(e)
                raise
            if djangoUser is None:
                raise ValueError('Authentication failed')
            if not djangoUser.is_active:
                raise ValueError('User deactivated')
            user = AuthenticatedUser(self, username)
        else:
            # Old Trosnoth auth, only exists for backward compatibility
            hash1 = sha1(b'Trosnoth' + password.encode('utf-8')).digest()
            hash2 = bytes(trosnothUser.oldPasswordHash)
            if hash1 != hash2:
                raise ValueError('Incorrect password')

            # Put the password into Django
            trosnothUser.user.set_password(password)
            trosnothUser.user.save()
            trosnothUser.oldPasswordHash = b''
            trosnothUser.save()

            user = AuthenticatedUser(self, username)

        user.seen()
        return user

    @in_synchronous_thread
    def createUser(self, username, password, nick=None):
        username = username.lower()
        if any(c not in USERNAME_CHARACTERS for c in username):
            raise ValueError('Username includes an invalid character')
        if self.checkUsername(username):
            raise ValueError('user %r already exists' % (username,))
        if not password:
            raise ValueError('Password cannot be blank')
        User.objects.create_user(username, password=password)

        user = AuthenticatedUser(self, username)
        user.setPassword(password)
        user.seen()
        if nick is not None:
            user.setNick(nick)
        return user

    def getNick(self, username):
        return run_in_synchronous_thread(TrosnothUser.from_user, username=username).nick


class AuthenticationFactory(Factory):
    protocol = AuthenticationProtocol
    authManagerClass = AuthManager
    instance = None

    def __init__(self, private_certificate, manholePassword=None, logfile=None):
        self.manholePassword = manholePassword
        self.logfile = logfile

        self.authManager = self.authManagerClass()
        self.private_key = private_certificate.privateKey.original.to_cryptography_key()
        self.arenaProxies = {}
        self.arenaAMPListener = None
        self.adminTokens = set()

        self.onArenaStarting = Event(['proxy'])
        self.onArenaStopped = Event(['proxy'])

        AuthenticationFactory.instance = self

    def build_token(self, username, now=None):
        if now is None:
            now = datetime.datetime.utcnow()
        now_data = now.strftime('%Y%m%d%H%M%S').encode('ascii')
        token_data = now_data + username.encode('utf-8')
        return now_data + self.private_key.sign(
            token_data,
            padding.PSS(padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())

    def check_token(self, username, token, not_before=None, not_after=None):
        if not_after is None:
            not_after = datetime.datetime.utcnow()
        if not_before is None:
            not_before = not_after - datetime.timedelta(days=365)

        issued_data, signature = token[:14], token[14:]
        issued = datetime.datetime.strptime(issued_data.decode('utf-8'), '%Y%m%d%H%M%S')
        if not not_before <= issued <= not_after:
            return None

        token_data = issued_data + username.encode('utf-8')
        try:
            self.private_key.public_key().verify(
                signature, token_data,
                padding.PSS(padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
        except InvalidSignature:
            return None
        return self.authManager.get_or_create_by_username(username)

    @defer.inlineCallbacks
    def getArena(self, arenaId, start=False):
        if not isinstance(arenaId, int):
            raise TypeError(
                'Expected numeric arenaId, not {!r}'.format(arenaId))
        try:
            result = self.arenaProxies[arenaId]
        except KeyError:
            if not start:
                raise
            result = ArenaProcessProtocol(
                arenaId, token=self.getNewArenaToken(),
                log_file=self.logfile,
            )
            if not result.processDied:
                self.arenaProxies[arenaId] = result
                result.onExit.addListener(self._arenaExited)
                self.onArenaStarting(result)
            log.error('Starting arena #%s', arenaId)
            yield result.start(self.getArenaAMPPort(), self.manholePassword)
        else:
            if not result.ready:
                yield result.onReady.waitOrRaise()
        defer.returnValue(result)

    def _arenaExited(self, proxy, reason):
        log.error('Arena #%s exited', proxy.arenaId)
        if self.arenaProxies.get(proxy.arenaId):
            del self.arenaProxies[proxy.arenaId]
            self.onArenaStopped(proxy)
        proxy.onExit.removeListener(self._arenaExited)

    @defer.inlineCallbacks
    def teardown(self):
        # Give a fraction of a second for the message to get through
        # the the children have ended, then send a kill signal.
        d = defer.Deferred()
        reactor.callLater(0.1, d.callback, None)
        yield d

        yield defer.DeferredList([
            p.killProcess() for p in list(self.arenaProxies.values())])

    def getNewArenaToken(self):
        if self.arenaAMPListener is None or \
                self.arenaAMPListener.disconnecting:
            self.startArenaAMPListener()
        return uuid.uuid4().hex.encode('ascii')

    def matchArenaToken(self, ampProtocol, token):
        for arenaProxy in list(self.arenaProxies.values()):
            if arenaProxy.token and arenaProxy.token == token:
                ampProtocol.arena = arenaProxy
                arenaProxy.matchedToken(ampProtocol)
                if not any(p.token for p in list(self.arenaProxies.values())):
                    self.stopArenaAMPListener()
                return True
        return False

    def getArenaAMPPort(self):
        return self.arenaAMPListener.getHost().port

    def startArenaAMPListener(self, port=0, interface='127.0.0.1'):
        factory = Factory.forProtocol(ArenaAMPProtocol)
        factory.authFactory = self
        self.arenaAMPListener = reactor.listenTCP(
            port, factory, interface=interface)
        factory.stopFactory = functools.partial(
            self._arenaAMPFactoryStopped, self.arenaAMPListener)

    def stopArenaAMPListener(self):
        if self.arenaAMPListener and not self.arenaAMPListener.disconnecting:
            self.arenaAMPListener.stopListening()

    def _arenaAMPFactoryStopped(self, listener):
        if listener == self.arenaAMPListener:
            self.arenaAMPListener = None

    @defer.inlineCallbacks
    def getArenaInfo(self, arenaId):
        try:
            arena = yield self.getArena(arenaId)
        except KeyError:
            arenaRecord = run_in_synchronous_thread(TrosnothArena.objects.get, id=arenaId)
            if not arenaRecord.enabled:
                status = 'DISABLED'
            else:
                status = 'not running'

            defer.returnValue({
                'status': status,
                'paused': False,
                'players': 0,
                'blue': {'shots': True, 'caps': True},
                'red': {'shots': True, 'caps': True},
            })

        defer.returnValue({
            'status': arena.status,
            'paused': arena.paused,
            'players': arena.players,
            'blue': arena.teamInfo[0],
            'red': arena.teamInfo[1],
        })

    @defer.inlineCallbacks
    def setArenaInfo(self, arenaId, info):
        try:
            arena = yield self.getArena(arenaId)
        except KeyError:
            return

        if info.get('action') == 'shutdown':
            yield arena.killProcess()
            return

        yield arena.setInfo(info)

    @defer.inlineCallbacks
    def startLevel(self, arenaId, levelInfo):
        try:
            arena = yield self.getArena(arenaId)
        except KeyError:
            return

        yield arena.amp.callRemote(
            arenaamp.StartLevel,
            infoJSON=simplejson.dumps(levelInfo),
        )

    def getAdminToken(self):
        token = uuid.uuid4().hex
        self.adminTokens.add(token)
        return token

    def revokeAdminToken(self, token):
        self.adminTokens.discard(token)

    def useAdminToken(self, token):
        if token not in self.adminTokens:
            return False
        self.revokeAdminToken(token)
        return True


class GameIsDisabled(Exception):
    pass


class ArenaProcessProtocol(ProcessProtocol):
    def __init__(self, arenaId, token, log_file):
        self.arenaId = arenaId
        self.token = token
        self.log_file = log_file
        self.amp = None
        self.port = None
        self.processDied = False
        self.startCalled = False
        self.ready = False
        self.onReady = Event(['result'])
        self.onExit = Event(['protocol', 'reason'])
        self.onInfoChanged = Event(['proxy'])

        self.status = 'starting up...'
        self.players = 0
        self.paused = False
        self.teamInfo = [
            {'shots': True, 'caps': True},
            {'shots': True, 'caps': True},
        ]

    def start(self, ampPort, manholePassword=None):
        if self.startCalled:
            raise RuntimeError('Cannot start ArenaProcessProtocol twice')
        self.startCalled = True
        result = self.onReady.waitOrRaise()

        arena_record = run_in_synchronous_thread(TrosnothArena.objects.get, id=self.arenaId)
        if not arena_record.enabled:
            raise GameIsDisabled('This arena is disabled')
        self.port = arena_record.gamePort

        cmd = self.getArenaCommand() + [str(self.arenaId), str(ampPort)]
        if manholePassword:
            cmd.extend(['--password', manholePassword])
        if self.log_file:
            cmd.extend(['--logfile', self.log_file])
        reactor.spawnProcess(
            self, cmd[0], cmd, env=None,
            childFDs=None if os.name == 'nt' else {0: 'w', 1: 1, 2: 2})
        return result

    def recordInfoChange(self, status=None, players=None, paused=None):
        if status is not None:
            self.status = status
        if players is not None:
            self.players = players
        if paused is not None:
            self.paused = paused
        self.onInfoChanged(self)

    @defer.inlineCallbacks
    def setInfo(self, info):
        teams = {'blue': 0, 'red': 1}
        teamAbilities = {}
        for team, abilities in info['teamAbilities'].items():
            teamIndex = teams[team]
            teamAbilities[teamIndex] = abilities
            self.teamInfo[teamIndex].update(abilities)
        yield self.amp.callRemote(
            arenaamp.SetArenaInfo,
            paused=info['paused'],
            teamAbilityJSON=simplejson.dumps(teamAbilities),
            action=info['action'],
        )

    @staticmethod
    def getArenaCommand():
        if getattr(sys, 'frozen', False):
            # Bundled by PyInstaller
            path = os.path.dirname(sys.executable)
            ext = '.exe' if os.name == 'nt' else ''
            return [os.path.join(path, 'support' + ext), 'arena']

        import trosnoth.server
        path = os.path.dirname(trosnoth.server.__file__)
        return [sys.executable, os.path.join(path, 'arena.py')]

    def matchedToken(self, ampProtocol):
        if self.processDied:
            return
        self.token = None
        self.amp = ampProtocol
        self.ready = True
        self.onReady(None)

    @defer.inlineCallbacks
    def connectionMade(self):
        self.processDied = False
        self.ready = False
        self.transport.write(self.token + b'\n')

        for i in range(30):
            d = defer.Deferred()
            reactor.callLater(0.5, d.callback, None)
            yield d

            if self.ready:
                return
            if self.processDied:
                break

        self.killProcess()

        self.onReady(Failure(
            RuntimeError('Child process did not complete initialisation')))

    @defer.inlineCallbacks
    def killProcess(self):
        try:
            if self.processDied:
                return

            self.transport.signalProcess('TERM')

            for i in range(3):
                d = defer.Deferred()
                reactor.callLater(1, d.callback, None)
                yield d
                if self.processDied:
                    return

            self.transport.signalProcess('KILL')
        except Exception:
            log.exception('Error while killing child process')

    def ampConnectionLost(self):
        if not self.processDied:
            log.warning('Lost AMP connection to arena #%s', self.arenaId)
            self.killProcess()

    def processExited(self, reason):
        self.processDied = True
        self.onExit(self, reason)


class ArenaAMPProtocol(amp.AMP):
    '''
    Local AMP connection from Arena process.
    '''
    arena = None

    def connectionMade(self):
        super(ArenaAMPProtocol, self).connectionMade()
        self.authFactory = self.factory.authFactory

    def connectionLost(self, reason):
        if self.arena:
            self.arena.ampConnectionLost()

    def locateResponder(self, name):
        '''
        Overriden to refuse all commands that arrive before ArenaListening.
        '''
        if self.arena is not None:
            # Pass through to super from now on.
            self.locateResponder = super(ArenaAMPProtocol, self).locateResponder
            return self.locateResponder(name)
        if name == b'ArenaListening':
            return super(ArenaAMPProtocol, self).locateResponder(name)
        return self.notYetListening

    def notYetListening(self, *args, **kwargs):
        raise arenaamp.NotYetListening()

    @arenaamp.ArenaListening.responder
    def arenaListening(self, token):
        if self.arena:
            raise arenaamp.AlreadyCalled()
        if not self.authFactory.matchArenaToken(self, token):
            self.transport.loseConnection()
        return {}

    @arenaamp.ArenaInfoChanged.responder
    def arenaInfoChanged(self, status=None, players=None, paused=None):
        self.arena.recordInfoChange(status, players, paused)
        return {}


class AuthenticatedUser(object):
    '''
    Represents a user which has been authenticated on the system.
    '''

    def __init__(self, authManager, username):
        self.authManager = authManager
        self.username = username = username.lower()

    def __eq__(self, other):
        if (isinstance(other, AuthenticatedUser) and other.username ==
                self.username):
            return True
        return False

    def __hash__(self):
        return hash(self.username)

    def getNick(self):
        return TrosnothUser.from_user(username=self.username).nick

    def setNick(self, nick):
        @dbqueue.add
        async def write_nick_to_db():
            user = await TrosnothUser.a_from_user(username=self.username)
            if nick != user.nick:
                user.nick = nick
                await sync_to_async(user.save)()

    def setPassword(self, password):
        # Don't put DB write in a queue as user will expect it to take place
        # immediately.
        user = run_in_synchronous_thread(User.objects.get, username=self.username)
        user.set_password(password)
        run_in_synchronous_thread(user.save)
        trosnothUser = TrosnothUser.from_user(pk=user.pk)
        trosnothUser.oldPasswordHash = b''
        trosnothUser.save()

    def seen(self):
        now = datetime.datetime.now()

        @dbqueue.add
        async def write_seen_time_to_db():
            user = await TrosnothUser.a_from_user(username=self.username)
            user.lastSeen = now
            await sync_to_async(user.save)()


def load_or_create_tls_certificate(settings):
    if settings.tls_certificate is not None:
        return PrivateCertificate.loadPEM(settings.tls_certificate)

    keys = KeyPair.generate(size=2048)
    distinguished_name = DistinguishedName(commonName='trosnoth-server')
    cert_request = keys.certificateRequest(distinguished_name)
    cert_data = keys.signCertificateRequest(distinguished_name, cert_request, lambda dn: True, 1)
    certificate = keys.newCertificate(cert_data)
    settings.tls_certificate = certificate.dumpPEM()
    settings.save()
    return certificate


command_line_log_file = None


def start_server(browser=False, safemode=False, web_port=None, logfile=None):
    global command_line_log_file
    command_line_log_file = logfile

    # Ensure that any database migrations have happened
    management.call_command('migrate')

    # Load settings from database
    settings = run_in_synchronous_thread(TrosnothServerSettings.get)
    if safemode:
        auth_port = 0
        manholePort = None
        web_port = web_port or 0
    else:
        auth_port = settings.serverPort
        manholePort = settings.manholePort
        web_port = web_port or settings.webPort

    manholePassword = settings.manholePassword
    certificate = load_or_create_tls_certificate(settings)

    pf = AuthenticationFactory(certificate, manholePassword, logfile)

    if manholePort is not None:
        namespace = {'authFactory': pf}
        startManhole(
            manholePort, namespace, manholePassword,
            authorised_keys=settings.manhole_authorised_keys,
        )

    listeningPort = startWebServer(pf, web_port)
    log.warning('Started web server on port %d', listeningPort.getHost().port)
    if browser:
        reactor.callWhenRunning(openBrowser, pf, listeningPort)


    try:
        listeningPort = reactor.listenSSL(auth_port, pf, certificate.options())
    except CannotListenError:
        log.error('Error listening on port %d.', auth_port)
    else:
        log.warning(
            'Started Trosnoth authentication server on port %d.',
            listeningPort.getHost().port)

        start_multicast_listener(listeningPort.getHost().port)
        reactor.addSystemEventTrigger('before', 'shutdown', pf.teardown)
        reactor.run()


def start_multicast_listener(auth_port):
    listener = MulticastListener(auth_port)
    try:
        port = reactor.listenMulticast(multicastPort, listener)
    except CannotListenError:
        log.error(
            'Could not listen on multicast port to publicise server on LAN.')
        return

    log.warning('Started multicast listener.')
    reactor.addSystemEventTrigger('before', 'shutdown', port.stopListening)


class MulticastListener(DatagramProtocol):
    def __init__(self, auth_port):
        self.auth_port = auth_port

    def startProtocol(self):
        # Join the correct multicast group.
        self.transport.joinGroup(multicastGroup)

    def datagramReceived(self, datagram, address):
        if datagram == b'%s:GetServer' % (MULTICAST_PROTOCOL_NAME,):
            self.transport.write(b'%s:Server:%s' % (
                MULTICAST_PROTOCOL_NAME,
                simplejson.dumps(self.auth_port).encode(),
            ), address)


def openBrowser(authFactory, listeningPort):
    log.warning('Opening web browser...')
    token = authFactory.getAdminToken()
    if not webbrowser.open('http://127.0.0.1:{}/tokenauth?token={}'.format(
            listeningPort.getHost().port, token)):
        log.error('Could not open web browser!')
        authFactory.revokeAdminToken(token)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Trosnoth server')
    parser.add_argument(
        '-d', '--debug', action='store_true', dest='debug',
        help='show debug-level messages on console')
    parser.add_argument(
        '-l', '--log-file', action='store', dest='logFile',
        help='file to write logs to')
    parser.add_argument(
        '--profile', action='store_true', dest='profile',
        help='dump kcachegrind profiling data to trosnoth.log')
    parser.add_argument(
        '--no-browser', action='store_false', dest='browser',
        help='do not attempt to launch a web browser for the UI')
    parser.add_argument(
        '--safemode', action='store_true',
        help='use safe values for all start-up settings')
    parser.add_argument(
        '--web-port', type=int, default=None,
        help='ignore server configuration and launch the web interface on this port instead '
    )

    options = parser.parse_args()

    initLogging(options.debug, options.logFile)

    kwargs = dict(
        browser=options.browser,
        safemode=options.safemode,
        web_port=options.web_port,
        logfile=options.logFile,
    )

    if options.profile:
        runWithProfiling(**kwargs)
    else:
        start_server(**kwargs)


def runWithProfiling(**kwargs):
    import cProfile
    from trosnoth.utils.profiling import KCacheGrindOutputter
    prof = cProfile.Profile()

    try:
        prof.runcall(start_server, **kwargs)
    except SystemExit:
        pass
    finally:
        kg = KCacheGrindOutputter(prof)
        with open('server.log', 'wb') as f:
            kg.output(f)



if __name__ == '__main__':
    main()
