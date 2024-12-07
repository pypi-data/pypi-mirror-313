'''
This is the main entrypoint for accessing Trosnoth bots.
'''

import logging
import random
from math import atan2
import os
import sys

from twisted.internet import defer

import trosnoth.bots
from trosnoth.bots.orders import (
    StandStill, MoveGhostToPoint, MoveToOrb, RespawnInZone, FollowPlayer,
    MoveToPoint, CollectTrosball,
)
from trosnoth.bots.pathfinding import PathFindingRoute
from trosnoth.const import (
    GAME_FULL_REASON, UNAUTHORISED_REASON, NICK_USED_REASON,
    USER_IN_GAME_REASON, ALREADY_JOINED_REASON, TICK_PERIOD,
    LEFT_STATE, RIGHT_STATE, JUMP_STATE, DOWN_STATE, DEFAULT_BOT_DIFFICULTY, BOT_DIFFICULTIES,
)
from trosnoth.messages import (
    TickMsg, ResyncPlayerMsg, WorldResetMsg,
    CannotJoinMsg, UpdatePlayerStateMsg,
    AimPlayerAtMsg, GrapplingHookMsg, RespondToGameEndMsg,
)
from trosnoth.model.agent import ConcreteAgent, DiscreteLocalDriver
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.model.upgrades import Bomber
from trosnoth.utils.event import Event
from trosnoth.utils.math import distance
from trosnoth.utils.message import MessageConsumer
from trosnoth.utils.twist import WeakLoopingCall

log = logging.getLogger('bots')
log.setLevel(logging.ERROR)

LOOK_AHEAD_TICKS = 20
MIN_EVASION_TICKS = 5


def get_available_bot_names(show_all=False):
    '''
    Returns a list of strings of the available AI classes.
    '''
    if getattr(sys, 'frozen', False):
        # When frozen, return a standard list
        return ['ranger', 'john', 'sirrobin', 'terminator']

    results = []
    files = os.listdir(os.path.dirname(trosnoth.bots.__file__))
    aiNames = [os.path.splitext(f)[0] for f in files if f.endswith('.py')]

    for aiName in aiNames:
        try:
            c = __import__(
                'trosnoth.bots.%s' % (aiName,), fromlist=['BotClass'])
        except Exception as e:
            log.warning('Error loading AI %r: %s', aiName, e)
            continue
        if hasattr(c, 'BotClass') and (c.BotClass.generic or show_all):
            results.append(aiName)
    return results


def get_bot_class(bot_name):
    c = __import__(f'trosnoth.bots.{bot_name}', fromlist=['BotClass'])
    return c.BotClass


def makeAIAgent(game, bot_name, fromLevel=False, nick=None, difficulty=DEFAULT_BOT_DIFFICULTY):
    bot_class = get_bot_class(bot_name)
    return AIAgent(game, bot_class, fromLevel=fromLevel, nick=nick, difficulty=difficulty)


class AIAgent(ConcreteAgent):
    '''
    Base class for an AI agent.
    '''
    local_player_driver_class = DiscreteLocalDriver

    def __init__(
            self, game, aiClass, fromLevel, nick=None, difficulty=DEFAULT_BOT_DIFFICULTY,
            *args, **kwargs):
        super(AIAgent, self).__init__(game=game, *args, **kwargs)
        self.aiClass = aiClass
        self.fromLevel = fromLevel
        self._initialisationNick = nick
        self.bot_difficulty = difficulty
        self.ai = None
        self.team = None
        self.requestedNick = None
        self._onBotSet = Event([])
        self._loop = WeakLoopingCall(self, '_tick')

    def __str__(self):
        if self.ai:
            bot = self.ai
        else:
            bot = 'None (was {})'.format(self.aiClass.__name__)
        return '{}<{}>'.format(self.__class__.__name__, bot)

    def start(self, team=None):
        self.team = team
        self._loop.start(2)

    def stop(self):
        super(AIAgent, self).stop()
        self._loop.stop()
        if self.ai:
            self.ai.disable()
            self.ai = None

    def detached(self):
        super().detached()
        self.stop()

    def _tick(self):
        if self.ai is not None:
            return

        if self.fromLevel and self._initialisationNick:
            nick = self._initialisationNick
        else:
            nick = self.aiClass.nick

        if self.team is None:
            teamId = NEUTRAL_TEAM_ID
        else:
            teamId = self.team.id

        self._joinGame(nick, teamId)

    def _joinGame(self, nick, teamId):
        self.requestedNick = nick
        self.sendJoinRequest(teamId, nick, bot=True, fromLevel=self.fromLevel)

    @CannotJoinMsg.handler
    def _joinFailed(self, msg):
        r = msg.reasonId
        nick = self.requestedNick

        if r == GAME_FULL_REASON:
            message = 'full'
        elif r == UNAUTHORISED_REASON:
            message = 'not authenticated'
        elif r == NICK_USED_REASON:
            message = 'nick in use'
        elif r == USER_IN_GAME_REASON:
            message = 'user already in game'    # Should never happen
        elif r == ALREADY_JOINED_REASON:
            message = 'tried to join twice'     # Should never happen
        else:
            message = repr(r)

        log.error('Join failed for AI %r (%s)', nick, message)
        self.stop()

    def setPlayer(self, player):
        if player is None and self.ai:
            self.ai.disable()
            self.ai = None

        super(AIAgent, self).setPlayer(player)

        if player:
            self.requestedNick = None
            self.ai = self.aiClass(self.world, self.localState.player, self)
            self._onBotSet()

    @defer.inlineCallbacks
    def getBot(self):
        '''
        @return: a Deferred which fires with this agent's Bot object,
            as soon as it has one.
        '''
        if self.ai is not None:
            defer.returnValue(self.ai)

        yield self._onBotSet.wait()
        defer.returnValue(self.ai)

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        super(AIAgent, self).handle_TickMsg(msg)
        if self.ai:
            self.ai.consumeMsg(msg)

    @ResyncPlayerMsg.handler
    def handle_ResyncPlayerMsg(self, msg):
        super(AIAgent, self).handle_ResyncPlayerMsg(msg)
        if self.ai:
            self.ai.playerResynced()

    @WorldResetMsg.handler
    def handle_WorldResetMsg(self, msg):
        super().handle_WorldResetMsg(msg)
        if self.ai:
            self.ai.worldReset()

    def defaultHandler(self, msg):
        super(AIAgent, self).defaultHandler(msg)
        if self.ai:
            self.ai.consumeMsg(msg)


class Bot(MessageConsumer):
    '''
    Base class for Trosnoth bots, provides functionality for basic orders like
    moving to points or zones, attacking enemies, and using upgrades.
    '''
    generic = False     # Change to True to allow bot to be selected for
                        # generic situations (e.g. lobby)
    maxShotDelay = 0.2
    detectStuck = True
    STUCK_CHECK_INTERVAL = 1    # seconds

    def __init__(self, world, player, agent, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.world = world
        self.player = player
        self.agent = agent

        pause, perfectionism, dodge = BOT_DIFFICULTIES[self.difficulty]
        self.pause_between_actions = pause
        self.pathfinding_perfectionism = perfectionism
        self.dodges_bullets = dodge

        self.currentOrder = StandStill(self)
        self.currentRoute = None
        self.aggression = True
        self.upgrade_choice = None
        self.upgrade_callback = None
        self.upgrade_callback_cost = 0
        self.upgrade_callback_delay = 0
        self.upgrade_callback_waited = 0
        self.stuckCall = None
        self.lastStuckCheckInfo = {}
        self._angleRequestedThisTick = None
        self.game_is_over = False

        self.start()

    def __str__(self):
        return '{}: {}'.format(
            self.__class__.__name__,
            repr(self.player.nick) if self.player else '-')

    @property
    def difficulty(self):
        return self.agent.bot_difficulty

    def sendRequest(self, msg):
        self.agent.sendRequest(msg)

    def applyStateChanges(self, changes):
        '''
        Sends messages to adjust this player's key state according to the
        given state changes. This is a utility method designed to be used by
        the bot movement system. Calling it directly from bot subclasses may
        interfere with bot motion and pathfinding.
        '''
        for key, value in changes:
            self.sendRequest(UpdatePlayerStateMsg(value, stateKey=key))

    def applyInputState(self, inputState):
        directions = [
            (LEFT_STATE, inputState.left),
            (RIGHT_STATE, inputState.right),
            (JUMP_STATE, inputState.jump),
            (DOWN_STATE, inputState.drop),
        ]
        for key, value in directions:
            if self.player.getState(key) != value:
                self.sendRequest(UpdatePlayerStateMsg(value, stateKey=key))

        self.sendRequest(AimPlayerAtMsg(inputState.angle, inputState.thrust))
        self._angleRequestedThisTick = (inputState.angle, inputState.thrust)
        self.sendRequest(GrapplingHookMsg(inputState.hook))

    def releaseMovementKeys(self):
        '''
        Updates the player's key state so that it is not pressing any of the
        keys. This method should not be called directly by subclasses. It
        should only be called by the bot movement system, otherwise it may
        interfere with other bot motion. To order the bot to stand still,
        use standStill() instead.
        '''
        changes = self.player.buildStateChanges({})
        self.applyStateChanges(changes)

    def start(self):
        self.player.onDied.addListener(self._playerDied)
        self.player.onRespawned.addListener(self._playerRespawned)
        self.player.onUsedUpgrade.addListener(self._playerUsedUpgrade)
        if not self.stuckCall:
            self.stuckCall = self.world.callLater(
                self.STUCK_CHECK_INTERVAL, self.doStuckCheck)

    def disable(self):
        self.clear_upgrade_callback()
        self.player.onDied.removeListener(self._playerDied)
        self.player.onRespawned.removeListener(self._playerRespawned)
        self.player.onUsedUpgrade.removeListener(self._playerUsedUpgrade)
        if self.stuckCall:
            self.stuckCall.cancel()
            self.stuckCall = None

    def doStuckCheck(self):
        if self.agent.stopped:
            log.error(
                'Bot loop running after stop: %r / %r', self, self.agent)
            self.stuckCall = None
            return

        self.stuckCall = self.world.callLater(
            self.STUCK_CHECK_INTERVAL, self.doStuckCheck)
        info = self.lastStuckCheckInfo
        if not self.detectStuck or self.player.dead or isinstance(
                self.currentOrder, StandStill):
            info['released'] = info['pos'] = info['yVel'] = None
            return
        if (
                info.get('pos') == self.player.pos
                and info.get('yVel') == self.player.yVel):
            if not info.get('released'):
                self.releaseMovementKeys()
                info['released'] = True
            elif not self.player.items.has(Bomber):
                self.buy_upgrade(Bomber)
        else:
            info['released'] = False
            info['pos'] = self.player.pos
            info['yVel'] = self.player.yVel

    @RespondToGameEndMsg.handler
    def handle_RespondToGameEndMsg(self, msg):
        if self.player and msg.player_id == self.player.id:
            self.game_is_over = True
            self.standStill()

    def defaultHandler(self, msg):
        pass

    def orderFinished(self):
        '''
        Called by an order when it is complete or cannot continue further. May
        be overridden by subclasses.
        '''
        self.standStill()

    #
    # ==== Order interface ====
    #

    def setOrder(self, order):
        '''
        Starts the given order. Generally, bots should use the methods below in
        preference to this one.
        '''
        if self.game_is_over:
            order = StandStill(self)
        self.currentRoute = None
        self.currentOrder = order
        order.start()

    def standStill(self):
        '''
        Orders the bot to stop moving. If it's in the air, it will complete its
        current jump / fall motion.
        '''
        self.setOrder(StandStill(self))

    def moveToPoint(self, pos):
        '''
        Orders the bot to move as close as possible to the given point.
        '''
        if self.player.dead:
            self.setOrder(MoveGhostToPoint(self, pos))
        else:
            self.setOrder(MoveToPoint(self, pos))

    def move_to_room(self, room, *, sprint=False):
        '''
        Orders the bot to move into the given room.
        '''
        if self.player.dead:
            self.setOrder(MoveGhostToPoint(self, room.centre, stopOnZoneEntry=room))
        else:
            self.setOrder(MoveToOrb(self, room, stop_on_entry=True, sprint=sprint))

    def move_to_orb(self, room, *, sprint=False):
        '''
        Orders the bot to touch the orb of the given room.
        '''
        if self.player.dead:
            self.setOrder(MoveGhostToPoint(self, room.orb_pos))
        else:
            self.setOrder(MoveToOrb(self, room, sprint=sprint))

    def attackPlayer(self, player):
        '''
        Orders the bot to hunt down and kill the given player.
        '''
        if self.player.dead:
            raise RuntimeError('ghosts cannot attack')

        self.setOrder(FollowPlayer(self, player, attack=True))

    def followPlayer(self, player):
        '''
        Orders the bot to get as close as possible to the given player and stay
        there until either the player dies, or another order is given.
        '''
        if self.player.dead:
            raise RuntimeError('ghosts cannot follow players')

        self.setOrder(FollowPlayer(self, player))

    def collectTrosball(self):
        '''
        Orders the bot to move towards the trosball.
        '''
        if self.player.dead:
            raise RuntimeError('ghosts cannot collect Trosball')

        self.setOrder(CollectTrosball(self))

    def respawn(self, zone=None):
        '''
        Orders the bot to respawn, with an optional zone to move to first.
        '''
        if not self.player.dead:
            raise RuntimeError('living player cannot respawn')

        if zone is None:
            zone = self.player.getZone()
            if zone is None:
                raise RuntimeError('player is currently outside all zones')

        self.setOrder(RespawnInZone(self, zone))

    def setAggression(self, aggression):
        '''
        Determines whether the bot will, while carrying out its other orders,
        shoot at any enemies it sees.
        '''
        self.aggression = aggression

    def set_dodges_bullets(self, dodges_bullets):
        '''
        Determines whether the bot will attempt to avoid enemy bullets
        @param dodges_bullets: Boolean
        '''
        self.dodges_bullets = dodges_bullets

    def set_upgrade_callback(self, cost, callback, delay=0):
        '''
        Calls the given callback delay after the bot has cost money for
        delay seconds. Clears any previously set upgrade callback.
        '''
        self.upgrade_callback = callback
        self.upgrade_callback_cost = cost
        self.upgrade_callback_delay = delay
        self.upgrade_callback_waited = 0

    def clear_upgrade_callback(self):
        self.set_upgrade_callback(0, None)

    def setUpgradePolicy(self, upgrade, coinBuffer=0, delay=0):
        '''
        Tells this bot how to approach purchasing upgrades. This setting
        persists until it is changed with another call to this function.

        upgrade: which upgrade to purchase, or None to disable buying
        coinBuffer: how many surplus coins should there be before purchasing
        delay: how long should the bot wait after there are enough coins
        '''
        self.upgrade_choice = upgrade
        if upgrade is None:
            self.clear_upgrade_callback()
        else:
            cost = upgrade.requiredCoins + coinBuffer
            self.set_upgrade_callback(cost, self._do_upgrade_purchase, delay=delay)

    def _do_upgrade_purchase(self):
        if self.player.items.has(Bomber) or not self.upgrade_choice:
            return
        self.buy_upgrade(self.upgrade_choice)

    #
    # ==== End order interface ====
    #

    def _playerDied(self, killer, deathType):
        self.currentRoute = None
        self.sendRequest(AimPlayerAtMsg(0, 0))
        self.currentOrder.playerDied()

    def _playerRespawned(self):
        self.currentRoute = None
        self.currentOrder.playerRespawned()

    def _playerUsedUpgrade(self, upgrade):
        if isinstance(upgrade, Bomber) and self.player.bomber:
            # There's no point doing any calculations for moving anywhere
            self.standStill()

    def playerResynced(self):
        '''
        Called when the current player's position jumps due to a resync
        message.
        '''
        self.currentRoute = None
        self.currentOrder.restart()
        self.handle_TickMsg(None)

    def worldReset(self):
        '''
        Called when the current player's position jumps due to a world reset
        message.
        '''
        self.standStill()

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        self._angleRequestedThisTick = None

        if self.world.loading:
            return

        self.currentOrder.tick()

        if not self.player.dead:
            if self.aggression:
                self._shootAtEnemyIfPossible()

            if self.upgrade_callback:
                self._check_upgrade_callback()

            if self.hasUnfinishedRoute():
                self.currentRoute.applyOneFrame(self)

    def _shootAtEnemyIfPossible(self):
        for p in self.world.players:
            if self.player.isFriendsWith(p):
                continue
            if self.canHitPlayer(p):
                self.fireShotAtPoint(p.pos)

    def canHitPlayer(self, target):
        physics = self.world.physics
        gunRange = physics.shotLifetime * physics.shotSpeed

        if target.dead or target.invisible:
            return False

        if distance(self.player.pos, target.pos) < gunRange:
            # Check if we can shoot without hitting obstacles
            if self.player.can_shoot():
                shot = self.player.createShot()
                deltaX = target.pos[0] - self.player.pos[0]
                deltaY = target.pos[1] - self.player.pos[1]
                collision = physics.getCollision(
                    shot, (deltaX, deltaY), ignoreLedges=True)
                if collision is None:
                    return True
        return False

    def fireShotAtPoint(self, pos, error=0.15, delay=None):
        if delay is None:
            delay = random.random() * self.maxShotDelay
        if delay == 0:
            self._fireShotAtPointNow(pos, error)
        else:
            self.world.callLater(delay, self._fireShotAtPointNow, pos, error)

    def _fireShotAtPointNow(self, pos, error=0.15):
        if self.agent.stopped or self.player.dead:
            return
        thrust = 1.0
        x1, y1 = self.player.pos
        x2, y2 = pos
        angle = atan2(x2 - x1, -(y2 - y1))
        angle += error * (2 * random.random() - 1)
        self.sendRequest(AimPlayerAtMsg(angle, thrust))
        self.player.current_gun.please_shoot()

        if self._angleRequestedThisTick is not None:
            angle, thrust = self._angleRequestedThisTick
            self.sendRequest(AimPlayerAtMsg(angle, thrust))

    def _check_upgrade_callback(self):
        if self.player.coins < self.upgrade_callback_cost:
            self.upgrade_callback_waited = 0
        elif self.upgrade_callback_waited >= self.upgrade_callback_delay:
            self.upgrade_callback_waited = 0
            self.upgrade_callback()
        else:
            self.upgrade_callback_waited += TICK_PERIOD

    def buy_upgrade(self, upgrade_class):
        if upgrade_class.is_buyable(self.player):
            upgrade_class.please_use(self.player)

    def setRoute(self, route):
        self.currentRoute = route
        route.started(self)

    def getOrCreateRoute(self):
        if not self.hasUnfinishedRoute():
            self.setRoute(PathFindingRoute(self.player))
        return self.currentRoute

    def create_hypothetical_route(self):
        start_point = None
        if self.hasUnfinishedRoute():
            start_point = self.currentRoute.steps[0].end
        if start_point is None:
            start_point = self.player.last_stationary_point
        return PathFindingRoute(self.player, start_point=start_point)

    def hasUnfinishedRoute(self):
        return self.currentRoute and not self.currentRoute.isFinished()
