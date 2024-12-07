#!/usr/bin/env python3

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
from trosnoth.levels.maps import (
    SmallRingMap, LargeRingsMap, SmallStackMap, LabyrinthMap,
    StandardMap, SmallMap, WideMap, LargeMap, FreeFlowMap,
)
from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.coins import (
    SlowlyIncrementLivePlayerCoinsTrigger, AwardStartingCoinsTrigger,
)
from trosnoth.triggers.base import ScoreBoardStatTrigger
from trosnoth.triggers.deathmatch import AddOneBotTrigger
from trosnoth.triggers.elephant import (
    ElephantDurationScoreTrigger, EnsureMacGuffinIsInGameTrigger,
)
from trosnoth.triggers.shotstats import KillDeathRatioStatTrigger, AccuracyStatTrigger
from trosnoth.triggers.timestats import GameDurationStatTrigger, PlayerLivePercentageStatTrigger

from trosnoth.levels.base import Level, play_level, LevelOptions

BONUS_COINS_FOR_WINNER = 500


class ElephantKingLevel(Level):
    levelName = 'Elephant King'

    halfMapWidth = 1
    mapHeight = 2
    blockRatio = 0.35
    default_duration = 360
    map_selection = (
        SmallRingMap(),
        LargeRingsMap(),
        SmallStackMap(),
        LabyrinthMap(),
        FreeFlowMap(),
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )
    level_code = 'elephantking'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return None

    def pre_sync_teams_setup(self):
        self.pre_sync_create_teams(
            [(DEFAULT_TEAM_NAME_1, ()), (DEFAULT_TEAM_NAME_2, ())],
            neutral_players=self.world.players)
        self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    def pre_sync_setup(self):
        super().pre_sync_setup()
        self.level_options.apply_map_layout(self)
        self.world.uiOptions.highlight_macguffins = [self.world.elephant]

    async def run(self):
        startingCoinsTrigger = AwardStartingCoinsTrigger(self).activate()
        SlowlyIncrementLivePlayerCoinsTrigger(self, factor=2.5).activate()
        ElephantDurationScoreTrigger(self).activate()
        EnsureMacGuffinIsInGameTrigger(self, self.world.elephant, 'ElephantBot').activate()
        AddOneBotTrigger(self).activate()
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.setUserInfo('Elephant King', (
            '* To get the elephant, kill the player who has it',
            '* The player who holds the elephant for the longest wins',
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
        maxScore = max(playerScores.values())
        winners = [
            p for p, score in playerScores.items()
            if score == maxScore]

        return self.build_level_result(
            a_human_player_won=True,
            winners=winners,
        )


if __name__ == '__main__':
    play_level(ElephantKingLevel(level_options=LevelOptions(duration=120)), bot_count=2)
