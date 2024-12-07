#!/usr/bin/env python3

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import logging
import random

from trosnoth.const import (
    BOT_GOAL_CAPTURE_MAP, ACHIEVEMENT_TERRITORY,
    ACHIEVEMENT_TACTICAL,
)
from trosnoth.levels.base import (
    Level, play_level, SELECTABLE_TEAMS,
    FORCE_RANDOM_TEAMS, HVM_TEAMS, LevelStats,
)
from trosnoth.levels.maps import StandardMap, SmallMap, WideMap, LargeMap
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.bots import BalanceTeamsTrigger
from trosnoth.triggers.coins import (
    SlowlyIncrementLivePlayerCoinsTrigger, AwardStartingCoinsTrigger,
)
from trosnoth.triggers.coinstats import UnspentCoinsStatTrigger
from trosnoth.triggers.shotstats import (
    KillDeathRatioStatTrigger, DefensiveKillStatTrigger,
    AccuracyStatTrigger,
)
from trosnoth.triggers.timestats import (
    PlayerLivePercentageStatTrigger,
    StandardGameWinPercentStatTrigger, TeamPossessionStatTrigger, GrapplePercentStatTrigger,
    WalkPercentStatTrigger, ElevationStatTrigger, GameDurationStatTrigger,
)
from trosnoth.triggers.zonecaps import (
    StandardZoneCaptureTrigger, StandardGameVictoryTrigger,
    PlayerZoneScoreTrigger,
)
from trosnoth.triggers.zonestats import TeamCapEffectStatTrigger, PlayerCapScoreStatTrigger
from trosnoth.utils.event import waitForEvents

log = logging.getLogger(__name__)


class StandardLevel(Level):
    '''
    The base class used for levels with standard joining rules and win
    conditions.
    '''
    keepPlayerScores = True
    allowAutoBalance = True
    levelName = 'Trosnoth Match'
    countdown_time = 10

    default_duration = 20 * 60
    team_selection = (
        SELECTABLE_TEAMS,
        FORCE_RANDOM_TEAMS,
        HVM_TEAMS,
    )
    map_selection = (
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )
    coin_increment_factor = 1

    def getDuration(self):
        return None

    def pre_sync_setup(self):
        super().pre_sync_setup()
        if self.level_options.get_team_option(self) == SELECTABLE_TEAMS:
            self.world.uiOptions.team_ids_humans_can_join = [b'A', b'B']
            self.world.uiOptions.team_ids_humans_can_switch_to = [b'A', b'B']
        else:
            self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    async def run(self):
        team_option = self.level_options.get_team_option(self)
        if team_option == HVM_TEAMS and not self.world.botManager:
            self.begin_hvm()

        SlowlyIncrementLivePlayerCoinsTrigger(self, factor=self.coin_increment_factor).activate()

        await self.pregameCountdownPhase()

        win_stat = StandardGameWinPercentStatTrigger(self)
        self.stats.add_triggers([
            GameDurationStatTrigger(self),
            win_stat,
            PlayerLivePercentageStatTrigger(self),
            KillDeathRatioStatTrigger(self),
            DefensiveKillStatTrigger(self),
            PlayerCapScoreStatTrigger(self),
            random.choice([
                AccuracyStatTrigger(self),
                ElevationStatTrigger(self),
                GrapplePercentStatTrigger(self),
                WalkPercentStatTrigger(self),
                UnspentCoinsStatTrigger(self),
            ]),
            TeamCapEffectStatTrigger(self),
            possession_stat := TeamPossessionStatTrigger(self),
        ])
        self.stats.resume()
        time_ran_out = await self.mainGamePhase()

        max_zones = max(t.numZonesOwned for t in self.world.teams)
        winners = [t for t in self.world.teams if t.numZonesOwned == max_zones]
        win_stat.finalise(winners)
        possession_stat.finalise(winners=winners, time_ran_out=time_ran_out)
        if len(winners) > 1:
            winners = []
            winner = None
        else:
            winner = winners[0]

        self.world.onStandardGameFinished(winner)

        return self.build_level_result(winners=winners)

    async def pregameCountdownPhase(self):
        startingCoinsTrigger = AwardStartingCoinsTrigger(self).activate()

        self.setUserInfo('Get Ready...', (
            '* Game will begin soon',
            '* Capture or neutralise all enemy zones',
            '* To capture a zone, touch the orb',
            "* If a team's territory is split, the smaller section is neutralised",
            '* Use TAB and SPACE to select and buy items',
        ), BOT_GOAL_CAPTURE_MAP)
        self.world.clock.startCountDown(self.countdown_time, flashBelow=0)
        self.world.clock.propagateToClients()

        self.world.pauseStats()
        self.world.abilities.set(respawn=False, leaveFriendlyZones=False)
        self.world.onChangeVoiceChatRooms(self.world.teams, self.world.players)
        await self.world.clock.onZero.wait_future()
        startingCoinsTrigger.deactivate()

    async def mainGamePhase(self):
        winTrigger = StandardGameVictoryTrigger(self).activate()
        if self.keepPlayerScores:
            PlayerZoneScoreTrigger(self).activate()

        balanceTeamsTrigger = None
        if self.should_balance_teams():
            balanceTeamsTrigger = BalanceTeamsTrigger(self).activate()

        zoneCapTrigger = StandardZoneCaptureTrigger(self).activate()

        self.world.setActiveAchievementCategories({
            ACHIEVEMENT_TERRITORY, ACHIEVEMENT_TACTICAL})
        self.setMainGameUserInfo()
        self.notifyAll('The game is now on!!')
        self.playSound('startGame.ogg')
        self.world.resumeStats()
        self.world.abilities.set(respawn=True, leaveFriendlyZones=True)

        duration = self.getDuration()
        if duration:
            self.world.clock.startCountDown(duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        event, args = await waitForEvents([
            self.world.clock.onZero, winTrigger.onVictory])
        time_ran_out = event == self.world.clock.onZero

        winTrigger.deactivate()
        zoneCapTrigger.deactivate()
        if balanceTeamsTrigger:
            balanceTeamsTrigger.deactivate()

        return time_ran_out

    def should_balance_teams(self):
        if not self.world.abilities.balanceTeams:
            return False
        if not self.allowAutoBalance:
            return False
        if self.world.no_auto_balance:
            return False
        if self.level_options.get_team_option(self) == HVM_TEAMS:
            return False

        if not self.world.game.serverInterface:
            return True
        difficulty = self.world.game.serverInterface.get_balance_bot_difficulty()
        if difficulty is None:
            return False
        return True

    def setMainGameUserInfo(self):
        self.setUserInfo('Trosnoth Match', (
            '* Capture or neutralise all enemy zones',
            '* To capture a zone, touch the orb',
            "* If a team's territory is split, the smaller section is neutralised",
            '* Use TAB and SPACE to select and buy items',
        ), BOT_GOAL_CAPTURE_MAP)


class StandardRandomLevel(StandardLevel):
    '''
    A standard Trosnoth level with no special events or triggers, played on
    a randomised map.
    '''

    level_code = 'standard'
    hvm_level_name = 'Humans v Machines'

    def __init__(self, map_=None, layout=None, **kwargs):
        super().__init__(**kwargs)

        self.map = map_
        self.layout = layout
        self.duration = self.level_options.get_duration(self)

    def replay(self, **kwargs):
        return super().replay(map_=self.map, layout=self.layout, **kwargs)

    def pre_sync_setup(self):
        super().pre_sync_setup()
        if self.layout is not None:
            # Note: when merging forward to unstable, replace this with
            # self.world.set_map(self.layout, tag_team_pairs=...)
            self.world.setLayout(self.layout)
        elif self.map is None:
            self.layout = self.level_options.apply_map_layout(self)
        else:
            self.layout = self.map.apply(self)

    def getDuration(self):
        return self.duration


if __name__ == '__main__':
    play_level(StandardRandomLevel(), bot_count=1)
