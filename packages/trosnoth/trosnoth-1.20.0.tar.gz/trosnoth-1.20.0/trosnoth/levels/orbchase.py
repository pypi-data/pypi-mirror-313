#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import random

from trosnoth.const import BOT_GOAL_CAPTURE_MAP, ACHIEVEMENT_TACTICAL
from trosnoth.levels.base import play_level, Level, LevelOptions
from trosnoth.levels.maps import (
    LabyrinthMap, LargeRingsMap, SmallRingMap, FreeFlowMap,
    StandardMap, WideMap, LargeMap, SmallMap,
)
from trosnoth.messages import ZoneStateMsg
from trosnoth.model.universe import OrbRegion
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.base import ScoreBoardStatTrigger
from trosnoth.triggers.coins import SlowlyIncrementLivePlayerCoinsTrigger
from trosnoth.triggers.coinstats import UnspentCoinsStatTrigger
from trosnoth.triggers.timestats import (
    GameDurationStatTrigger, ElevationStatTrigger,
    GrapplePercentStatTrigger, WalkPercentStatTrigger,
)
from trosnoth.utils.event import waitForEvents
from trosnoth.utils.math import distance

BONUS_COINS_FOR_WINNER = 500


class OrbChaseLevel(Level):
    levelName = 'Orb Chase'
    default_duration = 6 * 60
    map_selection = (
        FreeFlowMap(),
        LabyrinthMap(),
        LargeRingsMap(),
        SmallRingMap(),
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )
    level_code = 'orbchase'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)

        self.team = None
        self.targetZone = None
        self.targetTeamId = None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        return self.team

    def pre_sync_teams_setup(self):
        self.team, _ = self.pre_sync_create_teams([
            ('Racers', self.world.players),
            ('Targets', ()),
        ])
        self.targetTeamId = self.world.teams[1].id
        self.world.uiOptions.team_ids_humans_can_join = [b'A']

    def pre_sync_setup(self):
        super().pre_sync_setup()
        self.level_options.apply_map_layout(self)
        for zone in self.world.zones:
            if zone.owner != self.team:
                zone.setOwnership(None, False)

    async def run(self):
        self.team.abilities.set(aggression=False)

        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.world.scoreboard.setMode(players=True)
        self.world.abilities.set(zoneCaps=False, balanceTeams=False)
        self.world.uiOptions.set(team_ids_humans_can_join=[b'A'])

        await self.pregameCountdownPhase()
        self.stats.add_triggers([
            GameDurationStatTrigger(self),
            ScoreBoardStatTrigger(self),
            ElevationStatTrigger(self),
            GrapplePercentStatTrigger(self),
            WalkPercentStatTrigger(self),
            UnspentCoinsStatTrigger(self),
        ])
        self.stats.resume()
        await self.mainPhase()

        # Game over!
        player_scores = self.world.scoreboard.playerScores
        max_score = max(player_scores.values())
        winners = [
            p for p, score in list(player_scores.items())
            if score == max_score
        ]

        self.team.abilities.set(aggression=True)
        return self.build_level_result(
            a_human_player_won=(max_score > 0),
            tutorial_score=max_score,
            winners=winners,
        )

    async def pregameCountdownPhase(self, delay=10):
        self.setUserInfo('Get Ready...', (
            '* Game will begin soon',
            '* Score points by touching the red orb',
        ), BOT_GOAL_CAPTURE_MAP)
        self.world.clock.startCountDown(delay, flashBelow=0)
        self.world.clock.propagateToClients()

        self.world.pauseStats()
        self.world.abilities.set(respawn=False)
        await self.world.clock.onZero.wait_future()

    async def mainPhase(self):
        self.setUserInfo('Orb Chase', (
            '* Score points by touching the red orb',
            '* Don’t forget you have a grappling hook (R.Click by default)',
        ), BOT_GOAL_CAPTURE_MAP)
        self.notifyAll('The game is now on!!')
        self.playSound('startGame.ogg')
        self.world.resumeStats()
        self.world.abilities.set(respawn=True)

        if self.duration:
            self.world.clock.startCountDown(self.duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        onClockZero = self.world.clock.onZero

        while True:
            zone = self.select_room()
            region = OrbRegion(self.world, zone)
            self.world.addRegion(region)
            try:
                event, args = await waitForEvents(
                    [onClockZero, region.onEnter])

                if event == onClockZero:
                    break

                self.playSound('short-whistle.ogg')
                self.world.scoreboard.playerScored(args['player'], 1)
            finally:
                self.world.removeRegion(region)

    def select_room(self):
        if self.targetZone:
            self.world.sendServerCommand(
                ZoneStateMsg(self.targetZone.id, NEUTRAL_TEAM_ID, False))

        all_rooms = [r for r in self.world.rooms if r.owner is None and r.orb_pos is not None]
        options = [r for r in all_rooms if not r.players]
        if options:
            zone = random.choice(options)
        else:
            zone = min(
                all_rooms,
                key=lambda r: min(distance(r.orb_pos, p.pos) for p in r.players))

        self.world.sendServerCommand(
            ZoneStateMsg(zone.id, self.targetTeamId, True))
        self.targetZone = zone
        return zone


if __name__ == '__main__':
    play_level(OrbChaseLevel(level_options=LevelOptions(duration=120)))
