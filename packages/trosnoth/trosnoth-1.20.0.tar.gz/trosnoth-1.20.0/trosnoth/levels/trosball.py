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
    FRONT_LINE_TROSBALL, BOT_GOAL_SCORE_TROSBALL_POINT,
    ACHIEVEMENT_TACTICAL,
    BONUS_COINS_FOR_TROSBALL_SCORE,
)
from trosnoth.levels.base import (
    Level, play_level, SELECTABLE_TEAMS,
    FORCE_RANDOM_TEAMS, HVM_TEAMS, LevelOptions,
)
from trosnoth.levels.maps import StandardMap, SmallMap, WideMap, LargeMap
from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.base import ScoreBoardStatTrigger
from trosnoth.triggers.coins import (
    SlowlyIncrementLivePlayerCoinsTrigger, AwardStartingCoinsTrigger,
)
from trosnoth.triggers.shotstats import KillDeathRatioStatTrigger, AccuracyStatTrigger
from trosnoth.triggers.timestats import (
    StandardGameWinPercentStatTrigger, GameDurationStatTrigger,
    PlayerLivePercentageStatTrigger,
)
from trosnoth.triggers.trosball import StandardTrosballScoreTrigger
from trosnoth.utils.event import waitForEvents

log = logging.getLogger(__name__)


class TrosballMatchBase(Level):
    levelName = 'Trosball'
    default_duration = 5 * 60
    team_selection = (
        SELECTABLE_TEAMS,
        FORCE_RANDOM_TEAMS,
        HVM_TEAMS,
    )
    map_selection = (
        WideMap(),
        SmallMap(),
        StandardMap(),
        LargeMap(),
    )

    def __init__(self, *args, **kwargs):
        super(TrosballMatchBase, self).__init__(*args, **kwargs)

        duration = self.level_options.get_duration(self)
        self.totalDuration = duration
        self.roundDuration = duration
        self.scoreTrigger = None

    def pre_sync_setup(self):
        super().pre_sync_setup()
        self.make_new_map(first=True)
        if self.level_options.get_team_option(self) == SELECTABLE_TEAMS:
            self.world.uiOptions.team_ids_humans_can_join = [b'A', b'B']
            self.world.uiOptions.team_ids_humans_can_switch_to = [b'A', b'B']
        else:
            self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    async def run(self):
        team_option = self.level_options.get_team_option(self)
        if team_option == HVM_TEAMS and not self.world.botManager:
            self.begin_hvm()

        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        startingCoinsTrigger = AwardStartingCoinsTrigger(self).activate()
        scoreTrigger = StandardTrosballScoreTrigger(self).activate()
        self.world.scoreboard.setMode(teams=True)

        self.setGameOptions()

        onBuzzer = self.world.clock.onZero
        on_score = scoreTrigger.onTrosballScore
        win_stat = StandardGameWinPercentStatTrigger(self)
        self.stats.add_triggers([
            GameDurationStatTrigger(self),
            win_stat,
            ScoreBoardStatTrigger(self),
            PlayerLivePercentageStatTrigger(self),
            KillDeathRatioStatTrigger(self, deaths=True),
            AccuracyStatTrigger(self),
        ])
        while True:
            self.initCountdown()
            await onBuzzer.wait_future()
            if startingCoinsTrigger:
                startingCoinsTrigger.deactivate()
                startingCoinsTrigger = None

            self.initRound()
            self.stats.resume()
            event, args = await waitForEvents([onBuzzer, on_score])
            self.stats.pause()
            if event == onBuzzer:
                break
            self.handle_score(**args)

            await self.world.sleep_future(3)
            self.resetMap()

        max_score = max(self.world.scoreboard.teamScores.values())
        winners = [
            t for t, score in list(self.world.scoreboard.teamScores.items())
            if score == max_score
        ]
        win_stat.finalise(winners)

        return self.build_level_result(winners=winners)

    def setGameOptions(self):
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.world.uiOptions.set(
            showNets=True,
            frontLine=FRONT_LINE_TROSBALL,
        )
        self.world.abilities.set(zoneCaps=False)

        self.world.trosballManager.enable()

        self.setUserInfo('Trosball', (
            '* Score points by getting the trosball through the net',
            '* To throw the trosball, press the "use upgrade" key',
            '* The trosball explodes if held for too long',
        ), BOT_GOAL_SCORE_TROSBALL_POINT)

    def handle_score(self, room, player):
        # Scoring team is the one who's not defending this net
        if room.owner == self.world.teams[0]:
            team = self.world.teams[1]
        else:
            team = self.world.teams[0]

        self.playSound('short-whistle.ogg')
        self.world.trosballManager.place_in_net(room)
        self.world.scoreboard.teamScored(team)

        self.world.clock.pause()
        self.world.clock.propagateToClients()
        self.roundDuration = self.world.clock.value

        if player is not None:
            if player.team == team:
                message = '%s scored for %s!' % (player.nick, team.teamName)
            else:
                message = '%s scores an own goal!' % (player.nick,)
            self.world.sendServerCommand(AwardPlayerCoinMsg(
                player.id, count=BONUS_COINS_FOR_TROSBALL_SCORE))
        else:
            message = 'Score for %s!' % (team.teamName,)
        self.notifyAll(message)

    def resetMap(self):
        self.world.trosballManager.resetToStartLocation()
        self.make_new_map(first=False)
        for player in self.world.players:
            zone = self.world.select_good_respawn_zone_for_team(player.team)
            player.makeAllDead(respawnTime=0.0)
            player.teleport_to_respawn_point(zone)
            player.resyncBegun()

        self.world.syncEverything()

    def initCountdown(self, delay=6):
        self.world.pauseStats()
        self.world.clock.startCountDown(delay, flashBelow=0)
        self.world.clock.propagateToClients()

        self.world.abilities.set(
            upgrades=False, respawn=False, leaveFriendlyZones=False)

    def initRound(self):
        self.playSound('startGame.ogg')
        self.world.resumeStats()
        self.world.abilities.set(
            upgrades=True, respawn=True, leaveFriendlyZones=True)

        self.world.clock.startCountDown(self.roundDuration)
        self.world.clock.propagateToClients()

    def make_new_map(self, first):
        raise NotImplementedError(f'{self.__class__.__name__}.make_new_map')


class RandomTrosballLevel(TrosballMatchBase):
    '''
    A standard Trosnoth level with no special events or triggers, played on
    a randomised map.
    '''

    level_code = 'trosball'
    hvm_level_name = 'HvM Trosball'

    def __init__(self, map_=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map = map_

    def replay(self, **kwargs):
        return super().replay(map_=self.map, **kwargs)

    def make_new_map(self, first):
        if self.map is None:
            self.level_options.apply_map_layout(self)
        else:
            self.map.apply(self)


if __name__ == '__main__':
    play_level(RandomTrosballLevel(level_options=LevelOptions(duration=90)), bot_count=7)
