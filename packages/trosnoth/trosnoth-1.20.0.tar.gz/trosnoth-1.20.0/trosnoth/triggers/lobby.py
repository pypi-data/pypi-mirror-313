import logging
import random

from twisted.internet import defer

from trosnoth.const import BOT_DIFFICULTY_EASY
from trosnoth.messages import SetPlayerTeamMsg
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.base import Trigger
from trosnoth.utils.twist import WeakLoopingCall

log = logging.getLogger(__name__)


class MakeNewPlayersNeutralTrigger(Trigger):
    def doActivate(self):
        self.world.onPlayerAdded.addListener(self.newPlayerAdded, lifespan=self.lifespan)

    def newPlayerAdded(self, player):
        if player.team is not None:
            self.world.sendServerCommand(
                SetPlayerTeamMsg(player.id, NEUTRAL_TEAM_ID))


class AddBotsForLobbyTrigger(Trigger):
    '''
    Adds a number of bots so even a single player can mess around in the
    lobby until others arrive.

    Keeps the total number of bots at least up to a particular minimum,
    adding and removing bots as necessary.
    '''

    def __init__(self, level, playerCount=6):
        from trosnoth.bots.base import get_available_bot_names

        super(AddBotsForLobbyTrigger, self).__init__(level)
        self.playerCount = playerCount
        self.loop = WeakLoopingCall(self, 'recheck')
        self.agents = []
        self.newAgents = set()
        self.aiNames = get_available_bot_names()
        self._deactivated = False

    def doActivate(self):
        if not self.loop.running:
            self.loop.start(3, False)

    def doDeactivate(self):
        if self.loop.running:
            self.loop.stop()
        self._stopAllAgents()
        self._deactivated = True

    @defer.inlineCallbacks
    def recheck(self):
        self._graduateNewAgents()
        yield self._adjustAgentsToTarget()

    def _graduateNewAgents(self):
        for agent in list(self.newAgents):
            if agent.player is not None:
                self.agents.append(agent)
                self.newAgents.remove(agent)

    def _stopAllAgents(self):
        if len(self.agents) != 0:
            log.info('AIInjector: Stopping all agents')
        for agent in self.agents:
            agent.stop()
            self.world.game.detachAgent(agent)
        self.agents = []
        while self.newAgents:
            agent = self.newAgents.pop()
            agent.stop()
            self.world.game.detachAgent(agent)

    @defer.inlineCallbacks
    def _adjustAgentsToTarget(self):
        worldPlayers = len(self.world.game.world.players)
        newAgents = len(self.newAgents)
        if self.playerCount > worldPlayers + newAgents:
            yield self._addAgents(self.playerCount - worldPlayers - newAgents)
        else:
            self._removeAgents(worldPlayers + newAgents - self.playerCount)

    @defer.inlineCallbacks
    def _addAgents(self, count):
        log.info('AIInjector: Adding %d agents', count)
        for i in range(count):
            agent = yield self.world.game.addBot(
                random.choice(self.aiNames), difficulty=BOT_DIFFICULTY_EASY)
            if agent is not None:
                if self._deactivated:
                    agent.stop()
                    self.world.game.detachAgent(agent)
                    break
                self.newAgents.add(agent)

    def _removeAgents(self, count):
        if count != 0:
            log.info('AIInjector: Removing %d agents', count)
        for i in range(count):
            if len(self.agents) == 0:
                break
            agent = self.agents.pop(0)
            agent.stop()
            self.world.game.detachAgent(agent)


class StartGameWhenReadyTrigger(Trigger):
    def __init__(self, level):
        super().__init__(level)
        self.loop = WeakLoopingCall(self, 'check')

    def doActivate(self):
        if not self.loop.running:
            self.loop.start(3, False)

    def doDeactivate(self):
        if self.loop.running:
            self.loop.stop()

    def check(self):
        try:
            self.level.start_new_game_if_ready()
        except Exception:
            log.exception('Error trying to start new game')