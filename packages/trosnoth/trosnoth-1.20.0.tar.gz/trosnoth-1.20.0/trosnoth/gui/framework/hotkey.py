# Trosnoth (Übertweak Platform Game)
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

from .framework import Element
import pygame

from trosnoth.const import KEY_UP
from trosnoth.gui.keyboard import mouseButton
from trosnoth.utils.event import Event


class Hotkeys(Element):
    '''
    Traps any keys which occur in the mapping and carries out some action on
    them. Note that this observes only, but does not stop the keypress events
    from passing through.
    '''

    def __init__(self, app, mapping, onActivated=None):
        super().__init__(app)
        self.mapping = mapping
        self.onActivated = Event()
        if onActivated is not None:
            self.onActivated.addListener(onActivated)

    def processEvent(self, event):
        action = None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button != 1:
            action = self.mapping.get(mouseButton(event.button))
        elif event.type == pygame.KEYDOWN:
            action = self.mapping.get(event.key)
        elif event.type == pygame.MOUSEBUTTONUP and event.button != 1:
            action = self.mapping.get(mouseButton(event.button))
            if action:
                action += KEY_UP
        elif event.type == pygame.KEYUP:
            action = self.mapping.get(event.key)
            if action:
                action += KEY_UP

        if action:
            # Process this hotkey.
            self.onActivated.execute(action)
        return event
