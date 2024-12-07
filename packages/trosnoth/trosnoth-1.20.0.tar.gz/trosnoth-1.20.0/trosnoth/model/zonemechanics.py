

import functools

from trosnoth.const import (
    COINS_PER_ENEMY_CAP, COINS_PER_NEUTRAL_CAP,
    COINS_PER_ZONE_NEUTRALISED, COIN_FACTOR_FOR_ASSIST, TICKS_BEFORE_DARK_CAPTURE,
)
from trosnoth.messages import (
    TaggingZoneMsg, AwardPlayerCoinMsg,
)
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID, NO_PLAYER


class ZoneCaptureCalculator(object):
    def __init__(self, world):
        self.finalised = False
        self.world = world

        self.capturedZones = {}     # zone -> captureInfo
        self.coinsForZone = {}      # zone -> coins
        self.pointsForZone = {}     # zone -> points
        self.neutralisedZones = set()

    @classmethod
    def apply_to_world(cls, world):
        if world.trosballManager.enabled:
            return
        if not world.abilities.zoneCaps:
            return

        cap_info = cls(world)
        for room in world.zones:
            info = cap_info.get_current_capture_info(room)
            if not info:
                continue

            cap_info.markZoneCaptured(room, info)

        cap_info.finalise(sendNeutraliseEvent=True)

        cap_info.triggerServerEvents()
        for msg in cap_info.buildMessages():
            world.sendServerCommand(msg)

    @classmethod
    def get_current_capture_info(cls, room):
        '''
        Checks to see whether the room is being captured this tick. If
        not, return None. Otherwise, return a dict with information
        about the capture.

        The returned dict contains:
            team - the team that should now own the zone (None if zone
                neutralised due to multiple simultaneous tags)
            player - the player who captured the zone (None if zone
                neutralised due to multiple simultaneous tags)
            defenders - players in the zone who are on the defending team
            attackers - players in the zone who are on the team(s) who
                tagged the zone
        '''
        teams_to_players = room.get_living_players_by_team()
        teams_who_can_tag = get_teams_fulfilling_all_capture_conditions(room)
        tagging_players = []

        if not teams_who_can_tag:
            return None

        attackers = set()
        attacker_count = 0
        for team in teams_who_can_tag:
            attacker_count = len(teams_to_players[team])
            for player in teams_to_players[team]:
                if player.is_touching_orb() and player.abilities.orb_capture:
                    tagging_players.append(player)
                    attackers.update(teams_to_players[team])
                    # Only allow one player from each team to have tagged it.
                    break

        defenders = set(teams_to_players.get(room.owner, []))
        defender_touching_orb = any(
            p.is_touching_orb() and p.abilities.orb_capture for p in defenders)
        if defender_touching_orb and attacker_count <= len(defenders):
            # You don't get to capture if the defender could
            # immediately recapture.
            return None

        result = {
            'attackers': attackers,
            'defenders': defenders,
        }
        if len(tagging_players) > 1:
            # Both teams tagged - becomes neutral
            if room.owner is None:
                return None

            result['player'] = None
            result['team'] = None
        elif len(tagging_players) == 1:
            result['player'] = tagging_players[0]
            result['team'] = tagging_players[0].team
        else:
            return None

        return result

    def markZoneCaptured(self, zone, captureInfo):
        if self.finalised:
            raise RuntimeError('already finalised')
        if zone in self.capturedZones:
            raise ValueError('zone cannot be captured twice in one tick')
        team = captureInfo['team']
        if team == zone.owner:
            raise ValueError('zone is already owned by that team')

        factor = self.world.scenarioManager.level.coins_for_caps_factor
        if team is None:
            coins = COINS_PER_ZONE_NEUTRALISED
            points = 1
        elif zone.owner:
            coins = COINS_PER_ENEMY_CAP
            points = 2
        else:
            coins = COINS_PER_NEUTRAL_CAP
            points = 1

        self.capturedZones[zone] = captureInfo
        self.coinsForZone[zone] = round(coins * factor)
        self.pointsForZone[zone] = points

    def getOwner(self, zone):
        if zone in self.capturedZones:
            return self.capturedZones[zone]['team']
        return zone.owner

    def finalise(self, sendNeutraliseEvent=False):
        if self.finalised:
            return
        self.finalised = True
        if not self.capturedZones:
            return

        factor = self.world.scenarioManager.level.coins_for_caps_factor

        teamSectors = self.getTeamSectors()

        for team, sectors in list(teamSectors.items()):
            if len(sectors) <= 1:
                continue

            self.removeBestSectorFromList(team, sectors)
            for sector in sectors:
                self.neutralisedZones.update(sector)
                coinsToAward = len(sector) * COINS_PER_ZONE_NEUTRALISED * factor
                cappedZones = self.getCapsRelatedToNeutralisedSector(
                    team, sector)
                coinsPerZone = int(coinsToAward / len(cappedZones) + 0.5)
                pointsPerZone = len(sector) / len(cappedZones)
                for zone in cappedZones:
                    self.coinsForZone[zone] += coinsPerZone
                    self.pointsForZone[zone] += pointsPerZone
                    if sendNeutraliseEvent:
                        tagger = self.capturedZones[zone]['player']
                        if tagger:
                            tagger.onNeutralisedSector(len(sector))

    def getTeamSectors(self):
        seenZones = set()
        teamSectors = dict((team, []) for team in self.world.teams)
        for zone in self.world.zones:
            if zone in seenZones:
                continue
            if self.getOwner(zone) is None:
                continue
            sector = zone.getContiguousZones(ownerGetter=self.getOwner)
            teamSectors[self.getOwner(zone)].append(sector)
            seenZones.update(sector)
        return teamSectors

    def removeBestSectorFromList(self, team, sectors):
        '''
        Accepts team and list of sectors, selects which one that team should
        keep, returns the rest.
        '''
        key = functools.partial(self.getSectorGoodnessKey, team)
        goodSector = max(sectors, key=key)
        sectors.remove(goodSector)

    def getSectorGoodnessKey(self, team, sector):
        '''
        Returns a key by which sectors can be sorted with sectors which should
        be kept sorted as maximum.
        '''
        livePlayerCount = 0
        deadPlayerCount = 0
        darkZoneCount = 0
        for zone in sector:
            for player in zone.players:
                if player.team == team:
                    if player.dead:
                        deadPlayerCount += 1
                    else:
                        livePlayerCount += 1
            if zone.isDark():
                darkZoneCount += 1

        if self.world.abilities.slow_dark_conquest:
            return (len(sector), darkZoneCount, livePlayerCount, deadPlayerCount)

        return (len(sector), livePlayerCount, darkZoneCount, deadPlayerCount)

    def getCapsRelatedToNeutralisedSector(self, oldOwner, sector):
        '''
        Goes through the registered zone captures and finds which ones
        contributed to the neutralisation of this sector. Usually this will
        just be a single zone, but in some rare cases multiple captures
        during the some tick will have together caused the neutralisation.
        '''
        result = set()
        for zone, captureInfo in list(self.capturedZones.items()):
            if captureInfo['team'] == oldOwner:
                # A capture for a given team cannot count towards
                # neutralising the same team's zones.
                continue
            if any(z in sector for z in zone.getAdjacentZones()):
                result.add(zone)
        return result

    def triggerServerEvents(self):
        if not self.finalised:
            self.finalise()

        for zone, captureInfo in list(self.capturedZones.items()):
            points = self.pointsForZone[zone]
            self.world.onZoneCaptureFinalised(
                dict(captureInfo, zone=zone, points=points))

    def buildMessages(self):
        if not self.finalised:
            self.finalise()

        for zone, captureInfo in list(self.capturedZones.items()):
            tagger = captureInfo['player']
            playerId = tagger.id if tagger else NO_PLAYER
            team = captureInfo['team']
            teamId = team.id if team else NEUTRAL_TEAM_ID
            yield TaggingZoneMsg(zone.id, playerId, teamId)
            if tagger:
                coins = self.coinsForZone[zone]
                yield AwardPlayerCoinMsg(tagger.id, count=coins)

            helpers = captureInfo['attackers'] - {tagger}
            if helpers:
                coins = int(
                    self.coinsForZone[zone] * COIN_FACTOR_FOR_ASSIST
                    / len(helpers) + 0.5)
                for helper in helpers:
                    yield AwardPlayerCoinMsg(helper.id, count=coins)

        for zone in self.neutralisedZones:
            yield TaggingZoneMsg(zone.id, NO_PLAYER, NEUTRAL_TEAM_ID)


def team_has_enough_players_to_capture(room, team, sub_player=None):
    '''
    :param room: the room in question
    :param team: the team in question
    :param sub_player: see documentation on
        get_living_players_by_team()
    :return: True iff this room contains enough players for the
        given team to capture it by simply touching the orb. Returns
        False if the given team already owns this room.
    '''
    if team == room.owner:
        return False
    if not team.abilities.zoneCaps:
        return False
    return team in get_teams_with_enough_players_to_capture(room, sub_player=sub_player)


def get_teams_fulfilling_all_capture_conditions(room, *, sub_player=None):
    possible_teams = {
        team for team in get_teams_with_enough_players_to_capture(room, sub_player=sub_player)
        if team.abilities.zoneCaps
    }
    progress = room.get_capture_progress(sub_player=sub_player)
    if progress.quick_capture:
        return possible_teams
    if progress.attacking_team is None or progress.progress < 1:
        return set()
    return possible_teams & {room.attacking_team}


def get_teams_with_enough_players_to_capture(room, sub_player=None):
    '''
    :param room: the room in question
    :param sub_player: see docs on get_living_players_by_team()
    :return: set of teams which have enough players in this room to
        capture it. Never contains the defending team.
    '''
    player_counts = {
        team: len(players)
        for team, players in room.get_active_players_by_team(sub_player=sub_player).items()
        if players and team.abilities.zoneCaps
    }
    return calculate_teams_who_could_capture(player_counts, defender=room.owner)


def calculate_teams_who_could_capture(player_counts, *, defender):
    '''
    :param player_counts: dict of team: count for active players in room
    :param defender: the team defending the room, or None if the
        room is currently neutral.
    :return: a set of the teams which have enough living players to
        capture the hypothetical room.
    '''
    if defender is None:
        # For a neutral room, you cannot capture if another team has
        # equal.
        if not player_counts:
            return set()
        max_attackers = max(count for team, count in player_counts.items())
        teams_with_max = {team for team, count in player_counts.items() if count == max_attackers}
        if len(teams_with_max) > 1:
            return set()
        return teams_with_max

    # Otherwise, any team with more players than the defending team can
    # capture.
    defence_count = min(player_counts.get(defender, 0), 2)
    return {
        team for team, count in player_counts.items()
        if count > defence_count and team != defender}
