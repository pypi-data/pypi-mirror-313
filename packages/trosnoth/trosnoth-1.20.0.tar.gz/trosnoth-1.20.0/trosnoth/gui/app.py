import asyncio
import contextlib
import functools
import logging
import os
import time
from typing import Tuple, Optional, TypeVar, Awaitable, Callable

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

import pygame
import pygame.surface

from trosnoth.gui.sound.soundPlayer import SoundPlayer
from trosnoth.utils.event import Event
from trosnoth.utils.lifespan import LifeSpan, ContextManagerFuture
from trosnoth.utils.utils import timeNow, run_async_main_function, UIScreenRunner
from trosnoth.welcome.nonqt import hide_qt_windows, ICON_FILE

log = logging.getLogger(__name__)

TARGET_FRAME_RATE = 60.


if pygame.version.vernum < (2, 0):
    raise ImportError('Trosnoth requires pygame >= 2.0')


class JitterLogger(object):
    def __init__(self, cycle):
        self.cycle = cycle
        self.lastTime = None
        self.thisCount = 0
        self.thisMax = 0
        self.jitter = None

    def noteGap(self):
        '''
        Called to tell the JitterLogger that there is currently a gap,
        so the timing of the next observation should be discarded.
        '''
        self.lastTime = None

    def observation(self, expectedTime, resume=False):
        if resume:
            self.noteGap()

        now = timeNow()
        if self.lastTime:
            value = now - self.lastTime - expectedTime
            self.thisMax = max(self.thisMax, value)
            self.thisCount += 1

            if self.thisCount >= self.cycle:
                self.jitter = self.thisMax
                self.thisCount = 0
                self.thisMax = 0

        self.lastTime = now


class FocusManager:
    def __init__(self):
        self.focused_element = None

    def clear_focus(self):
        self.set_focus(None)

    def set_focus(self, element):
        if self.focused_element is element:
            return
        if self.focused_element:
            previous_focus = self.focused_element
            self.focused_element = None
            previous_focus.hasFocus = False
            previous_focus.lostFocus()

        self.focused_element = element
        if element:
            element.hasFocus = True
            element.gotFocus()


class MultiWindowApplication:
    '''Instantiating the Main class will set up a ui. Calling the run()
    method will run the application.'''

    def __init__(self):
        '''Initialise the application.'''
        from .screenManager import windowManager

        self.focus = FocusManager()
        self._running = False
        self._top_level = None
        self.jitterLogger = JitterLogger(cycle=60)

        self.targetFrameInterval = 1. / TARGET_FRAME_RATE
        self.soundPlayer = SoundPlayer()
        self.screenManager = windowManager.WindowManager(self)
        self.fonts = self.screenManager.fonts

        from trosnoth.gui.framework.declarative import DeclarativeRenderer
        self.declarative_renderer = DeclarativeRenderer(self)

        self.runner = UIScreenRunner()
        self.closed_future = None

    @property
    def interface(self):
        return self.screenManager.interface

    def start(self):
        if self.closed_future:
            raise RuntimeError(f'{type(self).__name__}.start() was already called')
        self.jitterLogger.noteGap()
        self._running = True
        self._top_level = AppTopLevel(self)
        self.closed_future = ContextManagerFuture()

    def stop(self):
        if self._running:
            self._top_level.stop()
            if self.runner.running:
                self.runner.done(None)
            if not self.closed_future.done():
                self.closed_future.set_result(None)
            self._running = False

    @contextlib.contextmanager
    def activate(self):
        self.start()
        try:
            yield
        finally:
            self.stop()


class AppTopLevel:
    def __init__(self, app):
        self.app = app
        self.lifespan = LifeSpan()
        pygame_runner = get_pygame_runner()
        pygame_runner.on_pygame_event.addListener(self.process_event, lifespan=self.lifespan)
        pygame_runner.on_tick.addListener(self.tick, lifespan=self.lifespan)
        pygame_runner.on_draw.addListener(self.draw, lifespan=self.lifespan)

    def stop(self):
        self.lifespan.stop()

    def process_event(self, event):
        self.app.screenManager.processEvent(event)

    def tick(self, delta_t):
        self.app.declarative_renderer.tick(delta_t)
        self.app.jitterLogger.observation(self.app.targetFrameInterval)
        self.app.screenManager.tick(delta_t)

    def draw(self, screen):
        self.app.declarative_renderer.pre_draw()
        self.app.screenManager.draw(screen)


class PygameWindowNotOpen(RuntimeError):
    pass


class UserClosedPygameWindow(asyncio.CancelledError):
    pass


class PygameWindowAlreadyOpen(RuntimeError):
    pass


T = TypeVar('T')


class PygameRunnerAPI(Protocol):
    '''
    Defines the methods and attributes of the pygame runner which should
    be used outside of the class itself.
    '''
    on_resize: Event            # ()
    on_tick: Event              # (delta_t)
    on_pygame_event: Event      # (event)
    on_draw: Event              # (surface)

    def is_showing(self) -> bool:
        '''
        :return: true iff a Pygame window is open
        '''
        raise NotImplementedError

    def is_full_screen(self) -> bool:
        '''
        :return: true iff Pygame is running in full screen mode
        '''
        raise NotImplementedError

    def get_window_size(self) -> Tuple[int, int]:
        '''
        :return: the size of the Pygame window
        :raises:
            PygameWindowNotOpen: if no Pygame window is open
        '''
        raise NotImplementedError

    async def show_window(
            self,
            coroutine: Callable[[], Awaitable[T]],
            size: Optional[Tuple[int, int]] = None,
            full_screen: Optional[bool] = None,
            scaled: Optional[bool] = None,
            grab_mouse: Optional[bool] = None,
            *,
            target_frame_rate: float = 60,
            hide_qt: bool = True,
    ) -> T:
        '''
        Shows a Pygame window, and runs an asynchronous Pygame event
        loop until either the given coroutine completes, or the Pygame
        window is closed by the user.

        :param coroutine: This will be called once the Pygame window is
            shown. Once this coroutine completes, the Pygame window will
            be closed. If the Pygame window is closed by the user before
            this coroutine completes, the coroutine will be cancelled.
        :param size: If provided, this specifies the size of the Pygame
            window. If not provided and a Pygame window has been
            previously opened by this Pygame runner, uses the previous
            window size.
        :param full_screen: If provided, controls whether the window
            will be shown in full-screen mode. Note that if full_screen
            is True and size is not a supported full-screen size, a
            suitable size will be automatically chosen.
        :param scaled: If provided, controls whether the window will be
            scaled to be visible on higher resolution monitors. May have
            no effect if full_screen is True.
        :param grab_mouse: If provided, controls whether the mouse will
            be constrained to stay within the window.
        :param target_frame_rate: This value controls the length of
            delay between each frame of the event loop. Expressed in
            units of frames per second.
        :param hide_qt: If true, hides all Qt windows until the
            Pygame window is closed.
        :return: the result of coroutine, if it completed.
        :raises:
            UserClosedPygameWindow: if the Pygame window was closed
            WindowAlreadyOpen: if a Pygame window is already open when
                this is called.
        '''
        raise NotImplementedError

    def resize_window(
            self,
            window_size: Tuple[int, int],
            full_screen: Optional[bool] = None,
            scaled: Optional[bool] = None,
            grab_mouse: Optional[bool] = None,
            from_event=False,
    ) -> None:
        '''
        Resizes the currently showing Pygame window.

        :param window_size: The new size of the window.
        :param full_screen: If provided, controls whether the window
            will be shown in full-screen mode. If not provided, the
            current value will be used.
        :param scaled: If provided, controls whether the window will be
            scaled to be visible on higher resolution monutors.
        :param grab_mouse: If provided, controls whether the mouse will
            be constrained to stay within the window.
        :param from_event: Should be True iff this call is in response
            to a VIDEORESIZE event.
        :raises:
            PygameWindowNotOpen: if the Pygame window is not open
        '''
        raise NotImplementedError

    def launch_application_with_params(
            self,
            coroutine: Callable[[], Awaitable[T]],
            size: Tuple[int, int],
            full_screen: bool,
            scaled: bool,
            grab_mouse: bool,
            *,
            target_frame_rate: float = 60,
    ) -> T:
        '''
        Shows a Pygame window, and synchronously runs the Pygame event
        loop until either the given coroutine completes, or the Pygame
        window is closed by the user.

        :param coroutine: this will be called once the Pygame window is
            shown. Once this coroutine completes, the Pygame window will
            be closed. If the Pygame window is closed by the user before
            this coroutine completes, the coroutine will be cancelled.
        :param size: the size of the Pygame window.
        :param full_screen: controls whether the window will be shown in
            full-screen mode. Note that if full_screen is true and size
            is not a supported full-screen size, a suitable size will be
            automatically chosen.
        :param scaled: controls whether the window will be scaled to be
            visible on higher resolution monitors. May have no effect
            if full_screen is True.
        :param grab_mouse: controls whether the mouse will be
            constrained to stay within the window.
        :param target_frame_rate: This value controls the length of
            delay between each frame of the event loop. Expressed in
            units of frames per second.
        :return: the result of coroutine, if it completed.
        :raises:
            UserClosedPygameWindow: if the Pygame window was closed
            WindowAlreadyOpen: if a Pygame window is already open when
                this is called.
        '''
        raise NotImplementedError

    def launch_application(
            self,
            coroutine: Callable[[], Awaitable[T]],
            *,
            target_frame_rate: float = 60,
    ) -> T:
        '''
        Same as launch_application_with_params, but loads the param
        values from the Trosnoth settings file.
        '''
        raise NotImplementedError


class PygameRunner:
    instance = None

    def __init__(self):
        self.full_screen_requested = False
        self.grab_mouse_requested = False
        self.last_screen_size = (800, 600)
        self.scaled_requested = False
        self.on_resize = Event([])
        self.on_tick = Event(['delta_t'])
        self.on_pygame_event = Event(['event'])
        self.on_draw = Event(['surface'])
        pygame.init()
        pygame.display.init()

    def is_showing(self) -> bool:
        return bool(pygame.display.get_surface())

    def is_full_screen(self) -> bool:
        if not self.is_showing():
            return False
        return self.full_screen_requested

    def get_window_size(self) -> Tuple[int, int]:
        surface = pygame.display.get_surface()
        if not surface:
            raise PygameWindowNotOpen('No Pygame window currently open')
        return surface.get_size()

    def resize_window(
            self,
            window_size: Tuple[int, int],
            full_screen: Optional[bool] = None,
            scaled: Optional[bool] = None,
            grab_mouse: Optional[bool] = None,
            from_event=False,
    ) -> None:
        if not self.is_showing():
            raise PygameWindowNotOpen('No pygame window currently open')
        if full_screen is None:
            full_screen = self.full_screen_requested
        if scaled is None:
            scaled = self.scaled_requested
        if grab_mouse is None:
            grab_mouse = self.grab_mouse_requested
        self.set_display_mode(window_size, full_screen, scaled, grab_mouse, from_event=from_event)
        self.on_resize()

    def set_display_mode(
            self, size, full_screen, scaled=False, grab_mouse=False, from_event=False):
        if from_event:
            self.last_screen_size = size
            self.full_screen_requested = full_screen
            self.scaled_requested = scaled
            self.grab_mouse_requested = grab_mouse
        if (
                size == self.last_screen_size and
                full_screen == self.full_screen_requested and
                scaled == self.scaled_requested and
                grab_mouse == self.grab_mouse_requested and
                self.is_showing()):
            return

        self.last_screen_size = size
        self.full_screen_requested = full_screen
        self.scaled_requested = scaled
        self.grab_mouse_requested = grab_mouse

        kwargs = {}
        if full_screen:
            flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        elif scaled:
            flags = pygame.SCALED  | pygame.RESIZABLE
        else:
            flags = pygame.RESIZABLE

        if pygame.vernum[0] >= 2:
            # Ask for vertical sync if possible
            kwargs['vsync'] = True

        pygame.display.init()
        self.set_default_icon()
        pygame.display.set_mode(size, flags, **kwargs)

        if grab_mouse != pygame.event.get_grab():
            pygame.event.set_grab(grab_mouse)

    def set_default_icon(self):
        icon = pygame.image.load(str(ICON_FILE))
        if os.name == 'nt':
            # On Windows, icon transparency does not work unless the
            # icon is an approved Windows icon size.
            icon = pygame.transform.smoothscale(icon, (96, 96))
        pygame.display.set_icon(icon)

    async def show_window(
            self,
            coroutine: Callable[[], Awaitable[T]],
            size: Optional[Tuple[int, int]] = None,
            full_screen: Optional[bool] = None,
            scaled: Optional[bool] = None,
            grab_mouse: Optional[bool] = None,
            *,
            target_frame_rate: float = 60,
            hide_qt: bool = True
    ) -> T:

        if self.is_showing():
            raise PygameWindowAlreadyOpen('Pygame window is already showing')

        if size is None:
            size = self.last_screen_size
        if full_screen is None:
            full_screen = self.full_screen_requested
        if scaled is None:
            scaled = self.scaled_requested
        if grab_mouse is None:
            grab_mouse = self.grab_mouse_requested
        self.set_display_mode(size, full_screen, scaled, grab_mouse)

        try:
            if hide_qt:
                with hide_qt_windows():
                    return await self._run_body(coroutine, target_frame_rate)
            else:
                return await self._run_body(coroutine, target_frame_rate)
        finally:
            pygame.display.quit()

    async def _run_body(self, coroutine, target_frame_rate):
        task_from_caller = asyncio.create_task(coroutine())
        event_loop_task = asyncio.create_task(
            self.pygame_event_loop(1 / target_frame_rate))

        done, pending = await asyncio.wait(
            [task_from_caller, event_loop_task],
            return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        if task_from_caller in done:
            return task_from_caller.result()

        raise UserClosedPygameWindow('The user closed the Pygame window')

    async def pygame_event_loop(self, target_frame_interval):
        last_time = time.monotonic()

        while True:
            now = time.monotonic()
            for event in pygame.event.get():
                try:
                    self.on_pygame_event(event)
                except Exception:
                    log.exception('Error during Pygame event processing')

                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    self.resize_window(event.size, from_event=True)

            try:
                self.on_tick(now - last_time)
            except Exception:
                log.exception('Error in tick() method')
            last_time = now

            if pygame.display.get_active():
                try:
                    self.on_draw(pygame.display.get_surface())
                except pygame.error:
                    log.exception('Error in draw()')

                pygame.display.flip()

            processing_time = time.monotonic() - now
            await asyncio.sleep(max(0.001, target_frame_interval - processing_time))

    def launch_application_with_params(
            self,
            coroutine: Callable[[], Awaitable[T]],
            size: Tuple[int, int],
            full_screen: bool,
            scaled: bool,
            grab_mouse: bool,
            *,
            target_frame_rate: float = 60,
    ) -> T:
        pygame.init()
        pygame.display.init()
        try:
            return run_async_main_function(functools.partial(
                self.show_window, coroutine, size, full_screen, scaled, grab_mouse,
                target_frame_rate=target_frame_rate, hide_qt=False))
        except asyncio.CancelledError:
            raise UserClosedPygameWindow
        finally:
            pygame.quit()

    def launch_application(
            self,
            coroutine: Callable[[], Awaitable[T]],
            *,
            target_frame_rate: float = 60,
    ) -> T:
        from trosnoth.settings import ClientSettings
        params = ClientSettings.get().display.get_video_parameters()
        return self.launch_application_with_params(
            coroutine, *params, target_frame_rate=target_frame_rate)


def get_pygame_runner() -> PygameRunnerAPI:
    '''
    :return: the global pygame runner which can be used to query or
        control the open Pygame window.
    '''
    if PygameRunner.instance is None:
        PygameRunner.instance = PygameRunner()
    return PygameRunner.instance
