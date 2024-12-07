import logging
import platform

import pygame

from trosnoth.gui.app import get_pygame_runner
from trosnoth.gui.framework import framework
from trosnoth.gui.common import Location
from trosnoth.trosnothgui.common import get_mouse_pos
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)


class SystemHotKeys(framework.Element):
    '''
    Traps a Ctrl+Break / Ctrl+Pause keypress and terminates the game.
    Traps an Alt+Tab keypress and minimises the game.
    '''
    def processEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.mod & pygame.KMOD_CTRL and event.key in (
                    pygame.K_SCROLLOCK, pygame.K_BREAK, pygame.K_PAUSE):
                log.warning('Trapped Ctrl+Break keypress: Quitting.')
                self.app.stop()
                return None
            if (
                    event.key == pygame.K_BACKSLASH
                    and event.mod & pygame.KMOD_CTRL
                    and event.mod & pygame.KMOD_META):
                log.warning('Trapped Ctrl+Meta+Backslash: Quitting.')
                self.app.stop()
                return None
            if (event.key == pygame.K_TAB and (event.mod & pygame.KMOD_ALT) and
                    self.app.screenManager.isFullScreen()):
                if platform.system() != 'Darwin':
                    # Minimise.
                    pygame.display.iconify()
                return None
        return event


class Pointer(framework.CompoundElement):
    def __init__(self, app, element):
        super(Pointer, self).__init__(app)
        assert hasattr(element, 'setPos')
        self.elements = [element]

    def draw(self, screen):
        try:
            pos = get_mouse_pos()
            self.elements[0].setPos(Location(pos, 'center'))
        except Exception as e:
            log.exception(str(e))
        super(Pointer, self).draw(screen)


class ScreenFonts(object):
    def addFont(self, identifier, font):
        setattr(self, identifier, font)


class ScreenManager(framework.CompoundElement):
    '''Manages everything to do with the screen, especially any scaling due
    to the size of the screen.'''

    def __init__(self, app):
        super(ScreenManager, self).__init__(app)

        self.onResize = Event()
        self.size = None
        self.fonts = ScreenFonts()
        self.interface = None
        self.terminator = SystemHotKeys(self.app)
        self.elements = [self.terminator]

        self.scaleFactor = 1
        self.scaledSize = (1024, 768)
        self.offsets = (0, 0)
        self.scaledRect = pygame.Rect(self.offsets, self.scaledSize)
        self.rect = pygame.Rect(self.scaledRect)
        self.surface_has_been_resized()
        get_pygame_runner().on_resize.addListener(self.surface_has_been_resized)

    def set_interface(self, element):
        self.interface = element
        self.elements = [self.interface, self.terminator]

    def surface_has_been_resized(self):
        size = get_pygame_runner().get_window_size()

        if size != self.size:
            self.size = size
            self.scaleFactor = min(size[0] / 1024.,
                                   size[1] / 768.)

            # Calculate corner offset for strange screen sizes.
            self.scaledSize = self.scale((1024, 768))
            self.offsets = ((size[0] - self.scaledSize[0]) / 2,
                            (size[1] - self.scaledSize[1]) / 2)

            self.rect = pygame.Rect((0, 0), size)
            self.scaledRect = pygame.Rect(self.offsets, self.scaledSize)

            self.onResize()

    def isFullScreen(self):
        return get_pygame_runner().is_full_screen()

    def scale(self, point):
        '''Takes a point on a 1024x768 screen and scales it to this screen.'''
        return (int(point[0] * self.scaleFactor),
                int(point[1] * self.scaleFactor))

    def placePoint(self, point):
        '''Places the point from a 1024x768 screen onto the largest rectangle
        of that ratio that fits within this screen.'''
        return (int(point[0] * self.scaleFactor + self.offsets[0]),
                int(point[1] * self.scaleFactor + self.offsets[1]))
