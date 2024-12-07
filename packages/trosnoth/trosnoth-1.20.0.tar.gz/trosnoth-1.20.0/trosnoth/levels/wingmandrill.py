#!/usr/bin/env python3
# Trosnoth (Ubertweak Platform Game)
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

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import BOT_GOAL_CAPTURE_MAP
from trosnoth.levels.base import play_level
from trosnoth.levels.maps import CorridorMap
from trosnoth.levels.standard import StandardRandomLevel


class HumansAreWingmenLevel(StandardRandomLevel):
    levelName = 'Wingman Challenge'

    map_selection = (CorridorMap(),) + StandardRandomLevel.map_selection

    async def mainGamePhase(self):
        for player in self.world.players:
            if not player.bot:
                player.abilities.set(orb_capture=False)
        self.world.onPlayerAdded.addListener(self.player_added)
        try:
            return await super().mainGamePhase()
        finally:
            self.world.onPlayerAdded.removeListener(self.player_added)

    def setMainGameUserInfo(self):
        self.setUserInfo('Wingman Challenge', (
            '* Human players can’t capture orbs',
            '* Good luck!',
        ), BOT_GOAL_CAPTURE_MAP)

    def player_added(self, player):
        if not player.bot:
            player.abilities.set(orb_capture=False)


class HumansAreWingmenAndMustBeRedLevel(HumansAreWingmenLevel):
    def pre_sync_setup(self):
        super().pre_sync_setup()
        self.world.uiOptions.team_ids_humans_can_join = [b'B']


if __name__ == '__main__':
    play_level(HumansAreWingmenLevel(), bot_count=1)
