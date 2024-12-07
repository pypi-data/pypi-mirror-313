import logging
import time
import typing

from twisted.internet import reactor

from trosnoth.const import (
    TICK_PERIOD, BOT_GOAL_NONE, HEAD_CUEBALL,
)
from trosnoth.messages import (
    JoinRequestMsg, TickMsg, ResyncPlayerMsg, UpdatePlayerStateMsg,
    AimPlayerAtMsg, UpgradeApprovedMsg, PlayerHasUpgradeMsg,
    CheckSyncMsg, WorldResetMsg, PlayerUpdateMsg,
    PlayerAllDeadMsg, ContributeToTeamBoostMsg, PlayerTickActionsMsg,
)
from trosnoth.model.shot import LocalShot, LocalGrenade
from trosnoth.model.trosball import LocalTrosball
from trosnoth.model.upgrades import Shoxwave
from trosnoth.utils.event import Event
from trosnoth.utils.message import MessageConsumer

log = logging.getLogger(__name__)

SYNC_CHECK_PERIOD = 3


class Agent(object):
    '''
    Base class for things which can be connected to a Game using Game.addAgent.
    This may represent a user interface, an AI player, someone connecting over
    the network, or anything else that wants to receive interact with the game.
    '''

    def __init__(self, game, *args, **kwargs):
        super(Agent, self).__init__(*args, **kwargs)
        self.game = game
        self.user = None
        self.player = None
        self.onPlayerSet = Event([])
        self.stopped = False
        self.botPlayerAllowed = False
        self.botRequestFromLevel = False

    def allowBotPlayer(self, fromLevel):
        self.botPlayerAllowed = True
        self.botRequestFromLevel = fromLevel

    def stop(self):
        '''
        Disconnects this agent from things that it's subscribed to and stops
        any active timed or looping calls.
        '''
        self.stopped = True

    def detached(self):
        '''
        Called after this agent has been detached from a Game.
        '''
        pass

    def setPlayer(self, player):
        '''
        Called by the connected Game object when we are given authority to
        control the specified player. Also called with player=None when we no
        longer have the authority to control any player.
        '''
        self.player = player
        reactor.callLater(0, self.onPlayerSet.execute)

    def messageToAgent(self, msg):
        '''
        Called by the connected Game object when there is a message
        specifically for this Agent (as opposed to a general game message).
        '''
        raise NotImplementedError(
            '%s.messageToAgent' % (self.__class__.__name__,))


class AimMessageTracker:
    def __init__(self):
        self.last_angle_and_thrust = (None, None)
        self.last_angle_sent = None
        self.last_thrust_sent = None

    def check_for_change(self, player):
        if player is None:
            return False
        return self.last_angle_and_thrust != (player.angleFacing, player.ghostThrust)

    def update_was_sent(self, player):
        if player is None:
            self.last_angle_and_thrust = (None, None)
        else:
            self.last_angle_and_thrust = (player.angleFacing, player.ghostThrust)


class TickActionsBundler:
    def __init__(self, agent):
        self.agent = agent
        self.game = agent.game
        self.bundle = []
        self.tick_id = None
        self.aim_tracker = AimMessageTracker()

    def add_message(self, msg):
        if isinstance(msg, AimPlayerAtMsg):
            # Special case: apply aim messages to the local state, but don't
            # indiscriminately send them to the server as they are mostly
            # cosmetic.
            return
        if msg.requires_aim:
            self.append_aim_if_changed()

        self.bundle.append(msg)

    def append_aim_if_changed(self):
        player = self.agent.localState.player
        if self.aim_tracker.check_for_change(player):
            self.bundle.append(AimPlayerAtMsg(player.angleFacing, player.ghostThrust))
            self.aim_tracker.update_was_sent(player)

    def send_to_game(self):
        self.append_aim_if_changed()
        for msg in self.bundle:
            msg.tracePoint(self, 'send_to_game')
        self.game.agentRequest(self.agent, PlayerTickActionsMsg.build(
            tick_id=self.game.world.lastTickId, messages=self.bundle))
        self.tick_id = None
        self.bundle = []


class PlayerSyncChecker:
    def __init__(self, world, send_request):
        self.world = world
        self.send_request = send_request
        self.time_to_next_check = SYNC_CHECK_PERIOD

    def reset_check_time(self):
        self.time_to_next_check = SYNC_CHECK_PERIOD

    def tick(self, local_player):
        self.time_to_next_check -= TICK_PERIOD
        if local_player and self.time_to_next_check <= 0:
            self.time_to_next_check += SYNC_CHECK_PERIOD
            self.send_request(
                CheckSyncMsg(local_player.pos[0], local_player.pos[1], local_player.yVel))


class LocalPlayerDriver:
    def __init__(self, world, tick_callback):
        self.world = world
        self.tick_callback = tick_callback

    def reset(self):
        '''
        This is called when the player has been completely reset, e.g.,
        after a resync or a world reset.
        '''
        pass

    def game_paused(self):
        '''
        Called when the game is paused.
        '''
        pass

    def game_resumed(self):
        '''
        Called when the paused game is resumed.
        '''
        pass

    def world_ticked(self):
        '''
        This is called whenever the underlying world processes a tick.
        '''
        raise NotImplementedError

    def ui_tick(self, delta_t):
        '''
        This may be called to indicate that the UI has advanced one
        frame, with a time of delta_t since the last frame.

        It must return a tuple of (player_tick, player_fraction) for
        use when drawing the local player in the UI.

        Note that some concrete agents (e.g., AIAgent) might never call
        this method.
        '''
        raise NotImplementedError


class ConcreteAgent(Agent, MessageConsumer):
    '''
    Base class for Agents that actually represent the world (rather than
    proxying it through to the Network or some other agent).

    Note that a concrete agent is designed to represent only zero or one
    players.
    '''
    local_player_driver_class: typing.Type[LocalPlayerDriver]

    def __init__(self, *args, **kwargs):
        super(ConcreteAgent, self).__init__(*args, **kwargs)
        self.world = self.game.world
        self.tick_actions_bundler = TickActionsBundler(self)
        self.localState = LocalState(self)
        self.local_player_driver = self.local_player_driver_class(
            self.game.world, self.send_local_player_actions)
        self.alreadySendingRequest = False
        self.sendRequestQueue = []
        self.game.onServerCommand.addListener(self.gotServerCommand)
        self.game.world.on_pause_state_changed.addListener(self.world_pause_state_changed)

    def stop(self):
        super().stop()
        self.game.onServerCommand.removeListener(self.gotServerCommand)
        self.game.world.on_pause_state_changed.removeListener(self.world_pause_state_changed)
        self.localState.stop()

    def gotServerCommand(self, msg):
        msg.tracePoint(self, 'gotServerCommand')
        self.consumeMsg(msg)

    def world_pause_state_changed(self):
        if self.world.paused:
            self.local_player_driver.game_paused()
        else:
            self.local_player_driver.game_resumed()

    def messageToAgent(self, msg):
        msg.tracePoint(self, 'messageToAgent')
        self.consumeMsg(msg)

    def sendRequest(self, msg):
        if self.stopped:
            log.error('Stopped agent trying to send %r: %s', msg, self)
            # log.error(''.join(traceback.format_stack()))
            return
        msg.tracePoint(self, 'sendRequest')

        self.sendRequestQueue.append(msg)
        if self.alreadySendingRequest:
            # The actual sending will be done in the parent's loop
            return

        self.alreadySendingRequest = True
        try:
            while self.sendRequestQueue:
                self.processSendRequestQueue()
        finally:
            self.alreadySendingRequest = False

    def processSendRequestQueue(self):
        msg = self.sendRequestQueue.pop(0)
        msg.tracePoint(self, 'processSendRequestQueue')

        if not msg.clientValidate(
                self.localState, self.world, self._validationResponse):
            msg.tracePoint(self, 'failed clientValidate')
            return

        msg.applyRequestToLocalState(self.localState)
        self.request_approved_for_sending_to_game(msg)

    def request_approved_for_sending_to_game(self, msg):
        msg.tracePoint(self, 'request_approved_for_sending_to_game')
        if msg.is_tick_action:
            self.tick_actions_bundler.add_message(msg)
        else:
            reactor.callLater(0, self.game.agentRequest, self, msg)

    def _validationResponse(self, msg):
        self.consumeMsg(msg)

    def defaultHandler(self, msg):
        msg.tracePoint(self, 'defaultHandler')
        msg.applyOrderToLocalState(self.localState, self.world)

    def setPlayer(self, player):
        super(ConcreteAgent, self).setPlayer(player)
        if player:
            self.localState.playerJoined(player)
        elif self.player:
            self.localState.lostPlayer()

    @WorldResetMsg.handler
    def handle_WorldResetMsg(self, msg):
        if self.player is not None:
            oldKeyState = dict(self.localState.player._state)
            self.localState.refreshPlayer()
            self.resyncLocalPlayer(oldKeyState)

        self.localState.world_was_reset()

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        self.local_player_driver.world_ticked()
        self.localState.world_ticked()

    def send_local_player_actions(self):
        if self.player is None:
            return
        self.tick_actions_bundler.send_to_game()
        self.localState.player_tick()

    @ResyncPlayerMsg.handler
    def handle_ResyncPlayerMsg(self, msg):
        oldKeyState = dict(self.localState.player._state)
        self.localState.player.applyPlayerUpdate(msg)
        self.resyncLocalPlayer(oldKeyState)

    def resyncLocalPlayer(self, oldKeyState):
        newKeyState = self.localState.player._state
        self.sendRequest(self.localState.player.buildResyncAcknowledgement())
        self.localState.sync_checker.reset_check_time()
        self.local_player_driver.reset()

        for key, value in list(oldKeyState.items()):
            if value != newKeyState[key]:
                self.sendRequest(UpdatePlayerStateMsg(value, stateKey=key))

    @UpgradeApprovedMsg.handler
    def handle_UpgradeApprovedMsg(self, msg):
        self.sendRequest(PlayerHasUpgradeMsg(msg.upgradeType))

    def sendJoinRequest(
            self, teamId, nick, head=HEAD_CUEBALL, bot=False, fromLevel=False):
        if self.player is not None:
            raise RuntimeError('Already joined.')

        msg = JoinRequestMsg(teamId, nick=nick.encode(), bot=bot, head=head)
        if bot:
            msg.localBotRequest = True
        if fromLevel:
            msg.botRequestFromLevel = True

        self.sendRequest(msg)

    def please_contribute_to_team_boost(self, boost_class, coins):
        if not self.player or not self.player.team:
            return
        self.sendRequest(
            ContributeToTeamBoostMsg(boost_class.boost_code, coins, self.player.team.id))


class DiscreteLocalDriver(LocalPlayerDriver):
    '''
    For bots and other situations where a smooth UI isn't necessary.
    '''

    def __init__(self, world, tick_callback):
        super().__init__(world, tick_callback)
        self.time_progress = 0
        self.last_time = time.time()

    def reset(self):
        self.time_progress = 0

    def game_paused(self):
        now = time.time()
        self.time_progress += now - self.last_time
        self.last_time = now

    def game_resumed(self):
        self.last_time = time.time()

    def world_ticked(self):
        now = time.time()
        self.time_progress += now - self.last_time
        tick_period = TICK_PERIOD / self.world.uiOptions.speedup
        self.time_progress = min(tick_period, self.time_progress)

        # If ticks are coming too quickly, don't tick the local player
        if self.time_progress >= 0:
            self.time_progress -= tick_period
            self.tick_callback()

    def ui_tick(self, delta_t):
        # This local player driver class is not designed to be used by
        # the UI, so don't bother calculating anything for animations.
        return 0, 1


class LocalPlayerSmoother(LocalPlayerDriver):
    '''
    For the UI. If world ticks come too slowly, this driver gradually
    slows down the rate of local player ticks until they catch up again.
    '''

    # The time it takes for local player to smoothly stop and start
    # after world ticks stop or catch up
    TIME_TO_HALT = 5
    TIME_TO_RESUME = .5

    # From v = ut + ½at²
    DECELLERATION = 2 / TIME_TO_HALT
    ACCELERATION = 2 / TIME_TO_RESUME

    def __init__(self, world, tick_callback):
        super().__init__(world, tick_callback)
        self.counter = 0
        self.fraction = 1
        self.world_ticks_missed = 0
        self.rate = 1
        self.paused = False

    def reset(self):
        self.counter = 0
        self.fraction = 1
        self.world_ticks_missed = 0
        self.rate = 1

    def game_paused(self):
        self.paused = True

    def game_resumed(self):
        self.paused = False

    def world_ticked(self):
        self.world_ticks_missed = max(0, self.world_ticks_missed - 1)

    def ui_tick(self, delta_t):
        if self.paused:
            return (self.counter, min(1, self.fraction))

        if self.rate == 1 and self.world_ticks_missed < 2:
            # Give some leeway: only start slowing down if it exceeds 2
            pass
        elif self.world_ticks_missed > 1:
            # Gradually slow down until things catch up
            self.rate = max(0, self.rate - self.DECELLERATION * delta_t)
        else:
            # It's caught up, so gradually speed up again
            self.rate = min(1, self.rate + self.ACCELERATION * delta_t)

        tick_period = TICK_PERIOD / self.world.uiOptions.speedup
        self.fraction += delta_t * self.rate / tick_period
        if self.fraction >= 1:
            self.advance_local_player()
        return (self.counter, min(1, self.fraction))

    def advance_local_player(self):
        self.counter += 1
        self.fraction -= 1
        self.world_ticks_missed += 1
        self.tick_callback()


class LocalState(object):
    '''
    Stores state information which a client wants to keep which do not need to
    wait for a round trip to the server. e.g. when a player moves, it should
    start moving on the local screen even before the server has received the
    message.
    '''

    LOCAL_ID_CAP = 1 << 16

    def __init__(self, agent):
        self.onGameInfoChanged = Event([])
        self.agent = agent
        self.world = agent.world
        self.player = None
        self.onShoxwave = Event()
        self.onAddLocalShot = Event()
        self.onRemoveLocalShot = Event()
        self.shotById = {}
        self.localShots = {}
        self.local_grenades = []
        self.projectiles = LocalProjectileCollection(self)
        self.projectile_monitor = ProjectileMonitor(self)
        self.localTrosball = None
        self.trosballResetCall = None
        self.nextLocalId = 1
        self.userTitle = ''
        self.userInfo = ()
        self.botGoal = BOT_GOAL_NONE
        self.unverifiedItems = []
        self.pings = {}
        self.lastPingTime = None
        self.slow_pings = {}
        self.slow_ping_time = None
        self.checked_collectables_this_world_tick = False
        self.sync_checker = PlayerSyncChecker(self.world, self.agent.sendRequest)

        self.world.onShotRemoved.addListener(self.shotRemoved)
        self.world.on_before_tick.addListener(self.before_world_tick)

    def stop(self):
        self.world.onShotRemoved.removeListener(self.shotRemoved)
        self.world.on_before_tick.removeListener(self.before_world_tick)

    def gotPingTime(self, pingTime):
        self.lastPingTime = pingTime

    def got_slow_ping(self, ping_time):
        self.slow_ping_time = ping_time

    @property
    def shots(self):
        for shot in list(self.shotById.values()):
            yield shot
        for shot in list(self.localShots.values()):
            yield shot

    def playerJoined(self, player):
        # Create a shallow copy of the player object, and use it to simulate
        # movement before the server approves it.
        self.player = player.clone()

        player.onCoinsChanged.addListener(self.playerCoinsChanged)
        self.player.onDied.addListener(self.projectionDied)
        self.agent.player.on_phantom_respawn.addListener(self.projection_respawn_failed)

        self.reset_local_copies()

    def refreshPlayer(self):
        realPlayer = self.world.playerWithId[self.player.id]
        self.player.restore(realPlayer.dump())

    def world_was_reset(self):
        self.reset_local_copies()

    def reset_local_copies(self):
        self.projectiles.clear()
        self.projectile_monitor.reset()

        if self.player:
            # If we don't do this, grenades already thrown by this user
            # will not show. This is only really important for screeshot
            # generation, as the server removes all grenades, shots,
            # etc. when resetting a world.
            self.local_grenades = [
                LocalGrenade.rebuild(self.world, g.dump(), local_state=self)
                for g in self.world.grenades if g.player.id == self.player.id]
            for lg in self.local_grenades:
                lg.realShotStarted = True
                lg.realShotCaughtUp = True
        else:
            self.local_grenades = []

    def playerCoinsChanged(self, oldCoins):
        player = self.world.getPlayer(self.player.id)
        self.player.coins = player.coins

    def projection_respawn_failed(self):
        self.acknowledge_projection_is_dead(from_respawn=True)

    def projectionDied(self, killer, deathType):
        self.acknowledge_projection_is_dead()

    def acknowledge_projection_is_dead(self, from_respawn=False):
        for shot in list(self.localShots.values()):
            self.onRemoveLocalShot(shot)
        self.localShots.clear()
        self.agent.sendRequest(PlayerAllDeadMsg(from_respawn=from_respawn))

    def lostPlayer(self):
        realPlayer = self.world.getPlayer(self.player.id)
        if realPlayer:
            realPlayer.onCoinsChanged.removeListener(self.playerCoinsChanged)
        self.player.onDied.removeListener(self.projectionDied)
        self.agent.player.on_phantom_respawn.removeListener(self.projection_respawn_failed)
        self.player = None

    def shotFired(self, gun_type):
        if gun_type == Shoxwave:
            self.onShoxwave()
            localId = 0
        else:
            localId = self.nextLocalId
            self.nextLocalId = (self.nextLocalId + 1) % self.LOCAL_ID_CAP
            self.localShots[localId] = shot = self.player.createShot(
                shotClass=LocalShot, gun_type=gun_type)
            self.onAddLocalShot(shot)
        self.player.guns.gun_was_fired(gun_type)
        return localId

    def matchShot(self, localId, shotId):
        if localId in self.localShots:
            shot = self.localShots.pop(localId)
            shot.realShotStarted = True
            self.shotById[shotId] = shot

    def shotRemoved(self, shotId, *args, **kwargs):
        if shotId in self.shotById:
            shot = self.shotById[shotId]
            del self.shotById[shotId]
            self.onRemoveLocalShot(shot)

    def grenadeLaunched(self):
        self.local_grenades.append(LocalGrenade(self, self.world, self.player))

    def matchGrenade(self):
        for grenade in self.local_grenades:
            if not grenade.realShotStarted:
                grenade.realShotStarted = True
                break

    def grenadeRemoved(self):
        self.local_grenades.pop(0)

    def trosballThrown(self):
        self.localTrosball = LocalTrosball(self.world)
        self.localTrosball.onRealShotCaughtUp.addListener(
            self.trosballCaughtUp)
        vel = self.world.trosballManager.getThrowVelocity(self.player)
        self.localTrosball.teleport(self.player.pos, vel)
        if self.trosballResetCall:
            self.trosballResetCall.cancel()
        self.trosballResetCall = self.world.callLater(2, self.revertTrosball)

    def matchTrosball(self):
        self.localTrosball.realShotStarted = True

    def trosballCaughtUp(self, sprite):
        self.revertTrosball()

    def revertTrosball(self):
        self.localTrosball = None
        if self.trosballResetCall:
            self.trosballResetCall.cancel()

    def player_tick(self):
        if self.player:
            self.player.reset()
            self.player.advance()
            self.check_collectables()
            self.projectile_monitor.local_player_ticked()
            self.sync_checker.tick(self.player)

    def check_collectables(self):
        self.checked_collectables_this_world_tick = True
        if self.player is None or self.player.dead:
            return

        for unit in self.world.getCollectableUnits():
            if unit.hitLocalPlayer:
                continue
            if unit.checkCollision(self.player, 0):
                unit.collidedWithLocalPlayer(self.player)

    def before_world_tick(self):
        if not self.checked_collectables_this_world_tick:
            self.check_collectables()

    def world_ticked(self):
        for shot in list(self.shotById.values()) + list(self.localShots.values()):
            shot.reset()
            shot.advance()
        for grenade in self.local_grenades:
            grenade.reset()
            grenade.advance()
        if self.localTrosball:
            self.localTrosball.reset()
            self.localTrosball.advance()

        for unit in list(self.projectiles):
            unit.reset()
            unit.advance()

        for shotId, shot in list(self.shotById.items()):
            if shot.expired:
                del self.shotById[shotId]
                self.onRemoveLocalShot(shot)
        for localId, shot in list(self.localShots.items()):
            if shot.expired:
                del self.localShots[localId]
                self.onRemoveLocalShot(shot)

    def addUnverifiedItem(self, item):
        self.unverifiedItems.append(item)

    def discardUnverifiedItem(self, item):
        self.unverifiedItems.remove(item)

    def popUnverifiedItem(self):
        if self.unverifiedItems:
            return self.unverifiedItems.pop(0)
        return None


class LocalProjectileCollection:
    def __init__(self, local_state):
        self.local_state = local_state
        self.new_official_projectile = None
        self.projectiles = set()
        self.by_official_id = {}

    def __iter__(self):
        yield from self.projectiles

    def clear(self):
        self.new_official_projectile = None
        self.projectiles.clear()
        self.by_official_id.clear()

    def add(self, projectile):
        self.projectiles.add(projectile)

    def denied(self, projectile):
        self.projectiles.discard(projectile)

    def remove_by_id(self, projectile_id):
        if projectile_id in self.by_official_id:
            projectile = self.by_official_id.pop(projectile_id)
            self.projectiles.remove(projectile)

    def match(self, local_projectile):
        if self.new_official_projectile is None:
            log.error('match_projectile() called with no official projectile set')
            self.projectiles.discard(local_projectile)
            return

        local_projectile.match_projectile(self.new_official_projectile)
        self.by_official_id[self.new_official_projectile.id] = local_projectile
        self.new_official_projectile = None

    def official_projectile_added(self, official_projectile):
        if self.new_official_projectile:
            log.error('official_projectile_added() without previous projectile being matched')
        self.new_official_projectile = official_projectile


class LocalProjectileInfo:
    def __init__(self):
        self.hits = 0
        self.ticks_since_hit = 0

    def advance(self):
        self.ticks_since_hit += 1
        if self.ticks_since_hit >= 2:
            self.ticks_since_hit = 2
            self.hits = 0

    def hit(self):
        self.hits += 1
        self.ticks_since_hit = 0


class ProjectileMonitor:
    def __init__(self, local_state):
        self.local_state = local_state
        self.projectiles = {}

    def reset(self):
        self.projectiles = {}

    def get_hits(self, projectile):
        try:
            return self.projectiles[projectile.id].hits
        except KeyError:
            return 0

    def local_player_ticked(self):
        for shot in self.local_state.shots:
            if shot.originatingPlayer != self.local_state.player:
                continue
            if not shot.gun_type.shots_affect_projectiles:
                continue
            for projectile_id, projectile_info in self.projectiles.items():
                projectile = self.local_state.world.projectile_by_id[projectile_id]
                if shot.gun_type.check_projectile_collision(shot, projectile):
                    projectile_info.hit()

        for projectile_info in self.projectiles.values():
            projectile_info.advance()

    def projectile_launched(self, projectile):
        if projectile.triggered_by_detonation_beam:
            self.projectiles[projectile.id] = LocalProjectileInfo()

    def remove_projectile(self, projectile_id):
        try:
            del self.projectiles[projectile_id]
        except KeyError:
            pass
