import asyncio
import contextlib
import logging

import pygame

from trosnoth.data import get_overridable_path
from trosnoth.gui.app import MultiWindowApplication, get_pygame_runner
from trosnoth.gui.framework.framework import CompoundElement
from trosnoth.settings import ClientSettings
from trosnoth.themes import Theme
from trosnoth.utils.lifespan import LifeSpan

log = logging.getLogger(__name__)

CURSOR_HOTSPOT = (16, 16)


def load_cursor_image():
    return pygame.image.load(get_overridable_path('sprites/cursor.png'))


@contextlib.contextmanager
def initialise_trosnoth_app(interface=CompoundElement, game_title='Trosnoth'):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(CURSOR_HOTSPOT, load_cursor_image()))
    pygame.display.set_caption(game_title)
    pygame.key.set_repeat(300, 30)

    app = TrosnothApp()
    app.screenManager.set_interface(interface(app))

    listener = TrosnothAppEventListener(app)
    listener.apply_all()

    with app.activate():
        with listener.subscribe():
            yield app


class TrosnothAppEventListener:
    def __init__(self, app):
        self.app = app
        self.lifespan = LifeSpan()
        self._pending_screen_resize = None

    @contextlib.contextmanager
    def subscribe(self):
        self._subscribe()
        try:
            yield
        finally:
            self._unsubscribe()

    def apply_all(self):
        self.apply_audio_settings()
        self.apply_display_settings()

    def _subscribe(self):
        self.app.settings.display.on_change.addListener(
            self.apply_display_settings, lifespan=self.lifespan)
        self.app.settings.audio.on_change.addListener(
            self.apply_audio_settings, lifespan=self.lifespan)
        self.app.screenManager.onResize.addListener(self.screen_resized, lifespan=self.lifespan)

        # Keep self alive so that event handlers aren't garbage collected
        self.app.__event_listener = self

    def _unsubscribe(self):
        self.lifespan.stop()
        if self.app.__event_listener is self:
            self.app.__event_listener = None

    def screen_resized(self):
        if self._pending_screen_resize:
            self._pending_screen_resize.cancel()
        self._pending_screen_resize = asyncio.get_running_loop(
            ).call_later(1, self.screen_resize_finished)

    def screen_resize_finished(self):
        self._pending_screen_resize = None
        if self.app.screenManager.isFullScreen():
            return
        self.app.settings.display.size = self.app.screenManager.size
        self.app.settings.save()

    def apply_audio_settings(self):
        audio_settings = self.app.settings.audio
        self.app.soundPlayer.set_sfx_volume(
            audio_settings.sound_volume / 100 if audio_settings.sound_enabled else 0)
        self.app.soundPlayer.set_crowd_master_volume(
            audio_settings.crowd_volume / 100 if audio_settings.crowd_enabled else 0)

    def apply_display_settings(self):
        display_settings = self.app.settings.display
        get_pygame_runner().resize_window(*display_settings.get_video_parameters())


class TrosnothApp(MultiWindowApplication):
    def __init__(self):
        super().__init__()
        self.settings = ClientSettings.get()
        self.theme = Theme(self)
        self.theme.sprites.precache()
