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

'''
macguffins.py - code relating to the model for sought-after items like
the elephant, the juggernaut crosshairs, and maybe eventually the
trosball. Each MacGuffin can be held by at most one player at a time.
'''
from trosnoth.messages import PlayerHasMacGuffin
from trosnoth.model.universe_base import NO_PLAYER
from trosnoth.utils.event import Event


class MacGuffin:
    def __init__(self, world, macguffin_id):
        self.world = world
        self.macguffin_id = macguffin_id
        self.possessor = None

        self.on_death_of_possessor = Event(['killer'])
        self.on_possessor_left_game = Event()
        self.on_transfer = Event(['old_possessor', 'new_possessor'])

        world.macguffin_manager.register(self)

    def dump(self):
        return self.possessor.id if self.possessor else NO_PLAYER

    def restore(self, data):
        self.possessor = self.world.getPlayer(data)

    def give_to_player(self, player):
        assert self.world.isServer
        self.world.sendServerCommand(
            PlayerHasMacGuffin(player.id if player else NO_PLAYER, self.macguffin_id))


class MacGuffinManager:
    '''
    Keeps track of the state of all the available MacGuffins.
    '''

    def __init__(self, world):
        self.world = world
        self.macguffins = {}

    def register(self, macguffin):
        if macguffin.macguffin_id in self.macguffins:
            raise KeyError(f'MacGuffin with ID {macguffin.macguffin_id!r} already exists')
        self.macguffins[macguffin.macguffin_id] = macguffin

    def received_transfer_message(self, player, macguffin_id):
        macguffin = self.macguffins[macguffin_id]
        old_possessor = macguffin.possessor
        macguffin.possessor = player
        if old_possessor != player:
            macguffin.on_transfer(old_possessor, player)

    def player_is_leaving(self, player):
        for macguffin in self.macguffins.values():
            if macguffin.possessor == player:
                macguffin.on_possessor_left_game()

                # If the leave game event hasn't given the macguffin to
                # someone else, ensure everyone knows it's unowned now.
                if macguffin.possessor == player:
                    macguffin.give_to_player(None)

    def player_is_dying(self, player, killer):
        for macguffin in self.macguffins.values():
            if macguffin.possessor == player:
                macguffin.on_death_of_possessor(killer)

    def dump(self):
        return {mid: m.dump() for mid, m in self.macguffins.items()}

    def restore(self, data):
        for mid, m in self.macguffins.items():
            m.restore(data[mid])

    def reset(self):
        for macguffin in self.macguffins.values():
            macguffin.give_to_player(None)
