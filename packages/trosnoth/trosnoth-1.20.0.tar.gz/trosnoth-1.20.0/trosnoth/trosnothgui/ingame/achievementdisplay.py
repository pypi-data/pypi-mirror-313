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

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Tuple

from trosnoth.gui.framework.declarative import Rectangle, Text, Graphic, ComplexDeclarativeThing
from trosnoth.gamerecording.achievementlist import availableAchievements

if TYPE_CHECKING:
    from trosnoth.model.player import Player


log = logging.getLogger(__name__)


class RecentAchievements:
    def __init__(self):
        self.achievements = []

    def clear(self):
        self.achievements = []

    def add(self, achievement_msg):
        self.achievements.append(achievement_msg)


@dataclass(frozen=True)
class AchievementDisplay(ComplexDeclarativeThing):
    new_achievements: RecentAchievements
    player: 'Player'

    CYCLE_TIME = 3

    def build_state(self, renderer):
        return {
            'showing_ids': [],
            'time_until_cycle': 0,
        }

    def draw(self, frame, state):
        self.update_state_with_new_achievements(state)
        self.update_state_from_time_passing(state, frame.delta_t)
        showing_ids = state['showing_ids']
        if not showing_ids:
            return

        team = self.player.team or self.player.world.teams[-1]
        frame.add(
            AchievementBanner(
                current_id=showing_ids[0],
                count=len(showing_ids),
                border_colour=team.shade(0.5, 0),
                back_colour=team.shade(0.33, 0.9),
            ),
            alpha=0.8,
        )

    def update_state_from_time_passing(self, state, delta_t):
        state['time_until_cycle'] -= delta_t
        if state['time_until_cycle'] <= 0 and state['showing_ids']:
            state['showing_ids'].pop(0)
            state['time_until_cycle'] = self.CYCLE_TIME

    def update_state_with_new_achievements(self, state):
        if not state['showing_ids']:
            state['time_until_cycle'] = self.CYCLE_TIME
        for achievement_msg in self.new_achievements.achievements:
            if achievement_msg.playerId == self.player.id:
                state['showing_ids'].append(achievement_msg.achievementId)
        self.new_achievements.clear()


@dataclass(frozen=True)
class AchievementBanner(ComplexDeclarativeThing):
    current_id: bytes
    count: int
    border_colour: Tuple[int, int, int]
    back_colour: Tuple[int, int, int]

    def draw(self, frame, state):
        # Background and border
        frame.add(
            Rectangle(
                width=452, height=76, colour=self.back_colour,
                border=self.border_colour, border_width=1.5),
            at=(0, -38),
        )

        # White rectangle behind the achievement icon
        frame.add(
            Rectangle(
                width=66, height=66, colour=(255, 255, 255),
                border=self.border_colour, border_width=0.75),
            at=(-188, -38),
        )

        frame.add(AchievementIcon(self.current_id), at=(-188, -38))

        if self.count == 1:
            heading = 'ACHIEVEMENT!'
        else:
            heading = f'{self.count} ACHIEVEMENTS!'

        frame.add(
            Text(
                heading,
                height=18,
                font='orbitron-light.ttf',
                text_colour=self.border_colour,
                max_width=371,
            ),
            at=(35.5, -48),
        )

        achievement_name, *_ = availableAchievements.getAchievementDetails(self.current_id)
        frame.add(
            Text(
                achievement_name,
                height=21,
                font='Junction.ttf',
                text_colour=(0, 0, 0),
                max_width=371,
            ),
            at=(35.5, -13),
        )


@dataclass(frozen=True)
class AchievementIcon(ComplexDeclarativeThing):
    achievement_id: bytes

    def draw(self, frame, state):
        frame.add(Graphic(
            filepath=f'achievements/{self.achievement_id.decode()}.png',
            fallback_path='achievements/default.png',
            width=64, height=64,
        ))
