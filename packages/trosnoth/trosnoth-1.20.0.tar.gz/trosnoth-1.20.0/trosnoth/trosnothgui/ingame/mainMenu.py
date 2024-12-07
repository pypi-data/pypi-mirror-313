# Trosnoth (UberTweak Platform Game)
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

from trosnoth.const import (
    ACTION_CHAT, ACTION_MAIN_MENU, ACTION_REALLY_QUIT,
    ACTION_USE_UPGRADE, ACTION_PAUSE_GAME,
    ACTION_SETTINGS_MENU, ACTION_QUIT_MENU,
    ACTION_EMOTE, ACTION_RADIAL_UPGRADE_MENU,
)
from trosnoth.gui.framework.menu import MenuDisplay
from trosnoth.gui.menu.menu import MenuManager, Menu, MenuItem
from trosnoth.gui.common import Abs


class MainMenu(MenuDisplay):
    def __init__(self, app, location, interface, keymapping):
        self.interface = interface
        font = app.screenManager.fonts.gameMenuFont
        titleColour = (64, 64, 255)
        stdColour = (96, 96, 96)
        hvrColour = (255, 64, 0)
        backColour = (255, 255, 255)
        autosize = True
        hidable = True
        size = Abs(400, 10)   # Height doesn't matter when autosize is set.

        self.ACCELERATION = 2000    # pix/s/s

        manager = MenuManager()

        self.quit_menu = Menu(name='Really Quit?', listener=interface.doAction, items=[
            MenuItem('Leave game', ACTION_REALLY_QUIT),
            MenuItem('---'),
            MenuItem('Cancel', ACTION_MAIN_MENU)
        ])
        super().__init__(
            app, location, size, font, manager,
            titleColour, stdColour, hvrColour, None, backColour, autosize,
            hidable, keymapping, x_padding=20, y_padding=10, hidden=True)

        self.main_menu = None
        self.refresh_menu_items()

    def refresh_menu_items(self, joined=True, can_join=True):
        main_menu_items = []

        if not joined:
            main_menu_items.extend([
                MenuItem('Settings', ACTION_SETTINGS_MENU),
                MenuItem('---'),
                MenuItem('Quit', ACTION_QUIT_MENU)
            ])
        else:
            main_menu_items.extend([
                MenuItem('Taunt', ACTION_EMOTE),
                MenuItem('Toggle upgrade select', ACTION_RADIAL_UPGRADE_MENU),
                MenuItem('Activate upgrade', ACTION_USE_UPGRADE),
                MenuItem('Toggle chat', ACTION_CHAT),
            ])
            if self.interface.world.isServer:
                main_menu_items.append(
                    MenuItem('Pause / resume', ACTION_PAUSE_GAME)
                )
            main_menu_items.extend([
                MenuItem('Settings', ACTION_SETTINGS_MENU),
                MenuItem('---'),
                MenuItem('Leave game', ACTION_QUIT_MENU)
            ])
        self.main_menu = Menu(name='Menu', listener=self.do_action, items=main_menu_items)
        self.manager.setDefaultMenu(self.main_menu)
        self.manager.reset()

    def do_action(self, action):
        if action == ACTION_SETTINGS_MENU:
            self.hide()
        self.interface.doAction(action)

    def set_mode(self, joined=False, can_join=False):
        self.active = joined or not can_join
        self.refresh_menu_items(joined=joined)

    def showQuitMenu(self):
        self.manager.reset()
        self.manager.showMenu(self.quit_menu)

    def escape(self):
        if self.hidden:
            # Just show the existing menu.
            self.hide()
        elif self.manager.menu == self.manager.defaultMenu:
            # Main menu is already selected. Hide it.
            self.hide()
        else:
            # Main menu is not selected. Return to it.
            self.manager.cancel()
