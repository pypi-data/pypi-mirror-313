# Workaround for pyinstaller app to avoid ReactorAlreadyInstalledError
# See https://github.com/kivy/kivy/issues/4182#issuecomment-253159955
import sys

if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor']

# Install the asyncio reactor as early as possible
from trosnoth.qtreactor import install_async_qt_reactor
install_async_qt_reactor()

import functools
import os
from argparse import ArgumentParser

from trosnoth.levels.base import LevelOptions
from trosnoth.levels.maps import CustomStandardMap
from trosnoth.levels.standard import StandardRandomLevel
from trosnoth.run.main import launch_trosnoth
from trosnoth.run.solotest import launch_solo_game
from trosnoth.utils.utils import initLogging


def makeOptionParser():
    parser = ArgumentParser()
    parser.add_argument('replay_file', nargs='?', help='watch the given replay file')
    parser.add_argument(
        '-s', '--solo', action='store_const', dest='mode',
        const='solo', default='normal',
        help='run Trosnoth in solo mode.')
    parser.add_argument(
        '-i', '--isolate', action='store_const', dest='mode', const='isolate',
        help='run Trosnoth in isolated test mode. Creates client and server '
        'Universe objects, but does not use the network to connect them.')
    parser.add_argument(
        '-D', '--delay', action='store', dest='delay', type=float,
        help='implies --isolate. Adds a delay between client and server.')
    parser.add_argument(
        '--spike', action='store', dest='spike', type=float,
        help='implies --isolate. Adds a 1s delay spike at intervals.')
    parser.add_argument(
        '--trosball', action='store_const', dest='mode', const='trosball',
        help='run a solo Trosball game.')
    parser.add_argument(
        '-t', '--test', action='store_true', dest='testMode',
        help='run Trosnoth in test mode. This means that players will get 20 '
        'coins each and upgrades will only cost 1 coin.')
    parser.add_argument(
        '-b', '--testblock', action='store', dest='mapBlock',
        help='tests the map block with the given filename.')
    parser.add_argument(
        '-a', '--botcount', action='store', dest='bot_count', type=int,
        help='the number of AIs to include.')
    parser.add_argument(
        '-w', '--halfwidth', action='store', dest='half_width', type=int,
        help='the half map width')
    parser.add_argument(
        '-H', '--height', action='store', dest='height', type=int, help='the map height')
    parser.add_argument(
        '-m', '--duration', action='store', dest='duration', default=0,
        type=int, help='game duration in minutes')
    parser.add_argument(
        '-S', '--stack-teams', action='store_true', dest='stackTeams',
        help='stack all the AI players on one team.')
    parser.add_argument(
        '-A', '--botclass', action='store', dest='bot_class',
        help='the name of the module to import from trosnoth.bots.')
    parser.add_argument(
        '--list-bots', action='store_const', dest='mode',
        const='listbots', help='list available bot classes and exit')
    parser.add_argument(
        '-d', '--debug', action='store_true', dest='debug',
        help='show debug-level messages on console')
    parser.add_argument(
        '-p', '--profile', action='store_true', dest='profile',
        help='dump kcachegrind profiling data to trosnoth.log')
    parser.add_argument(
        '-r', '--log-reactor-calls', action='store_true',
        dest='log_reactor_calls', help='logs slow reactor calls')
    parser.add_argument(
        '-P', '--profile-reactor-calls', action='store_true',
        dest='profile_reactor_calls', help='profiles slow reactor calls')
    parser.add_argument(
        '-l', '--log-file', action='store', dest='logFile',
        help='file to write logs to')
    return parser


def list_bots():
    import trosnoth.bots.base
    print('Available bot classes:', file=sys.stderr)
    for name in trosnoth.bots.base.get_available_bot_names(show_all=True):
        print('  %s' % (name,), file=sys.stderr)
    return


TESTMODE_AI_COUNT = 7
TESTMODE_HALF_WIDTH = 1
TESTMODE_HEIGHT = 1
BLOCKTEST_HALF_WIDTH = 2
BLOCKTEST_HEIGHT = 1


def processOptions(options, parser):
    if options.mode == 'normal' and (
            options.testMode or options.mapBlock or
            options.bot_count or options.half_width or options.height or
            options.stackTeams or options.bot_class or options.duration):
        options.mode = 'solo'

    if options.bot_class is None:
        options.bot_class = 'ranger'

    if options.mode in ('solo', 'isolate', 'trosball'):
        isolate = options.mode == 'isolate' or options.delay or options.spike
        trosball = options.mode == 'trosball'
        options.mode = 'solo'
        if options.mapBlock is None:
            mapBlocks = []
            bot_count = options.bot_count or TESTMODE_AI_COUNT
            half_width = options.half_width or TESTMODE_HALF_WIDTH
            height = options.height or TESTMODE_HEIGHT
        else:
            mapBlocks = [options.mapBlock]
            bot_count = options.bot_count or 0
            half_width = options.half_width or BLOCKTEST_HALF_WIDTH
            height = options.height or BLOCKTEST_HEIGHT

        if trosball:
            from trosnoth.levels.trosball import RandomTrosballLevel
            if not options.duration:
                options.duration = 15
            level = RandomTrosballLevel(
                map_=CustomStandardMap(half_width, height),
                level_options=LevelOptions(duration=options.duration * 60))
        else:
            level = StandardRandomLevel(
                map_=CustomStandardMap(half_width, height),
                level_options=LevelOptions(duration=options.duration * 60))
        options.solo_args = dict(
            isolate=isolate, test_mode=options.testMode,
            map_blocks=mapBlocks,
            bot_count=int(bot_count),
            stack_teams=options.stackTeams, bot_class=options.bot_class,
            delay=options.delay, spike=options.spike,
            level=level,
        )

    elif options.mode not in ('normal', 'listbots'):
        assert False, 'Unknown mode {!r}'.format(options.mode)


def main():
    parser = makeOptionParser()

    options = makeOptionParser().parse_args()
    if options.replay_file and not os.path.exists(options.replay_file):
        parser.error(f'Replay file not found: {options.replay_file}')

    initLogging(options.debug, options.logFile)

    processOptions(options, parser)

    if options.mode == 'listbots':
        list_bots()
        return

    if options.mode == 'normal':
        main_function = functools.partial(launch_trosnoth, show_replay=options.replay_file)
    elif options.mode == 'solo':
        main_function = functools.partial(launch_solo_game, **options.solo_args)
    else:
        assert False, 'Unknown mode'

    if options.log_reactor_calls or options.profile_reactor_calls:
        from trosnoth.utils import twistdebug
        twistdebug.start(profiling=options.profile_reactor_calls)

    if options.profile:
        profile_call(main_function)
    else:
        main_function()


def profile_call(fn, *args, **kwargs):
    from trosnoth.utils.profiling import profilingOutput
    with profilingOutput('trosnoth.log'):
        return fn(*args, **kwargs)


if __name__ == '__main__':
    main()
