#!/usr/bin/env python3
if __name__ == '__main__':
    import os, sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.const import BOT_GOAL_CAPTURE_MAP
from trosnoth.levels.base import play_level
from trosnoth.levels.standard import StandardRandomLevel


class DefenceDrillLevel(StandardRandomLevel):
    levelName = 'Defence Drill'
    level_code = 'defencedrill'

    async def mainGamePhase(self):
        self.world.teams[1].abilities.set(zoneCaps=False)
        try:
            return await super(DefenceDrillLevel, self).mainGamePhase()
        finally:
            self.world.teams[1].abilities.set(zoneCaps=True)

    def setMainGameUserInfo(self):
        self.setUserInfo('Defence Drill', (
            '* Red players cannot capture zones',
            '* Try not to lose your zones',
        ), BOT_GOAL_CAPTURE_MAP)


if __name__ == '__main__':
    play_level(DefenceDrillLevel(), bot_count=1)
