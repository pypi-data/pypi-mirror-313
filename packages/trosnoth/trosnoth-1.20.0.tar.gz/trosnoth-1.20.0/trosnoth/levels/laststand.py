#!/usr/bin/env python3

if __name__ == '__main__':
    import os, sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import random

from trosnoth.levels.base import play_level
from trosnoth.levels.standard import StandardRandomLevel
from trosnoth.model.player import Player
from trosnoth.model.zonemechanics import ZoneCaptureCalculator


class LastStandLevel(StandardRandomLevel):
    levelName = 'Last Stand'

    def __init__(
            self, *args,
            defending_team_index=None,
            remaining_zone_indices=None,
            neutral_zone_indices=None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.defending_team_index = defending_team_index
        self.defending_team = None
        self.remaining_zone_indices = remaining_zone_indices
        self.neutral_zone_indices = neutral_zone_indices
        self.human_joined = False

    def replay(self, **kwargs):
        return super().replay(
            defending_team_index=self.defending_team_index,
            remaining_zone_indices=self.remaining_zone_indices,
            neutral_zone_indices=self.neutral_zone_indices,
            **kwargs)

    def get_team_to_join(self, preferred_team, user, nick, bot):
        if not bot and not self.human_joined:
            self.human_joined = True
            return self.defending_team
        return super().get_team_to_join(preferred_team, user, nick, bot)

    def pre_sync_setup(self):
        super().pre_sync_setup()

        if self.defending_team_index is None:
            self.defending_team = random.choice(self.world.teams)
            self.defending_team_index = self.world.teams.index(self.defending_team)
        else:
            self.defending_team = self.world.teams[self.defending_team_index]

        if self.remaining_zone_indices is None:
            self.deplete_to_two_zones()
            self.remaining_zone_indices = [
                z.id for z in self.world.rooms
                if z.owner == self.defending_team]
            self.neutral_zone_indices = [
                z.id for z in self.world.rooms
                if z.owner is None]
        else:
            attacking_team = [t for t in self.world.teams if t != self.defending_team][0]
            imaginary_player = Player(self.world, 'ImaginaryPlayer', team=attacking_team, id_=-1)
            # TODO: when merging forwards, replace getZone with world.rooms.get_with_id()
            defending_zones = set(self.world.getZone(i) for i in self.remaining_zone_indices)
            neutral_zones = set(self.world.getZone(i) for i in self.neutral_zone_indices)
            for z in self.world.rooms:
                if z in neutral_zones:
                    if z.owner is not None:
                        z.tag(None)
                elif z not in defending_zones:
                    if z.owner != attacking_team:
                        z.tag(imaginary_player)

    def deplete_to_two_zones(self):
        attacking_team = [t for t in self.world.teams if t != self.defending_team][0]
        imaginary_player = Player(self.world, 'ImaginaryPlayer', team=attacking_team, id_=-1)
        while len([z for z in self.world.rooms if z.owner == self.defending_team]) > 2:
            next_cap = random.choice([
                z2 for z1 in self.world.rooms if z1.owner == attacking_team
                for z2 in z1.open_neighbours if z2.owner != attacking_team])

            calculator = ZoneCaptureCalculator(self.world)
            calculator.markZoneCaptured(
                next_cap, dict(team=attacking_team, player=None, defenders=set(), attackers=set()))
            calculator.finalise(sendNeutraliseEvent=False)
            next_cap.tag(imaginary_player)
            for zone in calculator.neutralisedZones:
                zone.tag(None)


if __name__ == '__main__':
    play_level(LastStandLevel(), bot_count=5, return_when_level_completes=True)
