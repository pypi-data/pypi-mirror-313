from enum import IntEnum
import math
import typing

from trosnoth.utils.lifespan import LifeSpan

from trosnoth.const import TICK_PERIOD


class Trigger:
    '''
    Base class for defining standard triggers that multiple different levels
    might want to use.
    '''

    def __init__(self, level):
        assert level and level.world
        self.level = level
        self.world = level.world
        self.active = False
        self.lifespan = LifeSpan()

    def activate(self):
        if self.active:
            return
        self.active = True
        self.level.activeTriggers.add(self)
        self.doActivate()
        return self

    def deactivate(self):
        if not self.active:
            return
        self.active = False
        self.level.activeTriggers.discard(self)
        self.doDeactivate()
        self.lifespan.stop()
        self.lifespan = LifeSpan()  # Allow possible later reactivation

    def doActivate(self):
        '''
        Subclasses should override this to perform activation logic.
        '''
        raise NotImplementedError(
            '{}.doActivate'.format(self.__class__.__name__))

    def doDeactivate(self):
        '''
        Subclasses may override this to perform deactivation logic.
        '''
        pass


class StatType(IntEnum):
    PERCENTAGE = 0
    FLOAT = 1
    MONEY = 2
    TIME = 3
    FLOAT_OR_NONE = 4

    def format(self, value):
        if value is None:
            if self == StatType.FLOAT_OR_NONE:
                return '—'
            value = 0
        if value == math.inf:
            return '∞'
        if value == -math.inf:
            return '-∞'

        match self:
            case StatType.PERCENTAGE:
                if abs(value) >= 1:
                    return f'{value:.0%}'
                return f'{value:.1%}'
            case StatType.MONEY:
                return f'${value:,}'.replace(',', '\N{no-break space}')
            case StatType.TIME:
                return f'{int(value // 60):d}:{value % 60:04.1f}'
            case _:
                if abs(value) < 1:
                    return f'{value:.2g}'
                if abs(value) < 1000:
                    return f'{value:.3g}'
                if abs(value) < 1e6:
                    return f'{value/1000:.3g}k'
                if abs(value) < 1e9:
                    return f'{value / 1e6:.3g}M'
                return f'{value / 1e6:.0f}M'


class StatTrigger(Trigger):
    '''
    Base class for triggers which keep track of one or more game
    statistic which may be used by LevelStats to display at the end of
    a game.
    '''

    def get_match_stats(self) -> typing.Iterable[tuple[str, StatType, float]]:
        '''
        Iterator that yields (stat_name, stat_type, stat_value)
        '''
        return ()

    def get_team_stats(self) -> typing.Iterable[tuple[str, StatType, dict]]:
        '''
        Iterator that yields (stat_name, stat_type, {team: stat_value})
        '''
        return ()

    def get_player_stats(self) -> typing.Iterable[tuple[str, StatType, dict]]:
        '''
        Iterator that yields (stat_name, stat_type, {player: stat_value})
        '''
        return ()


class ScoreBoardStatTrigger(StatTrigger):
    def doActivate(self):
        pass

    def get_team_stats(self):
        scoreboard = self.world.scoreboard
        if scoreboard.teamScoresEnabled:
            yield 'Score', StatType.FLOAT, dict(scoreboard.teamScores)

    def get_player_stats(self):
        from trosnoth.levels.base import PlayerInfo
        scoreboard = self.world.scoreboard
        if scoreboard.playerScoresEnabled:
            yield 'Score', StatType.FLOAT, {
                PlayerInfo(p): s for p, s in scoreboard.playerScores.items()}


class DurationScoreTrigger(Trigger):
    '''
    Base class for triggers which increment player scores over time based on
    some condition.
    '''

    def __init__(self, level, interval=1):
        super(DurationScoreTrigger, self).__init__(level)
        self.interval = interval
        self.callback = None
        self.extraTicks = 0
        self.playerPortions = {}

    def doActivate(self):
        self.callback = self.world.callLater(self.interval, self.gotInterval)
        self.world.onServerTickComplete.addListener(self.gotTickComplete, lifespan=self.lifespan)

    def doDeactivate(self):
        if self.callback:
            self.callback.cancel()

    def gotInterval(self):
        self.callback = self.world.callLater(self.interval, self.gotInterval)
        for p in self.world.players:
            if p in self.playerPortions:
                self.world.scoreboard.playerScored(p, self.playerPortions[p])
            elif self.checkCondition(p):
                self.world.scoreboard.playerScored(p, 1)
        self.extraTicks = 0
        self.playerPortions = {}

    def gotTickComplete(self):
        self.extraTicks += 1

    def conditionLost(self, player):
        '''
        Should be called by subclasses when the given player previously met
        the condition, but no longer does.
        '''
        value = self.extraTicks * TICK_PERIOD / self.interval
        self.playerPortions.setdefault(player, value)

    def checkCondition(self, player):
        '''
        Must return whether or not the condition is true for this player.
        '''
        raise NotImplementedError('{}.checkCondition'.format(
            self.__class__.__name__))
