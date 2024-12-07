#!/usr/bin/env python3

if __name__ == '__main__':
    # Make sure that this version of trosnoth is run.
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_asyncio_reactor
    declare_this_module_requires_asyncio_reactor()


import argparse
import logging
import os
import sys
import uuid

from twisted.internet import defer, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import ProcessProtocol, Factory, ClientCreator
from twisted.protocols import amp

from trosnoth.const import DEFAULT_BOT_DIFFICULTY
from trosnoth.game import RemoteGame
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.network.client import TrosnothClientProtocol
from trosnoth.network.server import TrosnothServerFactory
from trosnoth.utils.event import Event
from trosnoth.utils.utils import initLogging

log = logging.getLogger(__name__)


LOCALHOST = '127.0.0.1'


class ServerSideBotProcessManager:
    def __init__(self, game, logPrefix, log_file):
        self.game = game
        self.logPrefix = logPrefix
        self.log_file = log_file
        self.process = None
        self.starting = None
        self.token = None
        self.waitForAMPConnection = None
        self.waitForProcessStart = None
        self.amp = None
        self.server = None
        self.joiningAgents = []
        self.stopped = False

    def stop(self):
        self.stopped = True
        if self.server:
            self.server.shutdown()
            self.server = None
        if self.amp:
            self.amp.transport.loseConnection()

    async def startBot(
            self, aiName, fromLevel=False, nick='', team=None, difficulty=DEFAULT_BOT_DIFFICULTY):
        if self.stopped:
            raise RuntimeError('Cannot start bot after game is over')
        if self.server is None:
            self.server = TrosnothServerFactory(
                self.game, noAuth=True, agentCallback=self.agentConnected)
            self.server.startListening(port=0, interface=LOCALHOST)

        await self.ensureProcessHasStarted()

        authTag = len(self.joiningAgents)
        agentHasJoined = defer.Deferred()
        self.joiningAgents.append((agentHasJoined, fromLevel))

        await self.amp.callRemote(
            StartBot, name=aiName, fromLevel=fromLevel, nick=nick or '',
            teamId=team.id if team else NEUTRAL_TEAM_ID,
            authTag=authTag, difficulty=difficulty,
        )
        agent = await agentHasJoined

        return agent

    def agentConnected(self, agent, authTag):
        d, fromLevel = self.joiningAgents[authTag]
        self.joiningAgents[authTag] = None
        while self.joiningAgents and self.joiningAgents[-1] is None:
            self.joiningAgents.pop()
        agent.allowBotPlayer(fromLevel)
        d.callback(agent)

    async def ensureProcessHasStarted(self):
        if self.starting:
            await self.starting.waitOrRaise()
            return
        if self.process:
            return

        success = False
        self.starting = Event(['result'])
        try:
            await self._startProcess()
            success = True
        except Exception as e:
            self.starting.execute(e)
            raise
        else:
            self.starting.execute(None)
        finally:
            self.starting = None
            if not success:
                self.process = None
                self.amp = None

    async def _startProcess(self):
        assert self.process is None
        self.process = BotProcessProtocol(self)
        self.token = uuid.uuid4().hex.encode('ascii')
        self.waitForAMPConnection = defer.Deferred()

        ampFactory = Factory.forProtocol(ArenaSideAMPProtocol)
        ampFactory.manager = self
        ampEndpoint = TCP4ServerEndpoint(reactor, 0)
        listeningPort = await ampEndpoint.listen(ampFactory)
        try:
            ampPort = listeningPort.getHost().port
            cmd = self.getCommand() + [str(ampPort)]
            if self.logPrefix:
                cmd += ['--logPrefix', self.logPrefix]
            if self.log_file:
                cmd += ['--logfile', self.log_file]
            log.info('Running command %r', cmd)
            self.waitForProcessStart = defer.Deferred()
            transport = reactor.spawnProcess(
                self.process, cmd[0], cmd,
                env=None,
                childFDs=None if os.name == 'nt' else {0: 'w', 1: 1, 2: 2})

            try:
                await self.waitForProcessStart
            finally:
                self.waitForProcessStart = None
            self.process.transport.write(self.token + b'\n')
            self.process.transport.closeStdin()

            try:
                self.amp = await self.waitForAMPConnection
            finally:
                self.waitForAMPConnection = None

            await self.amp.callRemote(
                ConnectToServer, port=self.server.port.getHost().port)
        finally:
            listeningPort.stopListening()

    def getCommand(self):
        if getattr(sys, 'frozen', False):
            # Bundled by PyInstaller
            path = os.path.dirname(sys.executable)
            ext = '.exe' if os.name == 'nt' else ''
            return [os.path.join(path, 'support' + ext), 'bots']

        return [sys.executable, __file__]

    def ampConnectionLost(self):
        if self.process:
            log.warning('Lost AMP connection to bot subprocess')
            self.process.killProcess()


class BotProcessProtocol(ProcessProtocol):
    def __init__(self, manager):
        self.manager = manager
        self.exited = False

    def connectionMade(self):
        self.manager.waitForProcessStart.callback(None)

    def processExited(self, reason):
        self.exited = True
        if self.manager.process is self:
            self.manager.process = None
        if self.manager.waitForProcessStart:
            self.manager.waitForProcessStart.errback(reason)
        if self.manager.waitForAMPConnection:
            self.manager.waitForAMPConnection.errback(reason)

    @defer.inlineCallbacks
    def killProcess(self):
        try:
            if self.exited:
                return

            self.transport.signalProcess('TERM')

            for i in range(3):
                d = defer.Deferred()
                reactor.callLater(1, d.callback, None)
                yield d
                if self.exited:
                    return

            self.transport.signalProcess('KILL')
        except Exception:
            log.exception('Error while killing child process')


class Initialise(amp.Command):
    arguments = [
        (b'token', amp.String()),
    ]
    response = []


class ConnectToServer(amp.Command):
    arguments = [
        (b'port', amp.Integer()),
    ]
    response = []


class StartBot(amp.Command):
    arguments = [
        (b'name', amp.Unicode()),
        (b'fromLevel', amp.Boolean()),
        (b'nick', amp.Unicode()),
        (b'teamId', amp.String()),
        (b'authTag', amp.Integer()),
        (b'difficulty', amp.Integer()),
    ]
    response = []


class ArenaSideAMPProtocol(amp.AMP):
    def connectionLost(self, reason):
        self.factory.manager.ampConnectionLost()

    @Initialise.responder
    def initialise(self, token):
        if self.factory.manager.token == token:
            self.factory.manager.waitForAMPConnection.callback(self)
        else:
            self.transport.loseConnection()
        return {}


class BotSideAMPProtocol(amp.AMP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None

    @ConnectToServer.responder
    @defer.inlineCallbacks
    def connectToServer(self, port):
        cc = ClientCreator(reactor, TrosnothClientProtocol)
        client = yield cc.connectTCP(LOCALHOST, port, timeout=10)
        settings = yield client.getSettings()
        client.onConnectionLost.addListener(self.lostServerConnection)

        self.game = RemoteGame()
        client.connectNode(self.game)
        self.game.connected(settings)
        return []

    def lostServerConnection(self, reason=None):
        # On Linux, if we've lost the connection because the parent has
        # died, the reactor will already stop soon, so calling
        # reactor.stop() immediately would result in an exception in the
        # logs. However, if we've lost the connection for any other
        # reason we definitely want to end the process.
        reactor.callLater(0.3, self._stop)

    def _stop(self):
        if reactor.running:
            reactor.stop()

    @StartBot.responder
    @defer.inlineCallbacks
    def startBot(self, name, fromLevel, nick, teamId, authTag, difficulty):
        assert self.game
        team = self.game.world.getTeam(teamId)
        bot = yield self.game.addBot(
            name, team, fromLevel, nick, forceLocal=True, authTag=authTag, difficulty=difficulty)

        return []


def _getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('ampPort', type=int)
    parser.add_argument('--logPrefix', default='', nargs='?')
    parser.add_argument('--logfile', default='', nargs='?')
    return parser


def main():
    args = _getParser().parse_args()
    token = input().encode('ascii')

    log_prefix = args.logPrefix + '-bots' if args.logPrefix else 'bots'
    initLogging(prefix=f'[{log_prefix}]', logFile=args.logfile)

    reactor.callWhenRunning(_twisted_main, args, token)
    reactor.run()


@defer.inlineCallbacks
def _twisted_main(args, token):
    ampProt = yield ClientCreator(reactor, BotSideAMPProtocol).connectTCP(
        LOCALHOST, args.ampPort, timeout=5)
    yield ampProt.callRemote(Initialise, token=token)


if __name__ == '__main__':
    main()

