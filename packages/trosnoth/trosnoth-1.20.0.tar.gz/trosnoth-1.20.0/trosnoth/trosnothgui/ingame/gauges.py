import logging
from dataclasses import dataclass

import pygame
from typing import Type, Tuple, Optional

from trosnoth.gui.framework.declarative import (
    Colour, Rectangle, Text, ComplexDeclarativeThing,
    PygameSurface,
)
from trosnoth.model.player import Player
from trosnoth.model.upgrades import SelectableShopItem, GunType

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class GaugeAppearance(ComplexDeclarativeThing):
    size: Tuple[float, float]
    ratio: float
    foreground: Colour
    background: Colour = (255, 255, 255, 0)
    border_width: float = 2

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        ratio = min(1., max(0., self.ratio))
        width, height = self.size

        if len(self.background) < 4 or self.background[-1] != 0:
            frame.add(Rectangle(
                width, height,
                self.background,
            ))

        if ratio > 0:
            foreground_width = width * ratio
            frame.add(
                Rectangle(
                    max(0, foreground_width),
                    max(0, height),
                    self.foreground,
                ),
                at=((foreground_width - width) / 2, 0),
            )

        # Add frame
        frame.add(Rectangle(
            width, height,
            colour=(255, 255, 255, 0),
            border=colours.gaugeBorder, border_width=self.border_width,
        ))


@dataclass(frozen=True)
class IconGauge(ComplexDeclarativeThing):
    icon: Optional[pygame.Surface]
    size: Tuple[float, float]
    ratio: float
    foreground: Colour
    background: Colour = (255, 255, 255, 0)
    border_width: float = 2
    icon_width: int = 38
    icon_height: int = 38

    def draw(self, frame, state):
        frame.add(GaugeAppearance(
            size=self.size,
            ratio=self.ratio,
            foreground=self.foreground,
            background=self.background,
            border_width=self.border_width,
        ))
        if self.icon is not None:
            frame.add(
                PygameSurface(self.icon, width=self.icon_width, height=self.icon_height),
                at=(-self.size[0] // 2 - 7, 0),
                alpha=.625,
            )


@dataclass(frozen=True)
class ItemCostGauge(ComplexDeclarativeThing):
    player: Player
    upgrade: Type[SelectableShopItem]
    size: Tuple[float, float]
    border_width: float = 1
    show_cost: bool = True

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        required_coins = self.upgrade.get_required_coins(self.player)
        if not self.upgrade.enabled:
            ratio = 1
            colour = frame.app.theme.colours.gaugeBad
            text_colour = frame.app.theme.colours.gauge_text_bad
        elif required_coins is None:
            return
        elif required_coins == 0:
            ratio = 1
            colour = frame.app.theme.colours.gaugeGood
            text_colour = frame.app.theme.colours.gauge_text_good
        else:
            ratio = self.player.coins / required_coins
            if ratio < 1:
                colour = frame.app.theme.colours.gaugeBad
                text_colour = frame.app.theme.colours.gauge_text_bad
            else:
                colour = frame.app.theme.colours.gaugeGood
                text_colour = frame.app.theme.colours.gauge_text_good

        frame.add(GaugeAppearance(
            ratio=ratio, foreground=colour, size=self.size, border_width=self.border_width))

        if self.show_cost and required_coins > 0:
            frame.add(
                Text(
                    text=f'${required_coins}',
                    height=self.size[1],
                    font='FreeSans.ttf',
                    max_width=self.size[0],
                    align=Text.A_right,
                    text_colour=text_colour,
                ),
                at=(self.size[0] / 2, -self.size[1] / 2),
            )


@dataclass(frozen=True)
class ReloadAmmoGauge(ComplexDeclarativeThing):
    player: Player
    gun: GunType
    size: Tuple[float, float]
    border_width: float = 1
    show_cost: bool = True

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        colours = frame.app.theme.colours

        frame.add(GaugeAppearance(
            size=self.size,
            border_width=self.border_width,
            ratio=1 if self.gun.max_ammo == 0 else self.gun.ammo / self.gun.max_ammo,
            foreground=colours.gauge_ammo,
        ))

        required_coins = self.gun.get_required_coins(self.player)
        if self.show_cost and required_coins and required_coins > 0:
            if not self.gun.enabled or self.player.coins < required_coins:
                text_colour = colours.gauge_text_bad
            else:
                text_colour = colours.gauge_text_good

            frame.add(
                Text(
                    text=f'${required_coins}',
                    height=self.size[1],
                    font='FreeSans.ttf',
                    max_width=self.size[0],
                    align=Text.A_right,
                    text_colour=text_colour,
                ),
                at=(self.size[0] / 2, -self.size[1] / 2),
            )
