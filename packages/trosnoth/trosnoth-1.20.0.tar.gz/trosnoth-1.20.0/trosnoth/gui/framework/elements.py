import functools
import logging
import pygame

from trosnoth.gui.common import (
    Location, FullScreenAttachedPoint, defaultAnchor,
    TextImage, RelativeLocation, AttachedPoint,
)
from trosnoth.utils.event import Event
from trosnoth.gui import colours

from .framework import Element, CompoundElement

log = logging.getLogger(__name__)


class SolidRect(Element):
    '''
    Solid rectangle.
    '''
    def __init__(self, app, colour, alpha, region, border=None):
        super(SolidRect, self).__init__(app)
        self.image = None
        self.colour = colour
        self.border = border
        self.alpha = alpha
        self.region = region

        app.screenManager.onResize.addListener(self.refresh)

    def refresh(self):
        self.image = None

    def draw(self, screen):
        r = self.region.getRect(self.app)
        if self.image is None or self.image.get_rect() != r:
            self.image = pygame.Surface(r.size)
            self.image.fill(self.colour)
            if self.alpha is not None:
                self.image.set_alpha(self.alpha)

        screen.blit(self.image, r.topleft)
        if self.border:
            pygame.draw.rect(screen, self.border, r, 1)


class PictureElement(Element):
    '''Displays a picture at a specified screen location.

    @param pos: an instance of trosnoth.ui.common.Location
    '''
    def __init__(self, app, image, pos=None):
        super(PictureElement, self).__init__(app)
        self.setImage(image)
        if pos is None:
            pos = Location(FullScreenAttachedPoint((0, 0), 'center'), 'center')
        self.pos = pos

    def setImage(self, image):
        self.image = image

    def setPos(self, pos):
        self.pos = pos

    def draw(self, screen):
        if hasattr(self.image, 'getImage'):
            surface = self.image.getImage(self.app)
        else:
            surface = self.image

        rect = pygame.Rect(surface.get_rect())
        if hasattr(self.pos, 'apply'):
            self.pos.apply(self.app, rect)
        elif hasattr(self.pos, 'getPoint'):
            rect.topleft = self.pos.getPoint(self.app)
        else:
            pos = self.pos
            setattr(rect, defaultAnchor, pos)

        screen.blit(surface, rect.topleft)


class TextElement(Element):
    '''Shows text at a specified screen location.
    @param pos: should be an instance of trosnoth.ui.common.Location'''

    def __init__(
            self, app, text, font, pos, colour=(0, 128, 0),
            anchor='topleft', shadow=False, backColour=None,
            antialias=True):
        super(TextElement, self).__init__(app)

        self.pos = pos
        self.anchor = anchor
        self.image = TextImage(text, font, colour, backColour, antialias)
        self.__shadow = None
        self.setShadow(shadow)
        self._surface = None
        self.rect = None

        app.screenManager.onResize.addListener(self.appResized)

    def appResized(self):
        self.rect = None
        self._surface = None

    def _getImage(self):
        if self._surface is None:
            self.image.refresh()
            self._surface = self.image.getImage(self.app)
        return self._surface

    def getRect(self, app):
        assert app is self.app
        return self._getRect()

    def _getRect(self):
        if self.rect is not None:
            return self.rect

        rect = self._getImage().get_rect()
        pos = self.pos
        if hasattr(pos, 'apply'):
            pos.apply(self.app, rect)
        else:
            setattr(rect, defaultAnchor, pos)

        self.rect = rect
        return rect

    def getText(self):
        return self.image.text

    def setColour(self, colour):
        self.image.colour = colour
        self._surface = None

    def setText(self, text):
        if self.image.text != text:
            self._surface = None
            self.image.text = text
            if self.__shadow is not None:
                self.__shadow.setText(text)

    def setFont(self, font):
        if self.image.font != font:
            self.image.font = font
            if self.__shadow is not None:
                self.__shadow.setFont(font)
            self._surface = None

    def setPos(self, pos):
        if self.pos != pos:
            self.pos = pos
            if self.__shadow is not None:
                self.__shadow.setPos(self.__getShadowPos())
            self._surface = None
            self.rect = None

    def __getShadowPos(self):
        x = self._shadowOffset
        pos = RelativeLocation(self.pos, (x, x))
        return pos

    def setShadow(self, shadow, offset=None):
        if shadow:
            if self.__shadow is None:
                if offset is None:
                    height = self.image.font.getHeight(self.app)
                    self._shadowOffset = (height / 45) + 1
                else:
                    self._shadowOffset = offset

                self.__shadow = TextElement(
                    self.app, self.image.text,
                    self.image.font, self.__getShadowPos(),
                    colours.shadowDefault, self.anchor, False)
                self._surface = None
        else:
            if self.__shadow is not None:
                self.__shadow = None
                self._surface = None

    def setShadowOffset(self, offset):
        if self.__shadow is not None:
            self.setShadow(False)
            self.setShadow(True, offset)

    def setShadowColour(self, colour):
        if self.__shadow is not None:
            self.__shadow.setColour(colour)
            self._surface = None

    def draw(self, screen):
        if self.__shadow is not None:
            assert self.__shadow.__shadow is None
            self.__shadow.draw(screen)

        rect = self._getRect()

        # Adjust text position based on anchor.
        image = self._getImage()

        rectPos = getattr(rect, self.anchor)
        imagePos = getattr(image.get_rect(), self.anchor)
        pos = (rectPos[0]-imagePos[0], rectPos[1]-imagePos[1])

        screen.blit(image, pos)


class HoverButton(Element):
    '''A button which changes image when the mouse hovers over it.
    @param  pos     should be a trosnoth.ui.common.Location instance
    '''
    def __init__(
            self, app, pos, stdImage, hvrImage, hotkey=None, onClick=None):
        super(HoverButton, self).__init__(app)

        self.stdImage = stdImage
        self.hvrImage = hvrImage
        self.pos = pos
        self.onClick = Event()
        self.hotkey = hotkey

        self.active = True
        self.mouseOver = False

        if onClick is not None:
            self.onClick.addListener(onClick)

    def set_active(self, active):
        self.active = active

    def _getSurfaceToBlit(self):
        img = self._getImageToUse()
        if hasattr(img, 'getImage'):
            return img.getImage(self.app)
        else:
            return img

    def _getImageToUse(self):
        if self.mouseOver:
            return self.hvrImage
        else:
            return self.stdImage

    def _getSize(self):
        img = self._getImageToUse()
        if hasattr(img, 'getSize'):
            return img.getSize(self.app)
        else:
            # pygame.surface.Surface
            return img.get_size()

    def _getPt(self):
        if hasattr(self.pos, 'apply'):
            rect = pygame.Rect((0, 0), self._getSize())
            self.pos.apply(self.app, rect)
            return rect.topleft
        elif hasattr(self.pos, 'getPoint'):
            return self.pos.getPoint(self.app)
        else:
            return self.pos

    def _getRect(self):
        if hasattr(self.pos, 'apply'):
            rect = pygame.Rect((0, 0), self._getSize())
            self.pos.apply(self.app, rect)
            return rect
        return pygame.Rect(self._getPt(), self._getSize())

    def processEvent(self, event):
        if not self.active:
            return event
        rect = self._getRect()
        # Passive events.
        if event.type == pygame.MOUSEMOTION:
            self.mouseOver = rect.collidepoint(event.pos)

        # Active events.
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                rect.collidepoint(event.pos)):
            self.onClick.execute(self)
        elif event.type == pygame.KEYDOWN and event.key == self.hotkey:
            self.onClick.execute(self)
        else:
            return event
        return None

    def draw(self, screen):
        if not self.active:
            return
        screen.blit(self._getSurfaceToBlit(), self._getPt())


def make_text_button_image(app, font, text, fore_colour, back_colour, x_padding=0, y_padding=0):
    normal_text = font.render(app, text, True, fore_colour, back_colour)

    r = normal_text.get_rect()
    width, height = normal_text.get_size()
    width += x_padding * 2
    height += y_padding * 2
    image = pygame.Surface((width, height))
    r.center = image.get_rect().center
    image.fill(back_colour)
    image.blit(normal_text, r)
    return image


def make_static_text_button(
        app, pos, font, text, standard_fore_colour, standard_back_colour,
        hover_fore_colour, hover_back_colour, x_padding=0, y_padding=0,
        hotkey=None, on_click=None):
    '''
    Similar to TextButton below, but can't have its text, font, or
    button size changed on the fly, and can have a background and
    padding.
    '''
    normal_image = make_text_button_image(
        app, font, text, standard_fore_colour, standard_back_colour, x_padding, y_padding)
    hover_image = make_text_button_image(
        app, font, text, hover_fore_colour, hover_back_colour, x_padding, y_padding)
    return HoverButton(app, pos, normal_image, hover_image, hotkey, on_click)


class TextButton(HoverButton):
    'A HoverButton which has text rather than images.'
    def __init__(
            self, app, pos, text, font, stdColour, hvrColour,
            hotkey=None, backColour=None, onClick=None, size=None):
        self.stdImage = TextImage(text, font, stdColour, backColour, size=size)
        self.hvrImage = TextImage(text, font, hvrColour, backColour, size=size)

        super().__init__(app, pos, self.stdImage, self.hvrImage, hotkey, onClick)

        self.app.screenManager.onResize.addListener(self.appResized)

    def appResized(self):
        # The font may be scaled, so refresh the images
        self.stdImage.refresh()
        self.hvrImage.refresh()

    def setText(self, text):
        self.stdImage.text = text
        self.hvrImage.text = text

    def setFont(self, font):
        self.stdImage.setFont(font)
        self.hvrImage.setFont(font)

    def setColour(self, colour):
        self.stdImage.setColour(colour)

    def setHoverColour(self, colour):
        self.hvrImage.setColour(colour)

    def setBackColour(self, colour):
        self.hvrImage.setBackColour(colour)
        self.stdImage.setBackColour(colour)


class OptionButtons(CompoundElement):
    def __init__(
            self, app, items, location,
            fore_colour, back_colour, hover_colour, selection_background,
            font, x_padding=20, y_padding=10, selected_index=0,
            on_change=None, vertical=False):
        super().__init__(app)

        self.selected_index = selected_index
        self.on_change = Event(['index'])
        if on_change:
            self.on_change.addListener(on_change)

        self.items = []

        if not hasattr(location, 'apply'):
            location = Location(location)
        self.location = location

        attach_anchor = 'midtop' if vertical else 'topleft'

        x, y = 0, 0
        width, height = 0, 0
        for index, text in enumerate(items):
            loc = Location(AttachedPoint((x, y), self.get_rect, attach_anchor), attach_anchor)
            bkg = back_colour[index] if isinstance(back_colour, list) else back_colour
            normal_element = make_static_text_button(
                app, loc, font, text,
                fore_colour[index] if isinstance(fore_colour, list) else fore_colour,
                bkg,
                hover_colour[index] if isinstance(hover_colour, list) else hover_colour,
                bkg,
                x_padding, y_padding, on_click=functools.partial(self.set_index, index))
            selected_image = make_text_button_image(
                self.app, font, text, bkg,
                selection_background[index] if isinstance(
                    selection_background, list) else selection_background,
                x_padding, y_padding)
            selected_element = PictureElement(app, selected_image, loc)
            self.items.append((normal_element, selected_element))
            if vertical:
                y += selected_image.get_height()
                width = max(width, selected_image.get_width())
                height = y
            else:
                x += selected_image.get_width()
                width = x
                height = max(height, selected_image.get_height())
        self.total_width = width
        self.total_height = height
        self.update_elements()

    def get_rect(self):
        r = pygame.Rect(0, 0, self.total_width, self.total_height)
        self.location.apply(self.app, r)
        return r

    def set_index(self, index, *args):
        if index == self.selected_index:
            return
        self.selected_index = index
        self.update_elements()
        self.on_change(index)

    def update_elements(self):
        self.elements.clear()
        for index, (normal, selected) in enumerate(self.items):
            self.elements.append(selected if self.selected_index == index else normal)
