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

from trosnoth import qtreactor
qtreactor.declare_this_module_requires_qt_reactor()

import asyncio
import logging

from PySide6.QtGui import QTextBlockFormat, QTextCharFormat
from PySide6.QtWidgets import QWidget, QFileDialog, QTextEdit
from PySide6.QtCore import QEvent, Qt, QPropertyAnimation
from twisted.internet import reactor
from twisted.web.client import Agent, readBody, RedirectAgent

from trosnoth import data
from trosnoth import version
from trosnoth.gamerecording.gamerecorder import REPLAY_DIR
from trosnoth.gamerecording.replays import IncompatibleReplayVersion
from trosnoth.music import get_music_player
from trosnoth.run.solotest import launch_replay
from trosnoth.utils.aio import as_future
from trosnoth.utils.utils import run_async_main_function, UIScreenRunner
from trosnoth.welcome.common import (
    initialise_qt_application, load_ui_file, EventFilter,
)
from trosnoth.welcome.messageviewer import WelcomeScreenMessageViewer
from trosnoth.welcome.nonqt import (
    async_callback, HasAsyncCallbacks,
    run_callback_in_async_loop,
    STOP_IMAGE_FILE,
)
from trosnoth.welcome.play import PlayScreen
from trosnoth.welcome.settings import SettingsScreen
from trosnoth.welcome.tutorials import TutorialsScreen

log = logging.getLogger(__name__)

CREDITS_FILE = data.base_path / 'welcome' / 'credits.txt'
WELCOME_UI_FILE = data.base_path / 'welcome' / 'welcome.ui'
BACKGROUND_FILE = data.base_path / 'welcome' / 'background.png'
KLEPTOCRACY_FONT_FAMILY = 'Kleptocracy'
JUNCTION_FONT_FAMILY = 'Junction'


class WelcomeScreen(HasAsyncCallbacks):
    def __init__(self):
        super().__init__()

        self.main_stack = None
        self.welcome_page = None
        self.credits_page = None
        self.credits_slider = None
        self.credits_animation = None
        self.event_filter = None
        self.new_version_label = None

        self.window = self._build_window()
        self.message_viewer = WelcomeScreenMessageViewer(self.window)
        self.tutorials_screen = TutorialsScreen(self)
        self.play_screen = PlayScreen(self)
        self.screen_runner = UIScreenRunner()

    def _build_window(self):
        window = load_ui_file(WELCOME_UI_FILE, {
            'welcome_form': {
                QEvent.Close: self.form_close_event,
            },
            'credits_text': {
                QEvent.KeyPress: self.ignore_event,
            },
        })

        background = window.findChild(QWidget, 'background')
        background.set_background(BACKGROUND_FILE)

        window.findChild(QWidget, 'exit_button').clicked.connect(
            run_callback_in_async_loop(window.close))
        window.findChild(QWidget, 'replay_button').clicked.connect(
            run_callback_in_async_loop(self.replay_clicked))
        window.findChild(QWidget, 'credits_button').clicked.connect(
            run_callback_in_async_loop(self.credits_clicked))
        window.findChild(QWidget, 'credits_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'settings_button').clicked.connect(
            run_callback_in_async_loop(self.settings_clicked))
        window.findChild(QWidget, 'tutorials_button').clicked.connect(
            run_callback_in_async_loop(self.tutorials_clicked))
        window.findChild(QWidget, 'play_button').clicked.connect(
            run_callback_in_async_loop(self.play_clicked))

        credits_text = window.findChild(QWidget, 'credits_text')
        self.load_credits(credits_text)

        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.welcome_page = window.findChild(QWidget, 'welcome_page')
        self.credits_page = window.findChild(QWidget, 'credits_page')
        self.credits_slider = credits_text.verticalScrollBar()

        self.event_filter = EventFilter({QEvent.Wheel: self.ignore_event})
        self.credits_slider.installEventFilter(self.event_filter)

        self.new_version_label = window.findChild(QWidget, 'new_version_label')
        self.new_version_label.hide()

        window.findChild(QWidget, 'version').setText(version.title_version)

        return window

    def ignore_event(self, obj, event):
        return True

    def load_credits(self, text_edit: QTextEdit):
        text_edit.clear()

        centred = QTextBlockFormat()
        centred.setAlignment(Qt.AlignHCenter)
        centred.setLineHeight(150, QTextBlockFormat.ProportionalHeight.value)

        heading1 = QTextCharFormat()
        heading1.setFontFamily(KLEPTOCRACY_FONT_FAMILY)
        heading1.setFontPointSize(45)

        heading2 = QTextCharFormat()
        heading2.setFontFamily(KLEPTOCRACY_FONT_FAMILY)
        heading2.setFontPointSize(36)

        paragraph = QTextCharFormat()
        paragraph.setFontFamily(JUNCTION_FONT_FAMILY)
        paragraph.setFontPointSize(18)

        for i in range(4):
            text_edit.textCursor().insertBlock(centred, heading1)

        with open(CREDITS_FILE, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('!!'):
                    line = line[len('!!'):]
                    style = heading1
                elif line.startswith('!'):
                    line = line[len('!'):]
                    style = heading2
                else:
                    style = paragraph
                text_edit.textCursor().insertBlock(centred, style)
                text_edit.textCursor().insertText(line)

        for i in range(6):
            text_edit.textCursor().insertBlock(centred, heading1)

    def credits_clicked(self):
        self.main_stack.setCurrentWidget(self.credits_page)
        self.credits_slider.setValue(0)

        self.credits_animation = QPropertyAnimation(self.credits_slider, b'value')
        self.credits_animation.setDuration(50 * 1000)
        self.credits_animation.setStartValue(self.credits_slider.minimum())
        self.credits_animation.setEndValue(self.credits_slider.maximum())
        self.credits_animation.start()

    def back_clicked(self):
        if self.credits_animation:
            self.credits_animation.stop()
            self.credits_animation = None
        self.main_stack.setCurrentWidget(self.welcome_page)

    @async_callback
    async def settings_clicked(self):
        # Keep the SettingsScreen as a local variable to prevent it
        # being garbage collected during screen.run().
        screen = SettingsScreen()
        await screen.run()

    @async_callback
    async def tutorials_clicked(self):
        await self.tutorials_screen.run()

    @async_callback
    async def play_clicked(self):
        await self.play_screen.run()

    @async_callback
    async def replay_clicked(self):
        dialog = FileChooserDialog(
            self.window,
            caption='Select replay file',
            accept_label='Watch',
            filetypes=(
                ('Trosnoth replays', '*.trosrepl'),
                ('All files', '*'),
            ),
            start_directory=REPLAY_DIR if REPLAY_DIR.is_dir() else None,
        )
        replay_filename = await dialog.run()
        if replay_filename is not None:
            await launch_replay(replay_filename)

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

    def form_close_event(self, obj, event):
        # Sometimes on Windows, Qt events interrupt running code
        loop = asyncio.get_running_loop()
        @loop.call_soon_threadsafe
        def this_runs_in_the_async_event_loop():
            self.screen_runner.done(None)
            self.async_manager.cancel_all()
        return False

    async def run(self, show_replay=None):
        with get_music_player().run():
            self.window.show()
            if show_replay:
                self.async_manager.start_coroutine(self.launch_replay(show_replay))
            self.async_manager.start_coroutine(self.check_latest_stable_release())
            await self.screen_runner.run()

    async def check_latest_stable_release(self):
        try:
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
            self.new_version_label.show()


class FileChooserDialog:
    def __init__(
            self, parent, *, caption='', filetypes=(), accept_label=None, cancel_label=None,
            start_directory=None):
        self.dialog = QFileDialog(parent)
        self.screen_runner = UIScreenRunner(self.dialog.show)

        self.dialog.setModal(True)
        self.dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        if start_directory:
            self.dialog.setDirectory(str(start_directory))
        self.dialog.fileSelected.connect(
            run_callback_in_async_loop(self.file_selected))
        self.dialog.finished.connect(
            run_callback_in_async_loop(self.finished))

        if caption:
            self.dialog.setWindowTitle(caption)
        if filetypes:
            self.dialog.setNameFilters([f'{desc} ({glob})' for desc, glob in filetypes])
        if accept_label:
            self.dialog.setLabelText(QFileDialog.Accept, accept_label)
        if cancel_label:
            self.dialog.setLabelText(QFileDialog.Reject, cancel_label)

    def file_selected(self, filename):
        self.screen_runner.done(filename)

    def finished(self, result):
        if self.screen_runner.running:
            self.screen_runner.done(None)

    def run(self):
        return self.screen_runner.run()


async def async_main():
    initialise_qt_application()

    welcome_screen = WelcomeScreen()
    await welcome_screen.run()


if __name__ == '__main__':
    run_async_main_function(async_main)
