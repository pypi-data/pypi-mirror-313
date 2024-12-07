import logging
import math
from typing import Type

import pygame.gfxdraw
import pygame.surface

from trosnoth.gui.common import TextImage
from trosnoth.gui.framework.framework import Element, CompoundElement
from trosnoth.model.upgrades import Categories, ShopItem, gun_types, GunType, team_boosts, TeamBoost
from trosnoth.trosnothgui.common import get_mouse_pos
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


VERTICES_IN_FULL_CIRCLE = 36

CENTRAL_AREA = object()


class RadialUpgradeMenu(CompoundElement):
    def __init__(self, app, player, select_shop_item):
        super().__init__(app)
        self.player = player
        self.select_shop_item = select_shop_item
        self.child = None

    def set_player(self, player):
        self.player = player
        if self.child:
            if player is None:
                self.set_child(None)
            else:
                self.child.set_player(player)

    def start(self):
        pass

    def stop(self):
        if self.child:
            self.child.stop()

    def set_child(self, child):
        if self.child:
            self.child.stop()
        self.child = child
        self.elements = [child] if child else []
        if self.child:
            self.child.start()

    def toggle(self):
        if self.child or self.player is None:
            self.set_child(None)
        else:
            self.set_child(self.build_category_menu())

    def build_category_menu(self):
        return CategoryMenu(self.app, self.player, self.set_child, self.select_shop_item)

    def get_screenshot_info(self):
        if self.child:
            return type(self.child).__name__
        return None

    def restore_screenshot_info(self, info):
        if info is None:
            child = None
        elif info == 'CategoryMenu':
            child = self.build_category_menu()
        elif info == 'GunMenu':
            child = GunMenu(self.app, self.player, self.set_child, self.select_shop_item)
        elif info == 'TeamMenu':
            child = TeamMenu(self.app, self.player, self.set_child)
        elif info == 'ItemMenu':
            child = ItemMenu(self.app, self.player, self.set_child, self.select_shop_item)
        else:
            raise ValueError(f'Unknown menu type: {info!r}')

        self.set_child(child)


class RadialMenu(Element):
    outline_offset = 0.05
    outline_colour = (125, 125, 125, 225)
    background_colour = (170, 170, 170, 225)
    disabled_colour = (170, 170, 170, 225)
    hover_colour = (255, 255, 100, 225)

    degrees_in_gap = 5

    def __init__(self, app, player, set_menu):
        super().__init__(app)
        self.player = player
        self.set_menu = set_menu
        self.surface = None

        self.screen_centre = (0, 0)
        self.display_radius_max = 0
        self.display_radius_min = 0
        self.current_selection = None
        self.options = []
        self.polygon_coordinates = {}
        self.image_coordinates = {}
        self.degrees_per_option = 0
        self.mouse_down_option = None

        self.item_label = ItemLabel(self.app, self.app.fonts.gameMenuFont)

    def start(self):
        self.app.screenManager.onResize.addListener(self.screen_resized)
        self.screen_resized()

    def stop(self):
        self.app.screenManager.onResize.removeListener(self.screen_resized)

    def set_player(self, player):
        self.player = player

    def screen_resized(self):
        self.surface = pygame.surface.Surface(self.app.screenManager.size, pygame.SRCALPHA)
        self.screen_centre = self.surface.get_rect().center
        self.display_radius_max = min(self.app.screenManager.size) / 4
        self.display_radius_min = self.display_radius_max * 0.5

        self.polygon_coordinates.clear()
        self.image_coordinates.clear()

        num_options = len(self.options)
        self.degrees_per_option = 360 / num_options
        vertex_count = VERTICES_IN_FULL_CIRCLE // num_options
        degrees_offset = {0: self.degrees_in_gap * 0.5, vertex_count: -self.degrees_in_gap * 0.5}

        for option_index, option in enumerate(self.options):
            polygon = []
            self.polygon_coordinates[option] = polygon
            arc_coordinates = []
            for vertex_index in range(vertex_count + 1):
                offset = degrees_offset.get(vertex_index, 0)

                arc_coordinates.append(self.get_position(
                    option_index * self.degrees_per_option + offset
                    + vertex_index * self.degrees_per_option / vertex_count, 1))

            for vertex_coordinate in arc_coordinates:
                polygon.append((
                    vertex_coordinate[0] * self.display_radius_max + self.screen_centre[0],
                    vertex_coordinate[1] * self.display_radius_max + self.screen_centre[1]))

            for vertex_coordinate in reversed(arc_coordinates):
                polygon.append((
                    vertex_coordinate[0] * self.display_radius_min + self.screen_centre[0],
                    vertex_coordinate[1] * self.display_radius_min + self.screen_centre[1]))

            image_position = self.get_position(
                (option_index + 0.5) * self.degrees_per_option, self.display_radius_max * 0.75)
            image_position = (
                image_position[0] + self.screen_centre[0], image_position[1] + self.screen_centre[1])
            self.image_coordinates[option] = image_position
        self.current_selection = self.selection_from_position(get_mouse_pos())

    def get_position(self, angle, magnitude):
        radians = math.radians(angle)
        x = magnitude * math.sin(radians)
        y = -magnitude * math.cos(radians)
        return (x, y)

    def processEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.current_selection = self.selection_from_position(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_selection == CENTRAL_AREA:
                self.close_menu()
                return None

            if self.current_selection is not None:
                option = self.current_selection
                if self.is_option_enabled(option):
                    self.mouse_down_option = option
                    self.click(option)
                return None
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.mouse_down_option:
                option = self.mouse_down_option
                self.mouse_down_option = None
                self.click_released(option)

        return event

    def selection_from_position(self, given_pos):
        magnitude = distance(given_pos, self.screen_centre)
        if self.display_radius_max > magnitude > self.display_radius_min:
            index = math.floor(
                math.degrees(math.atan2(
                    given_pos[0] - self.screen_centre[0],
                    -given_pos[1] + self.screen_centre[1])) % 360 / self.degrees_per_option)
            return self.options[index]
        elif magnitude < self.display_radius_min:
            return CENTRAL_AREA
        return None

    def draw(self, screen):
        # Draw the background
        self.surface.fill((0, 0, 0, 0))
        draw_circle(self.surface, self.outline_colour, self.screen_centre, math.floor(
            self.display_radius_max * (1 + self.outline_offset)))
        draw_circle(self.surface, (0, 0, 0, 0), self.screen_centre, math.floor(
            self.display_radius_min * (1 - self.outline_offset)))

        # Draw the ‘X’ in the centre
        background_colour = self.background_colour
        if self.current_selection == CENTRAL_AREA:
            background_colour = self.hover_colour
        central_radius = int(self.display_radius_min // 3)
        draw_circle(
            self.surface, self.outline_colour, self.screen_centre, central_radius + 3)
        draw_circle(
            self.surface, background_colour, self.screen_centre, central_radius)
        central_rect = pygame.Rect(
            0, 0, int(self.display_radius_min // 4), int(self.display_radius_min // 4))
        central_rect.center = self.screen_centre
        pygame.draw.line(
            self.surface, (96, 96, 96), central_rect.topleft, central_rect.bottomright, 5)
        pygame.draw.line(
            self.surface, (96, 96, 96), central_rect.topright, central_rect.bottomleft, 5)

        # Draw the segments around the circle
        for option in self.options:
            self.draw_segment(option)

        screen.blit(self.surface, (0, 0))

        # Add mouse hover text
        if self.current_selection is not None and self.current_selection != CENTRAL_AREA:
            self.item_label.set_text(self.get_display_name(self.current_selection))
            x, y = get_mouse_pos()
            self.item_label.blit_to(screen, (x, y + 30))

    def draw_segment(self, option):
        if self.is_option_enabled(option):
            self.draw_enabled_background(option)
        self.draw_icon(option, self.surface, self.image_coordinates[option])

    def draw_enabled_background(self, option):
        background_colour = self.background_colour
        if self.current_selection == option:
            background_colour = self.hover_colour
        draw_polygon(self.surface, background_colour, self.polygon_coordinates[option])

    def close_menu(self):
        self.set_menu(None)

    def is_option_enabled(self, option):
        raise NotImplementedError()

    def get_display_name(self, option):
        raise NotImplementedError()

    def draw_icon(self, option, surface, pos):
        raise NotImplementedError()

    def click(self, option):
        raise NotImplementedError()

    def click_released(self, option):
        pass


class CategoryMenu(RadialMenu):
    def __init__(self, app, player, set_menu, select_shop_item):
        super().__init__(app, player, set_menu)
        self.select_shop_item = select_shop_item
        self.options = list(Categories)

    def is_option_enabled(self, option):
        if option == Categories.WEAPON and not self.player.aggression:
            return False
        if option == Categories.TEAM and self.player.team is None:
            return False
        if option == Categories.TEAM and not self.player.world.abilities.upgrades:
            return False
        return True

    def get_display_name(self, option):
        return option.display_name

    def draw_icon(self, option, surface, pos):
        enabled = self.is_option_enabled(option)
        if enabled:
            image = self.app.theme.sprites.category_image(option.icon_filename)
        else:
            image = self.app.theme.sprites.disabled_category_image(option.icon_filename)

        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)

    def click(self, option):
        if option == Categories.WEAPON:
            self.set_menu(GunMenu(self.app, self.player, self.set_menu, self.select_shop_item))
        elif option == Categories.TEAM:
            self.set_menu(TeamMenu(self.app, self.player, self.set_menu))
        else:
            self.set_menu(
                ItemMenu(self.app, self.player, self.set_menu, self.select_shop_item))


class TextCache:
    def __init__(self, app):
        self.app = app
        self.cache = {}

    def render(self, text, colour):
        key = (text, colour)
        if key not in self.cache:
            self.cache[key] = TextImage(
                text,
                font=self.app.screenManager.fonts.cost_font,
                colour=colour,
            )

        return self.cache[key].getImage(self.app)


class ItemMenu(RadialMenu):
    def __init__(self, app, player, set_menu, select_shop_item):
        super().__init__(app, player, set_menu)
        self.select_shop_item = select_shop_item
        self.options = Categories.ITEM.upgrades
        self.text_cache = TextCache(app)

    def is_option_enabled(self, option: ShopItem):
        return option.get_required_coins(self.player) is not None

    def get_display_name(self, option: ShopItem):
        return option.name

    def draw_icon(self, option: ShopItem, surface, pos):
        enabled = self.is_option_enabled(option)
        image = option.get_icon(self.app.theme.sprites, enabled)
        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)

        if enabled:
            colours = self.app.theme.colours
            required_coins = option.get_required_coins(self.player)
            affordable = self.player.coins >= required_coins
            colour = colours.cost_affordable if affordable else colours.cost_prohibitive
            text = self.text_cache.render(f'${required_coins}', colour)
            text_rect = text.get_rect()
            text_rect.midtop = rect.midbottom
            surface.blit(text, text_rect)

    def click(self, option: ShopItem):
        self.select_shop_item(option)
        self.close_menu()


class GunMenu(RadialMenu):
    def __init__(self, app, player, set_menu, select_shop_item):
        super().__init__(app, player, set_menu)
        self.options = [g for g in gun_types if g.max_ammo > 0]
        self.text_cache = TextCache(app)
        self.select_shop_item = select_shop_item

    def is_option_enabled(self, option: Type[GunType]):
        if not self.player.aggression:
            return False
        return True

    def can_option_be_immediately_bought(self, option):
        required_coins = option.get_required_coins(self.player)
        if required_coins is None or self.player.coins < required_coins:
            return False
        return True

    def draw_segment(self, option):
        if self.is_option_enabled(option):
            if self.can_option_be_immediately_bought(option) or self.current_selection == option:
                self.draw_enabled_background(option)
        self.draw_icon(option, self.surface, self.image_coordinates[option])

    def get_display_name(self, option: Type[GunType]):
        return option.name

    def draw_icon(self, option: Type[GunType], surface, pos):
        enabled = self.is_option_enabled(option) and self.can_option_be_immediately_bought(option)
        image = option.get_icon(self.app.theme.sprites, enabled)
        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)
        next_point = rect.midbottom

        colours = self.app.theme.colours
        gun = self.player.guns.get(option)
        if gun.ammo > 0:
            ammo_rect = pygame.Rect(0, 0, rect.width, 5)
            ammo_rect.midtop = next_point
            next_point = ammo_rect.midbottom
            pygame.draw.rect(surface, colours.gauge_ammo, ammo_rect, 1)
            ammo_rect.width = round(rect.width * gun.ammo / option.max_ammo)
            pygame.draw.rect(surface, colours.gauge_ammo, ammo_rect)

        required_coins = option.get_required_coins(self.player)
        cost_string = f'${required_coins}'
        if required_coins is None:
            colour = colours.cost_unavailable
            cost_string = 'MAX'
        elif self.player.coins >= required_coins:
            colour = colours.cost_affordable
        else:
            colour = colours.cost_prohibitive

        text = self.text_cache.render(cost_string, colour)
        text_rect = text.get_rect()
        text_rect.midtop = next_point
        surface.blit(text, text_rect)

    def click(self, option: GunType):
        gun = self.player.guns.get(option)
        required_coins = option.get_required_coins(self.player)
        if gun.ammo_is_full or option.full_cost is None:
            self.player.guns.please_select(gun)
        elif required_coins is not None and self.player.coins >= required_coins:
            gun.please_buy_ammo()
        else:
            self.select_shop_item(gun)


class TeamMenu(RadialMenu):
    def __init__(self, app, player, set_menu):
        super().__init__(app, player, set_menu)
        self.options = team_boosts
        self.text_cache = TextCache(app)

    def stop(self):
        super().stop()
        if self.mouse_down_option:
            option = self.mouse_down_option
            self.mouse_down_option = None
            self.click_released(option)

    def is_option_enabled(self, option: Type[TeamBoost]):
        if not self.player.world.abilities.upgrades:
            return False
        if self.player.team is None:
            return False
        boost = self.player.team.boosts.get(option)
        if boost and boost.activated:
            return False
        if boost is None and self.player.coins < option.deposit_cost:
            return False
        return True

    def get_display_name(self, option: Type[TeamBoost]):
        return option.name

    def draw_icon(self, option: Type[TeamBoost], surface, pos):
        enabled = self.is_option_enabled(option)
        image = option.get_icon(self.app.theme.sprites, enabled)
        rect = image.get_rect()
        rect.center = pos
        surface.blit(image, rect)
        next_point = rect.midbottom
        if not self.player.team:
            return

        colours = self.app.theme.colours
        cost_string = f'${option.deposit_cost} + ${option.extra_cost}'
        boost = self.player.team.boosts.get(option)
        if boost is None and self.player.coins < option.deposit_cost:
            colour = colours.cost_prohibitive
        elif not enabled:
            colour = colours.cost_unavailable
        else:
            colour = colours.cost_affordable

        text = self.text_cache.render(cost_string, colour)
        text_rect = text.get_rect()
        text_rect.midtop = next_point
        surface.blit(text, text_rect)
        next_point = text_rect.midbottom

        purchase = self.player.agent.current_boost_purchase
        if option == purchase.boost_class:
            ratio = purchase.get_boost_progress_ratio()
            activated = ratio == 1
        elif boost:
            activated = boost.activated
            progress = boost.total_cost - boost.remaining_cost
            ratio = progress / boost.total_cost
        else:
            return

        if activated:
            text = self.text_cache.render('ACTIVE', colours.cost_unavailable)
            text_rect = text.get_rect()
            text_rect.midtop = next_point
            surface.blit(text, text_rect)
        else:
            progress_rect = pygame.Rect(0, 0, rect.width, 5)
            progress_rect.midtop = next_point
            pygame.draw.rect(surface, colours.gauge_boost_progress, progress_rect, 1)
            progress_rect.width = round(rect.width * ratio)
            pygame.draw.rect(surface, colours.gauge_boost_progress, progress_rect)

    def click(self, option: TeamBoost):
        self.player.agent.current_boost_purchase.start_boost_purchase(option)

    def tick(self, delta_t):
        if self.mouse_down_option:
            self.player.agent.current_boost_purchase.contribute(500 * delta_t)

    def click_released(self, option: TeamBoost):
        purchase = self.player.agent.current_boost_purchase
        if option == purchase.boost_class:
            purchase.complete_purchase()
        self.close_menu()


def draw_circle(surface, colour, centre, radius):
    pygame.gfxdraw.aacircle(surface, *centre, radius, colour)
    pygame.gfxdraw.filled_circle(surface, *centre, radius, colour)


def draw_polygon(surface, colour, points):
    pygame.gfxdraw.aapolygon(surface, points, colour)
    pygame.gfxdraw.filled_polygon(surface, points, colour)


class ItemLabel:
    def __init__(self, app, font, colour=(200, 200, 200), shadow=(50, 50, 50)):
        self.app = app
        self.font = font
        self.colour = colour
        self.shadow = shadow
        self.text = None
        self.main_surface = None
        self.shadow_surface = None

    def set_text(self, text):
        if text == self.text:
            return
        self.text = text
        self.main_surface = self.font.render(self.app, text, True, self.colour)
        self.shadow_surface = self.font.render(self.app, text, True, self.shadow)

    def blit_to(self, screen, position):
        r = self.main_surface.get_rect()
        r.center = position
        x, y = r.topleft
        screen.blit(self.shadow_surface, (x + 2, y + 2))
        screen.blit(self.main_surface, r)
