'''viewmanager.py - defines the ViewManager class which deals with drawing the
state of a universe to the screen.'''
import math
import logging
import random

import pygame
import pygame.gfxdraw

from trosnoth.const import (
    MAP_TO_SCREEN_SCALE, BODY_BLOCK_SCREEN_SIZE, INTERFACE_BLOCK_SCREEN_SIZE,
    HOOK_NOT_ACTIVE, RIGHT_STATE, MINIMAP_NORMAL,
)
from trosnoth.model.player import Player
from trosnoth.model.upgrades import Bomber, Shield, ThreatVision
from trosnoth.trosnothgui.ingame.nametag import draw_health_bar
from trosnoth.trosnothgui.ingame.replayInterface import ActionTracker
from trosnoth.utils import globaldebug
from trosnoth.utils.utils import timeNow
from trosnoth.themes import BLOCK_BACKGROUND_COLOURKEY, get_sprite_sheet_source_rect
from trosnoth.trosnothgui.ingame.minimap import MiniMap
from trosnoth.trosnothgui.ingame.utils import (
    mapPosToScreen, screenToMapPos, viewRectToMap,
)
from trosnoth.gui.framework import framework
from trosnoth.trosnothgui.ingame.leaderboard import LeaderBoard
from trosnoth.trosnothgui.ingame.statusBar import (
    ZoneProgressBar, FrontLineProgressBar)
from trosnoth.trosnothgui.ingame.gameTimer import GameTimer
from trosnoth.trosnothgui.ingame.sprites import (
    PlayerSprite, PlayerCrosshairDrawer, DoubleCrosshairDrawer,
)
from trosnoth.trosnothgui.ingame.universegui import UniverseGUI
from trosnoth.model.utils import getZonesInRect, getBlocksInRect

ZONE_SIZE = (2048, 768)

log = logging.getLogger(__name__)


class ViewManager(framework.Element):
    '''A ViewManager object takes a given universe, and displays a screenfull
    of the current state of the universe on the specified screen object.  This
    class displays only a section of the universe and no other information
    (scores, menu etc.).

    Note: self._focus represents the position that the ViewManager is currently
    looking at.  self.target is what the ViewManager should be trying to look
    at.

    self.target = None - the ViewManager will use its algorithm to follow a
        point of action.
    self.target = (x, y) - the ViewManager will look at the specified point.
    self.target = player - the ViewManager will follow the specified player.
    '''

    # The fastest speed that the viewing position can shift in pixels per sec
    maxSpeed = 1800
    acceleration = 1080

    # How far ahead of the targeted player we should look.
    lengthFromPlayer = 125

    def __init__(self, app, parent, universe: UniverseGUI, target=None, replay=False):
        '''
        Called upon creation of a ViewManager object.  screen is a pygame
        screen object.  universe is the Universe object to draw.  target is
        either a point, a PlayerSprite object, or None.  If target is None, the
        view manager will follow the action, otherwise it will follow the
        specified point or player.
        '''
        super(ViewManager, self).__init__(app)
        self.universe = universe
        self.parent = parent
        self.replay = replay

        # self._focus represents the point where the viewManager is currently
        # looking.
        if self.universe.map:
            self._focus = universe.map.centre
        else:
            self._focus = (0, 0)
        self.action_tracker = ActionTracker(universe.universe)
        self.lastUpdateTime = timeNow()
        self.speed = 0          # Speed that the focus is moving.

        self.loadingScreen = None
        self.loadingPlayer = None
        self.pauseMessage = None
        self.backgroundDrawer = BackgroundDrawer(app, universe)
        self.crosshairs = DoubleCrosshairDrawer(PlayerCrosshairDrawer, universe, app.theme)
        self.sRect = None

        # Now fill the backdrop with what we're looking at now.
        self.appResized()
        self.setTarget(target)

    def reset(self):
        self.action_tracker.view_was_reset()
        self.backgroundDrawer.reset()
        self.universe.world_was_reset()

    def stop(self):
        self.backgroundDrawer.stop()

    def tick(self, deltaT):
        if not self.active:
            return
        super(ViewManager, self).tick(deltaT)

    def appResized(self):
        self.loadingScreen = None
        self.pauseMessage = None
        self.sRect = sRect = pygame.Rect((0, 0), self.app.screenManager.size)
        centre = sRect.center
        if not self.replay:
            settings = self.app.settings.display
            sRect.width = min(settings.max_viewport_width, sRect.width)
            sRect.height = min(settings.max_viewport_height, sRect.height)
        sRect.center = centre

    def setTarget(self, target):
        '''Makes the viewManager's target the specified value.'''
        if isinstance(target, Player):
            target = self.universe.getPlayerSprite(target.id)

        self.target = target
        if isinstance(self.target, PlayerSprite):
            # Move directly to looking at player.
            self._focus = target.pos
        elif isinstance(self.target, (tuple, list)):
            self.target = self.trimTargetToMap(self.target)
        else:
            self.action_tracker.activate(self._focus)

    def getTargetPlayer(self):
        if isinstance(self.target, PlayerSprite):
            return self.target
        return None

    def getTargetPoint(self):
        '''Returns the position of the current target.'''
        if self.target is None:
            return self._focus
        return getattr(self.target, 'pos', self.target)

    def drawLoading(self, screen):
        if self.loadingPlayer is None:
            player = Player(self.universe.universe, 'Loading...', None, b'')
            player.updateState(RIGHT_STATE, True)
            self.loadingPlayer = PlayerSprite(
                self.app, self.universe, player, timer=timeNow)

        if self.loadingScreen is None:
            self.loadingScreen = pygame.Surface(screen.get_size())
            self.loadingScreen.fill((255, 255, 255))

            font = self.app.screenManager.fonts.mainMenuFont
            colour = self.app.theme.colours.mainMenuColour
            text = font.render(
                self.app, 'Loading...', True, colour, (255, 255, 255))
            r = text.get_rect()
            r.center = self.loadingScreen.get_rect().center
            self.loadingScreen.blit(text, r)

            self.loadingPlayer.rect.midbottom = r.midtop

        if random.random() < 0.03:
            self.loadingPlayer.unit.lookAt(random.random() * 2 * math.pi)

        screen.blit(self.loadingScreen, (0, 0))
        # self.loadingPlayer.update()
        # screen.fill((255, 255, 255), self.loadingPlayer.rect)
        # screen.blit(self.loadingPlayer.image, self.loadingPlayer.rect)

    def draw(self, screen, draw_scenery=True):
        '''Draws the current state of the universe at the current viewing
        location on the screen.  Does not call pygame.display.flip()'''

        if self.universe.universe.loading or not self.universe.map:
            self.drawLoading(screen)
            return

        # Update where we're looking at.
        self.updateFocus()

        if self.sRect.topleft != (0, 0):
            screen.fill((0, 0, 0))

        oldClip = screen.get_clip()

        screen.set_clip(self.sRect)
        self.backgroundDrawer.draw(screen, self.sRect, self._focus, draw_scenery)
        self._drawSprites(screen)
        self.drawOverlay(screen)
        screen.set_clip(oldClip)

    def getMapRect(self):
        '''
        :return: a Rect object in world coordinates representing the
            boundaries of the current viewport.
        '''
        return viewRectToMap(self._focus, self.sRect)

    def drawOverlay(self, screen):
        area = self.sRect

        target = self.getTargetPlayer()
        if target is not None and self.app.settings.display.show_range:
            physics = target.world.physics
            gunRange = physics.shotLifetime * physics.shotSpeed
            gunRange += max(
                target.X_SHOULDERS_TO_GUN, target.Y_SHOULDERS_TO_GUN)
            radius = int(gunRange * MAP_TO_SCREEN_SCALE + 0.5)
            pygame.draw.circle(screen, (192, 64, 64), area.center, radius, 1)

        if target and target.ninja:
            radius = int(200 * MAP_TO_SCREEN_SCALE + 0.5)
            for room in getZonesInRect(target.world, self.getMapRect()):
                if target.isFriendsWithTeam(room.owner) or room.orb_pos is None:
                    continue
                pos = mapPosToScreen(room.orb_pos, self._focus, area)
                pygame.draw.circle(screen, (128, 64, 128), pos, radius, 1)

        if self.universe.universe.paused:
            self._drawPauseMessage(screen)

    def _drawPauseMessage(self, screen):
        font = self.app.screenManager.fonts.mainMenuFont
        colour = self.app.theme.colours.pauseColour
        shadowColour = self.app.theme.colours.pauseShadow

        if not self.pauseMessage:
            message = 'PAUSED'
            offset = 3
            shadow = font.render(self.app, message, True, shadowColour)
            foreground = font.render(self.app, message, True, colour)
            width, height = foreground.get_size()
            self.pauseMessage = pygame.Surface(
                (width + offset, height + offset)).convert_alpha()
            self.pauseMessage.fill((0, 0, 0, 0))
            self.pauseMessage.blit(shadow, (offset, offset))
            self.pauseMessage.blit(foreground, (0, 0))

        rect = self.pauseMessage.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(self.pauseMessage, rect)

    def _drawSprites(self, screen):
        focus = self._focus
        area = self.sRect

        # Go through and update the positions of the players on the screen.
        extra_sprites = set()
        visible_players = set()

        target_player = self.getTargetPlayer()
        threat_vision = target_player and target_player.team and target_player.team.boosts.has(
            ThreatVision)
        for player in self.universe.iterPlayers():
            player.fader.tick()
            self.add_sprites_for_player(player, visible_players, extra_sprites)
            if not player.dead:
                self.draw_grappling_hook(screen, focus, area, player, target_player)

            if target_player:
                if threat_vision and player.invisible and not player.dead \
                        and not player.isFriendsWith(target_player):
                    player.locator_ping.draw(screen, focus, area, player.pos, player.team)
                else:
                    player.locator_ping.reset()

        # Draw the on-screen players and nametags.
        for s in visible_players:
            s.update()
            screen.blit(s.image, s.rect)
        for s in extra_sprites:
            screen.blit(s.image, s.rect)

        def draw_sprite(sprite):
            # Calculate the position of the sprite.
            sprite.rect.center = mapPosToScreen(sprite.pos, focus, area)
            if sprite.rect.colliderect(area):
                sprite.update()
                # Sometimes sprites may move slightly in update()
                sprite.rect.center = mapPosToScreen(sprite.pos, focus, area)
                screen.blit(sprite.image, sprite.rect)

        for coin in self.universe.iterCollectableCoins():
            draw_sprite(coin)

        for projectile in self.universe.iter_projectiles():
            draw_sprite(projectile)
            if threat_vision and projectile.hard_to_see and projectile.is_dangerous(target_player):
                projectile.draw_highlight(screen, focus, area)

            health_fraction = projectile.get_health_display_fraction()
            if health_fraction is not None:
                mine_x, mine_y = mapPosToScreen(projectile.pos, focus, area)
                draw_health_bar(
                    ratio=health_fraction,
                    bad_colour=self.app.theme.colours.badHealth,
                    fair_colour=self.app.theme.colours.fairHealth,
                    good_colour=self.app.theme.colours.goodHealth,
                    border_colour=self.app.theme.colours.healthBorder,
                    surface=screen, pos=(mine_x, mine_y + 5),
                )

        try:
            # Draw the grenades.
            for grenade in self.universe.iterGrenades():
                draw_sprite(grenade)
        except Exception as e:
            log.exception(str(e))

        # Draw the shots.
        for shot in self.universe.iterShots():
            shot.draw(screen, focus, area)

        for sprite in self.universe.iterExtras():
            draw_sprite(sprite)

        for animation in self.universe.special_animations:
            animation.draw(screen, focus, area)

        if __debug__ and globaldebug.enabled:
            if globaldebug.showSpriteCircles:
                for pos, radius in globaldebug.getSpriteCircles():
                    screenPos = mapPosToScreen(pos, focus, area)
                    pygame.draw.circle(
                        screen, (255, 255, 0), screenPos, radius, 2)

            for sprite in visible_players:
                sprite.player.onOverlayDebugHook(self, screen, sprite)

            if self.universe.universe.isServer:
                for region in self.universe.universe.regions:
                    region.debug_draw(self, screen)

    def draw_grappling_hook(self, screen, focus, area, player, target_player):
        extras_alpha = player.fader.get_extras_alpha()
        if extras_alpha == 0:
            return

        rope_colour = self.app.theme.colours.ropeColour
        thickness = 2

        hook = player.getGrapplingHook()
        if hook.hookState != HOOK_NOT_ACTIVE:
            # TODO: rope bending around corners
            x0, y0 = mapPosToScreen(player.pos, focus, area)
            x1, y1 = mapPosToScreen(player.hookPos, focus, area)
            if (x0, y0) != (x1, y1):
                angle = math.atan2(y1 - y0, x1 - x0)
            else:
                angle = 0
            sin_theta = math.sin(angle)
            cos_theta = math.cos(angle)

            points = (
                (x0 - thickness * sin_theta, y0 + thickness * cos_theta),
                (x0 - thickness * cos_theta, y0 - thickness * sin_theta),
                (x0 + thickness * sin_theta, y0 - thickness * cos_theta),
                (x1 + thickness * sin_theta, y1 - thickness * cos_theta),
                (x1 + thickness * cos_theta, y1 + thickness * sin_theta),
                (x1 - thickness * sin_theta, y1 + thickness * cos_theta),
            )
            pygame.gfxdraw.filled_polygon(screen, points, rope_colour)
            pygame.gfxdraw.aapolygon(screen, points, rope_colour)

    def add_sprites_for_player(self, player, visible_players, extras):
        player_alpha = player.fader.get_player_alpha()
        extras_alpha = player.fader.get_extras_alpha()

        if player_alpha == extras_alpha == 0:
            return

        # Calculate the position of the player.
        focus = self._focus
        area = self.sRect
        if player is self.getTargetPlayer():
            player.rect.center = area.center
        else:
            player.rect.center = mapPosToScreen(player.pos, focus, area)

        if not player.rect.colliderect(area):
            return

        if player_alpha > 0:
            visible_players.add(player)

        if extras is None or extras_alpha == 0:
            return

        if player.unit.items.has(Bomber) and not player.dead:
            player.countdown.update(extras_alpha)
            player.countdown.rect.midbottom = player.rect.midtop
            extras.add(player.countdown)

        last_point = player.rect.midbottom

        shield = player.unit.items.get(Shield)
        if shield:
            shield_bar = player.shieldBar
            shield_bar.setHealth(shield.protections, shield.maxProtections, alpha=extras_alpha)
            if shield_bar.visible:
                extras.add(shield_bar)
                shield_bar.rect.midtop = last_point
                last_point = shield_bar.rect.midbottom

        health_bar = player.healthBar

        health_bar.setHealth(player.unit.health, player.unit.max_health, alpha=extras_alpha)
        if health_bar.visible:
            extras.add(health_bar)
            health_bar.rect.midtop = last_point
            last_point = health_bar.rect.midbottom

        player.nametag.rect.midtop = last_point

        # Check that entire nametag's on screen.
        if player.nametag.rect.left < area.left:
            player.nametag.rect.left = area.left
        elif player.nametag.rect.right > area.right:
            player.nametag.rect.right = area.right
        if player.nametag.rect.top < area.top:
            player.nametag.rect.top = area.top
        elif player.nametag.rect.bottom > area.bottom:
            player.nametag.rect.bottom = area.bottom
        extras.add(player.nametag)

        if not player.dead:
            # Place the coin rectangle below the nametag.
            mx, my = player.nametag.rect.midbottom
            player.coinTally.setCoins(player.getCoinDisplayCount(), alpha=extras_alpha)
            player.coinTally.rect.midtop = (mx, my - 5)
            extras.add(player.coinTally)

        if player.is_juggernaut():
            extras.update(self.crosshairs.update(player, focus, area))

    def updateFocus(self):
        '''Updates the location that the ViewManager is focused on.  First
        calculates where it would ideally be focused, then moves the focus
        towards that point. The focus cannot move faster than self.maxSpeed
        pix/s, and will only accelerate or decelerate at self.acceleration
        pix/s/s. This method returns the negative of the amount scrolled by.
        This is useful for moving the backdrop by the right amount.
        '''

        # Calculate where we should be looking at.
        if isinstance(self.target, PlayerSprite):
            # Take into account where the player's looking.
            targetPt = self.target.pos

            # If the player no longer exists, look wherever we want.
            if not self.universe.hasPlayer(self.target.player):
                self.setTarget(None)
        elif isinstance(self.target, (tuple, list)):
            targetPt = self.target
        else:
            targetPt = self.action_tracker.get_target()

        # Calculate time that's passed.
        now = timeNow()
        deltaT = now - self.lastUpdateTime
        self.lastUpdateTime = now

        # Calculate distance to target.
        sTarget = sum(
            (targetPt[i] - self._focus[i]) ** 2 for i in (0, 1)) ** 0.5

        if sTarget == 0:
            return (0, 0)

        if self.target is not None:
            s = sTarget
        else:
            # Calculate the maximum velocity that will result in deceleration
            # to reach target. This is based on v**2 = u**2 + 2as
            vDecel = (2. * self.acceleration * sTarget) ** 0.5

            # Actual velocity is limited by this and maximum velocity.
            self.speed = min(
                self.maxSpeed, vDecel, self.speed + self.acceleration * deltaT)

            # Distance travelled should never overshoot the target.
            s = min(sTarget, self.speed * deltaT)

        # How far does the backdrop need to move by?
        #  (This will be negative what the focus moves by.)
        deltaBackdrop = tuple(
            -s * (targetPt[i] - self._focus[i]) / sTarget
            for i in (0, 1))

        # Calculate the new focus.
        self._focus = tuple(
            round(self._focus[i] - deltaBackdrop[i], 0) for i in (0, 1))

    def getZoneAtPoint(self, pt):
        x, y = screenToMapPos(pt, self._focus, self.sRect)
        if x < 0 or y < 0:
            return None

        return self.universe.rooms.get_at((x, y))

    def trimTargetToMap(self, targetPt):
        # No need to ever look beyond the boundary of the map
        map_rect = pygame.Rect((0, 0), self.universe.map.size)
        r = pygame.Rect(self.sRect)
        r.width //= MAP_TO_SCREEN_SCALE
        r.height //= MAP_TO_SCREEN_SCALE
        r.center = targetPt
        if r.width > map_rect.width:
            r.centerx = map_rect.centerx
        else:
            r.right = min(r.right, map_rect.right)
            r.left = max(r.left, map_rect.left)
        if r.height > map_rect.height:
            r.centery = map_rect.centery
        else:
            r.bottom = min(r.bottom, map_rect.bottom)
            r.top = max(r.top, map_rect.top)
        return r.center

    def get_screenshot_focus(self):
        return self.target.player.nick if isinstance(self.target, PlayerSprite) else self._focus

    def restore_screenshot_focus(self, focus):
        if isinstance(focus, str):
            self.setTarget([p for p in self.universe.universe.players if p.nick == focus][0])
        else:
            self._focus = focus


class BackgroundDrawer(object):
    def __init__(self, app, universe):
        self.app = app
        self.scenery = Scenery(app, universe)
        self.sBackgrounds = SolidBackgrounds(app, universe)
        self.orbs = OrbsDrawer(app, universe)
        self.debugs = DebugDrawer(app, universe)

        app.settings.display.on_detail_level_changed.addListener(
            self.detailLevelChanged)

    def stop(self):
        self.app.settings.display.on_detail_level_changed.removeListener(
            self.detailLevelChanged)

    def detailLevelChanged(self):
        self.sBackgrounds.bkgCache.clear()

    def reset(self):
        pass

    def draw(self, screen, sRect, focus, draw_scenery=True):
        if draw_scenery:
            self.scenery.draw(screen, sRect, focus)
        self.sBackgrounds.draw(screen, sRect, focus)
        self.orbs.draw(screen, sRect, focus)
        self.debugs.draw(screen, sRect, focus)


class Scenery(object):
    def __init__(self, app, universe, distance=3):
        self.app = app
        self.universe = universe
        self.image = app.theme.sprites.scenery
        self.scale = 1. / distance

    def draw(self, screen, area, focus):
        worldRect = viewRectToMap(focus, area)

        regions = []
        for block in getBlocksInRect(self.universe, worldRect):
            bd = block.defn
            pos = mapPosToScreen(bd.pos, focus, area)
            if bd.kind in ('top', 'btm'):
                if bd.zone is None:
                    regions.append(pygame.Rect(pos, BODY_BLOCK_SCREEN_SIZE))
                    continue
            elif bd.zone1 is None or bd.zone2 is None:
                regions.append(pygame.Rect(pos, INTERFACE_BLOCK_SCREEN_SIZE))
                continue

        x0, y0 = mapPosToScreen((0, 0), focus, area)
        if area.top < y0:
            r = pygame.Rect(area)
            r.bottom = y0
            regions.append(r)
        if area.left < x0:
            r = pygame.Rect(area)
            r.right = x0
            regions.append(r)

        x1, y1 = mapPosToScreen(
            self.universe.map.layout.worldSize, focus, area)
        if area.bottom > y1:
            r = pygame.Rect(area)
            r.top = y1
            regions.append(r)
        if area.right > x1:
            r = pygame.Rect(area)
            r.left = x1
            regions.append(r)

        clip = screen.get_clip()
        for region in regions:
            region = region.clip(clip)
            screen.set_clip(region)
            self.drawRegion(screen, region, worldRect.topleft)
        screen.set_clip(clip)

    def drawRegion(self, screen, area, focus):
        if not self.app.settings.display.parallax_backgrounds:
            screen.fill(BLOCK_BACKGROUND_COLOURKEY, area)
            return

        w, h = self.image.get_size()
        x = area.left - (int(round(focus[0] * self.scale + area.left)) % w)
        y0 = y = area.top - (int(round(focus[1] * self.scale + area.top)) % h)

        while x < area.right:
            while y < area.bottom:
                screen.blit(self.image, (x, y))
                y += h
            x += w
            y = y0


class SingleOrbDrawer:
    FRAME_COUNT = 120
    FRAMES_PER_ROW = 12
    FRAME_WIDTH = 80
    FRAME_HEIGHT = 80

    ANGULAR_ACCELERATION = 2
    DARK_ORB_MULTIPLIER = 1.6

    DIAG_X = 43
    DIAG_Y = 25
    VERT_Y = 50
    INDICATOR_OFFSETS = {
        (-1, -1): (-DIAG_X, -DIAG_Y),
        (0, -1): (0, -VERT_Y),
        (1, -1): (DIAG_X, -DIAG_Y),
        (-1, 1): (-DIAG_X, DIAG_Y),
        (0, 1): (0, VERT_Y),
        (1, 1): (DIAG_X, DIAG_Y),
    }

    def __init__(self, worldGUI, room):
        self.app = worldGUI.app
        self.worldGUI = worldGUI
        self.room = room
        self.world = worldGUI.universe
        self.frame = random.randrange(self.FRAME_COUNT)
        self.lastTime = worldGUI.getTime()
        self.angularVelocity = 0
        self.lastOwner = room.owner
        self.lastDark = room.dark
        if room.owner:
            self.targetAngularVelocity = random.choice([1, -1])
            if room.dark:
                self.targetAngularVelocity *= self.DARK_ORB_MULTIPLIER
        else:
            self.targetAngularVelocity = 0

    def advance_frame(self):
        t = self.worldGUI.realTime
        deltaT = t - self.lastTime
        self.lastTime = t
        if self.world.paused:
            return

        if self.lastOwner != self.room.owner or self.lastDark != \
                self.room.dark:
            if not self.room.owner:
                # Slow to stop
                self.targetAngularVelocity = 0
            elif self.lastOwner:
                # Change spin direction
                self.targetAngularVelocity = -self.targetAngularVelocity
            else:
                # Start from stopped
                self.targetAngularVelocity = random.choice([1, -1])

            if self.room.dark:
                self.targetAngularVelocity = math.copysign(
                    self.DARK_ORB_MULTIPLIER, self.targetAngularVelocity)
            self.lastOwner = self.room.owner
            self.lastDark = self.room.dark

        if self.angularVelocity < self.targetAngularVelocity:
            self.angularVelocity = min(
                self.targetAngularVelocity,
                self.angularVelocity + self.ANGULAR_ACCELERATION * deltaT)
        elif self.angularVelocity > self.targetAngularVelocity:
            self.angularVelocity = max(
                self.targetAngularVelocity,
                self.angularVelocity - self.ANGULAR_ACCELERATION * deltaT)

        if self.angularVelocity:
            self.frame += deltaT * 60 * self.angularVelocity
            self.frame %= self.FRAME_COUNT

    def draw(self, screen, focus, area):
        if self.room.orb_pos is None:
            return

        self.advance_frame()

        pic = self.app.theme.sprites.bigZoneLetter(self.room.defn.label)
        r = pic.get_rect()
        x, y = self.room.defn.pos
        r.center = mapPosToScreen((x, y + 80), focus, area)
        screen.blit(pic, r)

        if (self.worldGUI.universe.uiOptions.showNets and self.room.defn in
                self.worldGUI.map.layout.getTrosballTargetZones()):
            pic = self.app.theme.sprites.netOrb()
            frame = None
            r = pic.get_rect()
        else:
            if self.room.owner:
                colour = self.room.owner.colour
            else:
                colour = (128, 128, 128)
            pic = self.app.theme.sprites.orbs.get(colour)
            frame = self.get_sprite_sheet_rect()
            r = pygame.Rect(frame)
        r.center = mapPosToScreen(self.room.orb_pos, focus, area)
        screen.blit(pic, r, frame)

        progress = self.room.get_capture_progress(self.worldGUI.tweenFraction)
        if progress.progress is not None:
            frame_number = max(0, min(310, round(progress.progress * 310)))
            self.draw_progress_frame(
                screen,
                focus,
                area,
                progress.attacking_team,
                frame_number,
            )

        self.drawIndicator(screen, focus, area, 'F', -1, -1)
        self.drawIndicator(screen, focus, area, 'H', 0, -1)
        self.drawIndicator(screen, focus, area, 'B', 1, -1)
        self.drawIndicator(screen, focus, area, 'B', -1, 1)
        self.drawIndicator(screen, focus, area, 'H', 0, 1)
        self.drawIndicator(screen, focus, area, 'F', 1, 1)

        if progress.can_tag:
            # Draw glow
            self.draw_progress_frame(screen, focus, area, progress.attacking_team, 317)

    def draw_progress_frame(self, screen, focus, area, attacking_team, frame_number):
        if attacking_team is None:
            attacking_team = self.room.owner
        pic = self.app.theme.sprites.orb_progress.get(attacking_team.colour)
        frame = self.get_orb_progress_rect(frame_number)
        r = pygame.Rect(frame)
        r.center = mapPosToScreen(self.room.orb_pos, focus, area)
        screen.blit(pic, r, frame)

    def get_orb_progress_rect(self, index):
        y, x = divmod(index, 53)
        return get_sprite_sheet_source_rect(
            x, y,
            cell_map_width=100,
            cell_map_height=100,
        )

    def get_sprite_sheet_rect(self):
        j, i = divmod(int(self.frame), self.FRAMES_PER_ROW)
        return pygame.Rect(
            i * self.FRAME_WIDTH, j * self.FRAME_HEIGHT,
            self.FRAME_WIDTH, self.FRAME_HEIGHT)

    def drawIndicator(self, screen, focus, area, kind, xDir, yDir):
        nextZone = self.room.getNextZone(xDir, yDir)
        if nextZone is None:
            return
        img = self.app.theme.sprites.orbIndicator(kind, nextZone.owner)
        r = img.get_rect()
        x, y = self.room.defn.pos
        xOffset, yOffset = self.INDICATOR_OFFSETS[xDir, yDir]
        r.center = mapPosToScreen((x + xOffset, y + yOffset), focus, area)
        screen.blit(img, r)



class OrbsDrawer(object):
    def __init__(self, app, world):
        self.app = app
        self.world = world
        self.orbs = {}

    def get_orb(self, room):
        if room not in self.orbs:
            self.orbs[room] = SingleOrbDrawer(self.world, room)
        return self.orbs[room]

    def draw(self, screen, area, focus):
        world_rect = viewRectToMap(focus, area)

        for room in getZonesInRect(self.world, world_rect):
            self.get_orb(room).draw(screen, focus, area)


class DebugDrawer(object):
    def __init__(self, app, world):
        self.app = app
        self.universe = world

    def draw(self, screen, area, focus):
        if not __debug__:
            return
        if not (globaldebug.enabled and globaldebug.showObstacles):
            return

        worldRect = viewRectToMap(focus, area)
        for leafNode in self.universe.universe.layout.getCandidatePolygons(
                worldRect.left, worldRect.top,
                worldRect.right, worldRect.bottom):
            points = [
                mapPosToScreen(pt, focus, area)
                for pt in leafNode.get_points()]
            if leafNode.is_ledge():
                c = (255, 255, 0)
                closed = False
            else:
                c = (255, 0, 0)
                closed = True
                pygame.draw.polygon(screen, (128, 64, 128), points)
            pygame.draw.lines(screen, c, closed, points)


class SolidBackgrounds(object):
    def __init__(self, app, universe):
        self.app = app
        self.universe = universe
        self.bkgCache = BackgroundCache(app, universe)

    def draw(self, screen, area, focus):
        frontLine = self.universe.universe.uiOptions.getFrontLine()
        if frontLine is not None:
            self.drawShiftingBackground(screen, area, focus, frontLine)
        else:
            self.drawStandardBackground(screen, area, focus)

    def drawStandardBackground(self, screen, area, focus):
        worldRect = viewRectToMap(focus, area)
        for block in getBlocksInRect(self.universe, worldRect):
            pic = self.bkgCache.get(block)
            if pic is not None:
                screen.blit(pic, mapPosToScreen(block.defn.pos, focus, area))

    def drawShiftingBackground(self, screen, area, focus, trosballLocation):
        worldRect = viewRectToMap(focus, area)

        for block in getBlocksInRect(self.universe, worldRect):
            blueBlock = self.bkgCache.getForTeam(0, block)
            redBlock = self.bkgCache.getForTeam(1, block)
            if blueBlock is None or redBlock is None:
                continue

            blockHorizontalPosition = block.defn.pos[0]
            relativeLocation = trosballLocation - blockHorizontalPosition
            blockWidth = block.defn.rect.width
            relativeLocation = max(0, min(blockWidth, relativeLocation))

            x = int(relativeLocation * MAP_TO_SCREEN_SCALE + 0.5)
            topleft = mapPosToScreen(block.defn.pos, focus, area)

            r = blueBlock.get_rect()
            r.width = x
            screen.blit(blueBlock, topleft, r)

            r = redBlock.get_rect()
            r.left = x
            screen.blit(redBlock, (topleft[0] + x, topleft[1]), r)


class BackgroundCache(object):
    def __init__(self, app, universe, capacity=50):
        self.app = app
        self.universe = universe
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def clear(self):
        self.cache = {}
        self.order = []

    def getForTeam(self, teamId, block):
        backgroundPicTeam = self.app.theme.sprites.getFilledBlockBackground(
            block, self.universe.teams[teamId])
        if backgroundPicTeam is None:
            return None
        return self._getForegroundOnBackground(backgroundPicTeam, block)

    def get(self, block):
        backgroundPic = self.app.theme.sprites.blockBackground(block)
        return self._getForegroundOnBackground(backgroundPic, block)

    def _getForegroundOnBackground(self, backgroundPic, block):
        if block.defn.graphics is not None:
            foregroundPic = block.defn.graphics.getGraphic(self.app)
        else:
            foregroundPic = None

        if (backgroundPic, foregroundPic) in self.cache:
            self.order.remove((backgroundPic, foregroundPic))
            self.order.insert(0, (backgroundPic, foregroundPic))
            return self.cache[backgroundPic, foregroundPic]

        pic = self._makePic(backgroundPic, foregroundPic)
        self.cache[backgroundPic, foregroundPic] = pic
        self.order.insert(0, (backgroundPic, foregroundPic))
        if len(self.order) > self.capacity:
            del self.cache[self.order.pop(-1)]
        return pic

    def _makePic(self, backgroundPic, foregroundPic):
        if backgroundPic is None:
            return foregroundPic
        if foregroundPic is None:
            return backgroundPic
        pic = backgroundPic.copy()
        pic.blit(foregroundPic, (0, 0))
        return pic


class GameViewer(framework.CompoundElement):
    '''The gameviewer comprises a viewmanager and a minimap, which can be
    switched on or off.'''

    zoneBarHeight = 25

    def __init__(self, app, gameInterface, game, replay):
        super(GameViewer, self).__init__(app)
        self.replay = replay
        self.interface = gameInterface
        self.game = game
        self.world = game.world
        self.worldgui = UniverseGUI(app, self, self.world)
        self.app = app
        self.cached_surface_when_paused = None

        self.viewManager = ViewManager(
            self.app, self, self.worldgui, replay=replay)

        self.timerBar = GameTimer(app, game)

        self.miniMap = None
        self.leaderboard = None
        self.zoneBar = None
        self.makeWidgets()

        self.elements = [
            self.viewManager, self.zoneBar, self.timerBar, self.miniMap, self.leaderboard,
        ]
        self._screenSize = tuple(app.screenManager.size)

        self.world.uiOptions.onChange.addListener(self.uiOptionsChanged)

    def stop(self):
        self.viewManager.stop()
        self.worldgui.stop()
        self.world.uiOptions.onChange.removeListener(self.uiOptionsChanged)

    def uiOptionsChanged(self):
        self.reset(rebuildMiniMap=False)

    def getZoneAtPoint(self, pos):
        '''
        Returns the zone at the given screen position. This may be on the
        minimap or the main view.
        '''
        room = self.miniMap.getZoneAtPoint(pos)
        if room is None:
            room = self.viewManager.getZoneAtPoint(pos)
        return room

    def resizeIfNeeded(self):
        '''
        Checks whether the application has resized and adjusts accordingly.
        '''
        if self._screenSize == self.app.screenManager.size:
            return
        self._screenSize = tuple(self.app.screenManager.size)

        self.viewManager.appResized()
        # Recreate the minimap.
        self.reset()

    def reset(self, rebuildMiniMap=True):
        self.makeWidgets(rebuildMiniMap)
        self.viewManager.reset()

    def makeWidgets(self, rebuildMiniMap=True):
        if rebuildMiniMap:
            self.miniMap = MiniMap(
                self.app, 22, self.worldgui, self.viewManager)
        if self.world.uiOptions.getFrontLine() is not None:
            self.zoneBar = FrontLineProgressBar(self.app, self.world, self)
            self.leaderboard = None
        else:
            self.zoneBar = ZoneProgressBar(self.app, self.world, self)

        self.leaderboard = LeaderBoard(self.app, self.game, self)

        self.elements = [
            self.viewManager, self.zoneBar, self.timerBar, self.miniMap, self.leaderboard,
        ]

    def setTarget(self, target):
        'Target should be a player, a point, or None.'
        self.viewManager.setTarget(target)

    def draw(self, screen):
        # If the world is paused, cache our display and reuse it every frame
        if self.world.paused:
            if self.cached_surface_when_paused:
                screen.blit(self.cached_surface_when_paused, (0, 0))
                return
        else:
            self.cached_surface_when_paused = None

        super().draw(screen)

        if self.world.paused:
            self.cached_surface_when_paused = screen.copy()


    def tick(self, deltaT):
        if not self.active:
            return
        self.resizeIfNeeded()
        self.worldgui.set_tween_fraction(self.game.tweener.ui_tick(deltaT))
        self.worldgui.set_local_player_time(self.interface.local_player_driver.ui_tick(deltaT))

        target = self.viewManager.target
        if isinstance(target, PlayerSprite):
            minimap_status = target.get_minimap_status()
        else:
            minimap_status = MINIMAP_NORMAL
        self.miniMap.update_status(minimap_status)
        self.zoneBar.disrupt = minimap_status != MINIMAP_NORMAL

        super().tick(deltaT)
