# Trosnoth (Ubertweak Platform Game)
# Copyright (C) Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import asyncio
import contextlib

from PySide6.QtGui import QWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
import pygame

from trosnoth.gui import keyboard
from trosnoth.gui.framework.framework import Element
from trosnoth.utils.aio import single_entry_task
from trosnoth.utils.utils import wrapline
from trosnoth.welcome.nonqt import ICON_FILE


async def grab_key_from_qt_window(parent_window, prompt, title=None, hide_toplevels=True):
    grabber = PygameKeyGrabber(prompt, title=title)
    window_handle = pygame.display.get_wm_info()['window']
    qt_window = QWindow.fromWinId(window_handle)

    qt_window.setModality(Qt.WindowModality.ApplicationModal)
    qt_window.show()
    cm = hidden_qt_toplevels() if hide_toplevels else empty_context()
    try:
        with cm:
            return await grabber.run()
    finally:
        qt_window.hide()
        pygame.display.quit()


@contextlib.contextmanager
def empty_context():
    yield


@contextlib.contextmanager
def hidden_qt_toplevels():
    hidden = set()
    try:
        for toplevel in QApplication.topLevelWidgets():
            if not toplevel.isHidden():
                hidden.add(toplevel)
                toplevel.hide()

        yield
    finally:
        for toplevel in hidden:
            toplevel.show()


class PygameKeyGrabber:
    def __init__(
            self, prompt, *, foreground_colour=(64, 64, 64), background_colour=(255, 255, 255),
            padding=20, font_size=20, wrap_width=240, title=None):
        self.background_colour = background_colour
        self.padding = padding

        pygame.display.init()
        icon = pygame.image.load(str(ICON_FILE))
        pygame.display.set_icon(icon)
        pygame.font.init()

        if title is not None:
            pygame.display.set_caption(title)

        font = pygame.font.SysFont('arial', font_size)
        lines = wrapline(prompt, font, wrap_width)
        self.texts = [font.render(line, True, foreground_colour) for line in lines]
        width = max(t.get_width() for t in self.texts)
        height = sum(t.get_height() for t in self.texts)

        self.screen = pygame.display.set_mode((width + 2 * padding, height + 2 * padding))

    async def run(self):
        centre_x = self.screen.get_rect().centerx
        self.screen.fill(self.background_colour)
        top = self.padding
        for text in self.texts:
            r = text.get_rect()
            r.midtop = (centre_x, top)
            self.screen.blit(text, r)
            top += r.height
        pygame.display.flip()

        loop = asyncio.get_event_loop()
        now = loop.time()

        frame_rate = 1 / 30
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    return event.key
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        return keyboard.mouseButton(event.button)

            await asyncio.sleep(max(0, frame_rate + now - loop.time()))
            now += frame_rate


class KeyGrabberElement(Element):
    def __init__(
            self, app, prompt, *, foreground_colour=(64, 64, 64),
            background_colour=(255, 255, 255), padding=20, font_size=20, wrap_width=240,
            fade_fraction=0.5):
        super().__init__(app)
        self.showing = False
        self.future = None
        self.background_colour = background_colour
        self.padding = padding
        self.fade_alpha = round(255 * fade_fraction)

        font = pygame.font.SysFont('arial', font_size)
        lines = wrapline(prompt, font, wrap_width)
        self.texts = [font.render(line, True, foreground_colour) for line in lines]
        width = max(t.get_width() for t in self.texts)
        height = sum(t.get_height() for t in self.texts)
        self.box_rect = pygame.Rect(0, 0, width + 2 * padding, height + 2 * padding)
        self.surface = None
        self.build_surface()

    def build_surface(self):
        self.surface = pygame.Surface(self.app.screenManager.size, flags=pygame.SRCALPHA)
        self.surface.fill((128, 128, 128, self.fade_alpha))

        self.box_rect.center = self.surface.get_rect().center
        self.surface.fill(self.background_colour, self.box_rect)
        pygame.draw.rect(self.surface, (0, 0, 0), self.box_rect, 1)

        top = self.box_rect.top + self.padding
        for text in self.texts:
            r = text.get_rect()
            r.midtop = (self.box_rect.centerx, top)
            self.surface.blit(text, r)
            top += r.height

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def processEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.future.set_result(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.future.set_result(None)
            else:
                self.future.set_result(keyboard.mouseButton(event.button))
        return None

    def window_resized(self):
        self.build_surface()

    @single_entry_task
    async def show(self):
        self.future = asyncio.get_running_loop().create_future()
        self.app.screenManager.showDialog(self)
        try:
            window_handle = pygame.display.get_wm_info()['window']
            qt_window = QWindow.fromWinId(window_handle)
            qt_window.raise_()
            qt_window.requestActivate()
            with self.app.screenManager.onResize.subscribe(self.window_resized):
                return await self.future
        finally:
            self.app.screenManager.closeDialog(self)


async def grab_key(*args, **kwargs):
    try:
        return await PygameKeyGrabber(*args, **kwargs).run()
    finally:
        pygame.display.quit()


if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(
        grab_key('Please press the new key for "Move left".')))
