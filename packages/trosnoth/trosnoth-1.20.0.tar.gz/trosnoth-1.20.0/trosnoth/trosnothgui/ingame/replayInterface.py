import logging
import random

import pygame

from trosnoth.const import ACTION_LEFT, ACTION_RIGHT, ACTION_JUMP, ACTION_DOWN, ACTION_DEBUGKEY
from trosnoth.gui.framework import framework
from trosnoth.gui.keyboard import mouseButton
from trosnoth.utils import globaldebug
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


DEBUG_LOGGING = False


class ViewControlInterface(framework.Element):
    '''Interface for controlling the replay view.'''

    # The virtual keys we care about.
    nav_vkeys = frozenset([ACTION_LEFT, ACTION_RIGHT, ACTION_JUMP, ACTION_DOWN])

    def __init__(self, app, game_interface):
        super().__init__(app)

        world = game_interface.world
        self.game_interface = game_interface
        self.key_mapping = game_interface.keyMapping

        self.world = world
        self._state = dict([(k, False) for k in self.nav_vkeys])

        self.vx = 0
        self.vy = 0

    def update_state(self, state, enabled):
        self._state[state] = enabled
        if self._state[ACTION_LEFT] and not self._state[ACTION_RIGHT]:
            self.vx = -1000
        elif self._state[ACTION_RIGHT] and not self._state[ACTION_LEFT]:
            self.vx = 1000
        else:
            self.vx = 0

        if self._state[ACTION_JUMP] and not self._state[ACTION_DOWN]:
            self.vy = -1000
        elif self._state[ACTION_DOWN] and not self._state[ACTION_JUMP]:
            self.vy = 1000
        else:
            self.vy = 0

    def tick(self, deltaT):
        if self.vx != 0 or self.vy != 0:
            x, y = self.game_interface.gameViewer.viewManager.getTargetPoint()
            x += self.vx * deltaT
            y += self.vy * deltaT
            self.game_interface.gameViewer.setTarget((x, y))

    def processEvent(self, event):
        '''
        Event processing works in the following way:
        1. If there is a prompt on screen, the prompt will either use the
        event, or pass it on.
        2. If passed on, the event will be sent back to the main class, for it
        to process whether player movement uses this event. If it doesn't use
        the event, it will pass it back.
        3. If so, the hotkey manager will see if the event means anything to
        it. If not, that's the end, the event is ignored.
        '''

        # Handle events specific to in-game.
        if event.type == pygame.KEYDOWN:
            if self.process_keystroke(event.key, True):
                return None
        elif event.type == pygame.KEYUP:
            if self.process_keystroke(event.key, False):
                return None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button != 1:
            if self.process_keystroke(mouseButton(event.button), True):
                return None
        elif event.type == pygame.MOUSEBUTTONUP and event.button != 1:
            if self.process_keystroke(mouseButton(event.button), False):
                return None

        return event

    def process_keystroke(self, key, down):
        try:
            action = self.key_mapping[key]
        except KeyError:
            return False

        if __debug__ and action == ACTION_DEBUGKEY and globaldebug.enabled:
            globaldebug.debugKey = down
            return True

        if action not in self.nav_vkeys:
            return False

        self.update_state(action, down)
        return True


class ActionTracker:
    '''
    Used in replays and observer mode to automatically follow the game's
    action.
    '''
    ITERATIONS_PER_CHECK = 10
    NUM_BRACKETS = 4

    def __init__(self, world):
        self.world = world
        self.check_again_in = self.ITERATIONS_PER_CHECK
        self.tracking_player = None
        self.tracking_bracket = 3
        if world.map:
            self.last_point = world.map.centre
        else:
            self.last_point = (0, 0)

    def activate(self, current_focus):
        '''
        Called when action tracking is enabled.
        :param current_focus: the point in the map which the view is
            currently looking at.
        '''
        if DEBUG_LOGGING:
            log.error('activate()')
        self.select_target_player(near=current_focus)

    def view_was_reset(self):
        '''
        Called, for example, when a new map is applied.
        '''
        if DEBUG_LOGGING:
            log.error('view_was_reset()')
        self.select_target_player()

    def select_target_player(self, near=None):
        self.check_again_in = self.ITERATIONS_PER_CHECK
        if DEBUG_LOGGING and near:
            log.error('  looking near %s', near)

        current_player_bracket = self.NUM_BRACKETS
        if near is None and self.tracking_player:
            near = self.tracking_player.pos
            if not (self.tracking_player.dead or self.tracking_player.bomber):
                current_player_bracket, _ = self.rate_room(
                    self.tracking_player.getZone(), self.tracking_player.team)

            if DEBUG_LOGGING and near:
                log.error('  looking near previous target %s', self.tracking_player.nick)

        players_by_room_and_team = {}
        for player in self.world.players:
            if player.dead or player.bomber:
                continue
            key = (player.getZone(), player.team)
            players_by_room_and_team.setdefault(key, []).append(player)

        by_bracket = [[] for i in range(self.NUM_BRACKETS)]
        for room, team in players_by_room_and_team:
            bracket_number, score = self.rate_room(room, team)
            by_bracket[bracket_number].append((score, random.random(), room, team))

        for i, bracket in enumerate(by_bracket):
            if not bracket:
                continue

            self.tracking_bracket = i
            if DEBUG_LOGGING:
                log.error('  selected bracket %s', i)

            if current_player_bracket == i:
                if DEBUG_LOGGING:
                    log.error('  current player is still ok')
                return

            if near:
                near_room = self.world.rooms.get_at(near)
                limit_to_room = [(s, z, r, t) for s, z, r, t in bracket if r == near_room]
                if limit_to_room:
                    bracket = limit_to_room

            _, _, room, team = max(bracket)
            players = players_by_room_and_team[room, team]
            if DEBUG_LOGGING:
                log.error('  candidate players: %s', ', '.join(p.nick for p in players))
            if near:
                self.tracking_player = min(players, key=lambda p: distance(p.pos, near))
                if DEBUG_LOGGING:
                    log.error('    selected closest player: %s', self.tracking_player.nick)
            else:
                self.tracking_player = random.choice(players)
                if DEBUG_LOGGING:
                    log.error('    selected random player: %s', self.tracking_player.nick)
            return

        if DEBUG_LOGGING:
            log.error('  no live players: selected bracket 3')
        self.tracking_bracket = 3
        self.tracking_player = None

    def rate_room(self, room, team):
        if not room:
            return 0, 0
        if team is None:
            return 2, 0

        enemy = team.is_enemy_territory(room.owner)
        capturable = any(n.owner == team for n in room.all_neighbours)

        if enemy and capturable:
            zone_score = room.consequenceOfCapture()
            if zone_score > 2:
                # Top bracket: live players attacking an enemy room
                # which, if captured, would neutralise one or more
                # rooms.
                return 0, zone_score

            if room.owner.numZonesOwned == 1:
                # Also top bracket: attacking a team's final zone
                return 0, zone_score

            # Live players attacking a capturable enemy room
            return 1, zone_score

        capturable_adjacent_rooms = [
            r for r in room.all_neighbours
            if r.owner != team and any(n.owner == team for n in r.all_neighbours)]

        if any(r.owner != team for r in capturable_adjacent_rooms):
            # Live players in a room connected to a capturable enemy
            # room.
            if room.owner is None and capturable:
                # Give preference to those in a capturable neutral room
                return 1, 0
            return 1, -1

        if room.owner is None and capturable:
            # Live players attacking a capturable neutral room
            return 2, 3

        if any(r.owner is None for r in capturable_adjacent_rooms):
            # Live players in a room connected to a capturable neutral
            # room.
            return 2, 2

        if enemy:
            # Live players in other enemy rooms
            return 2, 1

        # Other live players
        return 2, 0

    def get_target(self):
        self.check_again_in -= 1
        if self.check_again_in <= 0:
            if DEBUG_LOGGING:
                log.error('periodic check')
            self.select_target_player()
        elif self.tracking_player:
            if self.tracking_player not in self.world.players:
                if DEBUG_LOGGING:
                    log.error('target player has left the game')
                self.select_target_player()
            else:
                bracket, _ = self.rate_room(
                    self.tracking_player.getZone(), self.tracking_player.team)
                if bracket < self.tracking_bracket:
                    if DEBUG_LOGGING:
                        log.error('target player has become less interesting')
                    self.select_target_player()

        if self.tracking_player:
            self.last_point = self.tracking_player.pos
        return self.last_point
