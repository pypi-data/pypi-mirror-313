import logging

from twisted.internet import defer

from trosnoth.const import DISABLE_BOTS
from trosnoth.model.map import ZoneLayout, ZoneStep
from trosnoth.triggers.base import Trigger, DurationScoreTrigger

log = logging.getLogger(__name__)


class PlayerKillScoreTrigger(Trigger):
    '''
    When a player is killed, award leaderboard points to the killer.
    '''

    def __init__(self, level, killScore=1, dieScore=-1):
        super(PlayerKillScoreTrigger, self).__init__(level)
        self.killScore = killScore
        self.dieScore = dieScore

    def doActivate(self):
        self.world.onPlayerKill.addListener(self.gotPlayerKill, lifespan=self.lifespan)
        self.world.scoreboard.setMode(players=True)

    def doDeactivate(self):
        if self.world.scoreboard:
            self.world.scoreboard.setMode(players=False)

    def gotPlayerKill(self, killer, target, hitKind):
        if killer:
            self.world.scoreboard.playerScored(killer, self.killScore)
        self.world.scoreboard.playerScored(target, self.dieScore)


class PlayerLifeScoreTrigger(DurationScoreTrigger):
    '''
    Players get points based on how long they have been alive.
    '''

    def __init__(self, level, interval=1, teams=None):
        super(PlayerLifeScoreTrigger, self).__init__(level, interval)
        self.teams = teams

    def doActivate(self):
        super(PlayerLifeScoreTrigger, self).doActivate()
        self.world.scoreboard.setMode(players=True)
        self.world.onPlayerKill.addListener(self.gotPlayerKill)

    def doDeactivate(self):
        self.world.onPlayerKill.removeListener(self.gotPlayerKill)
        if self.world.scoreboard:
            self.world.scoreboard.setMode(players=False)
        super(PlayerLifeScoreTrigger, self).doDeactivate()

    def gotInterval(self):
        self.callback = self.world.callLater(self.interval, self.gotInterval)
        for p in self.world.players:
            if p in self.playerPortions:
                self.world.scoreboard.playerScored(p, self.playerPortions[p])
            elif not p.dead:
                if self.teams is None or p.team in self.teams:
                    self.world.scoreboard.playerScored(p, 1)
        self.extraTicks = 0
        self.playerPortions = {}

    def checkCondition(self, player):
        if player.dead:
            return False
        return self.isPlayerInSelectedTeams(player)

    def isPlayerInSelectedTeams(self, player):
        return self.teams is None or player.team in self.teams

    def gotPlayerKill(self, killer, target, hitKind):
        if self.isPlayerInSelectedTeams(target):
            self.conditionLost(target)


def makeCirclesLayout():
    zones = ZoneLayout()

    # Centre
    zone = zones.firstLocation
    zones.setZoneOwner(zone, 0, dark=True)

    # Inner ring
    zone = zones.firstLocation
    zones.addZoneAt(zone + ZoneStep.SOUTH, ownerIndex=1, dark=False)
    zones.addZoneAt(zone + ZoneStep.NORTHEAST, ownerIndex=1, dark=False)
    zones.addZoneAt(zone + ZoneStep.NORTHWEST, ownerIndex=1, dark=False)
    se = zones.connectZone(
        zone, ZoneStep.SOUTHEAST, ownerIndex=1, dark=False)
    zones.connectZone(se, ZoneStep.SOUTHWEST)
    zones.connectZone(se, ZoneStep.NORTH)
    sw = zones.connectZone(
        zone, ZoneStep.SOUTHWEST, ownerIndex=1, dark=False)
    zones.connectZone(sw, ZoneStep.SOUTHEAST)
    zones.connectZone(sw, ZoneStep.NORTH)
    n = zones.connectZone(zone, ZoneStep.NORTH, ownerIndex=1, dark=False)
    zones.connectZone(n, ZoneStep.SOUTHEAST)
    zones.connectZone(n, ZoneStep.SOUTHWEST)

    # Outer ring
    zone = zones.connectZone(n, ZoneStep.NORTHEAST)
    zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
    zone = zones.connectZone(zone, ZoneStep.SOUTH)
    zones.connectZone(zone, ZoneStep.NORTHWEST)
    zone = zones.connectZone(zone, ZoneStep.SOUTH)
    zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
    zones.connectZone(zone, ZoneStep.NORTH)
    zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
    zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
    zones.connectZone(zone, ZoneStep.NORTHEAST)
    zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
    zone = zones.connectZone(zone, ZoneStep.NORTH)
    zones.connectZone(zone, ZoneStep.SOUTHEAST)
    zone = zones.connectZone(zone, ZoneStep.NORTH)
    zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
    zones.connectZone(zone, ZoneStep.SOUTH)
    zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
    zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)

    return zones.createMapLayout(autoOwner=False)


def make_small_circles_layout():
    zones = ZoneLayout()

    # Centre
    zone = zones.firstLocation
    zones.setZoneOwner(zone, 0, dark=True)

    # Inner ring
    zone = zones.firstLocation
    zones.addZoneAt(zone + ZoneStep.SOUTH, ownerIndex=1, dark=False)
    zones.addZoneAt(zone + ZoneStep.NORTHEAST, ownerIndex=1, dark=False)
    zones.addZoneAt(zone + ZoneStep.NORTHWEST, ownerIndex=1, dark=False)
    se = zones.connectZone(
        zone, ZoneStep.SOUTHEAST, ownerIndex=1, dark=False)
    zones.connectZone(se, ZoneStep.SOUTHWEST)
    zones.connectZone(se, ZoneStep.NORTH)
    sw = zones.connectZone(
        zone, ZoneStep.SOUTHWEST, ownerIndex=1, dark=False)
    zones.connectZone(sw, ZoneStep.SOUTHEAST)
    zones.connectZone(sw, ZoneStep.NORTH)
    n = zones.connectZone(zone, ZoneStep.NORTH, ownerIndex=1, dark=False)
    zones.connectZone(n, ZoneStep.SOUTHEAST)
    zones.connectZone(n, ZoneStep.SOUTHWEST)

    return zones.createMapLayout(autoOwner=False)


class AddOneBotTrigger(Trigger):
    '''
    Adds one bot to the game unless the total player count is equal to or
    greater than playerLimit.
    '''

    def __init__(self, level, playerLimit=4, *args, **kwargs):
        super(AddOneBotTrigger, self).__init__(level, *args, **kwargs)
        self.playerLimit = playerLimit
        self.bot = None
        self._checking = False

    def doActivate(self):
        self.world.onPlayerAdded.addListener(self.gotPlayerAdded, lifespan=self.lifespan)
        self.world.onPlayerRemoved.addListener(self.gotPlayerRemoved, lifespan=self.lifespan)

        self._check()

    def doDeactivate(self):
        self._stopBot()

    def gotPlayerAdded(self, player, *args, **kwargs):
        self._check()

    def gotPlayerRemoved(self, player, *args, **kwargs):
        self._check()

    def _stopBot(self):
        agent, self.bot = self.bot, None
        if agent:
            agent.stop()
            self.world.game.detachAgent(agent)

    @defer.inlineCallbacks
    def _check(self):
        if self._checking:
            return
        self._checking = True
        try:
            while True:
                humans = sum(not p.bot for p in self.world.players)
                shouldHaveBot = humans < self.playerLimit
                if self.bot and not shouldHaveBot:
                    self._stopBot()
                    break
                elif shouldHaveBot and not self.bot:

                    nick = 'RangerBot'
                    # Pretect against tricksy humans editing their nicks
                    while any(p.nick == nick for p in self.world.players):
                        nick += "'"
                    self.bot = yield self.level.addBot(None, nick, 'ranger')
                else:
                    break

        finally:
            self._checking = False


class AddLimitedBotsTrigger(Trigger):
    '''
    If increase_with_enemies is False, maintains a minimum number of
    players in a game. If increase_with_enemies is True, adds more bots
    the more players join the game on the opposite team to the bots.
    '''

    def __init__(
            self,
            level,
            max_bots,
            min_bots=0,
            bot_kind='ranger',
            bot_nick=None,
            bot_team=None,
            increase_with_enemies=True,
    ):
        super().__init__(level)
        self.minBots = max(0, min_bots)
        self.maxBots = max_bots
        self.botClass = bot_kind
        self.botNick = bot_nick
        self.botTeam = bot_team
        self.increase_with_enemies = increase_with_enemies
        self.bots = []
        self._checking = False

    def doActivate(self):
        self.world.onPlayerAdded.addListener(self.gotPlayerAdded, lifespan=self.lifespan)
        self.world.onPlayerRemoved.addListener(self.gotPlayerRemoved, lifespan=self.lifespan)

        self._check()

    def doDeactivate(self):
        bots = self.bots
        self.bots = []

        for agent in bots:
            self._stopBot(agent)

    def gotPlayerAdded(self, player, *args, **kwargs):
        self._check()

    def gotPlayerRemoved(self, player, *args, **kwargs):
        self._check()

    def _stopBot(self, agent=None):
        if not agent:
            agent = self.bots.pop(-1)
        agent.stop()
        self.world.game.detachAgent(agent)

    @defer.inlineCallbacks
    def _check(self):
        if DISABLE_BOTS or self.world.stopped:
            return
        if self._checking:
            return
        self._checking = True
        try:
            while True:
                botCount = len(self.bots)
                target = self.get_target_bot_count()
                if botCount == target:
                    break
                elif botCount > target:
                    for i in range(botCount - target):
                        self._stopBot()
                else:
                    if self.botNick:
                        nick = '{} #{}'.format(self.botNick, botCount + 1)
                    else:
                        nick = self.botNick
                    agent = yield self.level.addBot(self.botTeam, nick, self.botClass)
                    self.bots.append(agent)

        finally:
            self._checking = False

    def get_target_bot_count(self):
        if self.increase_with_enemies:
            bot_enemies = sum(
                p.team not in (None, self.botTeam)
                    for p in self.world.players)
            return min(self.maxBots, max(self.minBots, bot_enemies))

        unmanaged_players = len(self.world.players) - len(self.bots)
        return max(self.minBots, self.maxBots - unmanaged_players)
