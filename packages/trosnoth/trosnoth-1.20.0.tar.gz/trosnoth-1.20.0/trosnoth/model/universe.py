'''universe.py - defines anything that has to do with the running of the
universe. This includes players, shots, zones, and the level itself.'''
import asyncio
import cProfile
import heapq
import io
import logging
from contextlib import contextmanager
from math import sin, cos
import pstats
import random
import types
from typing import Iterable, Optional

import simplejson
from twisted.internet import defer, reactor

from trosnoth.const import (
    TROSBALL_DEATH_HIT, SHOXWAVE_HIT, GRENADE_HIT,
    COLLECTABLE_COIN_LIFETIME, TICK_PERIOD,
    MAX_PLAYER_NAME_LENGTH, BOMBER_DEATH_HIT, COINS_PER_KILL,
    FRONT_LINE_NORMAL, FRONT_LINE_TROSBALL, BOT_GOAL_NONE,
    SHOXWAVE_RADIUS, ZONE_CAP_DISTANCE, TEAM_1_COLOUR, TEAM_2_COLOUR,
    DEFAULT_ELEPHANT_NAME, DISCONNECT_IDLE_GHOST_AFTER,
)
from trosnoth.gui.app import JitterLogger
from trosnoth.levels.base import LobbyLevel, Level, LevelResult
from trosnoth.model.idmanager import IdManager
from trosnoth.model.macguffins import MacGuffinManager, MacGuffin
from trosnoth.model.projectile import MineProjectile
from trosnoth.model.settingsmanager import SettingsSynchroniser
from trosnoth.model.unit import InteractingUnit
from trosnoth.model.upgrades import upgradeOfType, allUpgrades, Shoxwave
from trosnoth.model.physics import WorldPhysics

from trosnoth.model.map import MapLayout, MapState, RoomCollectionProxy
from trosnoth.model.player import Player, PlayerGuns
from trosnoth.model.coin import CollectableCoin
from trosnoth.model.shot import Shot, GrenadeShot
from trosnoth.model.team import Team
from trosnoth.model.trosball import Trosball
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID, NO_PLAYER
from trosnoth.model.utils import Rect

from trosnoth.utils import globaldebug
from trosnoth.utils.aio import as_future, cancel_task, delay_so_messages_will_apply_immediately
from trosnoth.utils.event import Event
from trosnoth.utils.math import distance
from trosnoth.utils.message import MessageConsumer
from trosnoth.utils.twist import WeakCallLater
from trosnoth.utils.unrepr import unrepr
from trosnoth.utils.utils import timeNow
from trosnoth.messages import (
    TaggingZoneMsg, RespawnMsg, ChatFromServerMsg, PlaySoundMsg,
    RemovePlayerMsg, PlayerHitMsg,
    AddPlayerMsg, PlayerCoinsSpentMsg, ZoneStateMsg,
    WorldResetMsg, UpdateClockStateMsg, SetPlayerCoinsMsg, WorldLoadingMsg,
    CreateCollectableCoinMsg, RemoveCollectableCoinMsg,
    FireShoxwaveMsg, UpgradeChangedMsg, SetTeamScoreMsg, SetPlayerScoreMsg,
    PlayerHasTrosballMsg, TrosballPositionMsg, AwardPlayerCoinMsg,
    TickMsg, SetUIOptionsMsg,
    TICK_LIMIT, UpdateScoreBoardModeMsg,
    SetWorldAbilitiesMsg, PauseOrResumeMsg, ScenarioCompleteMsg,
)
import collections.abc

log = logging.getLogger(__name__)

PROFILE_LONG_TICKS = False


class DelayedCall(object):
    def __init__(self, when, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False
        self.when = when

    def cancel(self):
        self.cancelled = True

    def __eq__(self, other):
        return self.when == other.when

    def __ne__(self, other):
        return self.when != other.when

    def __lt__(self, other):
        return self.when < other.when

    def __le__(self, other):
        return self.when <= other.when

    def __gt__(self, other):
        return self.when > other.when

    def __ge__(self, other):
        return self.when >= other.when


class UnknownMapLayouts(Exception):
    def __init__(self, *args):
        super(UnknownMapLayouts, self).__init__(*args)
        self.keys = str(self)


class LongTickProfiler:
    def __init__(self):
        self.last_time = None
        self.profiler = None

    def note_gap(self):
        '''
        Called when there's a pause, etc., so the next observation
        should be discarded.
        '''
        if self.profiler:
            self.profiler.disable()
        self.profiler = None
        self.last_time = None

    def observation(self, expected_tick_length):
        now = timeNow()
        if self.profiler:
            self.profiler.disable()

            actual_tick_length = now - self.last_time
            if actual_tick_length > 1.5 * expected_tick_length:
                stream = io.StringIO()
                ps = pstats.Stats(self.profiler, stream=stream).sort_stats('cumulative')
                ps.print_stats(25)
                log.error('Long tick: %.3f s', actual_tick_length)
                log.error(stream.getvalue())

        self.last_time = now
        self.profiler = cProfile.Profile()
        self.profiler.enable()


class ScoreBoardBase(object):
    '''
    Synchronises scores for teams and for individual players, if scores make
    sense for the current level.
    '''

    def __init__(self, world):
        self.world = world
        self.teamScoresEnabled = False
        self.playerScoresEnabled = False
        self.teamScores = {t: 0 for t in world.teams}
        self.playerScores = {p: 0 for p in world.players}
        self.on_change = Event(['target', 'new_score'])
        world.onPlayerAdded.addListener(self._playerWasAdded)
        world.onPlayerRemoved.addListener(self._playerWasRemoved)

    def stop(self):
        self.world.onPlayerAdded.removeListener(self._playerWasAdded)
        self.world.onPlayerRemoved.removeListener(self._playerWasRemoved)

    def dumpState(self):
        return {
            'teamScoresEnabled': self.teamScoresEnabled,
            'playerScoresEnabled': self.playerScoresEnabled,
            'teamScores': {t.id: s for t, s in list(self.teamScores.items())},
            'playerScores': {p.id: s for p, s in list(self.playerScores.items())},
        }

    def restoreState(self, data):
        self.teamScoresEnabled = data['teamScoresEnabled']
        self.playerScoresEnabled = data['playerScoresEnabled']
        for team in self.teamScores:
            if team.id in data['teamScores']:
                self.teamScores[team] = data['teamScores'][team.id]
        for player in self.playerScores:
            if player.id in data['playerScores']:
                self.playerScores[player] = data['playerScores'][player.id]
        self.on_change(None, 0)

    def _playerWasAdded(self, player, *args, **kwargs):
        self.playerScores[player] = 0
        self.on_change(player, 0)

    def _playerWasRemoved(self, player, *args, **kwargs):
        del self.playerScores[player]

    def gotTeamScoreMsg(self, team, score):
        raise NotImplementedError('{}.gotTeamScoreMsg'.format(
            self.__class__.__name__))

    def gotPlayerScoreMsg(self, player, score):
        raise NotImplementedError('{}.gotPlayerScoreMsg'.format(
            self.__class__.__name__))

    def gotUpdateScoreBoardModeMsg(self, teams, players):
        raise NotImplementedError('{}.gotUpdateScoreBoardModeMsg'.format(
            self.__class__.__name__))


class ClientScoreBoard(ScoreBoardBase):
    def gotTeamScoreMsg(self, team, score):
        self.teamScores[team] = score
        self.on_change(team, score)

    def gotPlayerScoreMsg(self, player, score):
        self.playerScores[player] = score
        self.on_change(player, score)

    def gotUpdateScoreBoardModeMsg(self, teams, players):
        self.teamScoresEnabled = teams
        self.playerScoresEnabled = players


class ServerScoreBoard(ScoreBoardBase):
    '''
    Server score board immediately appends the given amount to avoid race
    conditions where you call playerScored() several times for the same
    player before the message gets through.
    '''

    def teamScored(self, team, amount=1):
        self.teamScores[team] += amount
        self.world.sendServerCommand(
            SetTeamScoreMsg(team.id, self.teamScores[team]))
        self.on_change(team, self.teamScores[team])

    def playerScored(self, player, amount=1):
        self.playerScores[player] += amount
        self.world.sendServerCommand(
            SetPlayerScoreMsg(player.id, self.playerScores[player]))
        self.on_change(player, self.playerScores[player])

    def setMode(self, teams=None, players=None):
        if teams is not None:
            self.teamScoresEnabled = teams
        if players is not None:
            self.playerScoresEnabled = players

        self.world.sendServerCommand(UpdateScoreBoardModeMsg(
            self.teamScoresEnabled, self.playerScoresEnabled))

    def gotTeamScoreMsg(self, team, score):
        # Already updated
        pass

    def gotPlayerScoreMsg(self, player, score):
        # Already updated
        pass

    def gotUpdateScoreBoardModeMsg(self, teams, players):
        # Already updated
        pass


class Clock(object):
    '''
    Keeps track of what should be displayed on the in-game clock. This may
    mean different things for different levels or game states, and may be
    used in UI displays, or by the level or game state, but outside things
    should not rely on it for calculating remaining game time etc.
    '''

    def __init__(self, world):
        self.onZero = Event([])

        self.world = world
        self.value = 0.0
        self.flashBelow = 0
        self.counting = False
        self.showing = False
        self.upwards = False

    def dumpState(self):
        return {
            'value': self.value,
            'flashBelow': self.flashBelow,
            'counting': self.counting,
            'showing': self.showing,
            'upwards': self.upwards,
        }

    def restoreState(self, data):
        self.value = data['value']
        self.flashBelow = data['flashBelow']
        self.setMode(
            showing=data['showing'],
            counting=data['counting'],
            upwards=data['upwards'],
        )

    def getTimeString(self):
        if not self.showing:
            return '--:--'

        if self.upwards:
            seconds = self.value
        else:
            # We add 0.999 so that the timer is rounding up the seconds
            # rather than rounding them down. This is so that the instant it
            # hits zero, the game starts.
            seconds = self.value + 0.999
        minutes, seconds = divmod(int(seconds), 60)
        return '%02d:%02d' % (minutes, seconds)

    def shouldFlash(self):
        if not self.showing:
            return False
        if self.flashBelow == 0 or not self.showing:
            return False
        return self.value <= self.flashBelow

    def setMode(self, counting=None, showing=None, upwards=None):
        if counting is not None:
            self.counting = counting
        if showing is not None:
            self.showing = showing
        if upwards is not None:
            self.upwards = upwards

    def startCountDown(self, seconds, flashBelow=10):
        self.value = seconds
        self.flashBelow = flashBelow
        self.setMode(counting=True, showing=True, upwards=False)

    def startCountUp(self, seconds=0):
        self.value = seconds
        self.flashBelow = 0
        self.setMode(counting=True, showing=True, upwards=True)

    def pause(self):
        self.setMode(counting=False)

    def resume(self):
        self.setMode(counting=True)

    def stop(self):
        self.setMode(showing=False, counting=False)

    def tick(self):
        if not self.counting:
            return

        if self.upwards:
            self.value += TICK_PERIOD
        else:
            oldValue = self.value
            self.value -= TICK_PERIOD
            self.value = max(0, self.value)
            if self.value == 0 and oldValue > 0:
                self.onZero()

    def propagateToClients(self):
        '''
        Should be called on the server immediately after any direct clock
        state changed. Only works on the server.
        '''
        self.world.sendServerCommand(UpdateClockStateMsg(
            showing=self.showing, counting=self.counting,
            upwards=self.upwards, value=self.value,
            flashBelow=self.flashBelow))


class Abilities(object):
    RESERVED_ATTRIBUTES = ('world',)

    def __init__(self, world):
        self.world = world

        self.upgrades = True
        self.respawn = True
        self.leaveFriendlyZones = True
        self.zoneCaps = True
        self.renaming = False
        self.balanceTeams = True
        self.respawn_time_factor = 1
        self.slow_dark_conquest = True

    def dumpState(self):
        return {
            'upgrades': self.upgrades,
            'respawn': self.respawn,
            'leaveFriendlyZones': self.leaveFriendlyZones,
            'zoneCaps': self.zoneCaps,
            'renaming': self.renaming,
            'balanceTeams': self.balanceTeams,
            'respawn_time_factor': self.respawn_time_factor,
            'slow_dark_conquest': self.slow_dark_conquest,
        }

    def restoreState(self, data):
        self.upgrades = data['upgrades']
        self.respawn = data['respawn']
        self.leaveFriendlyZones = data['leaveFriendlyZones']
        self.zoneCaps = data['zoneCaps']
        self.renaming = data['renaming']
        self.balanceTeams = data['balanceTeams']
        self.respawn_time_factor = data['respawn_time_factor']
        self.slow_dark_conquest = bool(data['slow_dark_conquest'])

    def set(self, **kwargs):
        assert self.world.isServer
        for key in kwargs:
            if not self._isKeyValid(key):
                raise KeyError('{!r} is not a valid abilities option', key)
        self.world.sendServerCommand(
            SetWorldAbilitiesMsg(simplejson.dumps(kwargs).encode('utf-8')))

    @contextmanager
    def modify(self, **kwargs):
        old = {k: getattr(self, k) for k in kwargs}
        try:
            self.set(**kwargs)
            yield
        finally:
            self.set(**old)

    def reset(self):
        self.set(
            upgrades=True, respawn=True, leaveFriendlyZones=True,
            zoneCaps=True, renaming=False, balanceTeams=True, respawn_time_factor=1)

    def _isKeyValid(self, key):
        if not hasattr(self, key):
            return False
        if key in self.RESERVED_ATTRIBUTES:
            return False
        if key.startswith('_'):
            return False
        if isinstance(getattr(self, key), collections.abc.Callable):
            return False
        return True

    def gotSetWorldAbilitiesMsg(self, settings):
        for key, value in list(settings.items()):
            if self._isKeyValid(key):
                setattr(self, key, value)


class UIOptions(SettingsSynchroniser):

    def __init__(self, world):
        super().__init__(self.dispatch_message, {
            'showNets': False,
            'highlight_macguffin_ids': [],
            'elephantName': DEFAULT_ELEPHANT_NAME,
            'frontLine': FRONT_LINE_NORMAL,
            'showReadyStates': False,
            'allow_scenario_voting': False,
            'team_name_suggestions': False,
            'team_ids_humans_can_join': [NEUTRAL_TEAM_ID],
            'team_ids_humans_can_switch_to': [],
            'speedup': 1,
            'crowd_kind': BOT_GOAL_NONE,
        })
        self.world = world

        self.onChange = Event([])
        self.onDefaultUserInfoChange = Event([])

        self.defaultUserTitle = ''      # Server only
        self.defaultUserInfo = ()       # Server only
        self.defaultBotGoal = BOT_GOAL_NONE     # Server only

    @property
    def highlight_macguffins(self):
        return [
            self.world.macguffin_manager.macguffins[m_id]
            for m_id in self.highlight_macguffin_ids]

    @highlight_macguffins.setter
    def highlight_macguffins(self, value):
        self.highlight_macguffin_ids = [m.macguffin_id for m in value]

    def setDefaultUserInfo(self, userTitle, userInfo, botGoal):
        assert self.world.isServer
        self.defaultUserTitle = userTitle
        self.defaultUserInfo = userInfo
        self.defaultBotGoal = botGoal
        self.onDefaultUserInfoChange()

    def getFrontLine(self):
        if self.frontLine == FRONT_LINE_TROSBALL:
            trosballPos = self.world.trosballManager.getPosition()
            if trosballPos is None:
                return None
            return trosballPos[0]
        return None

    def dispatch_message(self, settings_string):
        self.world.sendServerCommand(SetUIOptionsMsg(settings_string))

    def reset(self, new_level=None):
        if self.world.game.serverInterface:
            elephantName = self.world.game.serverInterface.getElephantName()
        else:
            elephantName = DEFAULT_ELEPHANT_NAME

        self.set(
            showNets=False, frontLine=FRONT_LINE_NORMAL,
            highlight_macguffin_ids=[], elephantName=elephantName,
            showReadyStates=False,
            allow_scenario_voting=False, team_name_suggestions=False,
            team_ids_humans_can_join=[NEUTRAL_TEAM_ID],
            team_ids_humans_can_switch_to=[],
        )

    def _isKeyValid(self, key):
        if not hasattr(self, key):
            return False
        if key in self.RESERVED_ATTRIBUTES:
            return False
        if key.startswith('_'):
            return False
        val = getattr(self, key)
        if isinstance(val, Event):
            return False
        if isinstance(val, types.MethodType):
            return False
        return True

    def applyMessage(self, data):
        super().applyMessage(data)
        self.onChange()


class TrosballManager(object):
    def __init__(self, world):
        self.world = world
        self.enabled = False
        self.trosballUnit = None
        self.trosballPlayer = None
        self.lastTrosballPlayer = None
        self.trosballCooldownPlayer = None
        self.playerGotTrosballTick = None

    def dumpState(self):
        if not self.enabled:
            return None

        if self.trosballUnit:
            return {
                'pos': self.trosballUnit.pos,
                'vel': [self.trosballUnit.xVel, self.trosballUnit.yVel],
                'playerId': None,
                'catchTicksAgo': None,
            }

        return {
            'pos': None,
            'vel': None,
            'playerId': self.trosballPlayer.id,
            'catchTicksAgo': (
                self.playerGotTrosballTick - self.world.getMonotonicTick()),
        }

    def restoreState(self, data):
        self.trosballCooldownPlayer = None

        if data is None:
            self.enabled = False
            self.trosballPlayer = None
            self.trosballCooldownPlayer = None
            self.trosballUnit = None
            self.playerGotTrosballTick = None
            return

        self.enabled = True
        if data['pos'] is not None:
            self.trosballPlayer = None
            self.trosballCooldownPlayer = None
            self.playerGotTrosballTick = None

            self.trosballUnit = Trosball(self.world)
            self.trosballUnit.teleport(data['pos'], data['vel'])
            return

        self.trosballUnit = None
        self.trosballPlayer = self.world.getPlayer(data['playerId'])
        self.lastTrosballPlayer = self.trosballPlayer
        self.playerGotTrosballTick = self.world.getMonotonicTick() - (
            data['catchTicksAgo'])

    #### Server / client routines

    def getPosition(self):
        if not self.enabled:
            return None

        if self.trosballUnit:
            return self.trosballUnit.pos
        return self.trosballPlayer.pos

    def getCooldownPlayer(self):
        if not self.enabled:
            return None
        return self.trosballCooldownPlayer

    def getAdvancables(self):
        if not self.enabled:
            return []
        if self.trosballUnit:
            return [self.trosballUnit]
        return []

    def getTargetZoneDefn(self, team):
        return self.world.layout.getTrosballTargetZoneDefn(team)

    def afterAdvance(self):
        '''
        Called once per tick on both client and server, to advance Trosball
        position etc. Most be deterministic or client and server could get
        out of sync.
        '''
        if not self.enabled:
            return

        self._update_zone_ownership()
        self._maybeExplode()

    def playerDroppedTrosball(self):
        '''
        Called on both client and server if the player carrying the Trosball
        died or left the game.
        '''
        assert self.trosballPlayer is not None
        self.trosballUnit = Trosball(self.world)
        self.trosballUnit.teleport(
            self.trosballPlayer.pos,
            self.trosballPlayer.getCurrentVelocity())
        self.trosballPlayer = None

    def _update_zone_ownership(self):
        trosball_position = self.getPosition()
        targetZones = {
            self.getTargetZoneDefn(team)
            for team in self.world.teams}

        for room in self.world.rooms:
            if room.defn not in targetZones:
                room.updateByTrosballPosition(trosball_position)

    def _maybeExplode(self):
        if self.trosballPlayer is None:
            return
        explodeTick = (
            self.playerGotTrosballTick
            + self.world.physics.trosballExplodeTime // TICK_PERIOD)
        if self.world.getMonotonicTick() < explodeTick:
            return

        self.world.trosballExploded(self.trosballPlayer)

    def getKickoffLocation(self):
        point = (self.world.map.centre[0], self.world.map.centre[1] - 50)
        start_zone = self.world.rooms.get_at(point)
        return start_zone.orb_pos

    #### Server-side only

    def enable(self, pos=None, vel=None, inNet=False):
        assert self.world.isServer
        if self.enabled:
            return
        if pos is None:
            pos = self.getKickoffLocation()
        if vel is None:
            vel = (0, 0)
        self.world.sendServerCommand(
            TrosballPositionMsg(pos[0], pos[1], vel[0], vel[1], inNet))

    def disable(self):
        assert self.world.isServer
        if not self.enabled:
            return
        self.world.sendServerCommand(PlayerHasTrosballMsg(NO_PLAYER))

    def retransmit(self):
        if self.enabled:
            if self.trosballPlayer:
                self.giveToPlayer(self.trosballPlayer)
            else:
                vel = (self.trosballUnit.xVel, self.trosballUnit.yVel)
                self.teleport(self.trosballUnit.pos, vel)
        else:
            self.world.sendServerCommand(PlayerHasTrosballMsg(NO_PLAYER))

    def giveToPlayer(self, player):
        assert self.world.isServer
        if not self.enabled:
            raise RuntimeError('trosball mode not enabled')
        self.world.sendServerCommand(PlayerHasTrosballMsg(player.id))

    def teleport(self, pos, vel, inNet=False):
        assert self.world.isServer
        if not self.enabled:
            raise RuntimeError('trosball mode not enabled')
        self.world.sendServerCommand(
            TrosballPositionMsg(pos[0], pos[1], vel[0], vel[1], inNet))

    def place_in_net(self, room):
        assert self.world.isServer
        self.teleport(room.orb_pos, (0, 0), True)

    def resetToStartLocation(self):
        pos = self.getKickoffLocation()
        self.lastTrosballPlayer = None
        self.teleport(pos, (0, 0))

    def getThrowVelocity(self, player):
        xVel, yVel = player.getCurrentVelocity()
        angle = player.angleFacing
        xVel += self.world.physics.trosballThrowVel * sin(angle)
        yVel += -self.world.physics.trosballThrowVel * cos(angle)
        return xVel, yVel

    def throwTrosball(self):
        assert self.world.isServer
        player = self.trosballPlayer
        xVel, yVel = self.getThrowVelocity(player)
        self.trosballCooldownPlayer = player

        self.world.callLater(0.5, self._clearTrosballCooldown, player)
        self.teleport(player.pos, (xVel, yVel))

    def _clearTrosballCooldown(self, player):
        if self.trosballCooldownPlayer == player:
            self.trosballCooldownPlayer = None

    #### Message handling

    def gotTrosballPositionMsg(self, pos, vel, inNet):
        self.enabled = True
        self.trosballPlayer = None
        if self.trosballUnit is None:
            self.trosballUnit = Trosball(self.world)

        if inNet:
            self.trosballUnit.setIsInNet(pos)
        else:
            self.trosballUnit.teleport(pos, vel)

    def gotPlayerHasTrosballMsg(self, player):
        if player is None:
            self.enabled = False
            self.trosballPlayer = None
            self.trosballCooldownPlayer = None
            self.trosballUnit = None
        else:
            self.enabled = True
            self.trosballUnit = None
            self.trosballPlayer = player
            self.lastTrosballPlayer = player
            self.playerGotTrosballTick = self.world.getMonotonicTick()


class Universe(MessageConsumer):
    '''
    Keeps track of where everything is in the level, including the locations
    and states of every alien, the terrain positions, and who owns the
    various territories and orbs.'''

    isServer = False
    scoreboardClass = ClientScoreBoard

    def __init__(self, onceOnly=False):
        super().__init__()

        self.onPlayerAdded = Event(['player'])
        self.on_player_join_complete = Event(['player'])
        self.onPlayerRemoved = Event(['player', 'oldId'])
        self.on_player_team_set = Event(['player'])
        self.onShotRemoved = Event()        # (shotId)
        self.on_projectile_removed = Event(['projectile_id'])
        self.on_shot_fired = Event(['shooter', 'shot'])
        self.on_shot_hit_something = Event(['shooter', 'hit'])
        self.onCollectableCoinSpawned = Event(['coin'])
        self.onCollectableCoinRemoved = Event()
        self.onStandardGameFinished = Event(['winner'])
        self.onZoneTagged = Event()         # (zone, player, previousOwner)
        self.onZoneStateChanged = Event()   # (zone)
        self.onOpenChatReceived = Event()   # (text, sender)
        self.onTeamChatReceived = Event()   # (team, text, sender)
        self.onPlayerKill = Event(['killer', 'target', 'hit_kind'])
        self.onPlayerRespawn = Event()      # (player)
        self.on_player_health_decreased = Event(['player', 'hitter', 'damage'])
        self.onGrenadeExplosion = Event()   # (pos, radius)
        self.onTrosballExplosion = Event()  # (player)
        self.onBomberExplosion = Event()    # (player)
        self.on_mine_explosion = Event(['pos'])
        self.onReset = Event()
        self.onServerTickComplete = Event()
        self.onChangeVoiceChatRooms = Event()   # (teams, players)
        self.onSound = Event(['filename'])
        self.onCoinSound = Event(['player'])
        self.on_before_tick = Event([])
        self.on_pause_state_changed = Event([])
        self.on_result_set = Event([])

        self.delayedCalls = []

        self.physics = WorldPhysics(self)

        self.playerWithId = {}
        self.shotWithId = {}
        self.teamWithId = {NEUTRAL_TEAM_ID: None}
        self.projectile_by_id = {}

        # Create Teams:
        self.teams = (
            Team(self, b'A', TEAM_1_COLOUR),
            Team(self, b'B', TEAM_2_COLOUR),
        )
        Team.setOpposition(self.teams[0], self.teams[1])

        for t in self.teams:
            self.teamWithId[t.id] = t

        # Set up zones
        self.zoneWithDef = {}
        self.layout = None
        self.map = None
        self.zoneWithId = {}
        self.zones = set()
        self.zoneBlocks = []

        self.players = set()
        self.grenades = set()
        self.collectableCoins = {}      # coinId -> CollectableCoin
        self.deadCoins = set()
        self.gameMode = 'Normal'
        self.rogueTeamName = 'Rogue'
        self.tickPeriod = TICK_PERIOD
        self._gameSpeed = 1.0
        self.lastTickId = 0
        self.monotonicTicks = 0
        self.loading = False
        self.paused = False

        self._onceOnly = onceOnly
        self.clock = Clock(self)
        self.scoreboard = self.scoreboardClass(self)
        self.trosballManager = TrosballManager(self)
        self.abilities = Abilities(self)
        self.uiOptions = UIOptions(self)
        self.macguffin_manager = MacGuffinManager(self)
        self.elephant = MacGuffin(self, 0)
        self.juggernaut = MacGuffin(self, 1)
        self.vampire = MacGuffin(self, 2)

        self.scenario_result = None
        self.stopped = False

    @property
    def path_finder(self):
        '''
        Temporary method to reduce differences between default and
        unstable branches, until the new larger rooms can be merged in.
        '''
        return self.map.layout.pathFinder

    @property
    def rooms(self):
        '''
        Temporary method so that we provide the same interface provided
        in unstable branch.
        '''
        return RoomCollectionProxy(self)

    def getMonotonicTick(self):
        '''
        Returns an integer representing the number of ticks seen since some
        arbitrary point in the past. Unlike world.lastTickId, this is
        guaranteed to be monotonic, but may not be the same between server
        and clients.
        '''
        return self.monotonicTicks

    def getMonotonicTime(self):
        return self.monotonicTicks * TICK_PERIOD

    def isValidNick(self, nick):
        if len(nick) < 2 or len(nick) > MAX_PLAYER_NAME_LENGTH:
            return False
        return True

    @property
    def shots(self):
        '''
        Used by UI to iterate through shots.
        '''
        return list(self.shotWithId.values())

    def defaultHandler(self, msg):
        msg.applyOrderToWorld(self)

    def select_good_respawn_zone_for_team(self, team):
        '''
        Randomly selects a zone, giving preference to:
            1. Zones owned by the given team that are adjacent to an enemy zone
            2. Zones owned by the given team that are adjacent to a zone not
                owned by the team.
            3. Other zones owned by the given team.
            4. Other zones.
        '''
        allTeamZones = [
            z for z in self.map.zones
            if z.owner is not None and z.owner.id == team.id] if team else []
        nextToEnemy = []
        nextToNeutral = []
        for zone in list(allTeamZones):
            enemy = neutral = False
            for adj in zone.getAdjacentZones():
                if adj.owner is None:
                    neutral = True
                elif adj.isEnemyTeam(team):
                    enemy = True
            if enemy:
                nextToEnemy.append(zone)
            elif neutral:
                nextToNeutral.append(zone)

        return random.choice(
            nextToEnemy
            or nextToNeutral
            or allTeamZones
            or list(self.map.zones))

    @WorldResetMsg.handler
    def gotWorldReset(self, msg):
        if not self.isServer:
            data = unrepr(msg.settings.decode('utf-8'))
            self.restoreEverything(data)

    def getTeam(self, team_id) -> Optional[Team]:
        if isinstance(team_id, str):
            team_id = team_id.encode('ascii')
        if team_id == NEUTRAL_TEAM_ID:
            return None
        return self.teamWithId[team_id]

    def getPlayer(self, player_id, default=None) -> Optional[Player]:
        if isinstance(player_id, str):
            player_id = player_id.encode('ascii')
        return self.playerWithId.get(player_id, default)

    def getUpgradeType(self, upgradeTypeId):
        return upgradeOfType[upgradeTypeId]

    def getZone(self, zoneId, default=None):
        return self.map.zoneWithId.get(zoneId, default)

    def getShot(self, sId):
        return self.shotWithId[sId]

    def setGameMode(self, mode):
        if self.physics.setMode(mode):
            self.gameMode = mode
            log.debug('Client: GameMode is set to ' + mode)

    def setGameSpeed(self, speed):
        '''Sets the speed of the game to a proportion of normal speed.
        That is, speed=2.0 is twice as fast a game as normal
        '''
        self._gameSpeed = speed
        self.tickPeriod = TICK_PERIOD * speed

    @PlaySoundMsg.handler
    def handle_PlaySoundMsg(self, msg):
        self.onSound(msg.filename.decode('utf-8'))

    @AddPlayerMsg.handler
    def handle_AddPlayerMsg(self, msg):
        team = self.teamWithId[msg.teamId]
        zone = self.zoneWithId[msg.zoneId]

        # Create the player.
        nick = msg.nick.decode('utf-8')
        player = Player(
            self, nick, team, msg.playerId, msg.dead, msg.bot, head=msg.head)
        player.teleport_to_respawn_point(zone, or_centre=True)

        self.addPlayer(player)

    def addPlayer(self, player):
        # Add this player to this universe.
        self.players.add(player)
        self.playerWithId[player.id] = player
        self.onPlayerAdded(player)

    def delPlayer(self, player):
        playerId = player.id
        player.removeFromGame()
        self.players.remove(player)
        del self.playerWithId[player.id]

        # In case anyone else keeps a reference to it
        player.id = -1
        player.onRemovedFromGame(playerId)
        self.onPlayerRemoved(player, playerId)

    def advanceEverything(self):
        '''Advance the state of the game by deltaT seconds'''

        for shot in list(self.shots):
            if shot.expired:
                del self.shotWithId[shot.id]
                self.onShotRemoved(shot.id)

        # Update the player and shot positions.
        advancables = (
            list(self.shotWithId.values()) + list(self.players) + list(self.grenades)
            + list(self.projectile_by_id.values())
            + list(self.collectableCoins.values()))
        advancables.extend(self.trosballManager.getAdvancables())
        for unit in advancables:
            unit.reset()
            unit.advance()

        self.updateZoneInhabitants(advancables)
        self.update_orb_progress()
        self.trosballManager.afterAdvance()

        for team in self.teams:
            team.advance()

    def update_orb_progress(self):
        if not self.abilities.slow_dark_conquest:
            return

        for room in self.rooms:
            room.advance_capture_progress()

    def getCollectableUnits(self):
        for coin in list(self.collectableCoins.values()):
            yield coin
        if self.trosballManager.enabled and self.trosballManager.trosballUnit:
            yield self.trosballManager.trosballUnit
        for unit in list(self.deadCoins):
            yield unit

    def updateZoneInhabitants(self, advancables):
        if not self.map:
            return
        for room in self.rooms:
            room.clear_players()
        for unit in advancables:
            if isinstance(unit, Player):
                room = unit.getZone()
                if room:
                    room.add_player(unit)

    def bomber_exploded(self, player):
        if not player.dead:
            self.onBomberExplosion(player)

    def canShoot(self):
        return self.physics.shooting

    @CreateCollectableCoinMsg.handler
    def createCollectableCoin(self, msg):
        self.addCollectableCoin(CollectableCoin(
            self, msg.coinId,
            (msg.xPos, msg.yPos), msg.xVel, msg.yVel,
            msg.value,
        ))

    @RemoveCollectableCoinMsg.handler
    def gotRemoveCollectableCoinMsg(self, msg):
        # On the server, the coin must be remembered in case a player is about
        # to collect it but we don't know yet.
        if not self.isServer:
            coin = self.collectableCoins[msg.coinId]
            if not coin.vanished:
                coin.onVanish(coin)

            del self.collectableCoins[msg.coinId]
            self.onCollectableCoinRemoved(msg.coinId)

    def getTeamName(self, id_):
        if id_ == NEUTRAL_TEAM_ID:
            return self.rogueTeamName
        return self.getTeam(id_).teamName

    @FireShoxwaveMsg.handler
    def gotFireShoxwaveMsg(self, msg):
        firingPlayer = self.getPlayer(msg.playerId)
        if not firingPlayer:
            return
        firingPlayer.guns.gun_was_fired(Shoxwave)

        for shot in list(self.shotWithId.values()):
            if (not firingPlayer.isFriendsWithTeam(shot.team) and
                    distance(shot.pos, firingPlayer.pos) <= SHOXWAVE_RADIUS):
                shot.expired = True

    def apply_fired_shot(self, player, gun, shot_id):
        shot = player.createShot(gun, shot_id)
        self.shotWithId[shot_id] = shot
        player.guns.gun_was_fired(gun)
        player.onShotFired(shot)
        self.on_shot_fired(player, shot)

    @TaggingZoneMsg.handler
    def zoneTagged(self, msg):
        if msg.playerId == NO_PLAYER:
            player = None
        else:
            player = self.playerWithId[msg.playerId]
        zone = self.map.zoneWithId[msg.zoneId]
        previous_owner = zone.owner
        zone.tag(player)
        self.onZoneTagged(zone, player, previous_owner)
        if player:
            player.onTaggedZone(zone, previous_owner)

    @ZoneStateMsg.handler
    def zoneOwned(self, msg):
        zone = self.map.zoneWithId[msg.zoneId]
        team = self.teamWithId[msg.teamId]
        zone.setOwnership(team, msg.dark)

    @RespawnMsg.handler
    def respawn(self, msg):
        player = self.getPlayer(msg.playerId)
        zone = self.getZone(msg.zoneId)
        if player and zone:
            if msg.phantom:
                player.phantom_respawn(zone)
            else:
                player.respawn(zone)

    @PlayerCoinsSpentMsg.handler
    def coinsSpent(self, msg):
        player = self.getPlayer(msg.playerId)
        if player:
            oldCoins = player.coins
            player.coins -= msg.count
            player.onCoinsChanged(oldCoins)
            player.onCoinsSpent(msg.count)

    @UpgradeChangedMsg.handler
    def changeUpgrade(self, msg):
        for upgradeClass in allUpgrades:
            if upgradeClass.upgradeType == msg.upgradeType:
                if msg.statType == b'S':
                    upgradeClass.requiredCoins = msg.newValue
                elif msg.statType == b'T':
                    upgradeClass.totalTimeLimit = msg.newValue
                elif msg.statType == b'E':
                    upgradeClass.enabled = bool(msg.newValue)

    def addGrenade(self, grenade):
        self.grenades.add(grenade)

    def removeGrenade(self, grenade):
        self.grenades.remove(grenade)

    def addCollectableCoin(self, coin):
        self.collectableCoins[coin.id] = coin
        self.onCollectableCoinSpawned(coin)

    def setLayout(self, layout):
        self.zoneWithDef = {}
        for team in self.teams:
            team.numZonesOwned = 0
        self.layout = layout
        self.map = MapState(self, self.layout)
        self.zoneWithId = self.map.zoneWithId
        self.zones = self.map.zones
        self.zoneBlocks = self.map.zoneBlocks

        # Layout has changed, so move units to sensible places
        self.resetUnits()

    def resetUnits(self):
        for player in self.players:
            zone = self.select_good_respawn_zone_for_team(player.team)
            player.teleport_to_respawn_point(zone, or_centre=True)
            player.health = 0
            player.items.clear()
            player.timeTillRespawn = 0.0

        self.deadCoins = set()
        self.collectableCoins = {}
        self.shotWithId = {}
        self.projectile_by_id = {}
        self.grenades = set()

    def setTestMode(self):
        for upgradetype in allUpgrades:
            upgradetype.requiredCoins = 1

    @TickMsg.handler
    def tickReceived(self, msg):
        if globaldebug.enabled:
            globaldebug.tick_logger.universe_saw_tick(self, msg.tickId)
        self.on_before_tick()
        self.monotonicTicks += 1
        self.clock.tick()
        self.advanceEverything()
        self.lastTickId = msg.tickId

        self.processDelayedCalls()

    def processDelayedCalls(self):
        thisTick = self.getMonotonicTick()
        while self.delayedCalls:
            if self.delayedCalls[0].when > thisTick:
                break
            call = heapq.heappop(self.delayedCalls)
            if call.cancelled:
                continue
            try:
                call.fn(*call.args, **call.kwargs)
            except Exception:
                log.exception('Error in delayed call')

    def dumpEverything(self):
        '''Returns a dict representing the settings which must be sent to
        clients that connect to this server.'''

        result = {
            'loading': self.loading,
            'teams': [
                team.dump() for team in self.teams
            ],
            'worldMap': self.map.layout.dumpState() if self.map else None,
            'mode': self.gameMode,
            'speed': self._gameSpeed,
            'zones': [
                {
                    'id': zone.id,
                    'teamId': zone.owner.id if zone.owner else NEUTRAL_TEAM_ID,
                    'dark': zone.dark,
                } for zone in self.zones
            ],
            'players': [player.dump() for player in self.players],
            'trosball': self.trosballManager.dumpState(),
            'upgrades': [
                {
                    'type': upgrade.upgradeType,
                    'cost': upgrade.requiredCoins,
                    'time': upgrade.totalTimeLimit,
                    'enabled': upgrade.enabled,
                } for upgrade in allUpgrades
            ],
            'macguffins': self.macguffin_manager.dump(),
            'shots': [shot.dump() for shot in self.shotWithId.values() if not shot.expired],
            'projectiles': [unit.dump() for unit in self.projectile_by_id.values()],
            'coins': [
                {
                    'id': coin.id,
                    'createdAgo': self.getMonotonicTick() - coin.creationTick,
                    'pos': coin.pos,
                    'xVel': coin.xVel,
                    'yVel': coin.yVel,
                    'value': coin.value,
                } for coin in list(self.collectableCoins.values())
            ],
            'grenades': [grenade.dump() for grenade in self.grenades],
            'physics': self.physics.dumpState(),
            'clock': self.clock.dumpState(),
            'scoreboard': self.scoreboard.dumpState(),
            'uiOptions': self.uiOptions.dumpState(),
            'abilities': self.abilities.dumpState(),
            'lastTickId': self.lastTickId,
            'result': self.scenario_result.dump(self) if self.scenario_result else None,
        }

        return result

    def restoreEverything(self, data):
        if data['result']:
            self.scenario_result = LevelResult.rebuild(self, data['result'])
        else:
            self.scenario_result = None

        self.loading = data['loading']
        if 'lastTickId' in data:
            self.lastTickId = data['lastTickId']

        for team_data in data['teams']:
            teamId = team_data['id']
            team = self.teamWithId[teamId]
            team.restore(team_data)

        self.physics.restoreState(data['physics'])
        self.clock.restoreState(data['clock'])
        self.uiOptions.restoreState(data['uiOptions'])
        self.abilities.restoreState(data['abilities'])

        mapSpec = data['worldMap']
        if mapSpec is None:
            self.map = None
        else:
            layout = MapLayout.fromDumpedState(mapSpec)
            self.setLayout(layout)

        self.setGameMode(data['mode'])
        self.setGameSpeed(data['speed'])

        for zoneData in data['zones']:
            self.getZone(zoneData['id']).setOwnership(
                self.teamWithId[zoneData['teamId']], zoneData['dark'])

        for playerData in data['players']:
            playerId = playerData['id']
            team = self.teamWithId[playerData['teamId']]
            nick = playerData['nick']

            if playerId in self.playerWithId:
                player = self.playerWithId[playerId]
            else:
                player = Player(self, nick, team, playerId)
                self.addPlayer(player)

            player.restore(playerData)

        self.scoreboard.restoreState(data['scoreboard'])
        self.trosballManager.restoreState(data['trosball'])

        for upgradeData in data['upgrades']:
            for upgradeClass in allUpgrades:
                if upgradeClass.upgradeType == upgradeData['type']:
                    upgradeClass.requiredCoins = upgradeData['cost']
                    upgradeClass.totalTimeLimit = upgradeData['time']
                    upgradeClass.enabled = upgradeData['enabled']

        if 'macguffins' in data:
            self.macguffin_manager.restore(data['macguffins'])

        self.shotWithId = {}
        for shot_data in data['shots']:
            shot = Shot.rebuild(self, shot_data)
            self.shotWithId[shot.id] = shot

        self.projectile_by_id = {}
        for projectile_data in data.get('projectiles', []):
            # For now, mines are the only thing in projectile_by_id, but
            # in future this should include grenades, so we’ll probably
            # want to call a classmethod on a base Projectile class.
            unit = MineProjectile.rebuild(self, projectile_data)
            self.projectile_by_id[unit.id] = unit

        self.deadCoins = set()
        self.collectableCoins = {}
        for coinData in data['coins']:
            coin = CollectableCoin(
                self, coinData['id'], tuple(coinData['pos']),
                coinData['xVel'], coinData['yVel'], value=coinData.get('value', None),
            )
            coin.creationTick = self.getMonotonicTick() - coinData[
                'createdAgo']
            self.collectableCoins[coin.id] = coin

        self.grenades = set()
        for grenade_data in data['grenades']:
            self.addGrenade(GrenadeShot.rebuild(self, grenade_data))

        self.onReset()

    def isOnceOnly(self):
        return self._onceOnly

    def playerHasDied(self, player, killer, deathType):
        pass

    def stop(self):
        self.stopped = True
        if self.scoreboard:
            self.scoreboard.stop()
        self.scoreboard = None

    def callLater(self, _delay, _fn, *args, **kwargs):
        '''
        Schedules the given function to be called at the given game time.
        '''
        ticksInFuture = -int(-_delay // TICK_PERIOD)    # ceiling division
        return self.callAfterTicks(ticksInFuture, _fn, *args, **kwargs)

    def callAfterTicks(self, _ticks, _fn, *args, **kwargs):
        futureTick = self.getMonotonicTick() + _ticks

        result = DelayedCall(futureTick, _fn, args, kwargs)
        heapq.heappush(self.delayedCalls, result)
        return result

    def sleep(self, delay):
        '''
        Returns a Deferred that fires after the given number of game seconds.
        '''
        d = defer.Deferred()
        self.callLater(delay, d.callback, None)
        return d

    def sleep_future(self, delay):
        '''
        Like self.sleep(), but returns an asyncio.Future.
        '''
        f = asyncio.get_event_loop().create_future()
        self.callLater(delay, f.set_result, None)
        return f

    def grenadeExploded(self, killer, pos, radius):
        if not killer.aggression:
            return
        self.onGrenadeExplosion(pos, radius)

    def trosballExploded(self, player):
        self.onTrosballExplosion(player)

    def remove_projectile(self, projectile):
        del self.projectile_by_id[projectile.id]
        self.on_projectile_removed(projectile.id)

    def set_result(self, scenario_result):
        if self.scenario_result:
            raise RuntimeError('Scenario cannot have two results!')
        self.scenario_result = scenario_result
        self.clock.pause()
        self.on_result_set()


class ScenarioManager:
    def __init__(self, world):
        self.world = world
        self.level = None
        self.level_task = None
        self.task = None

    def start(self, initial_level, wait_for_ready=False):
        # Called once when ScenarioManager is first starting
        self.level_task = asyncio.ensure_future(
            self.run_level(
                initial_level,
                wait_for_ready=wait_for_ready,
            ))
        self.level_task.level = initial_level

    def stop(self):
        if self.level_task and not self.level_task.done():
            self.level_task.cancel()

    def startLevel(self, level):
        task_to_stop = self.level_task
        self.level_task = asyncio.ensure_future(self.run_level(level, task_to_stop))
        self.level_task.level = level

    async def stopLevel(self):
        if self.level_task and not self.level_task.done():
            await cancel_task(self.level_task)

    async def run_level(
            self, level: Level, task_to_stop=None, wait_for_ready=False):
        level_result = None     # Will be returned if an exception occurs
        try:
            oldLevel = self.level
            if task_to_stop and not task_to_stop.done():
                await cancel_task(task_to_stop)

            self.level = level
            self.level.set_world(self.world)

            self.world.scenario_result = None
            if self.world.scoreboard:
                self.world.scoreboard.stop()
                self.world.scoreboard = self.world.scoreboardClass(self.world)
            self.world.abilities.reset()
            self.world.uiOptions.reset(level)
            self.world.macguffin_manager.reset()
            self.world.trosballManager.disable()
            self.world.clock = Clock(self.world)
            self.world.activeAchievementCategories = set()
            for team in self.world.teams:
                team.abilities.reset(sync=False)
            for projectile in list(self.world.projectile_by_id.values()):
                self.world.remove_projectile(projectile)

            # Remove any bots still in the game
            if not self.world.isOnceOnly():
                for agent in list(self.world.game.agents):
                    if agent.player and agent.player.bot:
                        log.warning(
                            '%s did not remove bot %s', oldLevel, agent)
                        agent.stop()
                        self.world.game.detachAgent(agent)

            for p in self.world.players:
                p.reset_abilities()
                p.max_health = self.world.physics.playerRespawnHealth
                p.readyToStart = False

            if level.resetPlayerCoins:
                for p in self.world.players:
                    p.coins = 0
                    p.guns = PlayerGuns(p)
                for t in self.world.teams:
                    t.boosts.clear_locally()
            level.pre_sync_setup()

            await as_future(self.world.syncEverything())

            if wait_for_ready:
                await level.run_lobby_period()

            self.world.onStartMatch()
            if level.recordGame:
                self.world.resumeStats()

            level_result = await level.run()

            self.world.sendServerCommand(ScenarioCompleteMsg(data=level_result.dump(self)))
        except Exception:
            log.exception('Error running level')
            return
        finally:
            if self.world.botManager is not None:
                self.world.botManager.stop()
                self.world.botManager = None
            self.world.on_end_match(level_result)
            self.world.finaliseStats()
            self.world.regions = []
            level.tearDownLevel()
            self.level = None
            if getattr(self.level_task, 'level') == level:
                # This is guarded because level_task would normally already
                # be set to the new level's task by this stage.
                self.level_task = None

        await self.world.sleep_future(6)

        # Only reached if level.run() has no errors and is not cancelled
        for p in list(self.world.players):
            self.world.sendServerCommand(RemovePlayerMsg(p.id))

        if self.world.isOnceOnly():
            self.world.game.once_only_game_completed()
        else:
            self.world.returnToLobby()


class ServerUniverse(Universe):
    '''
    A universe that contains a few extra functions that are only needed
    server-side.
    '''

    isServer = True
    scoreboardClass = ServerScoreBoard

    def __init__(
            self,
            game,
            *args,
            level=None,
            wait_for_ready=False,
            game_type=None,
            bots_only=False,
            no_auto_balance=False,
            speedup=1,
            slow_dark_conquest=True,
            **kwargs):
        self.onUnitsAllAdvanced = Event([])
        self.onSwitchStats = Event(['enabled', 'finished'])
        self.onStartMatch = Event([])
        self.on_end_match = Event(['scenario_result'])
        self.onActiveAchievementCategoriesChanged = Event([])
        self.onZoneCaptureFinalised = Event(['captureInfo'])
        self.on_player_dropped_coins = Event(['player', 'value'])

        super(ServerUniverse, self).__init__(*args, **kwargs)
        self.uiOptions.speedup = speedup
        self.abilities.slow_dark_conquest = slow_dark_conquest

        self.botManager = None
        self.game = game
        self.idManager = IdManager(self)
        self._lastTickId = 0
        self.nextGameType = game_type or 'normal'
        self.bots_only = bots_only
        self.no_auto_balance = no_auto_balance or bots_only
        self.paused = False
        self.scenarioManager = ScenarioManager(self)
        self._nextTick = None
        self._expectedTickTime = None
        self.regions = []
        self.activeAchievementCategories = set()
        self.jitterLogger = JitterLogger(20)
        self.sentGraceTick = False
        self.interaction_detector = InteractionDetector(self, 100)
        if PROFILE_LONG_TICKS:
            self.long_tick_profiler = LongTickProfiler()
        else:
            self.long_tick_profiler = None

        if __debug__ and globaldebug.enabled:
            globaldebug.serverUniverse = self

        if level is None:
            level = LobbyLevel(game.lobbySettings)
        if self.isOnceOnly():
            self.game_format = level.levelName
        else:
            self.game_format = 'variety games'
        self._startClock()
        self.scenarioManager.start(
            level,
            wait_for_ready=wait_for_ready,
        )
        self.elephant.on_death_of_possessor.addListener(self.seen_elephant_owner_die)
        self.elephant.on_possessor_left_game.addListener(self.returnElephantToOwner)

    def getLevelStatus(self):
        status = self.uiOptions.defaultUserTitle

        level = self.scenarioManager.level
        if level:
            levelName = level.levelName or level.__class__.__name__
        else:
            levelName = status

        if status == levelName:
            return levelName
        return '{}: {}'.format(levelName, status)

    def resumeStats(self):
        self.onSwitchStats(enabled=True, finished=False)

    def pauseStats(self):
        self.onSwitchStats(enabled=False, finished=False)

    def finaliseStats(self):
        self.onSwitchStats(enabled=False, finished=True)

    def setActiveAchievementCategories(self, categories):
        self.activeAchievementCategories = categories
        self.onActiveAchievementCategoriesChanged()

    def returnToLobby(self):
        if self.stopped:
            return
        self.scenarioManager.startLevel(LobbyLevel(self.game.lobbySettings))

    def addRegion(self, region):
        self.regions.append(region)

    def removeRegion(self, region):
        self.regions.remove(region)

    def pauseOrResumeGame(self):
        self.sendServerCommand(PauseOrResumeMsg(not self.paused))

    def make_everyone_ready(self):
        '''
        Makes this server treat all players as ready, even if the player
        hasn't actually selected ‘Ready’. This may be used to force a
        game to start.
        '''
        for player in self.players:
            player.readyToStart = True

    @delay_so_messages_will_apply_immediately
    def magically_move_player(self, player, pos, alive=None):
        '''
        Moves the given player to the given position. If alive is given,
        it should be a boolean indicating whether the player should become
        alive, or dead.
        '''
        self.magically_move_player_now(player, pos, alive)

    def magically_move_player_now(self, player, pos, alive=None):
        # So that we don't risk introducing inconsistencies between
        # server and clients, we operate on a clone of the player until
        # sending the resync message.
        clone = player.clone()
        if alive:
            if clone.dead:
                clone.returnToLife(force_full_health=True)
        elif alive is not None:
            if not clone.dead:
                clone.makeAllDead()
        clone.setPos(pos)
        player.sendResync(reason='', clone=clone)

    def sendServerCommand(self, msg):
        if not hasattr(self.game, 'world'):
            # This only happens in very initial game/world construction,
            # before any agents have had the chance to connect
            return

        self.game.sendServerCommand(msg)

    def advanceEverything(self):
        self.interaction_detector.reset_buckets()
        super(ServerUniverse, self).advanceEverything()
        self.interaction_detector.process_collisions()
        self.updateCollectableCoins()
        self.onUnitsAllAdvanced()
        if not self.isOnceOnly():
            self.bootTardyPlayers()

    def bootTardyPlayers(self):
        for player in list(self.players):
            if (
                    player.resyncing and
                    self.getMonotonicTick() > player.resyncExpiry):
                log.warning('%s took too long to resync', player)
                if player.agent:
                    player.agent.messageToAgent(ChatFromServerMsg(
                        error=True, text=(
                            'You have been removed from the game '
                            'because your client took too long to resync!').encode(
                            'utf-8')))
                self.sendServerCommand(RemovePlayerMsg(player.id))

            elif player.ghost_has_been_idle_for > DISCONNECT_IDLE_GHOST_AFTER + 1:
                # Player was idle for too long
                if player.agent:
                    player.agent.messageToAgent(ChatFromServerMsg(
                        error=True, text='You have been idle for too long!'.encode('utf-8')))
                self.sendServerCommand(RemovePlayerMsg(player.id))

    def updateCollectableCoins(self):
        try:
            for coin in list(self.collectableCoins.values()):
                endTick = coin.creationTick + (
                        COLLECTABLE_COIN_LIFETIME // TICK_PERIOD)
                if self.getMonotonicTick() >= endTick:
                    coin.removeDueToTime()

            for unit in list(self.deadCoins):
                unit.beat()
                if not unit.history:
                    self.deadCoins.remove(unit)
                    self.onCollectableCoinRemoved(unit.id)
        except Exception:
            log.error('Error updating collectable coins', exc_info=True)

    def returnElephantToOwner(self, *args, **kwargs):
        for p in self.players:
            if p.isElephantOwner():
                self.elephant.give_to_player(p)
                return
        self.elephant.give_to_player(None)

    def seen_elephant_owner_die(self, killer):
        if killer and not killer.dead:
            self.elephant.give_to_player(killer)
        else:
            self.returnElephantToOwner()

    def playerHasDied(self, player, killer, deathType):
        if deathType != BOMBER_DEATH_HIT:
            self.dropPlayerCoinsDueToDeath(player)
        if killer:
            if self.scenarioManager.level:
                factor = self.scenarioManager.level.coins_for_kills_factor
            else:
                factor = 1
            self.sendServerCommand(AwardPlayerCoinMsg(killer.id, round(COINS_PER_KILL * factor)))

    def dropPlayerCoinsDueToDeath(self, player):
        x, y = player.pos
        old_vel = player.getCurrentVelocity()
        coins_to_keep = player.coins
        for coin_value in player.getCoinsToDropOnDeath():
            coins_to_keep -= coin_value

            coin_id = self.idManager.coins.make_id()
            if coin_id is None:
                continue

            x_vel = 0.7 * old_vel[0] + random.random() * 200 - 100
            y_vel = 0.7 * old_vel[1] + random.random() * 200 - 100
            self.sendServerCommand(CreateCollectableCoinMsg(
                coin_id, x, y, x_vel, y_vel, coin_value))

        self.on_player_dropped_coins(player, player.coins - coins_to_keep)
        self.sendServerCommand(SetPlayerCoinsMsg(player.id, coins_to_keep))

    def delPlayer(self, player):
        if self.botManager:
            self.botManager.removingPlayer(player)
        self.macguffin_manager.player_is_leaving(player)
        super(ServerUniverse, self).delPlayer(player)

    @defer.inlineCallbacks
    def syncEverything(self):
        yield self.game.waitForEmptyCommandQueue()
        for player in self.players:
            player.resyncBegun()
        self.sendServerCommand(WorldResetMsg(repr(
            self.dumpEverything()).encode('utf-8')))

    def requestTickNow(self):
        '''
        If this game is currently being viewed by the UI, and the UI needs
        another tick to prevent it from freezing, it will call this method.
        '''
        if self.scenarioManager.level is None:
            # Tearing down or still setting up
            return

        if self._nextTick is not None:
            self._nextTick.cancel()
        self.tick()

    def tick(self):
        self._nextTick = None

        # Do our best to correct for any inaccuracies in call time, up to a
        # limit of one tick discrepancy.
        period = TICK_PERIOD / self.uiOptions.speedup
        if __debug__ and globaldebug.enabled:
            period *= globaldebug.slowMotionFactor
        now = reactor.seconds()
        if self._expectedTickTime is None:
            delay = period
        else:
            delay = max(0, self._expectedTickTime + period - now)
        self._expectedTickTime = now + delay
        self._nextTick = WeakCallLater(delay, self, 'tick')

        if self.long_tick_profiler:
            self.long_tick_profiler.observation(self.tickPeriod)
        self.jitterLogger.observation(self.tickPeriod)
        if self.jitterLogger.thisCount == 0 and self.jitterLogger.jitter:
            if self.jitterLogger.jitter < self.tickPeriod:
                log.info(
                    'Max server tick jitter: %d ms',
                    1000 * self.jitterLogger.jitter)
            else:
                log.error(
                    'Max server tick jitter: %d ms',
                    1000 * self.jitterLogger.jitter)

        loading = False
        if loading != self.loading:
            self.sendServerCommand(WorldLoadingMsg(loading))

        if loading or self.paused:
            return

        if len(self.players) == 0 or (not self.bots_only and all(
                p.bot for p in self.players)):
            # When there are no more human players in the game, send one
            # last tick to make sure that the RemovePlayerMsg gets through
            # to everyone.
            if self.sentGraceTick:
                return
            self.sentGraceTick = True
        else:
            self.sentGraceTick = False

        tickId = self._lastTickId = (self._lastTickId + 1) % TICK_LIMIT
        self.game.sendServerCommand(TickMsg(tickId))
        self.onServerTickComplete()

    def _startClock(self):
        if self._nextTick is not None:
            self._nextTick.cancel()
        delay = TICK_PERIOD / self.uiOptions.speedup
        if __debug__ and globaldebug.enabled:
            delay *= globaldebug.slowMotionFactor
        if self.long_tick_profiler:
            self.long_tick_profiler.note_gap()
        self.jitterLogger.noteGap()
        self._nextTick = WeakCallLater(delay, self, 'tick')

    def _stopClock(self):
        if self._nextTick is not None:
            self._nextTick.cancel()
            self._nextTick = None
        if self.long_tick_profiler:
            self.long_tick_profiler.note_gap()
        self.jitterLogger.noteGap()

    def stop(self):
        super(ServerUniverse, self).stop()
        self.elephant.on_possessor_left_game.removeListener(self.returnElephantToOwner)
        self.elephant.on_death_of_possessor.removeListener(self.seen_elephant_owner_die)
        self.scenarioManager.stop()

        self._stopClock()

    @TickMsg.handler
    def tickReceived(self, msg):
        super(ServerUniverse, self).tickReceived(msg)

        for region in self.regions:
            region.tick()

    def grenadeExploded(self, killer, pos, radius):
        super(ServerUniverse, self).grenadeExploded(killer, pos, radius)

        if not killer.aggression:
            return
        self.send_explosion_kills(
            killer=killer,
            killer_team=killer.team if killer else None,
            pos=pos,
            radius=radius,
            kill_type=GRENADE_HIT,
            hitpoints=2 * self.physics.playerRespawnHealth,
        )

    def send_explosion_kills(
            self, killer, killer_team, pos, radius, kill_type,
            hitpoints=1, dentonate_friendly_projectiles=False):

        # Kill enemy players in radius
        for player in self.players:
            if (
                    player.dead or player.is_invulnerable()
                    or player.isFriendsWithTeam(killer_team) or player == killer):
                continue
            if distance(player.pos, pos) < radius:
                self.sendKill(player, kill_type, killer, maxHits=hitpoints)

        # Detonate projectiles in radius
        for projectile in self.projectile_by_id.values():
            if not projectile.triggered_by_explosions:
                continue
            if not dentonate_friendly_projectiles:
                if projectile.team == killer_team and killer_team is not None:
                    continue
                if projectile.player == killer and killer is not None:
                    continue
            if distance(projectile.pos, pos) < radius:
                self.callLater(0.2, projectile.caught_in_explosion)

    def sendKill(self, player, hitKind, killer, maxHits=None):
        killerId = killer.id if killer is not None and killer.id != -1 else NO_PLAYER
        hits = player.getTotalHitPoints()
        if maxHits:
            hits = min(hits, maxHits)
        self.sendServerCommand(
            PlayerHitMsg(player.id, hitKind, hits, killerId))

    @FireShoxwaveMsg.handler
    def gotFireShoxwaveMsg(self, msg):
        super(ServerUniverse, self).gotFireShoxwaveMsg(msg)

        firing_player = self.getPlayer(msg.playerId)
        if not firing_player:
            return

        self.send_explosion_kills(
            killer=firing_player,
            killer_team=firing_player.team,
            pos=firing_player.pos,
            radius=SHOXWAVE_RADIUS,
            kill_type=SHOXWAVE_HIT,
        )

    def trosballExploded(self, player):
        self.sendKill(player, TROSBALL_DEATH_HIT, killer=None)
        super(ServerUniverse, self).trosballExploded(player)

    def bomber_exploded(self, player):
        self.sendKill(player, BOMBER_DEATH_HIT, killer=None)
        super(ServerUniverse, self).bomber_exploded(player)


class InteractionDetector:
    '''
    Calculates interactions between players and units such as shots or
    mines.

    This is not used for collectible coins, because they have special
    magic that makes them collectible based on where the client thinks
    the player is.
    '''

    def __init__(self, world: ServerUniverse, resolution=200):
        self.world = world
        self.resolution = resolution
        self.player_buckets = None
        self.projectile_buckets = None

    def get_players(self, *points, buffer=0.):
        if self.player_buckets is None:
            # Divide the live players into buckets so each unit only needs
            # to consider nearby players.
            self.player_buckets = Buckets(self.resolution)
            for player in self.world.players:
                if not player.dead:
                    self.player_buckets.add(player.pos, player)
        return self.player_buckets.get(*points, buffer=buffer)

    def get_projectiles(self, *points, buffer=0.):
        if self.projectile_buckets is None:
            # Divide the live players into buckets so each unit only needs
            # to consider nearby players.
            self.projectile_buckets = Buckets(self.resolution)
            for projectile in self.world.projectile_by_id.values():
                self.projectile_buckets.add(projectile.pos, projectile)
        return self.projectile_buckets.get(*points, buffer=buffer)

    def reset_buckets(self):
        self.player_buckets = None
        self.projectile_buckets = None

    def process_collisions(self):
        for unit in self.get_interacting_units():
            affects = [
                p for p in self.get_players(
                    unit.oldPos, unit.pos, buffer=unit.collision_check_buffer)
                if unit.check_collision(p)]
            if affects:
                unit.collided_with(affects)

        for shot in self.world.shots:
            if shot.gun_type.shots_affect_projectiles:
                for p in self.get_projectiles(
                        shot.oldPos, shot.pos, buffer=shot.collision_check_buffer):
                    if shot.gun_type.check_projectile_collision(shot, p):
                        p.hit_by_shot(shot)

    def get_interacting_units(self) -> Iterable[InteractingUnit]:
        yield from self.world.shots
        for projectile in self.world.projectile_by_id.values():
            if projectile.collides_with_players:
                yield projectile


class Buckets:
    def __init__(self, resolution):
        self.resolution = resolution
        self.buckets = {}

    def add(self, pos, thing):
        x, y = pos
        key = x // self.resolution, y // self.resolution
        if key in self.buckets:
            self.buckets[key].add(thing)
        else:
            self.buckets[key] = {thing}

    def get(self, *points, buffer=0.):
        '''
        Iterates through everything in the buckets bounded by the
        smallest rectangle containing all the given points.
        '''
        min_x = min(p[0] for p in points) - buffer
        max_x = max(p[0] for p in points) + buffer
        min_y = min(p[1] for p in points) - buffer
        max_y = max(p[1] for p in points) + buffer

        for i in range(int(min_x / self.resolution), int(max_x // self.resolution) + 1):
            for j in range(int(min_y // self.resolution), int(max_y // self.resolution) + 1):
                key = i, j
                if key in self.buckets:
                    yield from self.buckets[key]


class Region:
    '''
    Base class for regions for use as event triggers. Regions must be
    registered with the ServerUniverse to have effect.
    '''
    def __init__(self, world, *, include_ghost=False):
        self.world = world
        self.include_ghost = include_ghost
        self.players = set()
        self.onEnter = Event(['player'])
        self.onExit = Event(['player'])

    def debug_draw(self, viewManager, screen):
        pass

    def tick(self):
        players = set(p for p in self.world.players if self._check(p))
        for p in players - self.players:
            self.onEnter(p)
        for p in self.players - players:
            self.onExit(p)
        self.players = players

    def _check(self, player):
        '''
        Calls the subclass, unless the player is dead and dead players
        are excluded.
        '''
        if player.dead and not self.include_ghost:
            return False
        return self.check(player)

    def check(self, player):
        raise NotImplementedError('{}.check', self.__class__.__name__)


class RectRegion(Region):
    def __init__(self, world, rect, zoneDef=None, **kwargs):
        super(RectRegion, self).__init__(world, **kwargs)
        self.rect = Rect(rect)
        if zoneDef is not None:
            self.rect.left += zoneDef.pos[0]
            self.rect.top += zoneDef.pos[1]

    def check(self, player):
        return self.rect.collidepoint(player.pos)

    def debug_draw(self, viewManager, screen):
        from trosnoth.trosnothgui.ingame.utils import mapPosToScreen

        import pygame.draw

        focus = viewManager._focus
        area = viewManager.sRect

        topleft = mapPosToScreen(self.rect.topleft, focus, area)
        bottomright = mapPosToScreen(self.rect.bottomright, focus, area)
        size = (bottomright[0] - topleft[0], bottomright[1] - topleft[1])

        s = pygame.Surface(size)
        s.set_alpha(128)
        s.fill((0, 255, 255))
        screen.blit(s, topleft)

        # pygame.draw.rect(screen, (255, 0, 0, 0.5), pygame.Rect(topleft, size))


class CircleRegion(Region):
    def __init__(self, world, pos, radius, **kwargs):
        super(CircleRegion, self).__init__(world, **kwargs)
        self.pos = pos
        self.radius = radius

    def check(self, player):
        return distance(self.pos, player.pos) <= self.radius


class OrbRegion(CircleRegion):
    def __init__(self, world, room):
        CircleRegion.__init__(self, world, room.orb_pos, ZONE_CAP_DISTANCE)


class PlayerProximityRegion(Region):
    def __init__(self, world, player, dist, **kwargs):
        super(PlayerProximityRegion, self).__init__(world, **kwargs)
        self.player = player
        self.distance = dist

    def check(self, player):
        d = distance(player.pos, self.player.pos)
        return d <= self.distance


class ZoneRegion(Region):
    def __init__(self, zone, **kwargs):
        super(ZoneRegion, self).__init__(zone.world, **kwargs)
        self.zone = zone

    def check(self, player):
        return player in self.zone.players
