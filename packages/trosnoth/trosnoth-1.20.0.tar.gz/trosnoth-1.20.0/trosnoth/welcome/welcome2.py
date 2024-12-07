from trosnoth.qtreactor import declare_this_module_requires_asyncio_reactor

declare_this_module_requires_asyncio_reactor()

from dataclasses import dataclass
import logging

from twisted.internet import reactor
from twisted.web.client import Agent, readBody, RedirectAgent

from trosnoth import version
from trosnoth.gamerecording.replays import IncompatibleReplayVersion
from trosnoth.gui.framework.declarative import (
    DeclarativeElement, ComplexDeclarativeThing,
    Rectangle, Text,
)
from trosnoth.gui.framework import framework
from trosnoth.music import get_music_player
from trosnoth.run.common import initialise_trosnoth_app
from trosnoth.run.solotest import launch_replay
from trosnoth.welcome.nonqt import HasAsyncCallbacks, TUTOR_IMAGE_FILE, STOP_IMAGE_FILE
from trosnoth.utils.aio import as_future
from trosnoth.utils.lifespan import ContextManagerFuture

log = logging.getLogger(__name__)


class DummyMessageViewer:
    async def run(self, message, ok_text='got it!', back_text='back', image=TUTOR_IMAGE_FILE):
        print(message)


class WelcomeScreen(HasAsyncCallbacks):
    def __init__(self):
        super().__init__()

        self.message_viewer = DummyMessageViewer()
        self.completed_future = None

    async def launch_replay(self, replay_filename):
        try:
            await launch_replay(replay_filename)
        except IncompatibleReplayVersion as e:
            await self.message_viewer.run(
                'Unable to open replay file.\n\n'
                f'The replay was created in an incompatible Trosnoth version ({e}).',
                ok_text='ok',
                image=STOP_IMAGE_FILE,
            )

    async def run(self, app, *, show_replay=None):
        if self.completed_future:
            raise RuntimeError('WelcomeScreen.run() has already been called once')

        if show_replay:
            self.async_manager.start_coroutine(self.launch_replay(show_replay))
        self.async_manager.start_coroutine(self.check_latest_stable_release())

        with app.interface.show_element(
                DeclarativeElement(app, (0, 0), MiddleThing()),
                DeclarativeElement(app, (1, 1), VersionNumberDisplay())):

            self.completed_future = ContextManagerFuture()
            with app.closed_future.subscribe(
                    lambda f: self.completed_future.cancel('App closed')):
                return await self.completed_future

    async def check_latest_stable_release(self):
        try:
            # noinspection PyTypeChecker
            agent = RedirectAgent(Agent(reactor))
            response = await as_future(
                agent.request(b'GET', b'https://trosnoth.org/stable-version.txt'))
            stable_version = await as_future(readBody(response))
        except Exception as e:
            log.warning(f'Failed to check trosnoth.org for stable version: {e}')
            return
        stable_version = stable_version.decode('utf-8').strip()
        try:
            newer_version_exists = version.running_version_is_older(stable_version)
        except ValueError as e:
            log.warning(f'Unable to compare version numbers: {e}')
            return

        if newer_version_exists:
            pass
            # TODO
            # self.new_version_label.show()


@dataclass(frozen=True)
class MiddleThing(ComplexDeclarativeThing):
    def draw(self, frame, state):
        frame.add(Rectangle(
            width=600,
            height=50,
            colour=(208, 200, 192, 192),
        ))
        frame.add(Text(
            'Hello there!',
            height=20,
            font='Junction.ttf',
            text_colour=(0, 0, 0),
            max_width=580,
            align=Text.A_center,
        ), at=(0, 0))


@dataclass(frozen=True)
class VersionNumberDisplay(ComplexDeclarativeThing):
    def draw(self, frame, state):
        frame.add(Text(
            'Hello there!',
            height=16,
            font='FreeSans.ttf',
            text_colour=(136, 136, 136),
            align=Text.A_right,
        ))


class WhiteBackground(framework.Element):
    def draw(self, screen):
        screen.fill((255, 255, 255))


async def async_main():
    welcome_screen = WelcomeScreen()
    with get_music_player().run(), initialise_trosnoth_app() as app:
        with app.interface.show_element(WhiteBackground(app)):
            await welcome_screen.run(app)


if __name__ == '__main__':
    from trosnoth.gui.app import get_pygame_runner, UserClosedPygameWindow

    try:
        get_pygame_runner().launch_application(async_main)
    except UserClosedPygameWindow:
        pass
