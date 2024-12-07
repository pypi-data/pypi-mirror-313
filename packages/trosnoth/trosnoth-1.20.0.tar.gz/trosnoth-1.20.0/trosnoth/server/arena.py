#!/usr/bin/env python3

if __name__ == '__main__':
    # Make sure that this version of trosnoth is run.
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_asyncio_reactor
    declare_this_module_requires_asyncio_reactor()

    # Init django environment for database use
    import django
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'trosnoth.server.settings')
    django.setup()


import argparse
import logging
import os
import time

import simplejson
from twisted.internet import defer, reactor
from twisted.internet.error import ConnectionClosed
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp

from trosnoth import data
from trosnoth.djangoapp.models import (
    TrosnothArena, User, TrosnothUser, TrosnothServerSettings,
)
from trosnoth.dbqueue import run_in_synchronous_thread
from trosnoth.game import LocalGame
from trosnoth.gamerecording.stats import ServerGameStats
from trosnoth.levels.base import StandardLobbyLevel, ServerLobbySettings, LevelOptions, HVM_TEAMS
from trosnoth.levels.registry import scenario_class_by_code
from trosnoth.manholehelper import AuthServerManholeHelper
from trosnoth.network.server import TrosnothServerFactory
from trosnoth.server import arenaamp
from trosnoth.utils import twistdebug
from trosnoth.utils.event import Event
from trosnoth.utils.twist import WeakLoopingCall
from trosnoth.utils.utils import initLogging, filename_with_suffix

log = logging.getLogger(__name__)

REPLAY_SUB_PATH = os.path.join(
    'authserver', 'public', 'trosnoth', 'replays')
INITIAL_LOBBY_SIZE = (2, 1)


def startManhole(*args, **kwargs):
    # 2018-01-30 Twisted for Python 3 doesn't yet have manhole support
    try:
        from trosnoth.network.manhole import startManhole as realStart
    except ImportError as e:
        log.warning('Error starting manhole: %s', e)
        return
    realStart(*args, **kwargs)


def startArena(arenaId, ampPort, token, manholePassword=None, log_file=None):
    manager = ArenaManager(arenaId, log_file)
    record = manager.getArenaRecord()
    if not record.enabled:
        raise RuntimeError('This arena is disabled')

    if record.profileSlowCalls:
        log.info('Initialising profiling of slow calls.')
        twistdebug.start(profiling=True)

    namespace = {
        'manager': manager,
        'helper': AuthServerManholeHelper(manager),
    }
    startManhole(0, namespace, manholePassword)

    reactor.callWhenRunning(manager.start, ampPort, token)
    reactor.run()


class AuthTagTracker(object):
    lifetime = 5

    def __init__(self):
        self.tags = {}      # auth tag -> timestamp, username

    def addTag(self, tag, username):
        self.tags[tag] = (time.time(), username)

    def getUsername(self, tag):
        created, username = self.tags.get(tag, (0, None))
        if username is None:
            return None
        if created + self.lifetime < time.time():
            del self.tags[tag]
            return None
        return username

    def clean(self):
        threshold = time.time() - self.lifetime
        for tag, (created, username) in list(self.tags.items()):
            if created < threshold:
                del self.tags[tag]


class ActivityMonitor(object):
    def __init__(self, server, timeout=60):
        self.server = server
        self.timeout = timeout
        self.onInactive = Event([])

        server.onConnectionEstablished.addListener(
            self.gotConnectionEstablished)
        server.onConnectionLost.addListener(self.gotConnectionLost)
        self.timer = None

    def gotConnectionLost(self, protocol):
        self.cancelTimer()
        if not self.server.connectedClients:
            self.timer = reactor.callLater(self.timeout, self.onInactive)

    def gotConnectionEstablished(self, protocol):
        self.cancelTimer()

    def cancelTimer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None



class ArenaManager(object):
    def __init__(self, arenaId, log_file=None):
        self.arenaId = arenaId
        self.log_file = log_file
        self.game = None
        self.server = None
        self.lobbySettings = None
        self.game_stats = None
        self.amp = None
        self.activityMonitor = None
        self.tagTracker = AuthTagTracker()

    def getArenaRecord(self):
        return run_in_synchronous_thread(TrosnothArena.objects.get, id=self.arenaId)

    @defer.inlineCallbacks
    def start(self, ampPort, token):
        WeakLoopingCall(self.tagTracker, 'clean').start(5)

        gamePort = self.getArenaRecord().gamePort

        self.lobbySettings = ServerLobbySettings(self)
        self.game = LocalGame(
            serverInterface=ServerInterface(self),
            saveReplay=True,
            gamePrefix='Server',
            replay_path=data.user_path / REPLAY_SUB_PATH,
            level=StandardLobbyLevel(self.lobbySettings),
            lobbySettings=self.lobbySettings,
            botProcess=True,
            botProcessLogPrefix=self.arenaId,
            bot_process_log_file=filename_with_suffix(self.log_file, '-bots'),
            tweener_can_drive_ticks=False,
        )
        self.server = TrosnothServerFactory(self.game)
        self.server.startListening(gamePort)
        self.activityMonitor = ActivityMonitor(self.server)
        self.activityMonitor.onInactive.addListener(self.gotServerInactive)

        yield self._startAMPConnection(ampPort, token)

        self.game.world.uiOptions.onDefaultUserInfoChange.addListener(
            self.gotUserLevelInfoChange)
        self.game.world.onPlayerAdded.addListener(self.gotPlayerAdded)
        self.game.world.onPlayerRemoved.addListener(self.gotPlayerRemoved)
        self.game.world.on_pause_state_changed.addListener(self.gotPauseChange)
        self.game.world.onStartMatch.addListener(self.gotStartMatch)
        self.game.world.on_end_match.addListener(self.got_end_match)

        log.info('Arena initialised')
        self.sendArenaInfo()

    @defer.inlineCallbacks
    def sendArenaInfo(self):
        # TODO: subscribe to events when these change
        args = {}
        args['status'] = self.game.world.getLevelStatus()
        args['players'] = sum(not p.bot for p in self.game.world.players)
        args['paused'] = self.game.world.paused
        try:
            yield self.amp.callRemote(arenaamp.ArenaInfoChanged, **args)
        except ConnectionClosed:
            pass

    def gotServerInactive(self):
        log.error('Shutting down due to inactivity')
        if reactor.running:
            reactor.stop()

    def gotUserLevelInfoChange(self, *args, **kwargs):
        self.sendArenaInfo()

    def gotPlayerAdded(self, *args, **kwargs):
        self.sendArenaInfo()

    def gotPlayerRemoved(self, *args, **kwargs):
        self.sendArenaInfo()

    def gotPauseChange(self, *args, **kwargs):
        self.sendArenaInfo()

    def gotStartMatch(self, *args, **kwargs):
        self.sendArenaInfo()
        if self.game.world.scenarioManager.level.recordGame:
            self.game_stats = ServerGameStats(self.game, self.arenaId)

    def got_end_match(self, level_result):
        if self.game_stats:
            self.game_stats.stop(level_result)
            self.game_stats = None

    @defer.inlineCallbacks
    def _startAMPConnection(self, ampPort, token, host='127.0.0.1'):
        self.amp = yield ClientCreator(
            reactor, AuthAMPProtocol, self).connectTCP(
            host, ampPort, timeout=5)
        yield self.amp.callRemote(arenaamp.ArenaListening, token=token)


class ServerInterface(object):
    def __init__(self, arenaManager):
        self._arenaManager = arenaManager

    def getUserFromAuthTag(self, authTag):
        username = self._arenaManager.tagTracker.getUsername(authTag)
        if username:
            return TrosnothUser.from_user(username=username)
        return None

    def checkUsername(self, username):
        try:
            run_in_synchronous_thread(TrosnothUser.from_user, username=username)
        except User.DoesNotExist:
            return False
        return True

    def getElephantName(self):
        settings = run_in_synchronous_thread(TrosnothServerSettings.get)
        return settings.elephantName

    def get_machines_difficulty(self):
        arena = self._arenaManager.getArenaRecord()
        return arena.machines_difficulty

    def get_machines_bot_name(self):
        arena = self._arenaManager.getArenaRecord()
        return arena.machines_bot_kind

    def get_balance_bot_difficulty(self):
        arena = self._arenaManager.getArenaRecord()
        return arena.balance_bot_difficulty

    def get_balance_bot_name(self):
        arena = self._arenaManager.getArenaRecord()
        return arena.balance_bot_kind or 'balance'

    def get_extra_bot_count(self):
        arena = self._arenaManager.getArenaRecord()
        return arena.extra_bot_count


class AuthAMPProtocol(amp.AMP):
    '''
    Connects to authserver.ArenaAMPProtocol.
    '''

    def __init__(self, arenaManager, *args, **kwargs):
        super(AuthAMPProtocol, self).__init__(*args, **kwargs)
        self.arenaManager = arenaManager

    @arenaamp.RegisterAuthTag.responder
    def registerAuthTag(self, username, auth_tag):
        self.arenaManager.tagTracker.addTag(auth_tag, username)
        return {}

    @arenaamp.SetArenaInfo.responder
    def setArenaInfo(self, paused=None, teamAbilityJSON=None, action=None):
        world = self.arenaManager.game.world
        if paused is not None:
            if paused ^ world.paused:
                world.pauseOrResumeGame()
        if teamAbilityJSON is not None:
            for teamIndex, abilities in simplejson.loads(
                    teamAbilityJSON).items():
                team = world.teams[int(teamIndex)]
                if 'caps' in abilities:
                    team.abilities.set(zoneCaps=abilities['caps'])
                if 'shots' in abilities:
                    team.abilities.set(aggression=abilities['shots'])

        if action == 'lobby':
            world = self.arenaManager.game.world
            world.returnToLobby()

        return {}

    @arenaamp.StartLevel.responder
    def startLevel(self, infoJSON):
        level_info = simplejson.loads(infoJSON)
        log.error(f'{level_info=}')

        level_class = scenario_class_by_code[level_info['scenario']]
        duration = level_info.get('duration')
        if duration is not None:
            duration *= 60

        map_index_by_code = {
            map_class.code: i for i, map_class in enumerate(level_class.map_selection)}
        level_options = LevelOptions(
            duration=duration,
            team_option_index=level_class.team_selection.index(level_info['teams']),
            map_index=map_index_by_code[level_info['size']],
        )
        if level_info.get('teams') == HVM_TEAMS:
            level_options.team_option_index = level_class.team_selection.index(HVM_TEAMS)

        level = level_class(level_options=level_options)

        self.arenaManager.game.world.scenarioManager.startLevel(level)
        return {}


def getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('arenaId')
    parser.add_argument('ampPort', type=int)
    parser.add_argument(
        '--profile', action='store_true',
        help='dump kcachegrind profiling data to arena?.log')
    parser.add_argument(
        '--password', action='store', dest='manholePassword', default=None,
        help='the password to use for the manhole')
    parser.add_argument('--logfile', action='store', default=None)
    return parser


def main():
    parser = getParser()
    args = parser.parse_args()
    token = input().encode('ascii')

    prefix = f'[{args.arenaId}]'
    logfile_name = filename_with_suffix(args.logfile, args.arenaId)
    initLogging(logFile=logfile_name, prefix=prefix)

    if args.profile:
        from trosnoth.utils.profiling import profilingOutput
        with profilingOutput('arena{}.log'.format(args.arenaId)):
            startArena(args.arenaId, args.ampPort, token, args.manholePassword, logfile_name)
    else:
        startArena(args.arenaId, args.ampPort, token, args.manholePassword, logfile_name)


if __name__ == '__main__':
    main()
