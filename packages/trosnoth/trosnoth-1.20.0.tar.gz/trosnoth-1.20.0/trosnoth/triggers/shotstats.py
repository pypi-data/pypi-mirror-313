# Trosnoth
# Copyright (C) Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from collections import defaultdict
import math

from trosnoth.levels.base import PlayerInfo
from trosnoth.triggers.base import StatTrigger, StatType


class KillDeathRatioStatTrigger(StatTrigger):
    def __init__(self, level, kills=False, deaths=False):
        super().__init__(level)
        self.show_kills = kills
        self.show_deaths = deaths
        self.player_kills: dict[PlayerInfo, int] = defaultdict(int)
        self.player_deaths: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        results = {}
        for player_info in set(self.player_kills).union(self.player_deaths):
            kills, deaths = self.player_kills[player_info], self.player_deaths[player_info]
            results[player_info] = 0 if kills == 0 else math.inf if deaths == 0 else kills / deaths

        yield 'Kills/death', StatType.FLOAT_OR_NONE, results
        if self.show_kills:
            yield 'Kills', StatType.FLOAT, dict(self.player_kills)
        if self.show_deaths:
            yield 'Deaths', StatType.FLOAT, dict(self.player_deaths)

    def doActivate(self):
        self.world.onPlayerKill.addListener(self.got_player_kill, lifespan=self.lifespan)

    def got_player_kill(self, killer, target, hit_kind):
        self.player_deaths[PlayerInfo(target)] += 1
        if killer:
            self.player_kills[PlayerInfo(killer)] += 1


class DefensiveKillStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.result: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        yield 'Defensive kills', StatType.FLOAT, self.result

    def doActivate(self):
        self.world.onPlayerKill.addListener(self.got_player_kill, lifespan=self.lifespan)

    def got_player_kill(self, killer, target, hit_kind):
        if not killer:
            return
        if killer.dead or killer.team != killer.getZone().owner:
            if target.team == target.getZone().owner or target.team not in \
                    target.getZone().get_living_players_by_team():
                return
        self.result[PlayerInfo(killer)] += 1


class AccuracyStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.shot_count: dict[PlayerInfo, int] = defaultdict(int)
        self.hit_count: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        yield 'Accuracy', StatType.PERCENTAGE, {
            p: self.hit_count[p] / self.shot_count[p]
            for p in self.shot_count}

    def doActivate(self):
        self.world.on_shot_fired.addListener(self.got_shot_fired, lifespan=self.lifespan)
        self.world.on_shot_hit_something.addListener(
            self.got_shot_hit_something, lifespan=self.lifespan)

    def got_shot_fired(self, shooter, shot):
        self.shot_count[PlayerInfo(shooter)] += 1

    def got_shot_hit_something(self, shooter, hit):
        self.hit_count[PlayerInfo(shooter)] += 1
