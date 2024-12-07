import time

import pygame

from trosnoth import data
from trosnoth.const import TEAM_1_COLOUR, TEAM_2_COLOUR, HEAD_CUEBALL
from trosnoth.themes import Theme, ThemeColours, ThemeSprites
from trosnoth.trosnothgui.ingame.sprites import PlayerDrawer, PlayerSprite, PlayerAction
from trosnoth.trosnothgui.ingame.viewmanager import SingleOrbDrawer


class StubbedTheme(Theme):
    colours = ThemeColours()

    def __init__(self):
        self.paths = [str(data.USERHOME), data.base_path]
        self.sprites = ThemeSprites(self)

        self.initColours()
        self.sprites.init()



def draw_one_orb(theme, colour):
    pic = theme.sprites.orbs.get(colour)
    source = pygame.Rect(0, 0, SingleOrbDrawer.FRAME_WIDTH, SingleOrbDrawer.FRAME_HEIGHT)

    result = pygame.Surface(source.size, pygame.SRCALPHA)
    result.blit(pic, source, source)

    return result


def mask_orb(orb_graphic):
    TRANSPARENT = (255, 255, 255, 0)
    pygame.draw.polygon(orb_graphic, TRANSPARENT, [
        (0, 0), (62, 0), (18, 80), (0, 80),
    ])


def draw_orb(theme, surface, whiteness):
    blue_orb = draw_one_orb(theme, TEAM_1_COLOUR)
    r = blue_orb.get_rect()
    r.center = surface.get_rect().center
    surface.blit(blue_orb, r)

    red_orb = draw_one_orb(theme, TEAM_2_COLOUR)
    mask_orb(red_orb)
    blue_orb.blit(red_orb, (0, 0))

    fade_to_white(blue_orb, whiteness)

    surface.blit(blue_orb, r)


def fade_to_white(surface, whiteness):
    white_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    n = round(255 * (1 - whiteness))
    white_surface.fill((n, n, n))
    surface.blit(white_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    n = 255 - n
    white_surface.fill((n, n, n))
    surface.blit(white_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)


def draw_player(theme, surface, colour, x, angle, frame, action=PlayerAction.RUNNING, head=HEAD_CUEBALL):
    player_surface = pygame.Surface(PlayerSprite.canvasSize, pygame.SRCALPHA)
    drawer = PlayerDrawer(
        theme, gun_angle=angle, team_colour=colour, action=action, force_frame=frame, head=head)
    drawer.render(player_surface)

    surface_rect = surface.get_rect()
    r = player_surface.get_rect()
    r.midbottom = (surface_rect.centerx + x, surface_rect.height)
    surface.blit(player_surface, r)


def main():
    pygame.display.init()
    size = max(SingleOrbDrawer.FRAME_WIDTH, SingleOrbDrawer.FRAME_HEIGHT)
    window = pygame.display.set_mode((size, size))
    window.fill((192, 192, 192))
    theme = StubbedTheme()

    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill((255, 255, 255, 0))
    draw_orb(theme, surface, 0.3)
    draw_player(theme, surface, TEAM_1_COLOUR, 15, 1, 2)
    draw_player(theme, surface, TEAM_2_COLOUR, -15, -1, 3)

    window.blit(surface, (0, 0))
    pygame.image.save(surface, str(data.base_path / 'welcome' / 'icon.png'))

    pause()
    pygame.display.quit()


def pause():
    while True:
        pygame.display.flip()
        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            break
        time.sleep(.1)


if __name__ == '__main__':
    main()