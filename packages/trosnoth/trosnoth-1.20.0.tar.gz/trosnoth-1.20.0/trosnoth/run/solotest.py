import asyncio
import functools
import logging
import random
import sys

from twisted.internet import defer, reactor

from trosnoth.const import DEFAULT_BOT_DIFFICULTY
from trosnoth.game import LocalGame, RemoteGame
from trosnoth.gamerecording.replays import ReplayPlayer
from trosnoth.gui.app import get_pygame_runner, UserClosedPygameWindow
from trosnoth.manholehelper import LocalManholeHelper
from trosnoth.model.agenthub import LocalHub
from trosnoth.model.hub import Hub, Node
from trosnoth.run.common import initialise_trosnoth_app
from trosnoth.trosnothgui.ingame.gameInterface import GameInterface
from trosnoth.utils.utils import console_locals, run_in_pygame, new_console_context, clean_garbage

log = logging.getLogger(__name__)


class SoloGameClosed(Exception):
    pass


def launch_solo_game(**kwargs):
    with new_console_context():
        try:
            get_pygame_runner().launch_application(
                functools.partial(
                    launch_solo_game_async, **kwargs),
            )
        except (UserClosedPygameWindow, SoloGameClosed):
            pass


@run_in_pygame
async def launch_solo_game_async(*, return_when_level_completes=True, **kwargs):
    with initialise_trosnoth_app() as app:
        game, game_interface = build_game(app, **kwargs)
        return_value = None
        try:
            tasks = [asyncio.ensure_future(app.runner.run())]
            if return_when_level_completes:
                level_task = asyncio.ensure_future(game_interface.on_scenario_complete.wait_future())
                tasks.append(level_task)
            else:
                level_task = None

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            if level_task and level_task.done():
                return_value = level_task.result()['result']

            for task in pending:
                task.cancel()
        finally:
            game.stop()
            game_interface.stop()
            clean_garbage()
    if return_value is None:
        raise SoloGameClosed()
    return return_value


def build_game(
        app, level=None,
        isolate=False, bot_count=0, bot_class='ranger',
        map_blocks=(), test_mode=False, stack_teams=False,
        delay=None, bots_only=False, no_auto_balance=False,
        spike=None,
        game_prefix='unnamed',
        bot_difficulty=DEFAULT_BOT_DIFFICULTY,
        add_bots=(),
        save_replay=False,
        speedup=1,
        slow_dark_conquest=True,
):
    game_type = 'solo'
    game = LocalGame(
        onceOnly=True,
        level=level,
        game_type=game_type,
        gamePrefix=game_prefix,
        botProcess=True,
        bots_only=bots_only,
        no_auto_balance=no_auto_balance,
        saveReplay=save_replay,
        speedup=speedup,
        slow_dark_conquest=slow_dark_conquest,
    )
    if test_mode:
        game.world.setTestMode()

    bots = []

    try:
        for i in range(bot_count):
            if stack_teams:
                bot = game.addBot(
                    bot_class, team=game.world.teams[0], difficulty=bot_difficulty)
            else:
                bot = game.addBot(bot_class, difficulty=bot_difficulty)
            bots.append(bot)
    except ImportError:
        print('AI module not found: %s' % (bot_class,), file=sys.stderr)
        sys.exit(1)
    except AttributeError:
        print((
                'AI module does not define BotClass: %s' % (bot_class,)), file=sys.stderr)
        sys.exit(1)

    console_locals_dict = console_locals.get()

    # Create a client and an interface.
    if isolate:
        rgame = RemoteGame(smooth_remote_ticks=True)
        console_locals_dict['rgame'] = rgame
        hub = LocalHub(game)
        if delay or spike:
            delayer = DelayNodeHub(delay, spike)
            hub.connectNode(delayer)
            delayer.connectNode(rgame)
        else:
            hub.connectNode(rgame)
        gi = GameInterface(app, rgame, spectate=bots_only)
        rgame.connected(game.world.dumpEverything())
    else:
        gi = GameInterface(app, game, spectate=bots_only)
    console_locals_dict['game_interface'] = gi
    gi.on_clean_exit.addListener(app.stop)
    gi.on_lost_connection.addListener(app.stop)
    app.interface.elements.append(gi)

    for team_index, bot_specs in enumerate(add_bots):
        for bot_class, difficulty in bot_specs:
            bot = game.addBot(
                bot_class, team=game.world.teams[team_index], difficulty=difficulty)
            bots.append(bot)

    console_locals_dict.update({
        'game': game,
        'bots': bots,
        'helper': LocalManholeHelper(lambda: game),
    })
    return game, gi


class DelayNodeHub(Hub, Node):
    '''
    Delays messages by the given amount, and causes occasional delay
    spikes where nothing gets through for a second.
    '''
    SPIKE_SIZE = 1

    def __init__(self, delay, spike_interval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay = delay or 0
        self.cumulative_delay = 0
        self.spike_interval = spike_interval
        self.next_spike_time = reactor.seconds()
        self.call_queue = []

    def release_next_call(self):
        now = reactor.seconds()
        release_at, fn, args, kwargs = self.call_queue[0]
        if now >= release_at:
            self.call_queue.pop(0)

        if self.call_queue:
            reactor.callLater(max(0, self.call_queue[0][0] - now), self.release_next_call)

        if now >= release_at:
            fn(*args, **kwargs)

    def queue_call(self, fn, *args, **kwargs):
        now = reactor.seconds()
        if self.spike_interval is not None and now >= self.next_spike_time:
            delay = self.SPIKE_SIZE
            self.next_spike_time = now + (0.5 + random.random()) * self.spike_interval
        else:
            delay = self.delay

        self.call_queue.append((now + delay, fn, args, kwargs))
        if len(self.call_queue) == 1:
            reactor.callLater(delay, self.release_next_call)

    @defer.inlineCallbacks
    def connectNewAgent(self, authTag=0):
        result = yield self.hub.connectNewAgent(authTag=authTag)

        d = defer.Deferred()
        self.queue_call(d.callback, None)
        yield d

        defer.returnValue(result)

    def disconnectAgent(self, agentId):
        self.queue_call(self.hub.disconnectAgent, agentId)

    def sendRequestToGame(self, agentId, msg):
        msg.tracePoint(self, 'sendRequestToGame')
        self.queue_call(self.hub.sendRequestToGame, agentId, msg)

    def gotServerCommand(self, msg):
        msg.tracePoint(self, 'gotServerCommand')
        self.queue_call(self.node.gotServerCommand, msg)

    def gotMessageToAgent(self, agentId, msg):
        msg.tracePoint(self, 'gotMessageToAgent')
        self.queue_call(self.node.gotMessageToAgent, agentId, msg)

    def agentDisconnected(self, agentId):
        self.queue_call(self.node.agentDisconnected, agentId)


@run_in_pygame
async def launch_replay(filename):
    replayer = ReplayPlayer(filename)
    game = RemoteGame(smooth_remote_ticks=True)

    with initialise_trosnoth_app() as app:
        replayer.connectNode(game)
        game.connected(replayer.popSettings())

        game_interface = GameInterface(
            app, game, replay=True,
            on_clean_exit=app.stop)
        replayer.start()

        app.interface.elements = [game_interface]
        try:
            await app.runner.run()
        finally:
            replayer.stop()
            game_interface.stop()
            clean_garbage()
