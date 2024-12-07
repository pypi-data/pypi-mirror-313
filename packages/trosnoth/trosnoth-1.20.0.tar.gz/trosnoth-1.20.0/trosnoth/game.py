import asyncio
import dataclasses
import logging
from typing import List

from trosnoth.model.uithrottler import UIMsgThrottler, LocalGameTweener, Tweener
from twisted.internet import defer

from trosnoth import version
from trosnoth.bots.base import makeAIAgent
from trosnoth.const import (
    DEFAULT_BOT_DIFFICULTY,
    DISABLE_BOTS, TICK_PERIOD,
)
from trosnoth.gamerecording.achievements import AchievementManager
from trosnoth.gamerecording.gamerecorder import GameRecorder, REPLAY_DIR
from trosnoth.levels.standard import StandardRandomLevel
from trosnoth.messages import (
    RemovePlayerMsg, ConnectionLostMsg, TICK_LIMIT,
    UpdateGameInfoMsg, PlayerTickActionsMsg, FreezeOneFrameMsg, WorldResetMsg,
    AgentDetachedMsg,
)
from trosnoth.model.hub import Node
from trosnoth.model.universe import Universe, ServerUniverse
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)

VERIFY_PLAYER_CONSISTENCY = not version.release


class Game:
    '''
    The most important interface in the Trosnoth code base is the Game/Agent
    interface. A Game represents either a locally running server or a game that
    is running on a remote server. In both of these cases, the game will
    provide the same interface for agents to connect to for receiving orders
    from the game, sending requests, and examining the state of the Universe.
    '''

    tweener: Tweener

    def __init__(
            self, world, botProcess=False, *args,
            botProcessLogPrefix=None,
            bot_process_log_file=None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.world = world

        self.onServerCommand = Event()      # (msg)

        world.onPlayerRemoved.addListener(self.playerRemoved)

        if botProcess:
            from trosnoth.botprocess import ServerSideBotProcessManager
            self.botProcessManager = ServerSideBotProcessManager(
                self, botProcessLogPrefix, bot_process_log_file)
        else:
            self.botProcessManager = None

    def addAgent(self, agent, user=None, authTag=0):
        '''
        Connects an agent to this game. An agent may be a user interface,
        an AI player, or anything that wants to receive events from the game
        and potentially send actions to it.
        Every player in Trosnoth must be controlled by an agent and no agent
        can control more than one player.
        May return a deferred which will fire once the agent is successfully
        added.
        '''
        raise NotImplementedError('%s.addAgent' % (self.__class__.__name__,))

    @defer.inlineCallbacks
    def addBot(
            self, aiName, team=None, fromLevel=False, nick='',
            forceLocal=False, authTag=0, difficulty=DEFAULT_BOT_DIFFICULTY):

        if DISABLE_BOTS or self.world.stopped:
            return

        # Note: forceLocal should eventually be removed, but not until the
        # bot process has a way to control bots from the arena process.
        if forceLocal or not self.botProcessManager:
            ai = makeAIAgent(self, aiName, fromLevel=fromLevel, nick=nick, difficulty=difficulty)
            yield self.addAgent(ai, authTag=authTag)

            ai.start(team)
        else:
            ai = yield defer.ensureDeferred(self.botProcessManager.startBot(
                aiName, fromLevel=fromLevel, nick=nick, team=team, difficulty=difficulty))
        defer.returnValue(ai)

    def detachAgent(self, agent):
        raise NotImplementedError('%s.detachAgent' % (
            self.__class__.__name__,))

    def agentRequest(self, agent, msg):
        '''
        Called by an agent with an AgentRequest message that it wants to
        request.
        '''
        raise NotImplementedError('%s.agentRequest' % (
            self.__class__.__name__,))

    def stop(self):
        self.world.stop()
        if self.botProcessManager:
            self.botProcessManager.stop()
            self.botProcessManager = None

    def joinSuccessful(self, agent, playerId):
        '''
        Called when a join request succeeds.
        '''
        player = self.world.getPlayer(playerId)
        assert player.agent is None
        assert agent.player is None
        assert player is not None

        player.agent = agent
        agent.setPlayer(player)
        player.join_complete = True
        self.world.on_player_join_complete(player)
        player.onJoinComplete()

    def playerRemoved(self, player, playerId):
        '''
        Called when a player is removed from the game.
        '''
        if player.agent:
            player.agent.setPlayer(None)


class LocalGame(Game):
    def __init__(
            self,
            maxPerTeam=100, maxTotal=500, serverInterface=None,
            onceOnly=False, saveReplay=False,
            gamePrefix='unnamed', replay_path=REPLAY_DIR, level=None, game_type=None,
            wait_for_ready=False,
            lobbySettings=None, bots_only=False, no_auto_balance=False, *args,
            tweener_can_drive_ticks=True,
            speedup=1,
            slow_dark_conquest=True,
            **kwargs):

        self._serverCommandStack = []
        self._waitingForEmptyCommandQueue = []
        self.maxPerTeam = maxPerTeam
        self.maxTotalPlayers = min(2 * maxPerTeam, maxTotal)
        self.serverInterface = serverInterface
        self.lobbySettings = lobbySettings

        self.agents = set()
        self.agentInfos = {}

        if level is None:
            level = StandardRandomLevel()
        world = ServerUniverse(
            self,
            onceOnly=onceOnly, level=level, game_type=game_type, bots_only=bots_only,
            no_auto_balance=no_auto_balance, wait_for_ready=wait_for_ready, speedup=speedup,
            slow_dark_conquest=slow_dark_conquest,
        )
        super().__init__(world, *args, **kwargs)
        self.tweener = LocalGameTweener(self, drive_new_ticks=tweener_can_drive_ticks)

        self.idManager = world.idManager

        self.gameRecorder = GameRecorder(
            world, save_replay=saveReplay, game_prefix=gamePrefix, replay_path=replay_path)

        world.onServerTickComplete.addListener(self.worldTickDone)
        self.gameRecorder.start()

        self.achievementManager = AchievementManager(self)
        self.achievementManager.start()

        if VERIFY_PLAYER_CONSISTENCY:
            self.playerConsistencyVerifier = PlayerConsistencyVerifier(self)

    def once_only_game_completed(self):
        for agent in list(self.agents):
            self.detachAgent(agent)
        self.stop()

    def addAgent(self, agent, user=None, authTag=0):
        agent.user = user
        info = AgentInfo(self, agent)
        self.agentInfos[agent] = info
        self.agents.add(agent)

    def detachAgent(self, agent):
        if agent not in self.agents:
            return
        self.agents.remove(agent)
        if agent.player:
            self.kickPlayer(agent.player.id)
            self.agentInfos[agent].takePlayer()
        del self.agentInfos[agent]
        agent.detached()

    def kickPlayer(self, playerId):
        '''
        Removes the player with the specified ID from the game.
        '''
        self.sendServerCommand(RemovePlayerMsg(playerId))

    def agentRequest(self, agent, msg):
        '''
        Some messages need to be delayed until the correct time comes.
        '''
        msg.tracePoint(self, 'agentRequest')
        if agent not in self.agents:
            # Probably just because it's a delayed call
            log.debug('LocalGame got message %s from unconnected agent', msg)
            return
        info = self.agentInfos[agent]
        info.requestFromAgent(msg)

    def apply_agent_request(self, agent, msg):
        '''
        Called by an AgentInfo when the correct time comes for a request to be
        dispatched.
        '''
        msg.tracePoint(self, 'apply_agent_request')
        msg.serverApply(self, agent)

    def setPlayerLimits(self, maxPerTeam, maxTotal=40):
        '''
        Changes the player limits in the current game. Note that this does not
        affect players who are already in the game.

        @param maxPerTeam: Maximum number of players per team at once
        @param maxTotal: Maximum number of players in the game at once
        '''
        self.maxPerTeam = maxPerTeam
        self.maxTotalPlayers = min(2 * maxPerTeam, maxTotal)

    def stop(self):
        super(LocalGame, self).stop()
        self.gameRecorder.stop()
        self.achievementManager.stop()
        self.idManager.stop()

    def worldTickDone(self):
        '''
        Called when the universe has ticked.
        '''
        self.checkCollisionsWithCollectables()
        for info in self.agentInfos.values():
            info.tick()

    def checkCollisionsWithCollectables(self):
        '''
        When a player runs into a collectable unit (e.g. a coin or the
        trosball), we pay attention not to where we think the collectable units
        are, but where the player's client thinks they are. To do this, we need
        to project the collectable units back in time based on the player's
        current delay.
        '''
        greatest_delay = 0
        for info in self.agentInfos.values():
            if not info.player or info.player.dead:
                continue

            start_delay, end_delay = info.get_number_of_ticks_in_past()
            greatest_delay = max(greatest_delay, start_delay)

            for unit in self.world.getCollectableUnits():
                for delay in range(end_delay, start_delay):
                    if unit.checkCollision(info.player, delay):
                        unit.collidedWithPlayer(info.player)
                        break

        # Don't keep more than 10 seconds of history
        greatest_delay = min(greatest_delay, round(10 / TICK_PERIOD))
        for unit in self.world.getCollectableUnits():
            unit.clearOldHistory(greatest_delay)

    def joinSuccessful(self, agent, playerId):
        super(LocalGame, self).joinSuccessful(agent, playerId)
        if agent in self.agentInfos:
            self.agentInfos[agent].givePlayer(self.world.getPlayer(playerId))

    def playerRemoved(self, player, playerId):
        super(LocalGame, self).playerRemoved(player, playerId)
        info = self.agentInfos.get(player.agent)
        if info:
            info.takePlayer()

    def sendServerCommand(self, msg):
        '''
        Sends a command to the universe and all attached agents. Typically
        called by message classes in serverApply().
        '''
        self._serverCommandStack.append(msg)
        if len(self._serverCommandStack) > 1:
            # Sometimes one of the calls below (e.g. self.world.consumeMsg())
            # triggers another sendServerCommand() call, so to make sure
            # that all the messages arrive at the clients in the same order
            # as the server, we queue them and release them as soon as the
            # first message is completely sent.

            # NOTE: if the deffering of messages causes issues, you can
            #       decorate functions/methods with trosnoth.utils.aio.…
            #       delay_so_messages_will_apply_immediately.
            msg.tracePoint(
                self, f'(sendServerCommand: deferred from {self._serverCommandStack[0]})')
            return

        while self._serverCommandStack:
            cmd = self._serverCommandStack[0]
            cmd.tracePoint(self, 'sendServerCommand')
            if VERIFY_PLAYER_CONSISTENCY:
                self.playerConsistencyVerifier.preMessage(cmd)
            self.world.consumeMsg(cmd)
            self.gameRecorder.consume_msg(cmd)
            if VERIFY_PLAYER_CONSISTENCY:
                self.playerConsistencyVerifier.postMessage(cmd)
            self.onServerCommand(cmd)
            cmd.tracePoint(self, 'done sendServerCommand')
            self._serverCommandStack.pop(0)

        # Release things that are waiting for the command stack to empty
        while not self._serverCommandStack and self._waitingForEmptyCommandQueue:
            d = self._waitingForEmptyCommandQueue.pop(0)
            try:
                d.callback(None)
            except Exception:
                log.exception('Error in queued callback')

    def waitForEmptyCommandQueue(self):
        '''
        :return: a Deferred which will callback when the queue of server
            commands to send is empty. This is useful to be sure that the
            world is in a consistent state (all messages have been
            processed).
        '''
        if not self._serverCommandStack:
            return defer.succeed(None)

        d = defer.Deferred()
        self._waitingForEmptyCommandQueue.append(d)
        return d

    def sendResync(
            self, playerId,
            reason='Your computer was out of sync with the server!'):
        '''
        Resyncs the position of the player with the given id. Typically called
        by message classes in serverApply().
        '''
        player = self.world.getPlayer(playerId)
        player.sendResync(reason)


@dataclasses.dataclass
class ActionBatch:
    actions: List
    world_tick: int

    def __bool__(self):
        return bool(self.actions)


class AgentInfo(object):
    '''
    Used by a local game to keep track of information about a connected Agent.
    '''

    def __init__(self, game, agent):
        self.game = game
        self.agent = agent
        self.world = game.world
        self.player = None

        self.future_action_batches = []
        self.world_tick_start = None
        self.world_tick_end = None

    def get_number_of_ticks_in_past(self):
        last_real_tick = self.world.lastTickId
        start_delay = (last_real_tick - self.world_tick_start) % TICK_LIMIT
        end_delay = (last_real_tick - self.world_tick_end) % TICK_LIMIT
        return start_delay, end_delay

    def requestFromAgent(self, msg):
        '''
        When we receive a request from an agent, we first check to see if this
        request is supposed to occur at a specific time. If so, we delay the
        message until that time.
        '''
        from trosnoth.network.server import agent_tick_messages

        msg.tracePoint(self, 'requestFromAgent')
        if isinstance(msg, PlayerTickActionsMsg):
            batch = msg.unpack_contents(agent_tick_messages)
            for sub_msg in batch:
                sub_msg.tracePoint(self, 'add to future_action_batches')
            self.future_action_batches.append(ActionBatch(batch, msg.tick_id))
        else:
            self.game.apply_agent_request(self.agent, msg)

    def tick(self):
        if not self.player:
            return

        self.world_tick_start = self.world_tick_end
        if self.player.willNotChangeOnNextTick():
            # Catch up on lag while the player is static
            while self.future_action_batches and not self.future_action_batches[0]:
                self.advance_world_tick(self.future_action_batches.pop(0).world_tick)

        elif not self.future_action_batches:
            self.game.sendServerCommand(FreezeOneFrameMsg(self.player.id))
            return

        if self.future_action_batches:
            batch = self.future_action_batches.pop(0)
            self.advance_world_tick(batch.world_tick)
            for msg in batch.actions:
                self.game.apply_agent_request(self.agent, msg)

    def advance_world_tick(self, value):
        # Only allow the reported world tick value if it's increasing
        # and hasn't exceeded the last real world tick.
        if self.world_tick_end <= self.world.lastTickId:
            if self.world_tick_end < value <= self.world.lastTickId:
                self.world_tick_end = value
        else:
            if value < self.world.lastTickId or self.world_tick_end < value:
                self.world_tick_end = value

    def givePlayer(self, player):
        '''
        Called when this agent is being given control of the specified player.
        '''
        assert self.player is None
        self.player = player
        self.world_tick_start = self.world_tick_end = self.world.lastTickId

        userTitle = self.world.uiOptions.defaultUserTitle
        userInfo = self.world.uiOptions.defaultUserInfo
        botGoal = self.world.uiOptions.defaultBotGoal
        self.agent.messageToAgent(
            UpdateGameInfoMsg.build(userTitle, userInfo, botGoal))

    def takePlayer(self):
        self.player = None
        self.future_action_batches = []


class RemoteGame(Game, Node):
    '''
    Represents a game that is running on a remote server. This game object
    maintains the current state of the Universe based on messages from the
    server.
    '''

    def __init__(self, *args, smooth_remote_ticks=False, **kwargs):
        world = Universe()
        self.smooth_remote_ticks = smooth_remote_ticks
        super().__init__(world, *args, **kwargs)
        if smooth_remote_ticks:
            self.tweener = UIMsgThrottler(self)
        else:
            self.tweener = LocalGameTweener(self, drive_new_ticks=False)
        self.agentIds = {}
        self.agentById = {}

    def stop(self):
        super().stop()
        self.tweener.stop()

    def connected(self, settings):
        self.world.restoreEverything(settings)

    @defer.inlineCallbacks
    def addAgent(self, agent, user=None, authTag=0):
        assert agent not in self.agentIds
        agentId = yield self.hub.connectNewAgent(authTag=authTag)
        self.agentIds[agent] = agentId
        self.agentById[agentId] = agent

    def detachAgent(self, agent):
        if agent in self.agentIds:
            self.hub.disconnectAgent(self.agentIds[agent])

    def agentRequest(self, agent, msg):
        '''
        Called by an agent with an AgentRequest message that it wants to
        request.
        '''
        msg.tracePoint(self, 'agentRequest')
        if agent not in self.agentIds:
            log.warning('%r: got agentRequest for unconnected agent', self)
            log.warning(f'  : {agent=}')
            log.warning(f'  : {msg=}')
            return
        self.hub.sendRequestToGame(self.agentIds[agent], msg)

    def gotServerCommand(self, msg):
        '''
        Called when a server command is received from the network.
        '''
        msg.tracePoint(self, 'gotServerCommand')
        if self.smooth_remote_ticks:
            self.tweener.got_server_command(msg)
        else:
            self.apply_server_command(msg)

    def apply_server_command(self, msg):
        msg.tracePoint(self, 'apply_server_command')
        self.world.consumeMsg(msg)
        self.onServerCommand(msg)

    def gotMessageToAgent(self, agent_id, msg):
        msg.tracePoint(self, 'gotMessageToAgent')
        if self.smooth_remote_ticks and not isinstance(msg, AgentDetachedMsg):
            self.tweener.got_message_to_agent(agent_id, msg)
        else:
            self.pass_message_to_agent(agent_id, msg)

    def pass_message_to_agent(self, agent_id, msg):
        msg.tracePoint(self, 'pass_message_to_agent')
        agent = self.agentById[agent_id]
        agent.messageToAgent(msg)

    def agentDisconnected(self, agentId):
        agent = self.agentById[agentId]
        del self.agentIds[agent]
        del self.agentById[agentId]
        agent.messageToAgent(ConnectionLostMsg())


class PlayerConsistencyVerifier(object):
    '''
    This class exists entirely for debugging. When VERIFY_PLAYER_CONSISTENCY is
    true this class is used much like a ReplayRecorder, but it checks that
    player states in the "replay" match in the real world.
    '''
    dumpStates = True

    def __init__(self, localGame):
        self.realGame = localGame
        self.world = localGame.world

        self.replayGame = RemoteGame()
        self.replayGame.connected(self.world.dumpEverything())

        self.waitingMsg = None
        self.preRealState = None
        self.preReplayState = None
        self.prevInconsistent = False

    def preMessage(self, msg):
        self.resolveWaiting(None)

        self.waitingMsg = msg
        self.preRealState, self.preReplayState = self.getStates()

    def postMessage(self, msg):
        self.replayGame.gotServerCommand(msg)
        self.resolveWaiting(msg)

    def getStates(self):
        real = {p.id: p.dump() for p in self.realGame.world.players}
        replay = {p.id: p.dump() for p in self.replayGame.world.players}
        return real, replay

    def resolveWaiting(self, msg):
        if self.waitingMsg is None:
            if msg is not None:
                log.error(
                    'RECEIVED .postMessage() WITHOUT .preMessage: %s', msg)
            return

        waitingMsg, self.waitingMsg = self.waitingMsg, None
        preRealState, self.preRealState = self.preRealState, None
        preReplayState, self.preReplayState = self.preReplayState, None

        if waitingMsg is not msg:
            if preRealState != preReplayState:
                log.error('INCONSISTENCY BEFORE %s', waitingMsg)
                if self.dumpStates:
                    self.dumpInconsistency(preRealState, preReplayState)
            log.error(
                'DID NOT SEE MATCHING .postMessage() CALL for %s', waitingMsg)

            if msg is not None:
                log.error(
                    'RECEIVED .postMessage() WITHOUT .preMessage: %s', msg)
            return

        postRealState, postReplayState = self.getStates()
        inconsistentPre = (preRealState != preReplayState)
        inconsistentPost = (postRealState != postReplayState)

        if not inconsistentPre:
            if not inconsistentPost:
                if self.prevInconsistent:
                    log.error('INCONSISTENCY RESOLVED BEFORE %s', msg)
            else:
                log.error('INCONSISTENCY INTRODUCED IN %s', msg)
                if self.dumpStates:
                    self.dumpInconsistency(postRealState, postReplayState)
        elif inconsistentPost:
            if not self.prevInconsistent and not isinstance(msg, WorldResetMsg):
                log.error('INCONSISTENCY INTRODUCED BEFORE %s', msg)
                if self.dumpStates:
                    self.dumpInconsistency(preRealState, preReplayState)
        elif not isinstance(msg, WorldResetMsg):
            log.error('INCONSISTENCY RESOLVED IN %s', msg)
            if self.dumpStates:
                self.dumpInconsistency(preRealState, preReplayState)

        self.prevInconsistent = inconsistentPost

    def dumpInconsistency(self, realState, replayState):
        import pprint

        missingInReal = set(replayState) - set(realState)
        missingInReplay = set(realState) - set(replayState)
        if missingInReal:
            log.error('  not present on server: %r', missingInReal)
        if missingInReplay:
            log.error('  not present in replay: %r', missingInReplay)

        for playerId in realState:
            if playerId not in replayState:
                continue
            realPlayerState = realState[playerId]
            replayPlayerState = replayState[playerId]
            if realPlayerState != replayPlayerState:
                log.error('   === server ===')
                log.error(pprint.pformat(realPlayerState))
                log.error('   === replay ===')
                log.error(pprint.pformat(replayPlayerState))
                log.error('   ==============')
