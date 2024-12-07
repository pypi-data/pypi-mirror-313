'''miniMap.py - defines the MiniMap class which deals with drawing the
miniMap to the screen.'''

import random
import logging
import math

import pygame

from trosnoth.const import MAP_TO_SCREEN_SCALE, MINIMAP_PARTLY_DISRUPTED
from trosnoth.model.map import MapLayout
from trosnoth.model import mapblocks
import trosnoth.gui.framework.framework as framework
from trosnoth.model.utils import getZonesInRect
from trosnoth.model.zonemechanics import (
    get_teams_with_enough_players_to_capture,
)
from trosnoth.trosnothgui.ingame.sprites import PlayerSprite
from trosnoth.utils.utils import timeNow

log = logging.getLogger(__name__)

SHADOW_OFFSET = 1, 1


class MiniMapHexagonColours:
    def __init__(self, minimap):
        self.minimap = minimap
        self.team_colour = None
        self.team = None
        self.dark_hex = None
        self.light_hex = None

    def get_hex(self, team, dark):
        assert team is not None
        if team.colour != self.team_colour:
            self.redraw(team)
        return self.dark_hex if dark else self.light_hex

    def redraw(self, team):
        self.dark_hex = self.draw_hex(team.shade(0.4, 1))
        self.light_hex = self.draw_hex(team.shade(0.15, 0.9))
        self.team = team
        self.team_colour = team.colour

    def draw_hex(self, colour):
        dist_to_minimap = self.minimap.map_distance_to_minimap
        zone_width = MapLayout.zoneBodyWidth + 2 * MapLayout.zoneInterfaceWidth
        zone_edge_width = MapLayout.zoneInterfaceWidth
        zone_half_height = MapLayout.halfZoneHeight
        zone_height = zone_half_height * 2

        surface = pygame.Surface((dist_to_minimap((zone_width, zone_height))), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        colour += (192,)
        pygame.draw.polygon(
            surface, colour,
            (
                dist_to_minimap((0, zone_half_height)),
                dist_to_minimap((zone_edge_width, 0)),
                dist_to_minimap((zone_width - zone_edge_width, 0)),
                dist_to_minimap((zone_width, zone_half_height)),
                dist_to_minimap((zone_width - zone_edge_width, zone_height)),
                dist_to_minimap((zone_edge_width, zone_height)),
            )
        )
        return surface


class MiniMap(framework.Element):

    def __init__(self, app, scale, universeGui, viewManager):
        '''Called upon creation of a ViewManager object.  screen is a pygame
        screen object.  universe is the Universe object to draw.  target is
        either a point, a PlayerSprite object, or None.  If target is None, the
        view manager will follow the action, otherwise it will follow the
        specified point or player.'''
        super(MiniMap, self).__init__(app)
        self.universeGui = universeGui
        self.universe = universeGui.universe
        self.viewManager = viewManager
        self.disruption_status = False
        self.hex_colours = MiniMapHexagonColours(self)

        # Initialise the graphics in all the mapBlocks
        bodyBlockSize = (
            int(MapLayout.zoneBodyWidth / scale + 0.5),
            int(MapLayout.halfZoneHeight / scale + 0.5))
        self.bodyBlockRect = pygame.Rect((0,0), bodyBlockSize)

        interfaceBlockSize = (
            int(MapLayout.zoneInterfaceWidth / scale + 0.5),
            int(MapLayout.halfZoneHeight / scale + 0.5))
        self.interfaceBlockRect = pygame.Rect((0,0), interfaceBlockSize)

        # Recalculate scale based on integer-sized block rectangles
        self.scale = (
            (MapLayout.zoneBodyWidth + MapLayout.zoneInterfaceWidth + 0.)
            / (bodyBlockSize[0] + interfaceBlockSize[0]))
        self.graphicsScale = self.scale * MAP_TO_SCREEN_SCALE

        self.disruption_frame = None
        self.disruption_frame_began = 0

        # self._focus represents the point where the miniMap is currently
        # looking.
        self._focus = None
        self.updateFocus()

    def getScaledMaximumSize(self):
        x = self.app.screenManager.size[0] * 0.2775
        y = self.app.screenManager.scaledSize[1] * .35
        return x, y

    def getAbsoluteMaximumSize(self):
        # Could be aptly described as the minimum maximum
        return (300, 200)

    def getMaximumSize(self):
        size1 = self.getScaledMaximumSize()
        size2 = self.getAbsoluteMaximumSize()
        return tuple([max(size1[i], size2[i]) for i in (0,1)])

    def getUniverseScaledSize(self):
        if not self.universe.zoneBlocks:
            return (1, 1)

        universeSize = (len(self.universe.zoneBlocks[0]),
                len(self.universe.zoneBlocks))

        mapHeight = universeSize[1] * self.bodyBlockRect.height
        mapWidth = ((universeSize[0] / 2) * self.bodyBlockRect.width +
                (universeSize[0] / 2 + 1) * self.interfaceBlockRect.width)

        return (mapWidth, mapHeight)

    def getSize(self):
        size1 = self.getUniverseScaledSize()
        size2 = self.getMaximumSize()
        return tuple([min(size1[i], size2[i]) for i in (0,1)])

    def getOffset(self):
        return self.app.screenManager.size[0] - self.getSize()[0] - 5, 5

    def getRect(self):
        return pygame.Rect(self.getOffset(), self.getSize())

    def get_rect(self):
        # Temporary method so API matches that in unstable branch
        return self.getRect()

    def get_disruption_frame(self):
        now = timeNow()
        if not self.disruption_frame:
            self.disruption_frame = pygame.Surface(self.getRect().size)
        elif now <= self.disruption_frame_began + 0.1:
            return self.disruption_frame

        self.disruption_frame_began = now
        static = self.app.theme.sprites.static
        area = static.get_rect()
        area.left = random.randrange(static.get_width())
        area.top = random.randrange(static.get_height())
        x = y = 0
        while y < self.disruption_frame.get_height():
            while x < self.disruption_frame.get_width():
                r = self.disruption_frame.blit(static, (x, y), area)
                x += r.width
                area.left = 0
            x = 0
            y += r.height
            area.top = 0
        return self.disruption_frame

    def mapPosToMinimap(self, s_rect, pos):
        x, y = pos
        fx, fy = self._focus
        cx, cy = s_rect.center
        s = self.scale

        x1, y1 = round(x / s), round(y / s)
        x0, y0 = round(fx / s), round(fy / s)
        return (x1 - x0 + cx, y1 - y0 + cy)

    def map_distance_to_minimap(self, dist):
        dx, dy = dist
        s = self.scale
        return round(dx / s), round(dy / s)

    def minimap_pos_to_map(self, sRect, pos):
        x, y = pos
        fx, fy = self._focus
        cx, cy = sRect.center
        s = self.scale
        return ((x - cx) * s + fx, (y - cy) * s + fy)

    def draw(self, screen):
        '''Draws the current state of the universe at the current viewing
        location on the screen.  Does not call pygame.display.flip() .'''
        if not self.universe.map:
            return

        sRect = self.getRect()

        oldClip = screen.get_clip()
        screen.set_clip(sRect)

        colours = self.app.theme.colours
        pygame.draw.rect(screen, colours.black, sRect, 0)

        # If disrupted, draw static 95% of the time
        if self.disruption_status and random.random() > 0.05:
            screen.blit(self.get_disruption_frame(), self.getOffset())
            if self.disruption_status == MINIMAP_PARTLY_DISRUPTED and random.random() < 0.5:
                self.updateFocus()
                self.draw_friendly_zones(screen, sRect)
                self.draw_view_box(screen, sRect)
        else:
            # Update where we're looking at.
            self.updateFocus()
            frontLine = self.universe.uiOptions.getFrontLine()
            if frontLine is not None:
                self.drawShiftingBg(screen, sRect, frontLine)
            else:
                self.drawZones(screen, sRect)

            def drawCircle(sprite, colour, radius):
                pos = self.mapPosToMinimap(sRect, sprite.pos)
                if sRect.collidepoint(*pos):
                    pygame.draw.circle(screen, colour, pos, radius)

            # Draw the shots
            for shotSprite in self.universeGui.iterShots():
                shot = shotSprite.shot
                if shot and not shot.expired:
                    drawCircle(shotSprite, colours.white, 0)
            # Draw the coins
            for coin in list(self.universe.collectableCoins.values()):
                drawCircle(coin, colours.miniMapCoin, 2)

            # Draw the trosball
            sprite = self.universeGui.getTrosballSprite()
            if sprite:
                drawCircle(sprite, colours.white, 4)

            for macguffin in self.universe.uiOptions.highlight_macguffins:
                if macguffin.possessor:
                    sprite = self.universeGui.getPlayerSprite(macguffin.possessor.id)
                    drawCircle(sprite, colours.white, 4)

            # Go through and update the positions of the players on the screen.
            for playerSprite in self.universeGui.iterPlayers():
                self.drawPlayer(screen, sRect, playerSprite)

            if self.universe.uiOptions.showNets:
                for team in self.universe.teams:
                    drawCircle(
                        self.universe.trosballManager.getTargetZoneDefn(team), team.colour, 3)

            self.draw_view_box(screen, sRect)

        # Finally, draw the border
        screen.set_clip(oldClip)
        pygame.draw.rect(screen, colours.minimapBorder, sRect, 2)

    def draw_view_box(self, screen, s_rect):
        # Draw the box showing where the view is looking
        worldRect = self.viewManager.getMapRect()
        topLeft = self.mapPosToMinimap(s_rect, worldRect.topleft)
        bottomRight = self.mapPosToMinimap(s_rect, worldRect.bottomright)
        rect = pygame.Rect(topLeft, (
            bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]))
        pygame.draw.rect(screen, self.app.theme.colours.minimapViewBoxColour, rect, 1)

    def drawCircle(self, screen, sRect, sprite, colour, radius):
        pos = self.mapPosToMinimap(sRect, sprite.pos)
        if sRect.collidepoint(*pos):
            pygame.draw.circle(screen, colour, pos, radius)

    def drawPlayer(self, screen, sRect, playerSprite):
        player = playerSprite.player
        targetPlayer = self.get_target_player()
        colours = self.app.theme.colours

        if player == targetPlayer:
            # The player being drawn is the one controlled by the user.
            clr = colours.minimapOwnColour
            radius = 3
            self.drawCircle(screen, sRect, playerSprite, clr, radius)
            return

        if player.team is None and player.dead:
            clr = (128, 128, 128)
        elif player.team is None:
            clr = (255, 255, 255)
        elif player.dead:
            clr = player.team.shade(0.3, 0.8)
        else:
            clr = player.team.shade(0.5, 0.5)

        if player.dead or not (targetPlayer and player.isFriendsWith(targetPlayer)):
            radius = 2
            self.drawCircle(screen, sRect, playerSprite, clr, radius)
            return

        # Live friendly player: write letters instead of a circle
        img = playerSprite.renderMiniMapNameTag()
        rect = img.get_rect()
        rect.center = self.mapPosToMinimap(sRect, playerSprite.pos)
        screen.blit(img, rect)

    def screenToMap(self, pt):
        '''
        Converts the given point to a map position assuming it's inside the
        minimap's area.
        '''
        sRect = self.getRect()
        topCorner = [self._focus[i] - (sRect.size[i] / 2 * self.scale)
                     for i in (0,1)]
        mapOffset = ((pt[0] - sRect.left) * self.scale, (pt[1] - sRect.top) *
                self.scale)
        return (topCorner[0] + mapOffset[0], topCorner[1] + mapOffset[1])

    def drawShiftingBg(self, screen, sRect, frontLine):
        minimapTrosballPosition = self.mapPosToMinimap(
            sRect, (frontLine, 0))[0]
        colours = self.app.theme.colours
        blue = self.universe.teams[0].shade(0.4, 1)
        red = self.universe.teams[1].shade(0.4, 1)
        if minimapTrosballPosition > sRect.right:
            self.drawZones(screen, sRect, forceColour=blue)
        elif minimapTrosballPosition < sRect.left:
            self.drawZones(screen, sRect, forceColour=red)
        else:
            blueWidth = minimapTrosballPosition - sRect.left
            blueRect = pygame.Rect(sRect.left, sRect.top, blueWidth,
                    sRect.height)
            redRect = pygame.Rect(minimapTrosballPosition, sRect.top,
                    sRect.width - blueWidth, sRect.height)
            clip = screen.get_clip()
            try:
                screen.set_clip(blueRect)
                self.drawZones(screen, sRect, forceColour=blue)
                screen.set_clip(redRect)
                self.drawZones(screen, sRect, forceColour=red)
            finally:
                screen.set_clip(clip)

    def draw_friendly_zones(self, screen, s_rect):
        if not isinstance(self.viewManager.target, PlayerSprite):
            return
        team = self.viewManager.target.team
        if team is None:
            return

        x0, y0 = self.minimap_pos_to_map(s_rect, s_rect.topleft)
        x1, y1 = self.minimap_pos_to_map(s_rect, s_rect.bottomright)
        rect = pygame.Rect(x0, y0, x1 - x0, y1 - y0)
        # TODO: when merging forwards to unstable, getZonesInRect has moved
        for room in getZonesInRect(self.universe, rect):
            if room.owner != team:
                continue
            hexagon = self.hex_colours.get_hex(team, room.dark)
            r = hexagon.get_rect()
            r.center = self.mapPosToMinimap(s_rect, room.defn.pos)
            screen.blit(hexagon, r)

    def drawZones(self, screen, sRect, forceColour=None):
        '''Draws the miniMap graphics onto the screen'''
        topCorner = [self._focus[i] - (sRect.size[i] / 2 * self.scale)
                     for i in (0,1)]
        # Find which map blocks are on the screen.
        i, j = MapLayout.getMapBlockIndices(*topCorner)
        i = max(0, i)
        j = max(0, j)
        firstBlock = self.universe.zoneBlocks[i][j]


        # Set the initial position back to where it should be.
        firstPos = self.mapPosToMinimap(sRect, firstBlock.defn.rect.topleft)
        firstPos = [min(firstPos[a], sRect.topleft[a]) for a in (0, 1)]

        posToDraw = [firstPos[a] for a in (0,1)]
        y, x = i, j
        while posToDraw[1] < sRect.bottom:
            while posToDraw[0] < sRect.right:
                try:
                    block = self.universe.zoneBlocks[y][x]
                except IndexError:
                    break
                zone = None
                if isinstance(block, mapblocks.InterfaceMapBlock):
                    currentRect = self.interfaceBlockRect
                elif isinstance(block, mapblocks.BottomBodyMapBlock):
                    currentRect = self.bodyBlockRect
                    zone = block.zone
                else:
                    currentRect = self.bodyBlockRect
                currentRect.topleft = posToDraw
                area = currentRect.clip(sRect)
                draw = True
                if area.size == currentRect.size:
                    # Nothing has changed.
                    self._drawBlockMiniBg(
                        block, screen, sRect, currentRect,
                        forceColour=forceColour)
                elif area.size == (0,0):
                    # Outside the bounds of the minimap
                    draw = False
                else:
                    self._drawBlockMiniBg(
                        block, screen, sRect, currentRect, area,
                        forceColour=forceColour)

                if draw and zone:
                    self.draw_room_decoration(
                        zone, screen, sRect, currentRect.midtop)

                posToDraw[0] += currentRect.width
                x += 1
            x = j
            y += 1
            # Next Row
            posToDraw[0] = firstPos[0]
            posToDraw[1] += self.interfaceBlockRect.height

    def drawZoneLetter(self, screen, sRect, zone, centre):
        img = self.renderLetter(zone.defn.label)
        rect = img.get_rect()
        rect.center = centre
        screen.blit(img, rect)

    def get_room_highlight_and_progress(self, room):
        '''
        Returns (highlight, progress), where highlight is the highlight
        Surface or None if the room should not be highlighted, and
        progress is None or a tuple of (number, colour) where number is
        the capture progress between 0 and 1 and colour is the colour of
        the team capturing.
        '''
        if not self.universe.abilities.zoneCaps:
            return None, None

        sprites = self.app.theme.sprites

        player = self.get_target_player()
        if player is None or player.team is None:
            player_team = self.universe.teams[0]
        else:
            player_team = player.team
        owner = room.owner

        progress = room.get_capture_progress(self.universeGui.tweenFraction)
        active_players = room.get_active_players_by_team()
        teams_with_enough_players = get_teams_with_enough_players_to_capture(room)

        if progress.quick_capture or not progress.progress:
            rv_progress = None
        elif progress.attacking_team in teams_with_enough_players:
            # Attacker has a player in the room and owns an adjacent room
            rv_progress = (progress.progress, progress.attacking_team.shade(.75, .75))
        elif active_players.get(progress.attacking_team):
            # Attacker has a player in the room and owns an adjacent room
            rv_progress = (progress.progress, progress.attacking_team.shade(.5, .75))
        else:
            rv_progress = (progress.progress, progress.attacking_team.shade(.5, .5))

        if progress.can_tag:
            return sprites.zoneHighlight(
                player_team if player_team in teams_with_enough_players else progress.attacking_team,
                self.scale,
            ), rv_progress

        if not any(t for t in active_players if t != room.owner):
            # No teams have adjacent rooms
            return None, rv_progress

        defenders = min(len(active_players.get(room.owner, [])), 2)
        attackers = max(
            (len(players) for team, players in active_players.items() if team != room.owner),
            default=0)
        if attackers >= defenders:
            return sprites.zoneHighlight(None, self.scale), rv_progress
        return None, rv_progress

    def draw_room_decoration(self, zone, screen, sRect, centre):
        if not self.universe.uiOptions.showNets:
            highlight, progress = self.get_room_highlight_and_progress(zone)
            if highlight:
                rect = highlight.get_rect()
                rect.center = centre
                screen.blit(highlight, rect)
            if progress:
                progress_val, progress_colour = progress
                radius = int(300 / self.scale + .5) + 1
                rect = pygame.Rect(0, 0, 2 * radius, 2 * radius)
                rect.center = centre
                pygame.draw.arc(
                    screen,
                    progress_colour,
                    rect,
                    2 * math.pi * (.25 - progress_val),
                    math.pi / 2,
                    3,
                )
        self.drawZoneLetter(screen, sRect, zone, centre)

    def _drawBlockMiniBg(self, block, surface, sRect, rect, area=None,
            forceColour=None):
        if block.defn.kind == 'fwd':
            self._drawFwdBlockMiniBg(block, surface, rect, area, forceColour)
        elif block.defn.kind == 'bck':
            self._drawBckBlockMiniBg(block, surface, rect, area, forceColour)
        else:
            self._drawBodyBlockMiniBg(block, surface, rect, area, forceColour)
        self._drawBlockMiniArtwork(block, surface, rect, area)

    def _drawBlockMiniArtwork(self, block, surface, rect, area):
        if block.defn.graphics is None:
            return

        if area is not None:
            cropPos = (area.left - rect.left, area.top - rect.top)
            crop = pygame.rect.Rect(cropPos, area.size)
            surface.blit(block.defn.graphics.getMini(
                self.app, self.graphicsScale), area.topleft, crop)
        else:
            surface.blit(block.defn.graphics.getMini(
                self.app, self.graphicsScale), rect.topleft)

    def _drawBodyBlockMiniBg(self, block, surface, rect, area,
            forceColour=None):
        if block.zone:
            clr = (self._getMiniMapColour(block.zone) if forceColour is None
                    else forceColour)
        else:
            clr = (0, 0, 0)
        if area is not None:
            pygame.draw.rect(surface, clr, area)
        else:
            pygame.draw.rect(surface, clr, rect)

    def renderLetter(self, letter):
        if not hasattr(self, 'letters'):
            self.letters = {}
        if letter not in self.letters:
            font = self.app.screenManager.fonts.ingameMenuFont
            shadow = font.render(self.app, letter, False, (255, 255, 255))
            highlight = font.render(self.app, letter, False, (0, 0, 0))
            x, y = highlight.get_size()
            xOff, yOff = SHADOW_OFFSET
            result = pygame.Surface((x + xOff, y + yOff)).convert()
            result.fill((0, 0, 1))
            result.set_colorkey((0, 0, 1))
            result.blit(shadow, SHADOW_OFFSET)
            result.blit(highlight, (0, 0))
            self.letters[letter] = result
        return self.letters[letter]

    def _drawFwdBlockMiniBg(self, block, surface, rect, area, forceColour=None):
        if area:
            tempSurface = pygame.surface.Surface(rect.size)
            tempRect = tempSurface.get_rect()
        if block.zone1:
            clr = (self._getMiniMapColour(block.zone1) if forceColour is None
                    else forceColour)
        else:
            clr = (0, 0, 0)
        if area:
            pts = (tempRect.topleft, tempRect.topright, tempRect.bottomleft)
            pygame.draw.polygon(tempSurface, clr, pts)
        else:
            pts = (rect.topleft, rect.topright, rect.bottomleft)
            pygame.draw.polygon(surface, clr, pts)

        if block.zone2:
            clr = (self._getMiniMapColour(block.zone2) if forceColour is None
                    else forceColour)
        else:
            clr = (0, 0, 0)

        if area:
            pts = (tempRect.bottomright, tempRect.topright, tempRect.bottomleft)
            pygame.draw.polygon(tempSurface, clr, pts)
            # Now put it onto surface
            cropPos = (area.left - rect.left, area.top - rect.top)
            crop = pygame.rect.Rect(cropPos, area.size)
            surface.blit(tempSurface, area.topleft, crop)
        else:
            pts = (rect.bottomright, rect.topright, rect.bottomleft)
            pygame.draw.polygon(surface, clr, pts)

    def _drawBckBlockMiniBg(self, block, surface, rect, area, forceColour=None):
        if area:
            tempSurface = pygame.surface.Surface(rect.size)
            tempRect = tempSurface.get_rect()
        if block.zone1:
            clr = (self._getMiniMapColour(block.zone1) if forceColour is None
                    else forceColour)
        else:
            clr = (0, 0, 0)

        if area:
            pts = (tempRect.topleft, tempRect.bottomright, tempRect.bottomleft)
            pygame.draw.polygon(tempSurface, clr, pts)
        else:
            pts = (rect.topleft, rect.bottomright, rect.bottomleft)
            pygame.draw.polygon(surface, clr, pts)

        if block.zone2:
            clr = (self._getMiniMapColour(block.zone2) if forceColour is None
                    else forceColour)
        else:
            clr = (0, 0, 0)
        if area:
            pts = (tempRect.topleft, tempRect.bottomright, tempRect.topright)
            pygame.draw.polygon(tempSurface, clr, pts)
            # Now put it onto surface
            cropPos = (area.left - rect.left, area.top - rect.top)
            crop = pygame.rect.Rect(cropPos, area.size)
            surface.blit(tempSurface, area.topleft, crop)
        else:
            pts = (rect.topleft, rect.bottomright, rect.topright)
            pygame.draw.polygon(surface, clr, pts)

    def _getMiniMapColour(self, zone):
        colours = self.app.theme.colours
        if zone.owner is None:
            result = (224, 208, 224)
        elif zone.dark:
            result = zone.owner.shade(0.4, 1)
        else:
            result = zone.owner.shade(0.15, 0.9)
        return result

    # The right-most and left-most positions at which the minimap can focus
    def getBoundaries(self):
        if not self.universe.zoneBlocks:
            return (0, 0), (1, 1)
        # The edge of the map will always be an interfaceMapBlock
        indices = (len(self.universe.zoneBlocks) - 1,
                   len(self.universe.zoneBlocks[0]) - 1)

        block = self.universe.zoneBlocks[indices[0]][indices[1]]
        pos = block.defn.rect.bottomright
        sRect = self.getRect()
        rightMost = (pos[0] - sRect.size[0] * self.scale / 2,
                             pos[1] - sRect.size[1] * self.scale / 2)

        # The left-most position at which the minimap can focus
        leftMost = (sRect.size[0] * self.scale / 2,
                            sRect.size[1] * self.scale / 2)

        return rightMost, leftMost

    def get_target_player(self):
        if isinstance(self.viewManager.target, PlayerSprite):
            return self.viewManager.target.player
        return None

    def updateFocus(self):
        if isinstance(self.viewManager.target, PlayerSprite):
            self._focus = self.viewManager.target.pos
        elif self.viewManager.target is None:
            self._focus = self.viewManager._focus
        else:
            #assert isinstance(self._focus, tuple)
            self._focus = self.viewManager.target

        rightMost, leftMost = self.getBoundaries()
        self._focus = [max(min(self._focus[i], rightMost[i]), leftMost[i]) for
                i in (0,1)]

    def update_status(self, status):
        self.disruption_status = status

    def getZoneAtPoint(self, pt):
        if self.getRect().collidepoint(pt):
            x, y = self.screenToMap(pt)
            i, j = MapLayout.getMapBlockIndices(x, y)
            try:
                return self.universe.map.zoneBlocks[i][j].getZoneAtPoint(x, y)
            except IndexError:
                return None
        return None
