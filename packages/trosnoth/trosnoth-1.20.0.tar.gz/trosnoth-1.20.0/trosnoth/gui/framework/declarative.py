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

import logging
import time
from dataclasses import dataclass
from typing import Tuple, Optional, Union, Callable, TypeVar, Generic

import pygame

from trosnoth.const import MOUSE_UP, MOUSE_DOWN
from trosnoth.data import get_overridable_path
from trosnoth.gui.app import get_pygame_runner
from trosnoth.gui.framework.framework import Element
from trosnoth.trosnothgui.common import setAlpha, get_mouse_pos

log = logging.getLogger(__name__)

LOG_NEW_SURFACES = False


Colour = Union[Tuple[int, int, int], Tuple[int, int, int, int]]
Position = Tuple[float, float]


'''
A declarative element object, which may be passed as `root` to the
constructor of DeclarativeElement, must define one of `draw()` and
`build_pygame_surface()`. See the docstrings for the following protocols
for more information.
'''


class PrimitiveDeclarativeThing:
    def build_pygame_surface(
            self,
            renderer: 'DeclarativeRenderer',
            scale: float
    ) -> Tuple[pygame.Surface, Position]:
        '''
        Called to get the Pygame surface used to draw this element. This
        will only be called once unless the object changes or is not
        used in a frame.

        :param renderer: the DeclarativeRenderer, just in case you need
            access to external things like `renderer.app`.
        :param scale: the scale that this element is being drawn at.
            This should be multiplied by any length.
        :return: (surface, origin), where origin is the location of this
            element's origin within the returned surface.
        '''
        pass


T = TypeVar('T')


class ComplexDeclarativeThing(Generic[T]):
    def build_state(self, renderer: 'DeclarativeRenderer') -> T:
        '''
        Called once when this element wasn't in the previous frame, to
        create the initial state object for this element. The state
        object can be any mutable object, and is used to store internal
        state such as progress through an animation. An empty dict
        can be used to ensure that the object is not marked as static,
        in order that `draw()` is called each frame. If this method
        returns `None` (the default), the object will be marked as
        static if in any frame `draw()` does not add any non-static
        child elements.

        It's important to remember, that the state applies to
        this exact element only, and if a new element is created that
        does not compare equal to this one, the state object will be
        reset.

        :param renderer: the DeclarativeRenderer, just in case you need
            access to external things like `renderer.app`.
        :return: typically a dict, but can be any mutable object
        '''
        return None

    def draw(self, frame: 'FrameInterface', state: T):
        '''
        Defines what this element looks like by calling `frame.add()`
        to add child elements in various positions.

        :param frame: represents the current frame for this element
        :param state: the object created in `build_state()`
        :return: None
        '''
        pass


DeclarativeThing = Union[PrimitiveDeclarativeThing, ComplexDeclarativeThing]


class DeclarativeRenderer:
    def __init__(self, app):
        self.app = app
        self.last_delta_t = 0
        self.cached_screen_size = None
        self.scale_factor = None

        self.last_frame = {}
        self.this_frame = {}

        self.new_blits = {}
        self.old_blits = {}
        self.new_shortcuts = {}
        self.old_shortcuts = {}

    def tick(self, delta_t):
        self.last_delta_t = delta_t

    def pre_draw(self):
        self.last_frame = self.this_frame
        self.this_frame = {}
        self.old_blits = self.new_blits
        self.new_blits = {}
        self.old_shortcuts = self.new_shortcuts
        self.new_shortcuts = {}

        w, h = get_pygame_runner().get_window_size()
        if (w, h) != self.cached_screen_size:
            self.scale_factor = min(w / 1024, h / 768)
            self.cached_screen_size = (w, h)
            self.old_blits = {}
            self.old_shortcuts = {}

    def blit_root_element(self, screen, element: DeclarativeThing, pos):
        w, h = get_pygame_runner().get_window_size()
        rx, ry = pos
        x = (1 + rx) * w / 2
        y = (1 + ry) * h / 2

        frame = self.resolve_element(
            element,
            absolute_offset=(x / self.scale_factor, y / self.scale_factor))
        blits = self.build_blits(frame)
        screen.blits(offset_blits(blits, (x, y)), doreturn=False)
        return frame

    def resolve_element(self, element: DeclarativeThing, absolute_offset):
        existing = self.this_frame.get(element)
        if existing is not None:
            return existing

        # Element hasn't already been drawn this renderer frame
        last_frame = self.last_frame.get(element)
        if last_frame is None:
            # Element wasn't in the last renderer frame
            if hasattr(element, 'build_state') and hasattr(element, 'draw'):
                try:
                    state = element.build_state(self)
                except Exception:
                    log.exception(f'Error in {type(element).__name__}.build_state()')
                    state = None
            else:
                state = None
            canonical = element
            build_new_frame = True
        else:
            canonical = last_frame.element
            state = last_frame.state
            build_new_frame = not last_frame.static

        if build_new_frame:
            # Evaluate the element contents for this frame
            result = FrameInterface(self, canonical, state, absolute_offset)
        else:
            result = last_frame

        self.this_frame[canonical] = result

        return result

    def get_raw_blits(self, frame):
        if frame.static and frame.element in self.old_blits:
            result = self.old_blits[frame.element]
        else:
            result = self.combine_child_blits(frame)
            if hasattr(frame.element, 'build_pygame_surface'):
                try:
                    surface, origin = frame.element.build_pygame_surface(self, self.scale_factor)
                except Exception:
                    log.exception(
                        f'Error in {type(frame.element).__name__}.build_pygame_surface()')
                else:
                    if surface:
                        ox, oy = origin
                        result.insert(0, (surface, (-ox, -oy)))

        if frame.static and len(result) > 1:
            result = flatten_blits(result)
        self.new_blits[frame.element] = tuple(result)
        return result

    def combine_child_blits(self, parent_frame):
        scale = self.scale_factor
        result = []

        for (at_x, at_y), frame, alpha in parent_frame.children:
            if alpha < 1:
                blits = self.build_blits(frame, alpha)
            else:
                # Calling build_blits will build shortcuts, but we don't
                # know they're needed, so just use get_raw_blits().
                blits = self.get_raw_blits(frame)
            blits = offset_blits(blits, (round(at_x * scale), round(at_y * scale)))
            result.extend(blits)

        return result

    def build_blits(self, frame, alpha=1.0):
        if alpha <= 0:
            return []

        if frame.element not in self.new_blits:
            self.get_raw_blits(frame)

        raw_blits = self.new_blits[frame.element]
        if not raw_blits:
            return []
        if len(raw_blits) == 1 and alpha >= 1:
            return raw_blits

        try:
            shortcut = self.old_shortcuts[raw_blits, alpha]
        except KeyError:
            # This is the first frame we've seen these blits.
            if alpha >= 1:
                # If there's no translucency, so don't flatten this
                # time, but note that we've seen these blits.
                self.new_shortcuts[raw_blits, alpha] = None
                return raw_blits

            # If there's alpha involved, we have to flatten, so act as
            # if we've seen this before but not built a shortcut.
            shortcut = None

        if shortcut is not None:
            # We've already built a shortcut for this case, so use it
            self.new_shortcuts[raw_blits, alpha] = shortcut
            return shortcut

        # Build a shortcut by flattening these blits and applying alpha
        shortcut = flatten_blits(raw_blits)
        if alpha < 1:
            setAlpha(shortcut[0][0], round(255 * alpha))
        self.new_shortcuts[raw_blits, alpha] = self.old_shortcuts[raw_blits, alpha] = shortcut
        return shortcut


class DeclarativeElement(Element):
    def __init__(self, app, pos, root: DeclarativeThing):
        '''
        :param pos: ranges from -1 to 1 in x and y, representing the full screen
        '''
        super().__init__(app)
        self.pos = pos
        self.root: DeclarativeThing = root
        self.frame = None

    def draw(self, screen):
        self.frame = self.app.declarative_renderer.blit_root_element(screen, self.root, self.pos)

    def processEvent(self, event):
        if self.frame is None:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_event(
                    MOUSE_DOWN, self.frame.screen_pos_to_frame(event.pos), event.button):
                return None
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.handle_event(
                    MOUSE_UP, self.frame.screen_pos_to_frame(event.pos), event.button):
                return None

        return event

    def handle_event(self, event_kind, *args):
        if event_kind not in self.frame.listeners:
            return False
        return self.handle_event_with_frame(self.frame, event_kind, args)

    def handle_event_with_frame(self, frame, event_kind, args):
        for at, child, alpha in reversed(frame.children):
            if event_kind in child.listeners:
                if self.handle_event_with_frame(child, event_kind, args):
                    return True
        for listener in frame.listeners[event_kind]:
            if listener(frame.state, *args):
                return True
        return False


def flatten_blits(blits):
    surface, pos = blits[0]
    rect = surface.get_rect()
    rect.topleft = pos

    for surface, pos in blits[1:]:
        child_rect = surface.get_rect()
        child_rect.topleft = pos
        rect.union_ip(child_rect)

    result = pygame.Surface(rect.size, pygame.SRCALPHA)
    if LOG_NEW_SURFACES:
        log.error(f'flatten_blits(): created new surface {result}')
    result.blits(offset_blits(blits, (-rect.left, -rect.top)), doreturn=False)
    return [(result, rect.topleft)]


def offset_blits(blits, offset):
    ox, oy = offset
    return [(surface, (ox + bx, oy + by)) for (surface, (bx, by)) in blits]


class FrameInterface:
    def __init__(self, renderer, element: DeclarativeThing, state, absolute_offset):
        self.renderer = renderer
        self.element = element
        self.state = state
        self.absolute_offset = absolute_offset

        self.children = []
        self.listeners = {}
        self.static = state is None

        if hasattr(element, 'draw'):
            try:
                element.draw(self, state)
            except Exception:
                log.exception(f'Error in {type(element).__name__}.draw()')

    @property
    def delta_t(self):
        return self.renderer.last_delta_t

    @property
    def app(self):
        return self.renderer.app

    def get_mouse_pos(self):
        self.static = False
        return self.screen_pos_to_frame(get_mouse_pos())

    def screen_pos_to_frame(self, screen_pos):
        x, y = screen_pos
        rx, ry = self.absolute_offset
        scale = self.renderer.scale_factor
        return x / scale - rx, y / scale - ry

    def add(self, element: DeclarativeThing, *, at=(0, 0), alpha=1.0):
        if not hasattr(element, 'draw') and not hasattr(element, 'build_pygame_surface'):
            raise TypeError(f'{type(element)} does not implement draw() or build_pygame_surface()')
        if alpha <= 0:
            return
        rx, ry = self.absolute_offset
        child_frame = self.renderer.resolve_element(element, (rx + at[0], ry + at[1]))
        self.children.append((at, child_frame, alpha))
        for event_kind in child_frame.listeners:
            self.listeners.setdefault(event_kind, [])
        self.static = self.static and child_frame.static

    def register_listener(self, event_kind, listener):
        self.listeners.setdefault(event_kind, []).append(listener)


@dataclass(frozen=True)
class FadeIn(ComplexDeclarativeThing):
    duration: float
    contents: DeclarativeThing

    def build_state(self, renderer):
        return {
            'start': time.monotonic(),
            'done': False,
        }

    def draw(self, frame, state):
        if state['done']:
            alpha = 1
        else:
            alpha = min(1, (time.monotonic() - state['start']) / self.duration)
            if alpha == 1:
                state['done'] = True
        frame.add(self.contents, alpha=alpha)


@dataclass(frozen=True)
class Rectangle(PrimitiveDeclarativeThing):
    width: float
    height: float
    colour: Colour
    border: Colour = (0, 0, 0)
    border_width: float = 0

    def __new__(cls, width, height, *args, **kwargs):
        if width < 0 or height < 0:
            raise ValueError(f'Cannot create rectangle with {width=} and {height=}')
        return super().__new__(cls)

    def build_pygame_surface(self, renderer, scale):
        w = round(self.width * scale)
        h = round(self.height * scale)
        b = max(1, round(self.border_width * scale)) if self.border_width else 0

        flags = pygame.SRCALPHA if len(self.colour) == 4 and self.colour[-1] < 255 else 0
        surface = pygame.Surface((w + b, h + b), flags)
        if LOG_NEW_SURFACES:
            log.error(f'Rectangle: created new surface {surface}: {self}')
        if b:
            surface.fill(self.border)
        r = pygame.Rect(0, 0, w - b, h - b)
        r.center = surface.get_rect().center
        surface.fill(self.colour, r)

        return surface, r.center


@dataclass(frozen=True)
class FullScreenRectangle(ComplexDeclarativeThing):
    colour: Colour

    def draw(self, frame, state):
        w, h = get_pygame_runner().get_window_size()
        frame.add(Rectangle(
            width=w / frame.renderer.scale_factor,
            height=h / frame.renderer.scale_factor,
            colour=self.colour,
        ))


@dataclass(frozen=True)
class Graphic(PrimitiveDeclarativeThing):
    filepath: str
    width: float
    height: float
    fallback_path: Optional[str] = None
    contain: bool = True

    def build_pygame_surface(self, renderer, scale):
        w = round(self.width * scale)
        h = round(self.height * scale)

        try:
            path = str(get_overridable_path(self.filepath))
        except FileNotFoundError:
            if self.fallback_path:
                path = str(get_overridable_path(self.fallback_path))
            else:
                raise

        image = pygame.image.load(path).convert_alpha()
        if self.contain:
            sw, sh = image.get_size()
            w, h = contain_rect(sw, sh, w, h)
        surface = pygame.transform.smoothscale(image, (w, h))
        if LOG_NEW_SURFACES:
            log.error(f'Graphic: loaded {path!r}')
        return surface, surface.get_rect().center


@dataclass(frozen=True)
class PygameSurface(PrimitiveDeclarativeThing):
    # Before using PygameSurface, consider using Graphic above
    surface: pygame.Surface
    width: float
    height: float
    contain: bool = True

    def build_pygame_surface(self, renderer, scale):
        sw, sh = self.surface.get_size()
        cw = round(self.width * scale)
        ch = round(self.height * scale)
        if self.contain:
            cw, ch = contain_rect(sw, sh, cw, ch)
        else:
            cw, ch = cover_rect(sw, sh, cw, ch)
        scaled = pygame.transform.smoothscale(self.surface, (cw, ch))
        if LOG_NEW_SURFACES:
            log.error('Graphic: scaled surface')
        return scaled, scaled.get_rect().center


def contain_rect(inner_width, inner_height, outer_width, outer_height):
    if inner_width / inner_height > outer_width / outer_height:
        return outer_width, round(inner_height * outer_width / inner_width)
    return round(inner_width * outer_height / inner_height), outer_height


def cover_rect(inner_width, inner_height, outer_width, outer_height):
    if inner_width / inner_height > outer_width / outer_height:
        return round(inner_width * outer_height / inner_height), outer_height
    else:
        return outer_width, round(inner_height * outer_width / inner_width)


@dataclass(frozen=True)
class Text(ComplexDeclarativeThing):
    A_left = 0
    A_right = 1
    A_center = 2

    text: str
    height: float
    font: str = None
    text_colour: Colour = (255, 255, 255)
    max_width: Optional[float] = None
    align: int = A_center
    shadow_offset: Optional[Tuple[float, float]] = None
    shadow_colour: Colour = (0, 0, 0, 255)
    truncate: bool = False

    def draw(self, frame, state):
        if self.shadow_offset:
            frame.add(
                ShadowlessText(
                    text=self.text, height=self.height,
                    font=self.font, text_colour=self.shadow_colour,
                    max_width=self.max_width, align=self.align,
                    truncate=self.truncate,
                ),
                at=self.shadow_offset,
            )

        frame.add(ShadowlessText(
            text=self.text, height=self.height, font=self.font, text_colour=self.text_colour,
            max_width=self.max_width, align=self.align, truncate=self.truncate))


@dataclass(frozen=True)
class ShadowlessText(PrimitiveDeclarativeThing):
    A_left = 0
    A_right = 1
    A_center = 2

    text: str
    height: float
    font: str = None
    text_colour: Colour = (255, 255, 255)
    max_width: Optional[float] = None
    align: int = A_center
    truncate: bool = False

    def build_pygame_surface(self, renderer, scale):
        h = round(self.height * scale)
        font_name = str(get_overridable_path('fonts/' + self.font)) if self.font else None
        font = pygame.font.Font(font_name, h)
        surface = font.render(self.text, True, self.text_colour)
        if LOG_NEW_SURFACES:
            log.error(f'Text: created new surface for {self.text!r}')
        if self.max_width is not None:
            mw = round(self.max_width * scale)
            if surface.get_width() > mw:
                if not self.truncate:
                    new_height = round(surface.get_height() * mw / surface.get_width())
                    surface = pygame.transform.smoothscale(surface, (mw, new_height))
                else:
                    ellipses = font.render('…', True, self.text_colour)
                    text_surface = surface
                    surface = pygame.Surface((mw, surface.get_height()), pygame.SRCALPHA)
                    surface.blit(
                        text_surface, (0, 0),
                        pygame.Rect(0, 0, mw - ellipses.get_width(), text_surface.get_height()))
                    surface.blit(ellipses, (mw - ellipses.get_width(), 0))

        if self.align == self.A_center:
            origin = surface.get_rect().midbottom
        elif self.align == self.A_right:
            origin = surface.get_rect().bottomright
        else:
            origin = surface.get_rect().bottomleft
        return surface, origin


@dataclass(frozen=True)
class Button(ComplexDeclarativeThing):
    caption: str
    pos: Tuple[float, float]
    size: Tuple[float, float]
    mouse_pos: Tuple[float, float]
    font: str
    disabled: bool = False
    text_colour: Colour = (0, 0, 0)
    background_colour: Colour = (255, 255, 255)
    hover_colour: Colour = (255, 255, 0)
    disabled_background: Colour = (255, 255, 255)
    disabled_text: Colour = (128, 128, 128)
    font_height: Optional[float] = None
    subcaption: Optional[str] = None
    padding: float = 2
    on_click: Optional[Callable] = None

    def build_state(self, renderer):
        return {'down': False}

    def draw(self, frame, state):
        if self.disabled:
            background_colour = self.disabled_background
            text_colour = self.disabled_text
        else:
            background_colour = self.background_colour
            text_colour = self.text_colour
            hh = self.size[1] / 2
            if self.pos[1] - hh <= self.mouse_pos[1] <= self.pos[1] + hh:
                hw = self.size[0] / 2
                if self.pos[0] - hw <= self.mouse_pos[0] <= self.pos[0] + hw:
                    background_colour = self.hover_colour

            if self.on_click:
                frame.register_listener(MOUSE_DOWN, self.seen_click)

        frame.add(
            ButtonAppearance(
                caption=self.caption,
                size=self.size,
                font=self.font,
                text_colour=text_colour,
                background_colour=background_colour,
                font_height=self.font_height,
                subcaption=self.subcaption,
                padding=self.padding,
            ),
            at=self.pos,
        )

    def seen_click(self, state, pos, button):
        if button != 1:
            return False
        hh = self.size[1] / 2
        if self.pos[1] - hh <= self.mouse_pos[1] <= self.pos[1] + hh:
            hw = self.size[0] / 2
            if self.pos[0] - hw <= self.mouse_pos[0] <= self.pos[0] + hw:
                state['down'] = True
                self.on_click()
                return True
        return False


@dataclass(frozen=True)
class ButtonAppearance(ComplexDeclarativeThing):
    caption: str
    size: Tuple[float, float]
    font: str
    text_colour: Colour = (0, 0, 0)
    background_colour: Colour = (255, 255, 255)
    font_height: Optional[float] = None
    subcaption: Optional[str] = None
    padding: float = 2

    def draw(self, frame, state):
        frame.add(
            Rectangle(width=self.size[0], height=self.size[1], colour=self.background_colour),
        )
        pad_count = 5 if self.subcaption else 3
        padding = min(self.padding, self.size[1] / pad_count, self.size[0] / 3)
        font_height = (self.size[1] - pad_count * padding)
        if self.subcaption:
            font_height /= 2
        if self.font_height is not None:
            font_height = min(font_height, self.font_height)

        if self.subcaption:
            main_y = -padding / 2
            frame.add(
                Text(
                    self.subcaption,
                    height=font_height,
                    font=self.font,
                    text_colour=self.text_colour,
                    max_width=self.size[0] - 2 * padding,
                ),
                at=(0, font_height + padding / 2),
            )
        else:
            main_y = font_height / 2

        frame.add(
            Text(
                self.caption,
                height=font_height,
                font=self.font,
                text_colour=self.text_colour,
                max_width=self.size[0] - 2 * padding,
            ),
            at=(0, main_y),
        )
