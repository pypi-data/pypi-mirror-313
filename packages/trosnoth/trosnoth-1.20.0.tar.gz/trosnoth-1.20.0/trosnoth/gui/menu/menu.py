# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2012 Joshua D Bartlett
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

from trosnoth.utils.event import Event


class MenuManager(object):
    def __init__(self, defaultMenu=None):
        self.defaultMenu = defaultMenu
        self.menu = defaultMenu
        self.menuStack = []
        self.onShowMenu = Event()   # (menu)
        self.on_contents_changed = Event([])

    def _change_menu(self, menu):
        if self.menu is not None:
            self.menu.on_contents_changed.removeListener(self.on_contents_changed.execute)
        menu.on_contents_changed.addListener(self.on_contents_changed.execute)
        self.menu = menu
        self.onShowMenu.execute(menu)

    def setDefaultMenu(self, defaultMenu):
        default = len(self.menuStack) == 0 and self.menu is self.defaultMenu
        self.defaultMenu = defaultMenu

        if default or self.menu is None:
            self._change_menu(defaultMenu)

    def reset(self):
        self.menuStack = []
        self._change_menu(self.defaultMenu)

    def cancel(self):
        if len(self.menuStack) > 0:
            menu = self.menuStack.pop()
        else:
            menu = self.defaultMenu
        self._change_menu(menu)

    def showMenu(self, menu):
        self.menuStack.append(self.menu)
        self._change_menu(menu)


class MenuItem(object):
    '''
    @param name     the caption of the menu item
    @param action   a callable for when the item is selected
    '''
    def __init__(self, name, action=None, listener=None, enabled=True):
        self.name = name
        self.onClick = Event()      # (MenuItem)
        self.onAction = Event()     # (action)
        self.action = action
        self.enabled = enabled
        if listener is not None:
            self.onClick.addListener(listener)

    def execute(self):
        self.onClick.execute(self)
        if self.action is not None:
            self.onAction.execute(self.action)

class Menu(object):
    '''
    @param name     the caption of this menu
    @param items    a sequence of MenuItem objects to be displayed in this menu
    '''
    def __init__(self, name, items=(), listener=None):
        self.name = name
        self.items = list(items)

        self.onAction = Event()     # (action)
        self.on_contents_changed = Event([])
        if listener is not None:
            self.onAction.addListener(listener)
        for item in items:
            item.onAction.addListener(self.onAction.execute)

    def popItem(self, index):
        item = self.items.pop(index)
        item.onAction.removeListener(self.onAction.execute)
        self.on_contents_changed()
        return item

    def removeItem(self, item):
        self.popItem(self.items.index(item))

    def insertItem(self, pos, item):
        self.items.insert(pos, item)
        item.onAction.addListener(self.onAction.execute)
        self.on_contents_changed()

    def appendItem(self, item):
        self.insertItem(len(self.items), item)
