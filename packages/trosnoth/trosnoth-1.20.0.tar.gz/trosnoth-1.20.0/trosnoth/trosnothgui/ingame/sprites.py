import collections
import datetime
import logging
from enum import Enum
from math import pi, sin, cos, atan2
import random
import time

import pygame
import pygame.gfxdraw
from trosnoth.model.player import Player

from trosnoth.const import (
    MAP_TO_SCREEN_SCALE, COLLECTABLE_COIN_LIFETIME, TICK_PERIOD,
    DEFAULT_COIN_VALUE, HEAD_LOCATIONS, HEAD_BOT, HEAD_CUEBALL, DISCONNECT_IDLE_GHOST_AFTER,
    EMOTE_BOOGIE, EMOTE_CHARLESTON, EMOTE_WAVE, LEFT_STATE, RIGHT_STATE, JUMP_STATE, DOWN_STATE,
    HOOK_NOT_ACTIVE,
)
from trosnoth.themes import get_sprite_sheet_source_rect
from trosnoth.trosnothgui.common import setAlpha
from trosnoth.trosnothgui.ingame.nametag import (
    NameTag, CoinTally, HealthBar, CountDown,
)
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen
from trosnoth.utils.math import fadeValues, isNear
from trosnoth.model.upgrades import Shoxwave, MachineGun, Ricochet, DefaultGun

log = logging.getLogger(__name__)


class UnitSprite(pygame.sprite.Sprite):
    hard_to_see = False

    def __init__(self, app, worldGUI, unit, tweener_function=None):
        super(UnitSprite, self).__init__()
        self.app = app
        self.worldGUI = worldGUI
        self.unit = unit
        self.tweener_function = tweener_function

    def get_tween_fraction(self):
        if self.tweener_function:
            return self.tweener_function()
        return self.worldGUI.tweenFraction

    @property
    def pos(self):
        return self.do_tween()

    def do_tween(self):
        return self.unit.tweenPos(self.get_tween_fraction())


class ShotSprite(object):
    TICK_TRAIL = 1.3

    def __init__(self, app, worldGUI, shot):
        self.app = app
        self.worldGUI = worldGUI
        self.shot = shot
        self.thickness = shot.gun_type.shot_visual_radius * 2
        self.flickers = shot.gun_type.shots_flicker
        if shot.team is None:
            self.colour = app.theme.colours.neutral_shot
        else:
            self.colour = shot.team.shot_colour
        ticks = worldGUI.universe.monotonicTicks - 1
        self.draw_points = [(ticks, shot.tweenPos(0), False)]

        shot.onRebound.addListener(self.gotRebound)
        shot.onExpire.addListener(self.gotExpire)

    def get_screenshot_info(self):
        shot = self.shot
        self._addDrawPoint(self.shot.pos)
        self._discardDrawPointsBefore(self.worldGUI.universe.monotonicTicks - self.TICK_TRAIL)
        result = {
            'team': shot.team.teamName if shot.team else None,
            'points': [pos for ticks, pos, rebounded in self.draw_points],
        }
        del self.draw_points[-1]

        if shot.gun_type != DefaultGun:
            result['gun'] = shot.gun_type.gun_code
        return result

    def restore_screenshot_info(self, data):
        ticks = self.worldGUI.universe.monotonicTicks - 1
        self.draw_points = [(ticks, val, False) for val in data['points']]

    def noLongerInUniverse(self):
        if self.shot:
            self.shot.onRebound.removeListener(self.gotRebound)
            self.shot.onExpire.removeListener(self.gotExpire)
            self.shot = None

    def gotRebound(self, pos):
        self._addDrawPoint(pos, rebounded=True)

    def gotExpire(self):
        self._addDrawPoint(self.shot.pos)

    def _addDrawPoint(self, pos, rebounded=False):
        self.draw_points.append((self.worldGUI.universe.monotonicTicks, pos, rebounded))

    @property
    def pos(self):
        if self.shot:
            return self.shot.tweenPos(self.worldGUI.tweenFraction)
        return None

    def shouldRemove(self):
        if self.shot is not None:
            return False
        if len(self.draw_points) >= 2:
            return False
        return True

    def draw(self, screen, focus, area):
        wg = self.worldGUI
        worldTicks = wg.universe.monotonicTicks

        addedFinalPoint = False
        if self.shot and self.draw_points:
            tick, _, _ = self.draw_points[-1]
            if tick < worldTicks:
                addedFinalPoint = True
                self._addDrawPoint(self.shot.pos)

        ticksNow = worldTicks - 1 + wg.tweenFraction
        tickCutoff = ticksNow - self.TICK_TRAIL
        self._discardDrawPointsBefore(tickCutoff)
        self._drawPointsUntil(ticksNow, screen, focus, area)

        if addedFinalPoint:
            del self.draw_points[-1]

    def _discardDrawPointsBefore(self, tickCutoff):
        lastTick = lastPos = None
        while True:
            if not self.draw_points:
                return
            thisTick, thisPos, rebounded = self.draw_points[0]
            if thisTick >= tickCutoff:
                break
            self.draw_points.pop(0)
            lastTick, lastPos = thisTick, thisPos

        if lastTick is not None:
            fraction = (tickCutoff - lastTick) / (thisTick - lastTick)
            insertPoint = (
                fadeValues(lastPos[0], thisPos[0], fraction),
                fadeValues(lastPos[1], thisPos[1], fraction),
            )
            self.draw_points.insert(0, (tickCutoff, insertPoint, False))

    def _drawPointsUntil(self, ticksNow, screen, focus, area):
        if not self.draw_points:
            return

        # TODO
        ticks0, pos, rebounded = self.draw_points[0]
        screenPos0 = mapPosToScreen(pos, focus, area)
        points = [screenPos0]
        for ticks1, pos, rebounded in self.draw_points[1:]:
            screenPos1 = mapPosToScreen(pos, focus, area)
            if ticks1 > ticksNow:
                fraction = (ticksNow - ticks0) / (ticks1 - ticks0)
                points.append((
                    fadeValues(screenPos0[0], screenPos1[0], fraction),
                    fadeValues(screenPos0[1], screenPos1[1], fraction),
                ))
                break

            if rebounded:
                self.worldGUI.shot_rebounded(self, pos)

            points.append(screenPos1)
            screenPos0 = screenPos1
            ticks0 = ticks1

        if len(points) > 1:
            self.drawLines(screen, area, self.colour, points, thickness=self.thickness)

    def drawLines(self, screen, area, colour, points, thickness):
        rect = pygame.Rect(points[0], (thickness, thickness))
        for point in points[1:]:
            rect.union_ip(point, (thickness, thickness))
        rect.left -= thickness // 2
        rect.top -= thickness // 2

        if not rect.colliderect(area):
            return

        if self.flickers:
            alpha = random.randrange(256)
            colour = colour[:3] + (alpha,)

        if not self.app.settings.display.antialiased_shots:
            pygame.draw.lines(screen, colour, False, points, thickness)
            return

        halfThick = thickness / 2
        outline = []
        x0, y0 = points[0]
        angle = 0
        pt0 = pt5 = None
        for (x1, y1) in points[1:]:
            if (x0, y0) != (x1, y1):
                angle = atan2(y1 - y0, x1 - x0)
            sinTheta = sin(angle)
            cosTheta = cos(angle)

            pt1 = (x0 + halfThick * sinTheta, y0 - halfThick * cosTheta)
            pt2 = (x1 + halfThick * sinTheta, y1 - halfThick * cosTheta)
            pt3 = (x1 - halfThick * sinTheta, y1 + halfThick * cosTheta)
            pt4 = (x0 - halfThick * sinTheta, y0 + halfThick * cosTheta)

            outline.append(pt1)
            outline.append(pt2)
            outline.insert(0, pt4)
            outline.insert(0, pt3)

            pygame.gfxdraw.filled_polygon(screen, [pt1, pt2, pt3, pt4], colour)
            if pt0 and pt5:
                pygame.gfxdraw.filled_polygon(screen, [pt0, pt1, pt4, pt5], colour)
                pygame.gfxdraw.filled_polygon(screen, [pt0, pt1, pt5, pt4], colour)

            x0, y0 = x1, y1
            pt0 = pt1
            pt5 = pt4

        pygame.gfxdraw.aapolygon(screen, outline, colour)


class SingleAnimationSprite(pygame.sprite.Sprite):
    def __init__(self, worldGUI, pos):
        super(SingleAnimationSprite, self).__init__()
        self.app = worldGUI.app
        self.worldGUI = worldGUI
        self.pos = pos
        self.animation = self.getAnimation()
        self.image = self.animation.getImage()
        self.rect = self.image.get_rect()

    def get_screenshot_info(self):
        return {
            'pos': self.pos,
            'progress': self.animation.get_current_frame_number() / len(self.animation.images),
        }

    @classmethod
    def from_screenshot_info(cls, world_gui, data):
        result = cls(world_gui, data['pos'])
        result.animation.set_current_frame_number(data['progress'] * len(result.animation.images))
        return result

    def getAnimation(self):
        raise NotImplementedError('getAnimation')

    def update(self):
        if self.isDead():
            return
        self.image = self.animation.getImage()

    def isDead(self):
        return self.animation.isComplete()


class GrenadeExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.grenade_explosion(self.worldGUI.getTime)


class ShoxwaveExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.shoxwave_explosion(self.worldGUI.getTime)


class TrosballExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.trosballExplosion(self.worldGUI.getTime)


class BomberExplosionParticle:
    MAX_INITIAL_VEL = 1000
    GRAVITY = 1000
    SIZE = 3

    def __init__(self, pos, team, player_id=None):
        self.player_id = player_id
        self.team = team

        angle = random.random() * 2 * pi
        start = random.random()
        x = pos[0] + round(start * cos(angle) * Player.HALF_WIDTH)
        y = pos[1] + round(start * sin(angle) * Player.HALF_HEIGHT)
        self.pos = x, y

        thrust = random.random()
        self.x_vel = thrust * cos(angle) * self.MAX_INITIAL_VEL
        self.y_vel = thrust * sin(angle) * self.MAX_INITIAL_VEL
        self.image = pygame.Surface((self.SIZE, self.SIZE))

        if team is None:
            r = round(random.random() * 255)
            colour = (r, r, r)
        else:
            colour = team.shade(random.random(), random.choice([0, 1]))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.last_time = time.time()
        self.lifetime = 2

    def update(self):
        now = time.time()
        delta_t = now - self.last_time
        self.last_time = now
        self.y_vel += self.GRAVITY * delta_t
        x, y = self.pos
        self.pos = x + self.x_vel * delta_t, y + self.y_vel * delta_t
        self.lifetime -= delta_t

    def isDead(self):
        return self.lifetime <= 0


class MineExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.mine_explosion(self.worldGUI.getTime)


class GrenadeSprite(UnitSprite):
    def __init__(self, app, worldGUI, grenade):
        super(GrenadeSprite, self).__init__(app, worldGUI, grenade)
        self.grenade = grenade
        self.image = app.theme.sprites.teamGrenade(grenade.player.team)
        self.rect = self.image.get_rect()


class MineSprite(UnitSprite):
    ANGULAR_SPEED = 3   # rad/s
    hard_to_see = True

    def __init__(self, app, world_gui, mine):
        super().__init__(app, world_gui, mine)
        self.mine = mine
        self.image = self.app.theme.sprites.mine(0, None)
        self.rect = self.image.get_rect()
        self.angle = 0
        self.updated_stuck = False
        self.updated_active = False
        direction = 1 if mine.initial_angle > 0 else -1
        self.angular_velocity = self.ANGULAR_SPEED * direction
        self.x_offset = self.y_offset = 0
        self.crosshairs = DoubleCrosshairDrawer(SpriteCrosshairDrawer, world_gui, app.theme)

    def is_dangerous(self, player):
        return not self.mine.is_player_friendly(player)

    def get_health_display_fraction(self):
        local_state = self.worldGUI.gameViewer.interface.localState
        hits = local_state.projectile_monitor.get_hits(self.mine)
        if hits == 0:
            return None
        return 1 - hits / self.mine.required_detonation_beam_hits

    def draw_highlight(self, screen, focus, area):
        self.crosshairs.draw(self, screen, focus, area)

    def update(self):
        colour = None
        if self.mine.stuck:
            if self.updated_active or (self.updated_stuck and not self.mine.active):
                return
            if self.mine.active:
                if self.mine.team:
                    colour = self.mine.team.colour
                elif self.mine.player.id == self.worldGUI.localPlayerId:
                    colour = self.app.theme.colours.own_rogue_mine
                else:
                    colour = self.app.theme.colours.rogue_mine
                self.updated_active = True
            self.updated_stuck = True
            self.angle = -self.mine.stuck_angle
            self.x_offset = -2 * sin(self.angle)
            self.y_offset = -2 * cos(self.angle)
        else:
            self.angle += self.angular_velocity * TICK_PERIOD
            self.angle %= 2 * pi

        self.image = self.app.theme.sprites.mine(self.angle, colour)

    @property
    def pos(self):
        x, y = self.do_tween()
        return x + self.x_offset, y + self.y_offset


class CollectableCoinSprite(UnitSprite):
    def __init__(self, app, worldGUI, coin):
        super(CollectableCoinSprite, self).__init__(app, worldGUI, coin)
        self.coin = coin
        if coin.value >= 2 * DEFAULT_COIN_VALUE:
            self.animation = app.theme.sprites.bigCoinAnimation(
                worldGUI.getTime)
        else:
            self.animation = app.theme.sprites.coinAnimation(worldGUI.getTime)
        self.image = self.animation.getImage()
        self.alphaImage = self.image.copy()
        self.rect = self.image.get_rect()
        self.timer = worldGUI.getTime

    def update(self):
        self.image = self.animation.getImage()
        tick = self.worldGUI.universe.getMonotonicTick()
        fadeTick = self.coin.creationTick + (
                COLLECTABLE_COIN_LIFETIME - 2) // TICK_PERIOD
        if tick >= fadeTick:
            alpha = random.randint(32, 192)
            self.image = self.image.copy()
            setAlpha(self.image, alpha, alphaSurface=self.alphaImage)


class TrosballSprite(pygame.sprite.Sprite):
    def __init__(self, app, worldGUI, world):
        super(TrosballSprite, self).__init__()
        self.app = app
        self.worldGUI = worldGUI
        self.world = world
        self.localState = worldGUI.gameViewer.interface.localState
        self.animation = app.theme.sprites.trosballAnimation(worldGUI.getTime)
        self.warningAnimation = app.theme.sprites.trosballWarningAnimation(
            worldGUI.getTime)
        # Need a starting one:
        self.image = self.animation.getImage()
        self.rect = self.image.get_rect()

    def get_screenshot_info(self):
        manager = self.world.trosballManager
        if not manager.trosballPlayer:
            return {'pos': manager.trosballUnit.pos}

        result = {'player': manager.trosballPlayer.nick}
        if self.show_warning_animation():
            result['flashing'] = True

        return result

    def restore_screenshot_info(self, info):
        if info.get('flashing'):
            print('flashing!')
            self.warningAnimation = self.app.theme.sprites.trosballWarningAnimation(
                self.worldGUI.getTime, True)

    def show_warning_animation(self):
        trosball_explode_tick = self.world.trosballManager.playerGotTrosballTick + (
                self.world.physics.trosballExplodeTime // TICK_PERIOD)
        warning_tick = trosball_explode_tick - 2 // TICK_PERIOD
        print(f'{self.world.getMonotonicTick()=}, {warning_tick=}')
        return self.world.getMonotonicTick() > warning_tick

    def update(self):
        self.image = self.animation.getImage()
        manager = self.world.trosballManager
        if manager.trosballPlayer is not None:
            if self.show_warning_animation():
                self.image = self.warningAnimation.getImage()
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    @property
    def pos(self):
        manager = self.world.trosballManager
        if self.localState.localTrosball:
            x, y = self.localState.localTrosball.tweenPos(
                self.worldGUI.tweenFraction)
        elif manager.trosballUnit:
            x, y = manager.trosballUnit.tweenPos(self.worldGUI.tweenFraction)
        else:
            p = self.worldGUI.getPlayerSprite(manager.trosballPlayer.id)
            x, y = p.do_tween()
            x += 5 if p.isFacingRight() else -5
        return (x, y)


class PlayerFader:
    '''
    Used to determine how faded a player should appear. This class has
    two main accessor methods: get_player_alpha() returns the alpha to
    be used for displaying the player; get_extras_alpha() returns the
    alpha to be used for displaying the player's name and coins etc.
    This class also has a tick() method, which should be called once per
    frame, to calculate the new faded values.
    '''
    NINJA_ALPHA = 80
    GHOST_ALPHA = 128

    PLAYER_VANISH_TIME = 0.3

    def __init__(self, player_sprite):
        self.world_gui = player_sprite.worldGUI
        self.player = player_sprite.player
        self.timer = player_sprite.timer
        self.previous_time = self.timer()
        self.live_alpha = 255
        self.was_fully_visible = True

    def get_extras_alpha(self):
        if self._viewport_is_friends_with_me() or self.player.dead:
            return 255
        return self.get_player_alpha()

    def get_player_alpha(self):
        if self.player.dead:
            return self.GHOST_ALPHA
        return round(self.live_alpha)

    def tick(self):
        now = self.timer()
        self.previous_time, delta_t = now, now - self.previous_time

        previous_alpha = self.live_alpha
        target_alpha = self._get_target_alpha_value()
        was_fully_visible = self.was_fully_visible
        self.was_fully_visible = target_alpha == 255

        if self.player.dead:
            # get_extras_alpha() and get_player_alpha() both
            # short-circuit in the case that the player is dead, but
            # this ensures that there are no unwanted fading effects
            # when a player respawns.
            self.live_alpha = 255
            return

        if was_fully_visible and target_alpha != 255 and self.live_alpha != 255:
            # If the player went invisible again before the UI had drawn
            # the player as completely visible, make them fully visible
            # for a moment. This prevents momentary decloaks from being
            # imperceptible in practice.
            self.live_alpha = 255
            return

        max_alpha_change = 255 * delta_t / self.PLAYER_VANISH_TIME
        if abs(target_alpha - previous_alpha) <= max_alpha_change:
            self.live_alpha = target_alpha
        elif target_alpha > previous_alpha:
            self.live_alpha = previous_alpha + max_alpha_change
        else:
            self.live_alpha = previous_alpha - max_alpha_change

    def _get_target_alpha_value(self):
        player = self.player
        if not player.invisible:
            return 255
        if self._viewport_is_friends_with_me():
            return self.NINJA_ALPHA
        return 0

    def _viewport_is_friends_with_me(self):
        if self.world_gui.gameViewer.replay:
            return True

        target = self._get_viewport_player()
        if target is None:
            # Observer mode
            return False
        return self.player.isFriendsWith(target)

    def _get_viewport_player(self):
        target = self.world_gui.gameViewer.viewManager.target
        if isinstance(target, PlayerSprite):
            return target.player
        return None


class PlayerSprite(UnitSprite):
    # These parameters are used to create a canvas for the player sprite object
    canvasSize = (
        int(33 * MAP_TO_SCREEN_SCALE + 0.5),
        int(40 * MAP_TO_SCREEN_SCALE + 0.5))

    def __init__(self, app, worldGUI, player, *args, timer=None, **kwargs):
        super(PlayerSprite, self).__init__(app, worldGUI, player, *args, **kwargs)
        if timer is None:
            timer = self.worldGUI.getTime
        self.timer = timer
        self.drawer = PlayerDrawer(app.theme, timer)
        self._animationStart = None
        self.spriteTeam = player.team
        self.player = player
        self.nametag = NameTag(app, player.nick)
        self.countdown = CountDown(app, self.player)
        self._oldName = player.nick
        self.fader = PlayerFader(self)
        self._old_extras_alpha = self.fader.get_extras_alpha()
        self._miniMapNameTag = None
        self.coinTally = CoinTally(app, 0)
        self.healthBar = HealthBar(
            app,
            badColour=self.app.theme.colours.badHealth,
            fairColour=self.app.theme.colours.fairHealth,
            goodColour=self.app.theme.colours.goodHealth)
        self.shieldBar = HealthBar(
            app,
            badColour=self.app.theme.colours.badShield,
            fairColour=self.app.theme.colours.fairShield,
            goodColour=self.app.theme.colours.goodShield)

        sprites = app.theme.sprites
        self.sprites = sprites

        flags = pygame.SRCALPHA
        self.alphaImage = pygame.Surface(self.canvasSize, flags)

        self.image = pygame.Surface(self.canvasSize, flags)
        self.rect = self.image.get_rect()

        # This probably shouldn't be done here.
        _t = datetime.date.today()
        self.is_christmas = _t.day in (24, 25, 26) and _t.month == 12
        self.locator_ping = LocatorPing(worldGUI)

    def get_screenshot_info(self):
        result = {
            'angle': self.player.angleFacing,
            'coins': self.player.coins,
            'nick': self.player.nick,
            'head': 'bot' if self.player.bot else self.player.head,
            'pos': self.player.pos,
            'team': self.player.team.teamName if self.player.team else None,
        }
        if self.player.health != 1:
            result['health'] = self.player.health
        if self.player.readyToStart:
            result['ready'] = True

        keys = bytes(
            key[0] for key in [LEFT_STATE, RIGHT_STATE, JUMP_STATE, DOWN_STATE]
            if self.player.getState(key))
        if keys:
            result['keys'] = keys

        if (vel := (self.player.xVel, self.player.yVel)) != (0, 0):
            result['vel'] = vel

        if self.player.dead:
            if (thrust := self.player.ghostThrust) != 1:
                result['thrust'] = thrust
            if self.player.timeTillRespawn > 0:
                result['respawn_in'] = self.player.timeTillRespawn

        if self.player.grabbedSurfaceAngle:
            result['grab_surface_angle'] = self.player.grabbedSurfaceAngle

        if self.player.max_health != 1:
            result['max_health'] = self.player.max_health

        if self.player.health != 1:
            result['health'] = self.player.health

        if abilities := self.player.abilities.dumpState():
            result['abilities'] = abilities

        if emote := self.player.emote:
            result['emote'] = emote.emoteId

        hook = self.player.grapplingHook
        if hook.hookState != HOOK_NOT_ACTIVE:
            result['hook'] = hook.pos

        if reload_time := self.player.guns.reload_time:
            result['reload'] = reload_time / self.player.guns.reload_from
        gun_code = self.player.guns.selected.gun_code
        if gun_code != DefaultGun.gun_code:
            result['gun'] = gun_code
        guns = [gun.dump() for gun in self.player.guns.instances.values() if gun.ammo]
        if guns:
            result['guns'] = guns
        if items := self.player.items.dump():
            result['items'] = items

        return result

    @property
    def hookPos(self):
        oldPos, pos = self.player.getGrapplingHookPos()
        fraction = self.get_tween_fraction()
        return (
            fadeValues(oldPos[0], pos[0], fraction),
            fadeValues(oldPos[1], pos[1], fraction),
        )

    def getAngleFacing(self):
        return self.player.angleFacing

    @property
    def angleFacing(self):
        return self.player.angleFacing

    def __getattr__(self, attr):
        '''
        Proxy attributes through to the underlying player class.
        '''
        return getattr(self.player, attr)

    def update(self):
        extras_alpha = self.fader.get_extras_alpha()
        if self.player.nick != self._oldName or self._old_extras_alpha != extras_alpha:
            self._oldName = self.player.nick
            self._old_extras_alpha = extras_alpha
            self.nametag = NameTag(self.app, self.player.nick, alpha=extras_alpha)
            self._miniMapNameTag = None

        self.set_image()

    def set_image(self):
        self.image.fill((127, 127, 127, 0))
        self.image.set_colorkey((127, 127, 127))

        self.drawer.update_from_player(
            self.player, self.get_tween_fraction(), alpha=self.fader.get_player_alpha())
        self.drawer.render(self.image)

        if self.player.resyncing or self.player.was_frozen:
            self.greyOutImage()

    def greyOutImage(self):
        grey_colour = (100, 100, 100)
        grey = pygame.Surface(self.image.get_size())
        grey.fill(grey_colour)
        self.image.blit(grey, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        self.image.blit(grey, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    def getShownPlayer(self):
        target = self.worldGUI.gameViewer.viewManager.target
        if isinstance(target, PlayerSprite):
            return target.player
        return None

    def renderMiniMapNameTag(self):
        if self._miniMapNameTag:
            return self._miniMapNameTag

        nick = self.player.nick
        if len(nick) <= 3:
            shortName = nick
        else:
            for middleLetter in nick[1:-1]:
                if middleLetter.isupper():
                    break
            shortName = nick[0] + middleLetter + nick[-1]

        font = self.app.screenManager.fonts.miniMapLabelFont
        if self.player.team is None and self.player.dead:
            colour = (128, 128, 128)
        elif self.player.team is None:
            colour = (255, 255, 255)
        elif self.player.dead:
            colour = self.player.team.shade(0.3, 0.8)
        else:
            colour = self.player.team.shade(0.5, 0.5)
        HIGHLIGHT = (192, 192, 192)
        shadow = font.render(self.app, shortName, False, HIGHLIGHT)
        highlight = font.render(self.app, shortName, False, colour)
        x, y = highlight.get_size()
        xOff, yOff = 1, 1
        result = pygame.Surface((x + xOff, y + yOff)).convert()
        result.fill((0, 0, 1))
        result.set_colorkey((0, 0, 1))
        result.blit(shadow, (xOff, yOff))
        result.blit(highlight, (0, 0))
        self._miniMapNameTag = result
        return result


class PlayerAction(Enum):
    STANDING = 0
    WALKING = 1
    RUNNING = 2
    JUMPING = 3
    FALLING = 4
    GRABBING = 5
    NORMAL_GHOST = 6
    FADING_GHOST = 7


#### Spite sheets ####

SpriteSheetDefinition = collections.namedtuple(
    'SpriteSheetDefinition', 'get_sprite_sheet cell_map_width cell_map_height')


def sprite_sheet_definition(cell_map_width, cell_map_height):
    def inner(fn):
        return SpriteSheetDefinition(fn, cell_map_width, cell_map_height)
    return inner


@sprite_sheet_definition(cell_map_width=28, cell_map_height=40)
def player_sprite_sheet(sprites, flip):
    return sprites.playerSpriteSheet(flip)


@sprite_sheet_definition(cell_map_width=33, cell_map_height=39)
def ghost_sprite_sheet(sprites, flip, team_colour):
    return sprites.ghost_sprite_sheet(team_colour, flip)


#### Animations ####

SpriteSheetAnimationDefinition = collections.namedtuple(
    'SpriteSheetAnimationDefinition', 'sheet frame_rate frame_indices loop')

ghost_animation = SpriteSheetAnimationDefinition(
    sheet=ghost_sprite_sheet,
    frame_rate=0.04,
    frame_indices=(
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0),
        (15, 0), (14, 0), (13, 0), (12, 0), (11, 0), (10, 0), (9, 0),
        (8, 0), (7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0),
    ),
    loop=True,
)
fading_ghost_animation = SpriteSheetAnimationDefinition(
    sheet=ghost_sprite_sheet,
    frame_rate=.1,
    frame_indices=(
        (0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
        (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1),
        (15, 2), (14, 2), (13, 2), (12, 2), (11, 2), (10, 2), (9, 2),
        (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2), (0, 2),
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
        (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3),
    ),
    loop=False,
)
GHOST_FADE_TIME = fading_ghost_animation.frame_rate * len(fading_ghost_animation.frame_indices)

bomber_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.08, frame_indices=((11, 0), (12, 0)), loop=True)
blocker_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.1, frame_indices=((9, 0), (9, 0), (10, 0)), loop=True)
runner_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.1, frame_indices=((1, 0), (2, 0), (3, 0), (4, 0)),
    loop=True)
walker_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.1, frame_indices=((5, 0), (6, 0), (7, 0), (8, 0)),
    loop=True)
emote_boogie_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.12, frame_indices=[(i, 11) for i in range(6)],
    loop=True)
emote_charleston_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.08,
    frame_indices=[(i, 11) for i in (8, 7, 6, 7, 8, 9, 10, 9)], loop=True)
emote_wave_animation = SpriteSheetAnimationDefinition(
    sheet=player_sprite_sheet, frame_rate=0.08, frame_indices=[(i, 11) for i in range(11, 17)],
    loop=True)

EMOTE_ANIMATIONS = {
    EMOTE_BOOGIE: emote_boogie_animation,
    EMOTE_CHARLESTON: emote_charleston_animation,
    EMOTE_WAVE: emote_wave_animation,
}


#### Drawing the player ####


class PlayerDrawer:
    def __init__(
            self, theme, timer=time.time, alpha=255,
            action=PlayerAction.STANDING, gun_angle=1.57, bomber_time=None,
            emote=None, grabbed_surface_angle=None,
            grappling_hook_attached=False,
            has_shield=False, gun_type=DefaultGun,
            has_ninja=False,
            has_elephant=False, flickering=False,
            head=HEAD_CUEBALL, team_colour=(255, 255, 255), resyncing=False,
            force_frame=None, randomise_frame=False,
    ):
        self.theme = theme
        self._alpha_image = None

        self.timer = timer
        self.force_frame = force_frame
        self.randomise_frame = randomise_frame
        self.alpha = alpha
        self.action = action
        self.gun_angle = gun_angle
        self.bomber_time = bomber_time
        self.emote = emote
        self.grabbed_surface_angle = grabbed_surface_angle
        self.grappling_hook_attached = grappling_hook_attached
        self.has_shield = has_shield
        self.gun_type = gun_type
        self.has_ninja = has_ninja
        self.has_elephant = has_elephant
        self.flickering = flickering
        self.respawn_ratio = 1
        self.head = head
        self.team_colour = team_colour
        self.resyncing = resyncing
        self.last_head_details = None

        self._frame_alpha = 255

        self._animation_start = None
        self._current_animation = None
        self._current_animation_iteration = 0
        today = datetime.date.today()
        self._christmas = today.day in (24, 25, 26) and today.month == 12

    def update_from_player(self, player, fraction_through_tick, alpha=None):
        time_through_tick = fraction_through_tick * player.world.tickPeriod
        time_until_tick_completes = player.world.tickPeriod - time_through_tick

        self.gun_angle = player.angleFacing
        self.bomber_time = player.bomber.timeRemaining if player.bomber else None
        self.emote = player.emote
        self.grabbed_surface_angle = player.grabbedSurfaceAngle
        self.grappling_hook_attached = player.grapplingHook.isAttached()

        if player.dead:
            idle_time = player.ghost_has_been_idle_for - time_until_tick_completes
            if idle_time > DISCONNECT_IDLE_GHOST_AFTER - GHOST_FADE_TIME:
                self.action = PlayerAction.FADING_GHOST
            else:
                self.action = PlayerAction.NORMAL_GHOST
        elif player.getGroundCollision():
            if isNear(player.xVel, 0):
                self.action = PlayerAction.STANDING
            else:
                x_motion = player.getXKeyMotion()
                if x_motion < 0:
                    walking = player.isFacingRight()
                elif x_motion > 0:
                    walking = not player.isFacingRight()
                else:
                    walking = False
                if walking:
                    self.action = PlayerAction.WALKING
                else:
                    self.action = PlayerAction.RUNNING
        elif player.grabbedSurfaceAngle is not None:
            self.action = PlayerAction.GRABBING
        elif player.yVel > 0:
            self.action = PlayerAction.FALLING
        else:
            self.action = PlayerAction.JUMPING

        self.has_shield = player.hasVisibleShield()
        self.gun_type = type(player.current_gun)
        self.has_ninja = bool(player.ninja)
        self.has_elephant = player.hasElephant()
        self.flickering = player.is_invulnerable() and not player.world.scenario_result
        if alpha is not None:
            self.alpha = alpha

        self.respawn_ratio = 1 - ((player.timeTillRespawn + time_until_tick_completes)
                                  / player.total_respawn_time)

        if player.bot:
            self.head = HEAD_BOT
        else:
            self.head = player.head

        if player.team is None:
            self.team_colour = (255, 255, 255)
        else:
            self.team_colour = player.team.colour

        self.resyncing = player.resyncing or player.was_frozen

    @property
    def facing_right(self):
        return self.gun_angle > 0

    @property
    def has_bomber(self):
        return self.bomber_time is not None

    @property
    def dead(self):
        return self.action in (PlayerAction.NORMAL_GHOST, PlayerAction.FADING_GHOST)

    def get_head_offset(self):
        '''
        Returns the offset in game units from the player's position to
        their head position, based on the most recent frame drawn.
        '''
        if self.last_head_details is None:
            return 0, 0
        head_option, flipped = self.last_head_details
        if head_option == 2:
            x, y = -6, -11
        elif head_option == 1:
            x, y = -8, -9
        else:
            x, y = -3, -12
        if flipped:
            x = -x
        return x, y

    def setup_frame_alpha(self):
        if self.dead:
            self._frame_alpha = 128
        else:
            self._frame_alpha = self.alpha

    def multiply_frame_alpha(self, value):
        self._frame_alpha *= value / 255

    def render(self, surface):
        self.setup_frame_alpha()
        if self._frame_alpha == 0:
            return

        surface.fill((127, 127, 127, 0))
        surface.set_colorkey((127, 127, 127))

        if self.dead:
            self.render_ghost(surface)
            self.last_head_details = None
        else:
            self.render_living_player(surface)

        if self.resyncing:
            self.grey_out_image(surface)

        self.set_image_alpha(surface, round(self._frame_alpha))

    def grey_out_image(self, surface):
        grey_colour = (100, 100, 100)
        grey = pygame.Surface(surface.get_size())
        grey.fill(grey_colour)
        surface.blit(grey, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        surface.blit(grey, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    def render_ghost(self, surface):
        self.draw_ghost_image(surface, flip=not self.facing_right)

        rect = surface.get_rect()
        rect.height -= 2
        pt = (int(0.5 + rect.width * self.respawn_ratio), rect.height)
        colours = self.theme.colours
        if self.respawn_ratio >= 1:
            pygame.draw.line(surface, colours.ghostBarFull, rect.bottomleft, rect.bottomright, 3)
        else:
            pygame.draw.line(surface, colours.ghostBarEmpty, pt, rect.bottomright, 3)
            pygame.draw.line(surface, colours.ghostBarFull, pt, rect.bottomleft, 1)

    def draw_ghost_image(self, surface, flip=False):
        if self.action == PlayerAction.NORMAL_GHOST:
            self.paste_sprite_sheet_animation(surface, ghost_animation, team_colour=self.team_colour)

        elif self.action == PlayerAction.FADING_GHOST:
            if self._current_animation == ghost_animation:
                iteration, frame = self.get_iteration_and_frame(ghost_animation, do_not_start=True)
                if iteration == self._current_animation_iteration:
                    self.paste_sprite_sheet_animation(
                        surface, ghost_animation, team_colour=self.team_colour)
                    return

            self.paste_sprite_sheet_animation(
                surface, fading_ghost_animation, team_colour=self.team_colour)

    def render_living_player(self, surface):
        show_weapon = True
        regular_arms = True
        animation = False
        head_option = 0
        flipHead = not self.facing_right
        if self.has_bomber:
            self.render_bomber(surface)
            show_weapon = False
            animation = True
        elif self.emote:
            self.render_emote(surface)
            show_weapon = False
            animation = True
        elif self.action == PlayerAction.GRABBING:
            head_option, flipHead = self.render_wall_grabber(surface)
            regular_arms = False
        elif self.grappling_hook_attached:
            self.render_falling(surface)
        elif self.action == PlayerAction.STANDING:
            self.render_stander(surface)
        elif self.action == PlayerAction.WALKING:
            self.render_walker(surface)
            animation = True
        elif self.action == PlayerAction.RUNNING:
            self.render_runner(surface)
            animation = True
        elif self.action == PlayerAction.FALLING:
            self.render_falling(surface)
        else:
            self.render_jumping(surface)

        if not animation:
            self._animation_start = None
            self._current_animation = None

        self.render_head(surface, head_option, flipHead)
        self.last_head_details = (head_option, flipHead)
        if show_weapon:
            self.render_weapon(surface, regular_arms)
        if self.has_shield:
            self.render_shield(surface)

        if self.flickering:
            self.multiply_frame_alpha(random.randint(30, 150))

    def render_bomber(self, surface):
        if self.bomber_time < 0.8:
            self.paste_sprite_sheet_animation(surface, bomber_animation)
        else:
            self.paste_sprite_sheet_animation(surface, blocker_animation)

    def render_emote(self, surface):
        i, j = self.get_weapon_sprite_indices()
        if i is not None:
            dx = -5 if self.facing_right else 5
            self.paste_player_sprite_sheet(
                surface, i + 14, j, autoflip=True, offset=(dx, -10))
        self.paste_sprite_sheet_animation(surface, EMOTE_ANIMATIONS[self.emote.emoteId])

    def render_wall_grabber(self, surface):
        wall_angle = self.grabbed_surface_angle
        # wall_index: 0 = vertical wall, 7 = horizontal roof
        wall_index = int(
            max(0, min(1, abs(wall_angle * 2 / pi) - 1)) * 7 + 0.5)
        flip = wall_angle > 0 and wall_index != 7

        # gun_angle: 0 = pointing upwards, clockwise to 2*pi = pointing upwards
        gun_angle = self.gun_angle % (2 * pi)
        gun_index = int(gun_angle * 16 / pi + 0.5)
        if self.gun_type == Shoxwave:
            if self.facing_right:
                gun_index = 7
            else:
                gun_index = 26
        elif gun_index > 16:
            gun_index += 1

        if 16 <= gun_index <= 17:
            if self.facing_right:
                gun_index = 16
            else:
                gun_index = 17
        # gun_index: 0 = pointing upwards, clockwise to 33 = pointing
        # upwards, with 0 to 16 facing right and 17 to 33 facing left.
        face_right = gun_index <= 16

        # When actually pasting from the spritesheet, the x-index needs to
        # take into account whether the image will then be flipped.
        if flip:
            gun_index = 33 - gun_index
        self.paste_player_sprite_sheet(surface, gun_index, 1 + wall_index, flip=flip)

        # Calculate which head angle to use
        if 3 <= wall_index <= 6:
            # Angled head
            flip_head = flip
            if face_right ^ flip:
                head_option = 1
            else:
                head_option = 2
        else:
            # Normal head
            head_option = 0
            flip_head = not face_right

        return head_option, flip_head

    def render_stander(self, surface):
        self.paste_player_sprite_sheet(surface, 0, 0, autoflip=True)

    def render_runner(self, surface):
        self.paste_sprite_sheet_animation(surface, runner_animation)

    def render_walker(self, surface):
        self.paste_sprite_sheet_animation(surface, walker_animation)

    def render_falling(self, surface):
        self.paste_player_sprite_sheet(surface, 3, 0, autoflip=True)

    def render_jumping(self, surface):
        self.paste_player_sprite_sheet(surface, 3, 0, autoflip=True)

    def get_weapon_sprite_indices(self):
        if self.gun_type == Shoxwave:
            return None, None
        if self.gun_type == MachineGun:
            return 0, 10
        if self.gun_type == Ricochet:
            return 17, 10
        return 17, 9

    def render_weapon(self, surface, draw_arms):
        if self.gun_type == Shoxwave:
            if draw_arms:
                self.paste_player_sprite_sheet(surface, 7, 9, autoflip=True)
            self.paste_player_sprite_sheet(surface, 13, 0, autoflip=True)
            return

        x0, y0 = self.get_weapon_sprite_indices()
        angle = (self.gun_angle + pi) % (2 * pi) - pi
        index = int(abs(angle * 16 / pi) + 0.5)

        if draw_arms:
            self.paste_player_sprite_sheet(surface, index, 9, autoflip=True)
        self.paste_player_sprite_sheet(surface, x0 + index, y0, autoflip=True)

    def render_head(self, surface, head_option, flip_head):
        santa = self._christmas
        self.paste_head(surface, head_option, flip=flip_head)

        if self.has_ninja:
            santa = False
            self.paste_player_sprite_sheet(
                surface, 31 + head_option, 0, flip=flip_head)

        if self.has_elephant:
            santa = False
            self.paste_player_sprite_sheet(
                surface, 28 + head_option, 0, flip=flip_head)

        if santa:
            self.paste_player_sprite_sheet(
                surface, 25 + head_option, 0, flip=flip_head)

    def render_shield(self, surface):
        self.paste_image_animation(surface, self.theme.sprites.shieldImages, 0.15)

    def paste_player_sprite_sheet(
            self, surface, x_index, y_index, *, flip=False, autoflip=False, offset=None):

        if autoflip:
            flip = not self.facing_right

        self.paste_sprite_sheet(
            surface, x_index, y_index, flip=flip, offset=offset,
            sheet=self.theme.sprites.playerSpriteSheet(flip),
            cell_map_width=28, cell_map_height=40,
        )

    def paste_sprite_sheet(
            self, surface, x_index, y_index, *, sheet, cell_map_width, cell_map_height,
            flip=False, offset=None):
        cell_width = cell_map_width * MAP_TO_SCREEN_SCALE
        cell_height = cell_map_height * MAP_TO_SCREEN_SCALE
        x_dest = (surface.get_width() - cell_width) // 2
        y_dest = (surface.get_height() - cell_height) // 2
        if offset:
            x_dest += offset[0]
            y_dest += offset[1]
        area = get_sprite_sheet_source_rect(
            x_index, y_index,
            sheet=sheet,
            cell_map_width=cell_map_width,
            cell_map_height=cell_map_height,
            flip=flip,
        )
        surface.blit(sheet, (x_dest, y_dest), area)

    def paste_head(self, surface, head_option, *, flip=False, autoflip=False):
        dx, y_index = HEAD_LOCATIONS[self.head]
        x_index = head_option + dx

        if autoflip:
            flip = not self.facing_right

        sheet = self.theme.sprites.playerHeadSheet(self.team_colour, flip)
        self.paste_sprite_sheet(
            surface, x_index, y_index, flip=flip,
            sheet=sheet, cell_map_width=28, cell_map_height=40)

    def get_animation_elapsed_time(self, animation=None, do_not_start=False):
        if self._current_animation != animation:
            self._animation_start = None
            self._current_animation = animation
        if self._animation_start is None:
            if not do_not_start:
                self._animation_start = self.timer()
            return 0
        return self.timer() - self._animation_start

    def get_iteration_and_frame(self, animation, do_not_start=False):
        if self.force_frame is not None:
            return 0, self.force_frame

        elapsed = self.get_animation_elapsed_time(animation, do_not_start=do_not_start)
        time_index = int(elapsed // animation.frame_rate)
        iteration, frame = divmod(time_index, len(animation.frame_indices))
        if self.randomise_frame:
            frame = random.randrange(len(animation.frame_indices))
        return iteration, frame

    def paste_sprite_sheet_animation(
            self, surface, animation: SpriteSheetAnimationDefinition, autoflip=True, flip=False,
            **kwargs):
        if autoflip:
            flip = not self.facing_right

        iteration, frame = self.get_iteration_and_frame(animation)
        if iteration == 0 or animation.loop:
            x_index, y_index = animation.frame_indices[frame]
            self._current_animation_iteration = iteration
        else:
            x_index, y_index = animation.frame_indices[-1]

        sheet = animation.sheet.get_sprite_sheet(self.theme.sprites, flip, **kwargs)
        self.paste_sprite_sheet(
            surface, x_index, y_index, flip=flip, sheet=sheet,
            cell_map_width=animation.sheet.cell_map_width,
            cell_map_height=animation.sheet.cell_map_height)

    def paste_image_animation(self, surface, images, framerate):
        if self.force_frame is not None:
            image = self.force_frame
        else:
            elapsed = self.get_animation_elapsed_time()
            image = images[int(elapsed // framerate) % len(images)]

        x_dest = (surface.get_width() - image.get_width()) // 2
        y_dest = (surface.get_height() - image.get_height()) // 2
        surface.blit(image, (x_dest, y_dest))

    def set_image_alpha(self, surface, alpha):
        if self._alpha_image is None \
                or self._alpha_image.get_size() != surface.get_size():
            self._alpha_image = pygame.Surface(
                surface.get_size(), pygame.SRCALPHA)
        setAlpha(surface, alpha, alphaSurface=self._alpha_image)


class CrosshairDrawer(pygame.sprite.Sprite):
    SLOW_FPS = 30
    FRAMES = 16

    def __init__(self, worldGUI, theme, timer, frame_offset=0):
        super().__init__()
        self.worldGUI = worldGUI
        self.theme = theme
        self.timer = timer
        self.frame_offset = frame_offset
        self.index = random.randrange(16)
        self.rate = random.randrange(-2, 3) if random.randrange(2) else 0
        self.change_time = random.random() + 1
        self.last_time = timer()

    def update(self, target, focus, area):
        now = self.timer()
        delta_t = now - self.last_time
        self.last_time = now

        self.change_time -= delta_t
        if self.change_time < 0:
            self.rate = random.randrange(-2, 3) if random.randrange(2) else 0
            self.change_time = random.random() + 1

        self.index += self.rate * self.SLOW_FPS * delta_t
        self.index %= self.FRAMES

        sheet = self.theme.sprites.crosshairs_sprite_sheet
        frame_index = int(self.index + self.frame_offset)
        j, i = divmod(frame_index, 4)
        self.image = sheet.subsurface(get_sprite_sheet_source_rect(
            i, j, sheet=sheet, cell_map_width=40, cell_map_height=40))
        self.rect = self.image.get_rect()
        x, y = self.get_pos(target)
        self.rect.center = mapPosToScreen((x, y), focus, area)

    def get_pos(self, target):
        raise NotImplementedError


class SpriteCrosshairDrawer(CrosshairDrawer):
    def get_pos(self, target):
        return target.pos


class PlayerCrosshairDrawer(CrosshairDrawer):
    def get_pos(self, target):
        x, y = target.pos
        dx, dy = target.drawer.get_head_offset()
        return x + dx, y + dy


class DoubleCrosshairDrawer:
    def __init__(self, crosshair_class, world_gui, theme):
        self.outer_crosshair = crosshair_class(world_gui, theme, world_gui.getTime)
        self.inner_crosshair = crosshair_class(
            world_gui, theme, world_gui.getTime, frame_offset=16)

    def update(self, target, focus, area):
        self.outer_crosshair.update(target, focus, area)
        self.inner_crosshair.update(target, focus, area)
        return [self.outer_crosshair, self.inner_crosshair]

    def draw(self, target, screen, focus, area):
        for sprite in self.update(target, focus, area):
            screen.blit(sprite.image, sprite.rect)


class LocatorPing:
    MAX_RADIUS = 200
    EXPAND_TIME = 0.15
    HOLD_TIME = 0.6

    def __init__(self, world_gui):
        self.world_gui = world_gui
        self.timer = world_gui.getTime
        self.last_time = self.timer()
        self.relocate_in = 0
        self.centre = None

    def reset(self):
        self.relocate_in = 0

    def draw(self, screen, focus, area, pos, team):
        now = self.timer()
        delta_t = now - self.last_time
        self.last_time = now

        self.relocate_in -= delta_t
        if self.relocate_in <= 0:
            self.relocate_in = self.EXPAND_TIME + self.HOLD_TIME
            x, y = pos
            theta = random.random() * 2 * pi
            offset_amount = random.random() * self.MAX_RADIUS
            self.centre = (x + offset_amount * cos(theta), y + offset_amount * sin(theta))
            radius = 0
        elif self.relocate_in < self.HOLD_TIME:
            radius = self.MAX_RADIUS
        else:
            radius = self.MAX_RADIUS * (1 - (self.relocate_in - self.HOLD_TIME) / self.EXPAND_TIME)

        screen_centre = mapPosToScreen(self.centre, focus, area)
        screen_radius = round(radius * MAP_TO_SCREEN_SCALE)
        if team is None:
            team = self.world_gui.universe.teams[-1]
        colour = team.shade(.5, random.random())
        pygame.draw.circle(screen, colour, screen_centre, screen_radius, min(screen_radius, 2))
