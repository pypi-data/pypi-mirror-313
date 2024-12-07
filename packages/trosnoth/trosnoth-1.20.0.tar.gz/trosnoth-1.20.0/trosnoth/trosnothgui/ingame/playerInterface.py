import logging
from math import atan2
from typing import TYPE_CHECKING

import pygame

from trosnoth.const import (
    ACTION_LEFT, ACTION_RIGHT, ACTION_JUMP, ACTION_DOWN, ACTION_HOOK,
    ACTION_RESPAWN, ACTION_USE_UPGRADE, MAP_TO_SCREEN_SCALE,
    LEFT_STATE, RIGHT_STATE, JUMP_STATE, DOWN_STATE,
    ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY,
)
from trosnoth.gui.framework import framework
from trosnoth.gui.keyboard import mouseButton
from trosnoth.messages import (
    UpdatePlayerStateMsg, AimPlayerAtMsg, GrapplingHookMsg,
)
from trosnoth.model.unit import TrajectoryClickAction
from trosnoth.trosnothgui.common import get_mouse_pos
from trosnoth.utils import globaldebug
from trosnoth.utils.math import distance

if TYPE_CHECKING:
    from trosnoth.trosnothgui.ingame.detailsInterface import DetailsInterface

log = logging.getLogger(__name__)


class PlayerInterface(framework.Element):
    '''Interface for controlling a player.'''

    # The virtual keys we care about.
    state_vkeys = {
        ACTION_LEFT: LEFT_STATE,
        ACTION_RIGHT: RIGHT_STATE,
        ACTION_JUMP: JUMP_STATE,
        ACTION_DOWN: DOWN_STATE,
    }

    NO_GHOST_THRUST_MOUSE_RADIUS = 50       # pixels
    FULL_GHOST_THRUST_MOUSE_RADIUS = 250    # pixels

    def __init__(self, app, gameInterface):
        super(PlayerInterface, self).__init__(app)

        world = gameInterface.world
        self.gameInterface = gameInterface
        self.keyMapping = None
        self._stateKeys = None
        self._hookKey = None
        self.keyMappingUpdated()

        self.receiving = True

        self.world = world
        self.worldGui = gameInterface.gameViewer.worldgui

        self.mousePos = (0, 0)
        self.discardOneMouseRel = True
        self.mouse_down = False

        # Make sure the viewer is focusing on this player.
        self.gameInterface.gameViewer.setTarget(self.playerSprite)

    def keyMappingUpdated(self):
        self.keyMapping = self.gameInterface.keyMapping
        self._stateKeys = {
            (self.keyMapping.getkey(vkey), state)
            for vkey, state in self.state_vkeys.items()
        }
        self._hookKey = self.keyMapping.getkey(ACTION_HOOK)

    def stop(self):
        pass

    @property
    def player(self):
        return self.gameInterface.localState.player

    @property
    def playerSprite(self):
        if self.player is None:
            return None
        return self.worldGui.getPlayerSprite(self.player.id)

    def tick(self, deltaT):
        if self.playerSprite is None:
            # Can happen just after PlayerInterface is removed
            return

        self.updateMouse()
        self.updatePlayerViewAngle()
        if self.player.can_shoot():
            if self.player.current_gun.can_hold_mouse and self.mouse_down:
                self._fireShot()

        # Sometimes Pygame seems to miss some keyboard events, so double
        # check here.
        if self.app.focus.focused_element is None:
            keys = pygame.key.get_pressed()
            desiredState = {
                code: keys[key] for key, code in self._stateKeys
                if key >= 0}
            changes = self.player.buildStateChanges(desiredState)
            for code, value in changes:
                self.gameInterface.sendRequest(UpdatePlayerStateMsg(value, stateKey=code))
                log.critical('Sent missing player state update: %r / %r',
                    code, value)
            if self._hookKey >= 0 and not keys[self._hookKey] and \
                    self.player.getGrapplingHook().isActive():
                self.gameInterface.sendRequest(
                    GrapplingHookMsg(False))

    def updateMouse(self):
        if self.playerSprite is None:
            return
        spritePos = self.playerSprite.rect.center
        pos = get_mouse_pos()
        self.mousePos = (pos[0] - spritePos[0], pos[1] - spritePos[1])

    def updatePlayerViewAngle(self):
        '''Updates the viewing angle of the player based on the mouse pointer
        being at the position pos. This gets its own method because it needs
        to happen as the result of a mouse motion and of the viewManager
        scrolling the screen.'''
        if self.world.paused:
            return

        di: DetailsInterface = self.gameInterface.detailsInterface
        player_is_dead = self.player and self.player.dead
        if player_is_dead and di.radialUpgradeMenu.child:
            theta = 0
            dist = 0
        elif player_is_dead and self.gameInterface.detailsInterface.trajectoryOverlay.enabled:
            # Move ghost towards the respawn point
            pos0 = self.player.pos
            room = self.player.getZone()
            if room is None:
                theta = 0
                dist = 0
            else:
                pos1 = room.respawn_pos
                theta = atan2(pos1[0] - pos0[0], -(pos1[1] - pos0[1]))
                dist = distance(pos0, pos1) * MAP_TO_SCREEN_SCALE
        else:
            dx, dy = self.mousePos
            pos = (self.playerSprite.rect.center[0] + dx,
                   self.playerSprite.rect.center[1] + dy)

            if self.playerSprite.rect.collidepoint(pos):
                return

            # Angle is measured clockwise from vertical.
            theta = atan2(dx, -dy)
            dist = (dx ** 2 + dy ** 2) ** 0.5

        # Calculate a thrust value based on distance.
        if dist < self.NO_GHOST_THRUST_MOUSE_RADIUS:
            thrust = 0.0
        elif dist > self.FULL_GHOST_THRUST_MOUSE_RADIUS:
            thrust = 1.0
        else:
            span = (
                self.FULL_GHOST_THRUST_MOUSE_RADIUS -
                self.NO_GHOST_THRUST_MOUSE_RADIUS)
            thrust = (dist - self.NO_GHOST_THRUST_MOUSE_RADIUS) / span
            thrust **= 2

        self.gameInterface.sendRequest(AimPlayerAtMsg(theta, thrust))

    def processEvent(self, event):
        '''Event processing works in the following way:
        1. If there is a prompt on screen, the prompt will either use the
        event, or pass it on.
        2. If passed on, the event will be sent back to the main class, for it
        to process whether player movement uses this event. If it doesn't use
        the event, it will pass it back.
        3. If so, the hotkey manager will see if the event means anything to
        it.  If not, that's the end, the event is ignored.
        '''

        # Handle events specific to in-game.
        di: DetailsInterface = self.gameInterface.detailsInterface
        if self.player:
            if event.type == pygame.KEYDOWN:
                self.processKeyEvent(event.key, True)
            elif event.type == pygame.KEYUP:
                self.processKeyEvent(event.key, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                    self.app.focus.clear_focus()

                    # See if trajectory overlay is showing
                    trajectory = di.trajectoryOverlay.getTrajectory()
                    if trajectory:
                        if trajectory.click_action == TrajectoryClickAction.SHOOT:
                            self._fireShot()

                        elif trajectory.click_action == TrajectoryClickAction.RESPAWN_SHOOT:
                            angle = trajectory.get_target_angle()
                            di.doAction(ACTION_RESPAWN)
                            self.gameInterface.sendRequest(AimPlayerAtMsg(angle, 1.0))
                            self._fireShot()

                        else:
                            di.doAction(ACTION_USE_UPGRADE)

                    elif self.player.dead:
                        di.doAction(ACTION_RESPAWN)
                        # Don’t immediately fire machine gun
                        self.mouse_down = False

                    elif not self.player.current_gun.can_hold_mouse:
                        self._fireShot()
                else:
                    self.processKeyEvent(mouseButton(event.button), True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
                else:
                    self.processKeyEvent(mouseButton(event.button), False)
            else:
                return event

    def processKeyEvent(self, key, keyDown):
        try:
            action = self.keyMapping[key]
        except KeyError:
            return

        if action == ACTION_HOOK:
            self.gameInterface.sendRequest(
                GrapplingHookMsg(keyDown))
            return

        if action == ACTION_SHOW_TRAJECTORY:
            di = self.gameInterface.detailsInterface
            di.trajectoryOverlay.setEnabled(keyDown)
            return

        if __debug__ and action == ACTION_DEBUGKEY and globaldebug.enabled:
            globaldebug.debugKey = keyDown
            return

        if action not in self.state_vkeys:
            return

        self.gameInterface.sendRequest(UpdatePlayerStateMsg(
            keyDown, stateKey=self.state_vkeys[action]))
        return

    def _fireShot(self):
        '''Fires a shot in the direction the player's currently looking.'''
        if self.world.paused:
            return
        self.player.current_gun.please_shoot()
