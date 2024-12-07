# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2012 Joshua D Bartlett
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

from trosnoth.const import MINIMAP_NORMAL, MINIMAP_PARTLY_DISRUPTED, MINIMAP_FULLY_DISRUPTED
from trosnoth.messages import SetTeamAbilitiesMsg
from trosnoth.model.settingsmanager import SettingsSynchroniser
from trosnoth.model.upgrades import MinimapDisruption, TeamBoosts
from trosnoth.utils import utils

log = logging.getLogger(__name__)


class Team(object):
    '''Represents a team of the game'''
    def __init__(self, world, teamID, teamColour, shot_colour=None):
        self.world = world
        self.numZonesOwned = 0
        self.colour = teamColour
        self.shot_colour = teamColour if shot_colour is None else shot_colour

        self.abilities = SettingsSynchroniser(
            self._dispatchAbilitiesMsg,
            {
                'aggression': True,
                'always_disrupted': False,
                'dark_zones': True,
                'zoneCaps': True,
            },
        )
        self.boosts = TeamBoosts(self)

        if (not isinstance(teamID, bytes)) or len(teamID) != 1:
            raise TypeError('teamID must be a single byte')
        self.id = teamID

        if teamID == b'A':
            self.teamName = 'Blue players'
        elif teamID == b'B':
            self.teamName = 'Red players'
        else:
            self.teamName = '%s Team' % (teamID,)

    def dump(self):
        return {
            'id': self.id,
            'name': self.teamName,
            'abilities': self.abilities.dumpState(),
            'boosts': self.boosts.dump(),
        }

    def restore(self, data):
        self.teamName = data['name']
        self.abilities.restoreState(data['abilities'])
        self.boosts.restore(data.get('boosts', []))

    def get_minimap_status(self):
        for team in self.world.teams:
            if team != self and team.boosts.has(MinimapDisruption):
                return MINIMAP_FULLY_DISRUPTED
        if self.abilities.always_disrupted:
            return MINIMAP_PARTLY_DISRUPTED
        return MINIMAP_NORMAL

    def advance(self):
        self.boosts.tick()

    def __str__(self):
        return self.teamName

    def _dispatchAbilitiesMsg(self, data):
        assert self.world.isServer
        self.world.sendServerCommand(SetTeamAbilitiesMsg(self.id, data))

    def shade(self, contrast, brightness):
        return utils.shade(self.colour, contrast, brightness)

    def zoneLost(self):
        '''Called when a orb belonging to this team has been lost'''
        self.numZonesOwned -= 1

    def zoneGained(self, score=0):
        '''Called when a orb has been attributed to this team'''
        self.numZonesOwned += 1

    @staticmethod
    def setOpposition(teamA, teamB):
        teamA.opposingTeam = teamB
        teamB.opposingTeam = teamA

    def is_enemy_territory(self, room_team):
        # Note: for the time being, this may sometimes be called as a
        # class method, because a player's team might be None (for
        # rogues). It would be much nicer to introduce a separate team
        # object for rogues, and leave None for neutral zones.
        if room_team is None:
            # Neutral room is not the same as an enemy room
            return False
        return self != room_team

    def is_friendly_territory(self, room_team):
        return self == room_team
