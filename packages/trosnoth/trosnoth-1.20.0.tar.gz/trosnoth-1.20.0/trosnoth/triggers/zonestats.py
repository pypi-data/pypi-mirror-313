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

from trosnoth.levels.base import PlayerInfo
from trosnoth.triggers.base import StatTrigger, StatType


class TeamCapEffectStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.points = defaultdict(int)

    def doActivate(self):
        self.world.onZoneCaptureFinalised.addListener(self.got_zone_cap, lifespan=self.lifespan)

    def get_team_stats(self):
        yield 'Zone cap. score', StatType.FLOAT, dict(self.points)

    def got_zone_cap(self, capture_info):
        team = capture_info['team']
        if team:
            self.points[team] += capture_info['points']


class PlayerCapScoreStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.points = defaultdict(float)

    def doActivate(self):
        self.world.onZoneCaptureFinalised.addListener(self.got_zone_cap, lifespan=self.lifespan)

    def get_player_stats(self):
        yield 'Offence score', StatType.FLOAT, dict(self.points)

    def got_zone_cap(self, capture_info):
        diff = capture_info['points'] / len(capture_info['attackers'])
        for player in capture_info['attackers']:
            self.points[PlayerInfo(player)] += diff
