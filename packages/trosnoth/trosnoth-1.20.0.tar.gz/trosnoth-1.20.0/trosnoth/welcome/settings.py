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
import functools

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QStyle, QTableWidgetItem, QMessageBox,
    QCheckBox, QComboBox,
)

from trosnoth import data, keymap
from trosnoth.const import (
    ACTION_JUMP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT, ACTION_HOOK,
    ACTION_EMOTE, ACTION_USE_UPGRADE, ACTION_SHOW_TRAJECTORY, ACTION_READY,
    ACTION_CLEAR_UPGRADE, ACTION_BUY_AMMO, ACTION_PAUSE_GAME,
    ACTION_TERMINAL_TOGGLE, ACTION_MAIN_MENU, ACTION_CHAT, ACTION_FOLLOW,
    ACTION_RADIAL_UPGRADE_MENU, ACTION_NEXT_WEAPON, ACTION_PREVIOUS_WEAPON,
    ACTION_CONTRIBUTE_TO_TEAM_BOOST, ACTION_NEXT_TEAM_BOOST, ACTION_TOGGLE_FULLSCREEN,
    ACTION_GUN_SLOT_1, ACTION_GUN_SLOT_2, ACTION_GUN_SLOT_3, ACTION_GUN_SLOT_4, ACTION_GUN_SLOT_5,
)
from trosnoth.gui import keyboard
from trosnoth.model.upgrades import allUpgrades, gun_types
from trosnoth.settings import ClientSettings
from trosnoth.utils.utils import parse_server_string, run_async_main_function, UIScreenRunner
from trosnoth.welcome import keygrab
from trosnoth.welcome.common import (
    initialise_qt_application, load_ui_file, message_box,
)
from trosnoth.welcome.nonqt import (
    async_callback, HasAsyncCallbacks,
    run_callback_in_async_loop,
)


SETTINGS_UI_FILE = data.base_path / 'welcome' / 'settings.ui'

ACTION_SEQUENCE = [
    ('Jump', ACTION_JUMP),
    ('Drop down', ACTION_DOWN),
    ('Move left', ACTION_LEFT),
    ('Move right', ACTION_RIGHT),
    ('Grappling hook', ACTION_HOOK),
    ('Next Weapon', ACTION_NEXT_WEAPON),
    ('Previous Weapon', ACTION_PREVIOUS_WEAPON),
    ('Buy Ammo', ACTION_BUY_AMMO),
    ('Gun slot 1', ACTION_GUN_SLOT_1),
    ('Gun slot 2', ACTION_GUN_SLOT_2),
    ('Gun slot 3', ACTION_GUN_SLOT_3),
    ('Gun slot 4', ACTION_GUN_SLOT_4),
    ('Gun slot 5', ACTION_GUN_SLOT_5),
]
ACTION_SEQUENCE.extend((u.name, u.action) for u in gun_types)
ACTION_SEQUENCE.extend([
    ('Taunt', ACTION_EMOTE),
    ('Select upgrade', ACTION_RADIAL_UPGRADE_MENU),
    ('Activate upgrade', ACTION_USE_UPGRADE),
    ('Contribute to team boost', ACTION_CONTRIBUTE_TO_TEAM_BOOST),
    ('Show next team boost', ACTION_NEXT_TEAM_BOOST),
])
ACTION_SEQUENCE.extend((u.name, u.action) for u in sorted(allUpgrades, key=lambda u: u.sort_order))
ACTION_SEQUENCE.extend([
    ('Deselect upgrade', ACTION_CLEAR_UPGRADE),
    ('Show trajectory', ACTION_SHOW_TRAJECTORY),
    ('Toggle ready', ACTION_READY),
    ('Toggle terminal', ACTION_TERMINAL_TOGGLE),
    ('Pause (server)', ACTION_PAUSE_GAME),
    ('Toggle main menu', ACTION_MAIN_MENU),
    ('Chat', ACTION_CHAT),
    ('Auto pan (replay)', ACTION_FOLLOW),
    ('Toggle fullscreen', ACTION_TOGGLE_FULLSCREEN),
])


class KeyboardSettingsEditor:
    '''
    There's a fair bit of logic involved in storing and updating the
    keyboard settings within the settings form. This class exists to
    manage all this, so as to keep the other classes neater.
    '''

    def __init__(self, grab_key, window):
        self.grab_key = grab_key
        self.controls_table = window.findChild(QWidget, 'controls_table')
        self.key_mapping = keyboard.KeyboardMapping(keymap.default_game_keys)
        self.key_mapping.load()
        self.action_names = {}
        self.index_by_action = {}
        self.set_up_table()

    def save(self):
        self.key_mapping.save()

    def set_up_table(self):
        self.action_names = {}
        self.index_by_action = {}
        self.controls_table.setRowCount(len(ACTION_SEQUENCE))

        for i, (display_name, action) in enumerate(ACTION_SEQUENCE):
            self.action_names[action] = display_name
            self.index_by_action[action] = i
            try:
                key = self.key_mapping.getkey(action)
            except KeyError:
                display_key = ''
            else:
                display_key = keyboard.shortcutName(key)

            label = QTableWidgetItem(display_name)
            label.setTextAlignment(Qt.AlignCenter)
            self.controls_table.setItem(i, 0, label)

            key_label = QTableWidgetItem(display_key)
            key_label.setTextAlignment(Qt.AlignCenter)
            self.controls_table.setItem(i, 1, QTableWidgetItem(key_label))

    def refresh_table(self):
        for i, (display_name, action) in enumerate(ACTION_SEQUENCE):
            try:
                key = self.key_mapping.getkey(action)
            except KeyError:
                display_key = ''
            else:
                display_key = keyboard.shortcutName(key)
            self.controls_table.item(i, 1).setText(display_key)

    def restore_default_controls(self, *args):
        self.key_mapping = keyboard.KeyboardMapping(keymap.default_game_keys)
        self.refresh_table()

    async def edit_key(self, window, row_index=-1):
        if row_index < 0:
            row_index = self.controls_table.currentRow()

        display_name, action = ACTION_SEQUENCE[row_index]
        try:
            old_key = self.key_mapping.getkey(action)
        except KeyError:
            old_key = None

        key = await self.grab_key(
            window, f'Press new key or mouse button for "{display_name}".',
            'Trosnoth :: Press new key')
        if key is None:
            return

        display_key = keyboard.shortcutName(key)
        existing_action = self.key_mapping.get(key, action)
        if existing_action != action:
            existing_action_name = self.action_names.get(existing_action, 'unknown action')
            result = await message_box(
                QMessageBox.Question, QMessageBox.Ok | QMessageBox.Cancel,
                f'The key "{display_key}" is currently assigned to "{existing_action_name}". '
                f'If you continue, it will be remapped to "{display_name}" instead.',
                title='Replace existing key?'
            )
            if result != QMessageBox.StandardButton.Ok:
                return

            self.clear_key_assignment(existing_action)

        if old_key:
            del self.key_mapping[old_key]
        self.key_mapping[key] = action
        self.controls_table.item(row_index, 1).setText(display_key)

    def clear_key_assignment(self, action):
        if action not in self.index_by_action:
            return
        index = self.index_by_action[action]
        self.controls_table.item(index, 1).setText('')


class ServersEditor:
    '''
    Encapsulates logic related to editing the servers table.
    '''
    def __init__(self, window):
        self.servers_table = window.findChild(QWidget, 'servers_table')
        self.servers_table.itemChanged.connect(
            run_callback_in_async_loop(self.item_changed))
        self.item_values = []
        self.server_credentials = {}
        self.logged_out_servers = set()
        self.loaded = False

        window.findChild(QWidget, 'delete_server_button').clicked.connect(
            run_callback_in_async_loop(self.delete_server))
        window.findChild(QWidget, 'add_server_button').clicked.connect(
            run_callback_in_async_loop(self.add_server))
        window.findChild(QWidget, 'log_out_server_button').clicked.connect(
            run_callback_in_async_loop(self.log_out_server))

    def item_changed(self, item):
        if not self.loaded:
            return
        if item.column() != 0:
            return

        new_value = item.text()
        try:
            parse_server_string(new_value)
        except ValueError:
            item.setText(self.item_values[item.row()])
        else:
            self.refresh_username(item.row())

    def delete_server(self):
        current_row = self.servers_table.currentRow()
        if current_row < 0:
            return
        del self.item_values[current_row]
        self.servers_table.removeRow(current_row)

    def add_server(self):
        self.item_values.append('')
        self.servers_table.setRowCount(len(self.item_values))
        row = len(self.item_values) - 1

        server_item = QTableWidgetItem()
        self.servers_table.setItem(row, 0, server_item)

        username_item = QTableWidgetItem()
        username_item.setTextAlignment(Qt.AlignCenter)
        username_item.setFlags(username_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.servers_table.setItem(row, 1, username_item)
        self.refresh_username(row)

    def log_out_server(self):
        current_row = self.servers_table.currentRow()
        if current_row < 0:
            return
        server = self.item_values[current_row]
        self.logged_out_servers.add(server)
        self.refresh_username(current_row)

    def refresh_username(self, row):
        server = self.item_values[row]
        if server in self.logged_out_servers:
            username = '—'
        else:
            try:
                username = self.server_credentials[server].username
            except KeyError:
                username = '—'
        self.servers_table.item(row, 1).setText(username)

    def load(self, connection_settings):
        self.item_values = list(connection_settings.servers)
        self.server_credentials = dict(connection_settings.server_credentials)
        self.servers_table.setRowCount(len(self.item_values))

        for i, server_string in enumerate(self.item_values):
            server_item = QTableWidgetItem(server_string)
            self.servers_table.setItem(i, 0, server_item)

            username_item = QTableWidgetItem()
            username_item.setFlags(username_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.servers_table.setItem(i, 1, username_item)
            self.refresh_username(i)

        self.loaded = True

    def save(self, connection_settings):
        servers = []
        for i in range(self.servers_table.rowCount()):
            server = self.servers_table.item(i, 0).text()
            if server:
                servers.append(server)
        connection_settings.servers = tuple(servers)

        for server in self.logged_out_servers:
            try:
                del connection_settings.server_credentials[server]
            except KeyError:
                pass


class SettingsSaverAndLoader:
    def __init__(self, settings=None):
        if settings is None:
            settings = ClientSettings.get()
        self.settings = settings
        self.detail_slider = None
        self.fullscreen_checkbox = None
        self.upscale_checkbox = None
        self.grab_mouse_checkbox = None
        self.show_range_checkbox = None
        self.show_timings_checkbox = None
        self.disable_buttons_checkbox = None
        self.show_experimental_checkbox = None
        self.resolution_combobox = None
        self.music_checkbox = None
        self.music_slider = None
        self.sfx_checkbox = None
        self.sfx_slider = None
        self.crowd_checkbox = None
        self.crowd_slider = None
        self.servers_editor = None

    def load_values(self, screen, window):
        display_settings = self.settings.display
        self.detail_slider = window.findChild(QWidget, 'detail_slider')
        self.detail_slider.setValue(
            display_settings.DETAIL_LEVELS.index(display_settings.detail_level))
        self.fullscreen_checkbox = window.findChild(QWidget, 'fullscreen_checkbox')
        self.fullscreen_checkbox.setChecked(display_settings.full_screen)
        self.upscale_checkbox = window.findChild(QWidget, 'upscale_checkbox')
        self.upscale_checkbox.setChecked(display_settings.upscale)
        self.grab_mouse_checkbox = window.findChild(QWidget, 'grab_mouse_checkbox')
        self.grab_mouse_checkbox.setChecked(display_settings.grab_mouse)
        self.show_range_checkbox = window.findChild(QWidget, 'show_range_checkbox')
        self.show_range_checkbox.setChecked(display_settings.show_range)
        self.show_timings_checkbox = window.findChild(QWidget, 'show_timings_checkbox')
        self.show_timings_checkbox.setChecked(display_settings.show_timings)
        self.disable_buttons_checkbox = window.findChild(QWidget, 'disable_buttons_checkbox')
        self.disable_buttons_checkbox.setChecked(display_settings.disable_shop_buttons)
        self.show_experimental_checkbox = window.findChild(QWidget, 'show_experimental_checkbox')
        self.show_experimental_checkbox.setChecked(display_settings.show_experimental)

        self.resolution_combobox = window.findChild(QWidget, 'resolution_combobox')
        self.load_resolution_combobox(display_settings)

        audio_settings = self.settings.audio
        self.music_checkbox = window.findChild(QWidget, 'music_checkbox')
        self.music_checkbox.setChecked(audio_settings.music_enabled)
        self.music_slider = window.findChild(QWidget, 'music_slider')
        self.music_slider.setEnabled(audio_settings.music_enabled)
        self.music_slider.setValue(audio_settings.music_volume)
        self.sfx_checkbox = window.findChild(QWidget, 'sfx_checkbox')
        self.sfx_checkbox.setChecked(audio_settings.sound_enabled)
        self.sfx_slider = window.findChild(QWidget, 'sfx_slider')
        self.sfx_slider.setEnabled(audio_settings.sound_enabled)
        self.sfx_slider.setValue(audio_settings.sound_volume)
        self.crowd_checkbox = window.findChild(QWidget, 'crowd_checkbox')
        self.crowd_checkbox.setChecked(audio_settings.crowd_enabled)
        self.crowd_slider = window.findChild(QWidget, 'crowd_slider')
        self.crowd_slider.setEnabled(audio_settings.crowd_enabled)
        self.crowd_slider.setValue(audio_settings.crowd_volume)

        self.servers_editor = screen.servers_editor
        self.servers_editor.load(self.settings.connection)

    def load_resolution_combobox(self, display_settings):
        self.resolution_combobox.clear()
        self.resolution_combobox.addItem('—')
        available_resolutions = display_settings.get_available_resolutions()
        if available_resolutions:
            for i, (w, h) in enumerate(available_resolutions):
                self.resolution_combobox.addItem(f'{w}x{h}')

            best_index = available_resolutions.index(max(available_resolutions)) + 1
            self.fullscreen_checkbox.clicked.connect(run_callback_in_async_loop(
                set_combobox_index_if_checked_is, self.fullscreen_checkbox, True,
                self.resolution_combobox, best_index))

            if display_settings.full_screen:
                try:
                    selected_index = available_resolutions.index(
                        display_settings.full_screen_size) + 1
                except ValueError:
                    selected_index = best_index
                self.resolution_combobox.setCurrentIndex(selected_index)
            else:
                self.resolution_combobox.setCurrentIndex(0)
        else:
            self.fullscreen_checkbox.setChecked(False)

    def save(self):
        display_settings = self.settings.display
        display_settings.detail_level = display_settings.DETAIL_LEVELS[
            int(self.detail_slider.value())]
        display_settings.full_screen = self.fullscreen_checkbox.isChecked()
        if display_settings.full_screen:
            size_text = self.resolution_combobox.currentText()
            if 'x' in size_text:
                display_settings.full_screen_size = tuple(
                    int(item) for item in size_text.split('x', 1))
        display_settings.upscale = self.upscale_checkbox.isChecked()
        display_settings.grab_mouse = self.grab_mouse_checkbox.isChecked()
        display_settings.show_range = self.show_range_checkbox.isChecked()
        display_settings.show_timings = self.show_timings_checkbox.isChecked()
        display_settings.disable_shop_buttons = self.disable_buttons_checkbox.isChecked()
        display_settings.show_experimental = self.show_experimental_checkbox.isChecked()

        self.servers_editor.save(self.settings.connection)

        audio_settings = self.settings.audio
        audio_settings.music_enabled = self.music_checkbox.isChecked()
        audio_settings.music_volume = self.music_slider.value()
        audio_settings.sound_enabled = self.sfx_checkbox.isChecked()
        audio_settings.sound_volume = self.sfx_slider.value()
        audio_settings.crowd_enabled = self.crowd_checkbox.isChecked()
        audio_settings.crowd_volume = self.crowd_slider.value()

        self.settings.save()


def set_combobox_index_if_checked_is(checkbox: QCheckBox, checked, combobox: QComboBox, index):
    if checkbox.isChecked() == checked:
        combobox.setCurrentIndex(index)


def set_checked_unless_combobox_index(checkbox: QCheckBox, combobox: QComboBox, index, new_index):
    if new_index == index:
        checkbox.setChecked(False)
    else:
        checkbox.setChecked(True)


def checkbox_enables(checkbox: QCheckBox, widget: QWidget):
    widget.setEnabled(checkbox.isChecked())


def checkbox_toggles_icon(checkbox: QCheckBox, false_icon: int, true_icon: int):
    icon = QApplication.style().standardIcon(true_icon if checkbox.isChecked() else false_icon)
    checkbox.setIcon(icon)


class SettingsScreen(HasAsyncCallbacks):
    def __init__(self, grab_key=None, start_tab=None):
        super().__init__()
        if grab_key is None:
            grab_key = keygrab.grab_key_from_qt_window
        self.grab_key = grab_key
        self.start_tab = start_tab
        self.window = None
        self.screen_runner = UIScreenRunner(functools.partial(self.show, modal=True))
        self.key_settings = None
        self.servers_editor = None
        self.io = SettingsSaverAndLoader()

    async def run(self):
        try:
            with ClientSettings.get().display.keep_windowed():
                await self.screen_runner.run()
        finally:
            self.async_manager.cancel_all()

    def show(self, modal=False):
        if self.window is None:
            self.window = self.build_window(modal)
            self.window.show()

    def raise_to_top(self):
        if self.window:
            self.window.activateWindow()

    def build_window(self, modal):
        window = load_ui_file(
            SETTINGS_UI_FILE,
            event_filters={
                'settings_form': {
                    QEvent.Close: self.form_close_event,
                },
            },
        )
        if modal:
            window.setWindowModality(Qt.WindowModality.ApplicationModal)
        window.findChild(QWidget, 'cancel_button').clicked.connect(
            run_callback_in_async_loop(window.close))
        window.findChild(QWidget, 'ok_button').clicked.connect(
            run_callback_in_async_loop(self.ok_clicked))

        music_checkbox = window.findChild(QWidget, 'music_checkbox')
        music_checkbox.clicked.connect(run_callback_in_async_loop(
            checkbox_enables, music_checkbox, window.findChild(QWidget, 'music_slider')))
        music_checkbox.clicked.connect(run_callback_in_async_loop(
            checkbox_toggles_icon, music_checkbox,
            QStyle.SP_MediaVolumeMuted, QStyle.SP_MediaVolume))

        sfx_checkbox = window.findChild(QWidget, 'sfx_checkbox')
        sfx_checkbox.clicked.connect(run_callback_in_async_loop(
            checkbox_enables, sfx_checkbox, window.findChild(QWidget, 'sfx_slider')))
        sfx_checkbox.clicked.connect(run_callback_in_async_loop(
            checkbox_toggles_icon, sfx_checkbox,
            QStyle.SP_MediaVolumeMuted, QStyle.SP_MediaVolume))

        crowd_checkbox = window.findChild(QWidget, 'crowd_checkbox')
        crowd_checkbox.clicked.connect(run_callback_in_async_loop(
            checkbox_enables, crowd_checkbox, window.findChild(QWidget, 'crowd_slider')))
        crowd_checkbox.clicked.connect(run_callback_in_async_loop(
            checkbox_toggles_icon, crowd_checkbox,
            QStyle.SP_MediaVolumeMuted, QStyle.SP_MediaVolume))

        fullscreen_checkbox = window.findChild(QWidget, 'fullscreen_checkbox')
        resolution_combobox = window.findChild(QWidget, 'resolution_combobox')
        fullscreen_checkbox.clicked.connect(run_callback_in_async_loop(
            set_combobox_index_if_checked_is, fullscreen_checkbox, False, resolution_combobox, 0))
        resolution_combobox.currentIndexChanged.connect(run_callback_in_async_loop(
            set_checked_unless_combobox_index, fullscreen_checkbox, resolution_combobox, 0))

        window.findChild(QWidget, 'restore_defaults_button').clicked.connect(
            run_callback_in_async_loop(self.restore_defaults))
        window.findChild(QWidget, 'edit_control_button').clicked.connect(
            run_callback_in_async_loop(self.edit_clicked))
        window.findChild(QWidget, 'controls_table').cellDoubleClicked.connect(
            run_callback_in_async_loop(self.control_double_clicked))
        self.key_settings = KeyboardSettingsEditor(self.grab_key, window)

        self.servers_editor = ServersEditor(window)
        self.io.load_values(self, window)

        music_checkbox.setIcon(QApplication.style().standardIcon(
            QStyle.SP_MediaVolume if music_checkbox.isChecked() else QStyle.SP_MediaVolumeMuted))
        sfx_checkbox.setIcon(QApplication.style().standardIcon(
            QStyle.SP_MediaVolume if sfx_checkbox.isChecked() else QStyle.SP_MediaVolumeMuted))
        crowd_checkbox.setIcon(QApplication.style().standardIcon(
            QStyle.SP_MediaVolume if crowd_checkbox.isChecked() else QStyle.SP_MediaVolumeMuted))

        if self.start_tab:
            tab_widget = window.findChild(QWidget, 'tab_widget')
            tab_widget.setCurrentWidget(tab_widget.findChild(QWidget, self.start_tab))
        return window

    def form_close_event(self, obj, event):
        # Sometimes on Windows, Qt events interrupt running code
        asyncio.get_running_loop().call_soon_threadsafe(self.screen_runner.done, None)
        return False

    def ok_clicked(self):
        self.io.save()
        self.key_settings.save()
        self.window.close()

    def restore_defaults(self):
        self.key_settings.restore_default_controls()

    @async_callback
    async def edit_clicked(self):
        await self.key_settings.edit_key(self.window)

    @async_callback
    async def control_double_clicked(self, row_index, column_index):
        await self.key_settings.edit_key(self.window, row_index)


async def async_main():
    initialise_qt_application()

    settings_screen = SettingsScreen()
    await settings_screen.run()


if __name__ == '__main__':
    run_async_main_function(async_main)
