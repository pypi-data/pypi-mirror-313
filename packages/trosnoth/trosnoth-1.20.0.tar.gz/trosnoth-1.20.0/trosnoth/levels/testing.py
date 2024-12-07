#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import logging

from trosnoth.levels.base import play_level
from trosnoth.levels.standard import StandardRandomLevel
from trosnoth.triggers.coins import AwardStartingCoinsTrigger

log = logging.getLogger(__name__)


class TestingLevel(StandardRandomLevel):

    allowAutoBalance = False

    async def pregameCountdownPhase(self, **kwargs):
        AwardStartingCoinsTrigger(self, coins=10000).activate()


if __name__ == '__main__':
    from trosnoth.levels.base import LevelOptions
    play_level(
        TestingLevel(), #level_options=LevelOptions(map_index=1)),
        bot_count=0,
        slow_dark_conquest=True,
    )
