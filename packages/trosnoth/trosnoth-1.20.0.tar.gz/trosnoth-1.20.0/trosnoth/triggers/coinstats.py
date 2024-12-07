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


class UnspentCoinsStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.totals: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        results = defaultdict(int, self.totals)
        for p in self.world.players:
            results[PlayerInfo(p)] += p.coins
        yield 'Unspent', StatType.MONEY, results

    def doActivate(self):
        self.world.on_player_dropped_coins.addListener(
            self.got_player_dropped_coins, lifespan=self.lifespan)
        self.world.onPlayerRemoved.addListener(self.got_player_removed, lifespan=self.lifespan)

    def got_player_dropped_coins(self, player, value):
        self.totals[PlayerInfo(player)] += value

    def got_player_removed(self, player, old_id):
        self.totals[PlayerInfo(player)] += player.coins
