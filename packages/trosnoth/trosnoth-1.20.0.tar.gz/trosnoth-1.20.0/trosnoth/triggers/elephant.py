import logging

from trosnoth.triggers.base import DurationScoreTrigger, Trigger
from twisted.internet import defer

log = logging.getLogger(__name__)


class ElephantDurationScoreTrigger(DurationScoreTrigger):
    '''
    Players get points based on how long they hold the elephant for.
    '''
    def __init__(self, *args, **kwargs):
        super(ElephantDurationScoreTrigger, self).__init__(*args, **kwargs)
        self.playerWithElephant = self.world.elephant.possessor

    def doActivate(self):
        super(ElephantDurationScoreTrigger, self).doActivate()
        self.world.scoreboard.setMode(players=True)
        self.world.onPlayerKill.addListener(self.gotPlayerKill)

    def doDeactivate(self):
        self.world.onPlayerKill.removeListener(self.gotPlayerKill)
        if self.world.scoreboard:
            self.world.scoreboard.setMode(players=False)
        super(ElephantDurationScoreTrigger, self).doDeactivate()

    def gotInterval(self):
        self.playerWithElephant = self.world.elephant.possessor
        super(ElephantDurationScoreTrigger, self).gotInterval()

    def checkCondition(self, player):
        return player.hasElephant() and not player.dead

    def gotPlayerKill(self, killer, target, hitKind):
        if self.playerWithElephant == target:
            self.conditionLost(target)
            self.playerWithElephant = None


class EnsureMacGuffinIsInGameTrigger(Trigger):
    '''
    If at any point there is no live player with the given macguffin in
    the game, adds a bot to the game and gives it the macguffin. As soon
    as the bot loses the macguffin, it is removed from the game.
    '''
    def __init__(self, level, macguffin, bot_name, custom_give_function=None):
        super().__init__(level)
        self.macguffin = macguffin
        self.bot_name = bot_name
        self.custom_give_function = custom_give_function
        self.bot = None
        self.addingBot = False

    def doActivate(self):
        self.macguffin.on_transfer.addListener(self.seen_transfer, lifespan=self.lifespan)
        self.world.callLater(0, self.checkIfBotIsNeeded)

    def seen_transfer(self, old_possessor, new_possessor):
        self.checkIfBotIsNeeded()

    def checkIfBotIsNeeded(self):
        if self.bot:
            if self.macguffin.possessor and self.macguffin.possessor.id == self.bot.player.id:
                return

        if self.macguffin.possessor is None or self.macguffin.possessor.dead:
            self.add_bot_with_macguffin()
        else:
            self.removeBot()

    @defer.inlineCallbacks
    def add_bot_with_macguffin(self):
        if self.addingBot:
            return
        if self.bot and (self.bot.player is None or self.bot.player.dead):
            self.removeBot()

        # Add a bot
        if not self.bot:
            self.addingBot = True
            try:
                nick = self.bot_name
                # Pretect against tricksy humans editing their nicks
                while any(p.nick == nick for p in self.world.players):
                    nick += "'"
                self.bot = yield self.level.addBot(None, nick, 'ranger')
            finally:
                self.addingBot = False

        # Give the bot the MacGuffin
        if self.custom_give_function:
            self.custom_give_function(self.bot.player)
        else:
            self.macguffin.give_to_player(self.bot.player)

    def removeBot(self):
        agent, self.bot = self.bot, None
        if agent:
            agent.stop()
            self.world.game.detachAgent(agent)
