#!/usr/bin/env python3
# coding=utf-8
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import (
    ACHIEVEMENT_TACTICAL, BOT_GOAL_KILL_THINGS, DEFAULT_TEAM_NAME_1,
    DEFAULT_TEAM_NAME_2,
)
from trosnoth.levels.base import Level, play_level, LevelOptions
from trosnoth.levels.maps import (
    LargeRingsMap, SmallRingMap, SmallStackMap, LabyrinthMap,
    SmallMap, StandardMap, LargeMap, WideMap, FreeFlowMap,
)
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.base import ScoreBoardStatTrigger
from trosnoth.triggers.coins import (
    SlowlyIncrementLivePlayerCoinsTrigger, AwardStartingCoinsTrigger,
)
from trosnoth.triggers.deathmatch import (
    PlayerKillScoreTrigger, AddOneBotTrigger,
)
from trosnoth.triggers.shotstats import KillDeathRatioStatTrigger, AccuracyStatTrigger
from trosnoth.triggers.timestats import GameDurationStatTrigger, PlayerLivePercentageStatTrigger

BONUS_COINS_FOR_WINNER = 500


class FreeForAllLevel(Level):
    levelName = 'Free for All'
    default_duration = 6 * 60
    map_selection = (
        LargeRingsMap(),
        SmallRingMap(),
        SmallStackMap(),
        LabyrinthMap(),
        FreeFlowMap(),
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )
    level_code = 'free4all'

    def __init__(self, map_builder=None, add_one_bot=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_one_bot = add_one_bot
        self.duration = self.level_options.get_duration(self)
        self.map_builder = map_builder

    def replay(self, **kwargs):
        return super().replay(map_builder=self.map_builder, add_one_bot=self.add_one_bot, **kwargs)

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return None

    def pre_sync_teams_setup(self):
        self.pre_sync_create_teams(
            [(DEFAULT_TEAM_NAME_1, ()), (DEFAULT_TEAM_NAME_2, ())],
            neutral_players=self.world.players)
        self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    def pre_sync_setup(self):
        super().pre_sync_setup()
        if self.map_builder is None:
            self.level_options.apply_map_layout(self)
        else:
            self.world.setLayout(self.map_builder())

    async def run(self):
        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        AwardStartingCoinsTrigger(self).activate()
        PlayerKillScoreTrigger(self, dieScore=-0.5).activate()
        if self.add_one_bot:
            AddOneBotTrigger(self).activate()
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.setUserInfo('Free for All', (
            '* You gain 1 point per kill',
            '* You lose ½ point if you are killed',
            '* Kills earn you money',
            '* Use TAB to select an item to buy',
            '* Press SPACE to buy selected item',
        ), BOT_GOAL_KILL_THINGS)
        self.world.abilities.set(zoneCaps=False, balanceTeams=False)
        if self.duration:
            self.world.clock.startCountDown(self.duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        self.stats.add_triggers([
            GameDurationStatTrigger(self),
            ScoreBoardStatTrigger(self),
            PlayerLivePercentageStatTrigger(self),
            KillDeathRatioStatTrigger(self, kills=True),
            AccuracyStatTrigger(self),
        ])
        self.stats.resume()

        await self.world.clock.onZero.wait_future()

        # Game over!
        playerScores = self.world.scoreboard.playerScores
        max_score = max(playerScores.values())
        winners = [
            p for p, score in list(playerScores.items())
            if score == max_score]

        return self.build_level_result(
            tutorial_score=max_score,
            winners=winners,
        )


if __name__ == '__main__':
    play_level(FreeForAllLevel(level_options=LevelOptions(duration=60)), bot_count=0)
