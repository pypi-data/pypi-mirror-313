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
from trosnoth.levels.catpigeon import CatPigeonLevel
from trosnoth.levels.defencedrill import DefenceDrillLevel
from trosnoth.levels.elephantking import ElephantKingLevel
from trosnoth.levels.freeforall import FreeForAllLevel
from trosnoth.levels.hunted import HuntedLevel
from trosnoth.levels.juggernaut import JuggernautLevel
from trosnoth.levels.orbchase import OrbChaseLevel
from trosnoth.levels.positioningdrill import PositioningDrillLevel
from trosnoth.levels.solo import SoloRulesGame
from trosnoth.levels.spacevampire import SpaceVampireLevel
from trosnoth.levels.standard import StandardRandomLevel
from trosnoth.levels.trosball import RandomTrosballLevel


# available_scenario_classes is a list of level classes which may be
# selected automatically by the server, or manually by players.
# The order here corresponds to the order scenarios are shown to players.
available_scenario_classes = [
    StandardRandomLevel,
    SoloRulesGame,
    FreeForAllLevel,
    RandomTrosballLevel,

    CatPigeonLevel,
    ElephantKingLevel,
    HuntedLevel,
    JuggernautLevel,
    OrbChaseLevel,
    SpaceVampireLevel,

    DefenceDrillLevel,
    PositioningDrillLevel,
]


# Level classes that are in server_only will not appear in the list of
# available player preferences, and will not be automatically selected
# by the server.
server_only = {
    DefenceDrillLevel,
    PositioningDrillLevel,
}

scenario_options = [c for c in available_scenario_classes if c not in server_only]
scenario_class_by_code = {c.level_code: c for c in available_scenario_classes}
