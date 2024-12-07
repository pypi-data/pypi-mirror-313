#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import BOT_GOAL_CAPTURE_MAP
from trosnoth.levels.base import play_level
from trosnoth.levels.standard import StandardRandomLevel


class PositioningDrillLevel(StandardRandomLevel):
    levelName = 'Positioning Drill'
    level_code = 'positioningdrill'

    async def mainGamePhase(self):
        self.world.teams[0].abilities.set(aggression=False)
        self.world.teams[1].abilities.set(aggression=False)
        try:
            return await super(PositioningDrillLevel, self).mainGamePhase()
        finally:
            self.world.teams[0].abilities.set(aggression=True)
            self.world.teams[1].abilities.set(aggression=True)

    def setMainGameUserInfo(self):
        self.setUserInfo('Positioning Drill', (
            '* Shooting is deactivated',
            '* Pay attention to which zone you are standing in',
        ), BOT_GOAL_CAPTURE_MAP)


if __name__ == '__main__':
    play_level(PositioningDrillLevel(), bot_count=1)
