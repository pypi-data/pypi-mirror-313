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

from trosnoth.const import (
    BOT_GOAL_KILL_THINGS,
    ACHIEVEMENT_TACTICAL,
    COINS_PER_KILL,
)
from trosnoth.levels.base import (
    Level, play_level,
    FORCE_RANDOM_TEAMS, LevelOptions,
)
from trosnoth.levels.maps import (
    StandardMap, SmallMap, WideMap, LargeMap, SmallRingMap,
    LargeRingsMap, SmallStackMap, LabyrinthMap, FreeFlowMap,
)
from trosnoth.messages import (
    SetHealthMsg, SetPlayerTeamMsg,
    SetMaxHealthMsg,
)
from trosnoth.model.map import MapLayout
from trosnoth.triggers.base import ScoreBoardStatTrigger
from trosnoth.triggers.coins import (
    AwardStartingCoinsTrigger, SlowlyIncrementLivePlayerCoinsTrigger,
)
from trosnoth.triggers.deathmatch import AddLimitedBotsTrigger, PlayerKillScoreTrigger
from trosnoth.triggers.elephant import EnsureMacGuffinIsInGameTrigger
from trosnoth.triggers.juggernaut import (
    ReachScoreVictoryTrigger,
    JuggernautTransferTrigger, AwardCoinsOnHitTrigger,
)
from trosnoth.triggers.shotstats import KillDeathRatioStatTrigger, AccuracyStatTrigger
from trosnoth.triggers.timestats import GameDurationStatTrigger, PlayerLivePercentageStatTrigger
from trosnoth.utils.event import waitForEvents

BONUS_COINS_FOR_WINNER = 500

KILL_SCORE = 1
DIE_SCORE = 0

WINNING_SCORE = 20

JUGGERNAUT_HEALTH = 4
MAX_BOTS = 4
BOT_CLASS = 'terminator'

log = logging.getLogger(__name__)


class JuggernautLevel(Level):
    '''
    The base class used for levels playing juggernaut.
    '''
    levelName = 'Juggernaut'

    default_duration = 20 * 60
    team_selection = (
        FORCE_RANDOM_TEAMS,
    )
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
    level_code = 'juggernaut'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)

        self.juggernaut_team = self.hunter_team = None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return self.hunter_team

    def pre_sync_teams_setup(self):
        self.hunter_team, self.juggernaut_team = self.pre_sync_create_teams(
            [
                ('Hunters', self.world.players),
                ('Juggernaut', set()),
            ]
        )
        self.level_options.team_ids_humans_can_join = [self.hunter_team.id]

    def pre_sync_setup(self):
        super().pre_sync_setup()
        self.level_options.apply_map_layout(self)

        # Create alternating columns of juggernaut and hunter zones
        horizontal_zone_spacing = MapLayout.zoneBodyWidth + MapLayout.zoneInterfaceWidth
        for zone_def in self.world.map.layout.zones:
            zone_state = self.world.zoneWithDef[zone_def]
            relative_x = zone_def.pos[0] - self.world.layout.centreX
            if round(relative_x / horizontal_zone_spacing) % 2 == 0:
                zone_state.setOwnership(self.juggernaut_team, True)
            else:
                zone_state.setOwnership(self.hunter_team, True)

        self.world.uiOptions.highlight_macguffins = [self.world.juggernaut]

    async def run(self):
        AwardStartingCoinsTrigger(self).activate()
        SlowlyIncrementLivePlayerCoinsTrigger(self, factor=2.5).activate()
        AddLimitedBotsTrigger(
            self,
            MAX_BOTS,
            bot_kind=BOT_CLASS,
            bot_team=self.hunter_team,
            increase_with_enemies=False,
        ).activate()

        await self.main_game_phase()

        # Calculate the winning player or players
        player_scores = self.world.scoreboard.playerScores
        max_score = max(player_scores.values())
        winners = [p for p, score in list(player_scores.items()) if score == max_score]

        return self.build_level_result(tutorial_score=max_score, winners=winners)

    async def main_game_phase(self):
        win_trigger = ReachScoreVictoryTrigger(self, WINNING_SCORE).activate()
        killScoreTrigger = PlayerKillScoreTrigger(self, KILL_SCORE, DIE_SCORE).activate()
        hit_coins_trigger = AwardCoinsOnHitTrigger(self, COINS_PER_KILL).activate()
        transfer_trigger = JuggernautTransferTrigger(self, self.give_juggernaut).activate()
        juggerbot_trigger = EnsureMacGuffinIsInGameTrigger(
            self, self.world.juggernaut, 'JuggerBot',
            custom_give_function=self.give_juggernaut).activate()

        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.setUserInfo('Juggernaut', (
            '* Kill the juggernaut to become the juggernaut',
            '* Kill enemy players to earn points',
            f'* The game will end when one player has earned {WINNING_SCORE} points',
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
        event, args = await waitForEvents([self.world.clock.onZero, win_trigger.on_victory])

        transfer_trigger.deactivate()
        juggerbot_trigger.deactivate()
        win_trigger.deactivate()
        hit_coins_trigger.deactivate()
        self.world.clock.pause()
        self.world.clock.propagateToClients()

        # Don't keep a Juggernaut around in the lobby
        self.give_juggernaut(None)

    def give_juggernaut(self, new_juggernaut):
        old_juggernaut = self.world.juggernaut.possessor

        # Set the new juggernaut's health and team
        if new_juggernaut:
            new_health = max(new_juggernaut.max_health, JUGGERNAUT_HEALTH)
            self.world.sendServerCommand(SetMaxHealthMsg(new_juggernaut.id, new_health))
            if not new_juggernaut.dead:
                self.world.sendServerCommand(SetHealthMsg(new_juggernaut.id, new_health))
            self.world.sendServerCommand(
                SetPlayerTeamMsg(new_juggernaut.id, self.juggernaut_team.id))

        # Move the crosshairs etc.
        self.world.juggernaut.give_to_player(new_juggernaut)

        # Reset the old juggernaut's health and team
        if old_juggernaut:
            self.world.sendServerCommand(SetPlayerTeamMsg(old_juggernaut.id, self.hunter_team.id))
            self.world.sendServerCommand(
                SetMaxHealthMsg(old_juggernaut.id, self.world.physics.playerRespawnHealth))


if __name__ == '__main__':
    play_level(JuggernautLevel(level_options=LevelOptions(duration=120)), bot_count=1)
