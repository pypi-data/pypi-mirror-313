import logging

from twisted.internet import defer

from trosnoth.const import DISABLE_BOTS, BOT_DIFFICULTY_EASY
from trosnoth.triggers.base import Trigger


log = logging.getLogger(__name__)


class BalanceTeamsTrigger(Trigger):
    '''
    Keeps track of how many players are on each team, and if the teams are
    uneven, adds a bot to the disadvantaged team.
    '''

    def __init__(self, level, delayAfterPlayerLeaves=30):
        super(BalanceTeamsTrigger, self).__init__(level)
        self.delayAfterPlayerLeaves = delayAfterPlayerLeaves
        self.agents = set()
        self.players = set()
        self.delays = {}
        self.addingAgent = False

    def doActivate(self):
        if DISABLE_BOTS:
            return
        self.world.onPlayerAdded.addListener(self._playerWasAdded, lifespan=self.lifespan)
        self.world.onPlayerRemoved.addListener(self._playerWasRemoved, lifespan=self.lifespan)

        self.checkTeams()

    def doDeactivate(self):
        if DISABLE_BOTS:
            return

        agents = self.agents
        self.agents = set()

        for agent in agents:
            agent.stop()
            self.world.game.detachAgent(agent)

    def _playerWasAdded(self, player, *args, **kwargs):
        player.onTeamSet.addListener(lambda: self._playerTeamSet(player), lifespan=self.lifespan)
        self.checkTeams()

    def _playerWasRemoved(self, player, *args, **kwargs):
        self.players.discard(player)
        if player.agent in self.agents:
            self.agents.discard(player.agent)
            player.agent.stop()

        player.onTeamSet.removeListener(lambda: self._playerTeamSet(player))
        self.checkTeams(waitingTeam=player.team)

    def _playerTeamSet(self, player):
        self.checkTeams()

    def checkTeams(self, waitingTeam=None):
        if self.addingAgent:
            return

        teamsNeedingHelp = []
        teamPlayerCounts = {t: 0 for t in self.world.teams}
        for player in self.world.players:
            team = player.team
            if team and player not in self.players:
                teamPlayerCounts[team] += 1

        if len(teamPlayerCounts) > 1:
            maxPlayers = max(teamPlayerCounts.values())
            teamsNeedingHelp = {
                t for (t, n) in list(teamPlayerCounts.items()) if n < maxPlayers}

        # Remove bot from teams that no longer need it
        for agent in list(self.agents):
            if agent.player is None or agent.player.team not in teamsNeedingHelp:
                self.agents.discard(agent)
                agent.stop()
                self.world.game.detachAgent(agent)
            else:
                teamsNeedingHelp.discard(agent.player.team)

        for team in list(self.delays):
            if team not in teamsNeedingHelp:
                delayedCall = self.delays.pop(team)
                delayedCall.cancel()

        # Add bots to teams that need it
        for team in teamsNeedingHelp:
            if team in self.delays:
                continue
            if waitingTeam == team:
                delayedCall = self.world.callLater(
                    self.delayAfterPlayerLeaves, self._addBotPlayer, team)
                self.delays[team] = delayedCall
            else:
                self._addBotPlayer(team)

    @defer.inlineCallbacks
    def _addBotPlayer(self, team):
        self.addingAgent = True
        try:
            agent = yield self.world.game.addBot(
                self.get_bot_name(), team, difficulty=self.get_bot_difficulty())
            self.agents.add(agent)
            if agent.player is None:
                yield agent.onPlayerSet.wait()
            self.players.add(agent.player)
        finally:
            self.addingAgent = False
        self.world.callLater(0, self.checkTeams)

    def get_bot_name(self):
        if self.world.game.serverInterface:
            return self.world.game.serverInterface.get_balance_bot_name()
        return 'balance'

    def get_bot_difficulty(self):
        if not self.world.game.serverInterface:
            return BOT_DIFFICULTY_EASY

        difficulty = self.world.game.serverInterface.get_balance_bot_difficulty()
        if difficulty is None:
            # Server has disabled balance bots since this trigger was
            # activated.
            return BOT_DIFFICULTY_EASY
        return difficulty

