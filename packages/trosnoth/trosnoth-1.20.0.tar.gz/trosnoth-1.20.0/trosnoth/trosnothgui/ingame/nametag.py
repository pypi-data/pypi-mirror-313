

import logging

import pygame

from trosnoth.gui.common import TextImage
from trosnoth.model.upgrades import Bomber
from trosnoth.trosnothgui.common import setAlpha

log = logging.getLogger(__name__)


class NameTag(pygame.sprite.Sprite):
    '''Sprite object that every player has which indicates the player's nick.'''
    def __init__(self, app, nick, alpha=255):
        pygame.sprite.Sprite.__init__(self)
        self.app = app

        if len(nick) > 15:
            nick = nick[:13] + '...'
        self.nick = nick
        colours = app.theme.colours
        nameFont = app.fonts.nameFont
        self.image = nameFont.render(app, self.nick, True,
                colours.nameTagShadow)
        foreground = nameFont.render(app, self.nick, True,
                colours.nameTagColour)
        self.image.blit(foreground, (-2, -2))

        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        setAlpha(self.image, alpha)


class CoinTally(pygame.sprite.Sprite):
    def __init__(self, app, coins):
        pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.image = None
        self.rect = None
        self.coins = None

        self.setCoins(coins)

    def setCoins(self, coins, alpha=255):
        if self.coins == coins:
            return
        self.coins = coins

        pic = self.app.theme.sprites.smallCoin
        coinSize = pic.get_rect().size
        coins = max(coins, 0)

        flags = pygame.SRCALPHA

        if coins <= 5:
            self.image = pygame.Surface(
                (coinSize[0] * coins, coinSize[1]), flags)
            self.image.fill((255, 255, 255, 0))
            self.image.set_colorkey((255, 255, 255))

            # Blit the coins.
            for i in range(coins):
                self.image.blit(pic, (i * coinSize[0], 0))

            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface(
                (coinSize[0] * 5, coinSize[1] * 2), flags)
            self.image.fill((255, 255, 255, 0))
            self.image.set_colorkey((255, 255, 255))

            # Blit the coins.
            for i in range(5):
                self.image.blit(pic, (i * coinSize[0] - 1, 0))
            for i in range(coins-5):
                self.image.blit(pic, (i * coinSize[0] - 1, coinSize[1]))

            self.rect = self.image.get_rect()

        setAlpha(self.image, alpha)


class HealthBar(pygame.sprite.Sprite):
    WIDTH = 30
    HEIGHT = 5

    def __init__(self, app, badColour, fairColour, goodColour):
        pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.image = pygame.surface.Surface((self.WIDTH, self.HEIGHT)).convert()
        self.image.set_colorkey((0, 0, 1))
        self.rect = self.image.get_rect()

        self.badColour = badColour
        self.fairColour = fairColour
        self.goodColour = goodColour

        self.health = None
        self.maxHealth = None
        self.visible = False

    def setHealth(self, health, maxHealth, alpha=255):
        if (health, maxHealth) == (self.health, self.maxHealth):
            return
        self.health = health
        self.maxHealth = maxHealth
        if self.maxHealth == 1 or self.health == 0:
            self.visible = False
            return
        self.visible = True

        ratio = health / maxHealth
        if ratio <= 0.25 or health == 1:
            colour = self.badColour
        elif ratio <= 0.55:
            colour = self.fairColour
        else:
            colour = self.goodColour

        self.image.fill((0, 0, 1))
        r = pygame.Rect((0, 0), (self.WIDTH * ratio, self.HEIGHT))
        self.image.fill(colour, r)
        r.width = self.WIDTH
        pygame.draw.rect(
            self.image, self.app.theme.colours.healthBorder, r, 1)
        setAlpha(self.image, alpha)


def draw_health_bar(
        ratio, *,
        bad_colour, fair_colour, good_colour, border_colour,
        surface, pos, anchor='midtop',
        width=30, height=5,
    ):

    colour = bad_colour if ratio <= 0.25 else fair_colour if ratio <= 0.55 else good_colour
    outer_rect = pygame.Rect((0, 0), (width, height))
    setattr(outer_rect, anchor, pos)
    inner_rect = pygame.Rect(outer_rect.topleft, (round(width * ratio), height))
    surface.fill(colour, inner_rect)
    pygame.draw.rect(surface, border_colour, outer_rect, 1)


class CountDown(pygame.sprite.Sprite):

    def __init__(
            self, app, player, font=None, colour=None, shadowColour=None,
            backColour=None):
        pygame.sprite.Sprite.__init__(self)

        if font is None:
            font = app.fonts.countdownFont
        if colour is None:
            colour = app.theme.colours.countDownColour
        if shadowColour is None:
            shadowColour = app.theme.colours.countDownShadow

        self.app = app
        self.player = player
        self.font = font
        self.colour = colour
        self.shadowColour = shadowColour

        self.foreText = TextImage(' ', font, colour, backColour, antialias=True)
        self.shadowText = TextImage('', font, shadowColour, backColour, antialias=True)

    def update(self, alpha=255):
        bomber = self.player.items.get(Bomber)
        counter = int(5.99 * bomber.timeRemaining / bomber.totalTimeLimit)
        if counter == 0:
            text = ''
        else:
            text = str(counter)
        if text == self.foreText.text:
            return

        self.foreText.text = text
        self.shadowText.text = text

        image1 = self.foreText.getImage(self.app)
        image2 = self.shadowText.getImage(self.app)

        self.image = pygame.Surface((
            image1.get_width() + 2, image1.get_height() + 2), pygame.SRCALPHA)
        setAlpha(self.image, alpha)
        self.rect = self.image.get_rect()

        self.image.blit(image2, (2, 2))
        self.image.blit(image1, (0, 0))
