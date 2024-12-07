#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

from trosnoth.levels.base import play_level
from trosnoth.levels.maps import StandardMap, SmallMap, WideMap, LargeMap
from trosnoth.levels.standard import StandardRandomLevel


class SoloRulesGame(StandardRandomLevel):
    level_code = 'solo'
    levelName = 'Solo Rules Trosnoth'
    hvm_level_name = 'HvM Solo Rules'

    default_duration = 8 * 60
    coins_for_kills_factor = 0
    coins_for_caps_factor = 0
    respawn_time_factor = 0.6
    coin_increment_factor = 3

    map_selection = (
        SmallMap(),
        WideMap(),
        StandardMap(),
        LargeMap(),
    )


if __name__ == '__main__':
    play_level(SoloRulesGame(), bot_count=1)
