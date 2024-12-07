#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import ACHIEVEMENT_TACTICAL, BOT_GOAL_KILL_THINGS
from trosnoth.levels.base import Level, play_level, LevelOptions
from trosnoth.levels.maps import LargeRingsMap, SmallRingMap, SmallStackMap
from trosnoth.triggers.base import ScoreBoardStatTrigger
from trosnoth.triggers.coins import SlowlyIncrementLivePlayerCoinsTrigger
from trosnoth.triggers.deathmatch import (
    AddLimitedBotsTrigger, PlayerLifeScoreTrigger,
    PlayerKillScoreTrigger,
)
from trosnoth.triggers.shotstats import AccuracyStatTrigger
from trosnoth.triggers.timestats import (
    GameDurationStatTrigger, PlayerLivePercentageStatTrigger,
    ElevationStatTrigger, GrapplePercentStatTrigger, WalkPercentStatTrigger,
)


MIN_HUNTERS = 4
MAX_HUNTERS = 12
BONUS_COINS_FOR_WINNER = 500


class HuntedLevel(Level):
    levelName = 'Hunted'
    default_duration = 6 * 60
    map_selection = (
        LargeRingsMap(),
        SmallRingMap(),
        SmallStackMap(),
    )
    level_code = 'hunted'

    def __init__(self, *args, **kwargs):
        super(HuntedLevel, self).__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)
        self.blue_team = self.red_team = None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return self.red_team

    def pre_sync_teams_setup(self):
        self.blue_team, self.red_team = self.pre_sync_create_teams(
            [
                ('Hunters', ()),
                ('Hunted', self.world.players),
            ]
        )
        self.world.uiOptions.team_ids_humans_can_join = [b'B']

    def pre_sync_setup(self):
        super().pre_sync_setup()
        self.level_options.apply_map_layout(self)

    async def run(self):
        try:
            self.red_team.abilities.set(aggression=False)

            for player in self.world.players:
                if not player.bot:
                    room = self.world.select_good_respawn_zone_for_team(self.red_team)
                    self.world.magically_move_player_now(player, room.centre, alive=True)


            SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
            scoreTrigger = PlayerLifeScoreTrigger(
                self, teams={self.red_team}).activate()
            PlayerKillScoreTrigger(self, dieScore=0).activate()
            botTrigger = AddLimitedBotsTrigger(level=self, max_bots=MAX_HUNTERS,
                min_bots=MIN_HUNTERS, bot_kind='terminator', bot_nick='Terminator',
                bot_team=self.blue_team, increase_with_enemies=True).activate()
            self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
            self.setUserInfo('Hunted', (
                '* Die as few times as possible',
                '* Players score points for every second they are alive',
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
                AccuracyStatTrigger(self),
                ElevationStatTrigger(self),
                GrapplePercentStatTrigger(self),
                WalkPercentStatTrigger(self),
            ])
            self.stats.resume()

            await self.world.clock.onZero.wait_future()

            # Game over!
            self.world.finaliseStats()
            botTrigger.deactivate()
            player_scores = self.world.scoreboard.playerScores
            max_score = max(player_scores.values())
            winners = [
                p for p, score in list(player_scores.items())
                if score == max_score and p.team == self.red_team]

        finally:
            self.red_team.abilities.set(aggression=True)

        return self.build_level_result(
            a_human_player_won=True,
            tutorial_score=max_score,
            winners=winners,
        )


if __name__ == '__main__':
    play_level(HuntedLevel(level_options=LevelOptions(duration=120)), bot_count=1)
