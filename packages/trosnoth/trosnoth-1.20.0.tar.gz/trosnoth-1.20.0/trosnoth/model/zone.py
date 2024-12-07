import dataclasses
import logging
import string
import typing

from trosnoth.const import TICKS_BEFORE_DARK_CAPTURE
from trosnoth.model.maptree import ZonePolygon
from trosnoth.model.team import Team
from trosnoth.model.zonemechanics import (
    get_teams_with_enough_players_to_capture,
)
from trosnoth.utils import math
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)


class ZoneDef(object):
    '''Stores static information about the zone.

    Attributes:
        adjacentZones - mapping from adjacent ZoneDef objects to collection of
            map blocks joining the zones.
        id - the zone id
        initialOwnerIndex - the team that initially owned this zone,
            represented as a number (0 for neutral, 1 or 2 for a team).
        pos - the coordinates of this zone in the map
    '''

    def __init__(
            self, id, initialOwnerIndex, xCoord, yCoord,
            initialDarkState=True, label=None):
        self.id = id
        self.initialOwnerIndex = initialOwnerIndex
        self.initialDarkState = initialDarkState
        self.pos = xCoord, yCoord
        self.polygon = ZonePolygon(self)

        if label:
            self.label = label
        else:
            primes, index = divmod(id, 26)
            self.label = string.ascii_uppercase[index] + '′' * primes

        self.cached_adjacentZones = set()
        self.cached_unblockedNeighbours = set()
        self.cache_serial = 0

    def __str__(self):
        if self.id is None:
            return 'Z---'
        return 'Z%3d' % self.id


class DynamicZoneLogic(object):
    '''
    Contains all the methods for performing logic about whether zones are
    capturable and what happens if they are captured.

    This serves as a useful base class for both the in-game ZoneState class,
    and simulation classes used by bots to evaluate different options.
    '''

    def __init__(self, universe, zoneDef):
        self.defn = zoneDef
        self.id = zoneDef.id
        self.world = universe
        self.adjacentZonesCache = None

        # Subclasses may initialise these differently
        self.owner = None
        self.dark = False
        self.players = set()
        self.frozen = False

    def __str__(self):
        # Debug: uniquely identify this zone within the universe.
        if self.id is None:
            return 'Z---'
        return 'Z%3d' % self.id

    @property
    def centre(self):
        # Temporary property to provide the same API that TrosnothRoom
        # does in unstable branch.
        return self.defn.pos

    @property
    def orb_pos(self):
        # Temporary property to provide the same API that TrosnothRoom
        # does in unstable branch.
        return self.defn.pos

    @property
    def respawn_pos(self):
        # Temporary property to provide the same API that TrosnothRoom
        # does in unstable branch.
        return self.defn.pos

    def can_team_respawn_here(self, team):
        return team is None or self.owner == team

    def getZoneFromDefn(self, zoneDef):
        '''
        Helper function for getAdjacentZones(), getUnblockedNeighbours(), and
        functions that rely on these. Should return the zone object that
        corresponds to the given ZoneDef.
        '''
        raise NotImplementedError('{}.getZoneFromDefn'.format(
            self.__class__.__name__))

    def isNeutral(self):
        return self.owner is None

    def isEnemyTeam(self, team):
        return team != self.owner and team is not None

    def isDark(self):
        return self.dark

    def makeDarkIfNeeded(self):
        '''This method should be called by an adjacent friendly zone that has
        been tagged and gained. It will check to see if it now has all
        surrounding orbs owned by the same team, in which case it will
        change its zone ownership.'''

        # If the zone is already owned, ignore it
        if not self.dark and self.owner is not None:
            if not self.owner.abilities.dark_zones:
                return
            for zone in self.getAdjacentZones():
                if self.isEnemyTeam(zone.owner):
                    break
            else:
                self.dark = True
                self.world.onZoneStateChanged(self)

    def getContiguousZones(self, ownerGetter=None):
        '''
        Returns a set of all contiguous zones with orb owned by the same team
        as this zone.
        '''
        if ownerGetter is None:
            ownerGetter = lambda z: z.owner

        myOwner = ownerGetter(self)
        sector = set()
        stack = [self]
        while stack:
            zone = stack.pop()
            if zone in sector:
                continue
            sector.add(zone)
            for adjacentZone in zone.getAdjacentZones():
                if ownerGetter(adjacentZone) == myOwner:
                    stack.append(adjacentZone)
        return sector

    def clear_players(self):
        self.players.clear()

    def addPlayer(self, player):
        self.players.add(player)

    def add_player(self, player):
        # Temporary function to provide the API available in unstable branch.
        self.addPlayer(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def get_living_players_by_team(self, sub_player=None):
        '''
        :param sub_player: If provided, substitutes the given player for
            the player with the same id in the world. This is useful for
            doing calculations based on where an agent's player is
            going to be in the future.
        :return: {team: players} containing all living players in this
            room.
        '''
        result = {}
        for player in self.players:
            if player.dead or (sub_player and player.id == sub_player.id):
                continue
            result.setdefault(player.team, []).append(player)

        if sub_player and sub_player.getZone() == self:
            result.setdefault(sub_player.team, []).append(sub_player)

        return result

    def get_active_players_by_team(self, sub_player=None):
        '''
        :param sub_player: If provided, substitutes the given player for
            the player with the same id in the world. This is useful for
            doing calculations based on where an agent's player is
            going to be in the future.
        :return: {team: players} containing all living players in the
            room except those whose teams own neither this room nor an
            adjacent room.
        '''
        living_players_by_team = self.get_living_players_by_team(sub_player=sub_player)
        # if not living_players_by_team:
        #     return {}

        included_teams = {self.owner} if self.owner else set()
        included_teams.update(room.owner for room in self.all_neighbours if room.owner)
        return {
            team: living_players_by_team.get(team, []) for team in included_teams
        }

    def getPlayerCounts(self, sub_player=None):
        '''
        Returns a list of (count, teams) ordered by count descending, where
        count is the number of counted (living) players in the zone
        and teams is the teams with that number of players. Excludes teams
        which do not own the zone and cannot capture it.
        '''
        teamsByCount = {}
        for team, players in self.get_living_players_by_team(sub_player=sub_player).items():
            if (
                    team != self.owner
                    and not self.adjacentToAnotherZoneOwnedBy(team)):
                # If the enemy team doesn't have an adjacent zone, they don't
                # count towards numerical advantage.
                continue
            teamsByCount.setdefault(len(players), []).append(team)

        return sorted(iter(teamsByCount.items()), reverse=True)

    def isBorderline(self):
        '''
        Returns a value indicating whether this is a borderline zone. A borderline
        zone is defined as a zone which cannot be tagged by any enemy team, but
        could be if there was one more enemy player in the zone.
        '''
        moreThanThreeDefenders = False

        playerCounts = self.getPlayerCounts()
        while playerCounts:
            count, teams = playerCounts.pop(0)
            if moreThanThreeDefenders and count < 3:
                return False

            if count == 0:
                if any(t != self.owner for t in teams):
                    # There is a team which could tag if it had one attacker
                    return True

            elif count < 3:
                if len(teams) == 1:
                    # If it's an attacking team it's capturable, if it's a
                    # defending team it's not borderline.
                    return False

                # If an attacking team had one more player they could capture
                return True

            elif count == 3:
                if moreThanThreeDefenders:
                    return True

                if len(teams) == 1:
                    # If it's an attacking team it's capturable, if it's a
                    # defending team it's not borderline.
                    return False

                # Team could capture if it had 4 attackers
                return True

            else:
                if any(t != self.owner for t in teams):
                    # Already capturable
                    return False

                moreThanThreeDefenders = True

        return False

    @property
    def all_neighbours(self):
        # Temporary property to provide the same API that TrosnothRoom
        # does in unstable branch.
        return self.getAdjacentZones()

    def getAdjacentZones(self):
        '''
        Iterates through ZoneStates adjacent to this one.
        '''
        if self.adjacentZonesCache is None:
            self.adjacentZonesCache = {
                self.world.zoneWithDef[adjZoneDef] for adjZoneDef in
                    self.world.layout.getAdjacentZoneDefs(self.defn)
            }
        return iter(self.adjacentZonesCache)

    def getNextZone(self, xDir, yDir):
        x, y = self.defn.pos
        map = self.world.map
        return map.getZoneAtPoint((
            x + xDir * (map.layout.zoneBodyWidth +
                        map.layout.zoneInterfaceWidth),
            y + yDir * 1.5 * map.layout.halfZoneHeight,
        ))

    @property
    def open_neighbours(self):
        # Temporary property to provide the same API that TrosnothRoom
        # does in unstable branch.
        return self.getUnblockedNeighbours()

    def getUnblockedNeighbours(self):
        '''
        Iterates through ZoneStates adjacent to this one which are not blocked
        off.
        '''
        for adjZoneDef in self.world.layout.getUnblockedNeighbours(self.defn):
            yield self.world.zoneWithDef[adjZoneDef]

    def adjacentToAnotherZoneOwnedBy(self, team):
        '''
        Returns whether or not this zone is adjacent to a zone whose orb is
        owned by the given team.
        '''
        for adjZone in self.getAdjacentZones():
            if adjZone.owner == team:
                return True
        return False

    def consequenceOfCapture(self):
        '''
        Uses the zone neutralisation logic to calculate how many zone points an
        enemy team would gain by capturing this zone. That is, 2 points for the
        zone itself, plus one for each zone neutralised in the process.
        '''
        if self.owner is None:
            # Always one point for capturing a neutral zone
            return 1

        dark_multiplier = 2 if self.world.abilities.slow_dark_conquest else 1

        seen = {self}
        explore = [z for z in self.getAdjacentZones() if z.owner == self.owner]
        sectors = []
        while explore:
            zone = explore.pop(0)
            if zone in seen:
                continue

            thisSector = [zone]
            score = 0
            while thisSector:
                zone = thisSector.pop(0)
                seen.add(zone)
                score += dark_multiplier if zone.dark else 1
                for z in zone.getAdjacentZones():
                    if z.owner == self.owner and z not in seen:
                        thisSector.append(z)
            sectors.append(score)

        if sectors:
            # Largest sector is not lost
            sectors.remove(max(sectors))

        # Two points for capture, plus one for each zone neutralised
        return 2 * (dark_multiplier if self.dark else 1) + sum(sectors)


@dataclasses.dataclass
class CaptureProgress:
    attacking_team: typing.Optional[Team] = None
    progress: typing.Optional[int] = None
    can_tag: bool = False
    quick_capture: bool = True


class ZoneState(DynamicZoneLogic):
    '''
    Represents information about the dynamic state of a given zone during a
    game.
    '''

    def __init__(self, universe, zoneDef):
        super(ZoneState, self).__init__(universe, zoneDef)

        universe.zoneWithDef[zoneDef] = self

        teamIndex = zoneDef.initialOwnerIndex
        if teamIndex is None:
            self.owner = None
            self.dark = False
        else:
            self.owner = universe.teams[teamIndex]
            self.dark = zoneDef.initialDarkState

            # Tell the team object that it owns one more zone
            self.owner.zoneGained()

        self.previousOwner = self.owner
        self.old_progress_to_capture = 0
        self.progress_to_capture = 0
        self.attacking_team = None

        self.on_capture_progress_complete = Event(['room'])

    def get_capture_progress(self, tween_fraction=1, sub_player=None) -> CaptureProgress:
        if not self.world.abilities.zoneCaps:
            return CaptureProgress()

        possible_teams = {
            team for team in get_teams_with_enough_players_to_capture(self, sub_player=sub_player)
            if team.abilities.zoneCaps
        }
        if not (self.dark and self.world.abilities.slow_dark_conquest):
            # Quick capture: only show whether someone can tag now
            for team in possible_teams:
                return CaptureProgress(can_tag=True, attacking_team=team)
            return CaptureProgress()

        if self.progress_to_capture is None:
            progress_fraction = None
        else:
            progress_fraction = math.fadeValues(
                self.old_progress_to_capture, self.progress_to_capture, tween_fraction
            ) / TICKS_BEFORE_DARK_CAPTURE / 4

        return CaptureProgress(
            attacking_team=self.attacking_team,
            progress=progress_fraction,
            can_tag=self.attacking_team in possible_teams and progress_fraction >= 1,
            quick_capture=False,
        )

    def advance_capture_progress(self):
        self.old_progress_to_capture = self.progress_to_capture or 0
        if not (self.dark and self.world.abilities.slow_dark_conquest):
            self.progress_to_capture = None
        else:
            if not self.progress_to_capture:
                self.attacking_team = None
                self.progress_to_capture = 0

            already_complete = self.progress_to_capture >= 4 * TICKS_BEFORE_DARK_CAPTURE

            player_counts = {
                team: len(players)
                for team, players in self.get_active_players_by_team().items()
                if players and team.abilities.zoneCaps
            }
            max_player_count = max(player_counts.values()) if player_counts else 0
            top_teams = {t for t, c in player_counts.items() if c == max_player_count}

            if not self.progress_to_capture:
                self.attacking_team = None
                self.progress_to_capture = 0
                if len(top_teams) == 1:
                    attacking_team = top_teams.pop()
                    if attacking_team != self.owner:
                        self.attacking_team = attacking_team
                        attackers = max_player_count
                        defenders = max([0] + [
                            c for t, c in player_counts.items() if t != attacking_team])
                        self.progress_to_capture = 4 * (attackers - defenders)

            elif max_player_count == 0:
                self.progress_to_capture -= 1

            elif top_teams == {self.attacking_team}:
                attackers = max_player_count
                defenders = max([0] + [
                    c for t, c in player_counts.items() if (t != self.attacking_team)])
                self.progress_to_capture += 4 * (attackers - defenders)

            elif self.attacking_team not in top_teams:
                attackers = player_counts.get(self.attacking_team, 0)
                defenders = max_player_count
                self.progress_to_capture -= 2 * (defenders - attackers)

            self.progress_to_capture = max(0, min(
                4 * TICKS_BEFORE_DARK_CAPTURE, self.progress_to_capture))

            if self.progress_to_capture >= 4 * TICKS_BEFORE_DARK_CAPTURE and not already_complete:
                self.on_capture_progress_complete(self)

    def getZoneFromDefn(self, zoneDef):
        return self.world.zoneWithDef[zoneDef]

    def tag(self, player):
        '''This method should be called when the orb in this zone is tagged'''
        self.previousOwner = self.owner
        self.dark = False

        # Inform the team objects
        if self.owner:
            self.owner.zoneLost()
        if player is not None:
            team = player.team
            if team is not None:
                team.zoneGained()
        else:
            team = None

        self.owner = team
        for zone in self.getAdjacentZones():
            if zone.owner == team or self.isNeutral():
                # Allow the adjacent zone to check if it is entirely
                # surrounded by non-enemy zones
                zone.makeDarkIfNeeded()
        self.makeDarkIfNeeded()
        self.world.onZoneStateChanged(self)

    def updateByTrosballPosition(self, position):
        self.dark = False
        oldOwner = self.owner
        if abs(position[0] - self.defn.pos[0]) < 1e-5:
            self.owner = None
        elif position[0] < self.defn.pos[0]:
            self.owner = self.world.teams[1]
        else:
            self.owner = self.world.teams[0]
        if oldOwner != self.owner:
            self.world.onZoneStateChanged(self)

    def setOwnership(self, team, dark):
        if self.owner is not None:
            self.owner.zoneLost()
        self.owner = team
        if team is not None:
            team.zoneGained()
        self.dark = dark

    def set_owner(self, team, dark=None):
        # Part of the TrosnothRoom API in the unstable branch
        if dark is None:
            dark = self.dark
        self.setOwnership(team, dark)