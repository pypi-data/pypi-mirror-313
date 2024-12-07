# Trosnoth
# Copyright (C) Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from collections import defaultdict

from trosnoth.const import TICK_PERIOD
from trosnoth.levels.base import PlayerInfo
from trosnoth.triggers.base import StatTrigger, StatType


class GameDurationStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.total_ticks = 0

    def get_match_stats(self):
        yield 'Duration', StatType.TIME, self.total_ticks * TICK_PERIOD

    def doActivate(self):
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)

    def got_tick_complete(self):
        self.total_ticks += 1


class PlayerLivePercentageStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.total_ticks = 0
        self.unprocessed_ticks = 0
        self.player_live_ticks: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        self.process_ticks()
        if self.total_ticks == 0:
            alive_percentages = {p: 0 for p in self.player_live_ticks}
        else:
            alive_percentages = {
                p: ticks / self.total_ticks
                for p, ticks in self.player_live_ticks.items()
            }
        yield 'Alive', StatType.PERCENTAGE, alive_percentages

    def doActivate(self):
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)
        # Note: we don't need to listen for onPlayerAdded because newly
        # added players are never alive.
        self.world.onPlayerRemoved.addListener(self.got_player_removed, lifespan=self.lifespan)
        self.world.onPlayerKill.addListener(self.got_player_kill, lifespan=self.lifespan)
        self.world.onPlayerRespawn.addListener(self.got_player_respawn, lifespan=self.lifespan)

    def got_tick_complete(self):
        self.unprocessed_ticks += 1
        self.total_ticks += 1
        if self.unprocessed_ticks % 100 == 0:
            self.process_ticks()

    def process_ticks(self):
        for player in self.world.players:
            if not player.dead:
                self.player_live_ticks[PlayerInfo(player)] += self.unprocessed_ticks
        self.unprocessed_ticks = 0

    def got_player_removed(self, player, old_id):
        if not player.dead:
            info = PlayerInfo(player, id_=old_id)
            self.player_live_ticks[info] += self.unprocessed_ticks

    def got_player_kill(self, killer, target, hit_kind):
        self.player_live_ticks[PlayerInfo(target)] += self.unprocessed_ticks

    def got_player_respawn(self, player):
        self.player_live_ticks[PlayerInfo(player)] -= self.unprocessed_ticks


class ScenarioWinPercentStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.winners = None

    def doActivate(self):
        pass

    def finalise(self, winners):
        self.winners = set(winners)

    def get_player_stats(self):
        if self.winners is None:
            return
        yield 'Win', StatType.PERCENTAGE, {
            PlayerInfo(p): 1 if p in self.winners or p.team in self.winners else 0
            for p in self.world.players
        }


class StandardGameWinPercentStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.unprocessed_ticks = 0
        self.new_players = set()
        self.player_team_ticks: dict[PlayerInfo] = defaultdict(lambda: defaultdict(int))
        self.winning_teams = None
        self.scale = 1

    def finalise(self, winning_teams):
        self.winning_teams = set(winning_teams)
        if winning_teams is None:
            # Game is drawn
            self.winning_teams = self.world.teams
        self.scale = 1 / len(self.winning_teams)

    def get_player_stats(self):
        if not self.winning_teams:
            return
        self.process_ticks()

        result = {}
        for p, team_ticks in self.player_team_ticks.items():
            win_ticks = sum(
                ticks for team, ticks in team_ticks.items() if team in self.winning_teams)
            total_ticks = sum(team_ticks.values())
            if total_ticks > 0:
                result[p] = win_ticks / total_ticks * self.scale
        yield 'Win', StatType.PERCENTAGE, result

    def doActivate(self):
        # Players that first join are not counted against their team
        # until they first respawn, in case they accidentally join on
        # the wrong team and leave again.
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)
        self.world.onPlayerAdded.addListener(self.got_player_added, lifespan=self.lifespan)
        self.world.onPlayerRemoved.addListener(self.got_player_removed, lifespan=self.lifespan)
        self.world.onPlayerRespawn.addListener(self.got_player_respawn, lifespan=self.lifespan)
        self.world.on_player_team_set.addListener(self.got_player_team_set, lifespan=self.lifespan)

    def got_tick_complete(self):
        self.unprocessed_ticks += 1
        if self.unprocessed_ticks % 100 == 0:
            self.process_ticks()

    def process_ticks(self):
        for player in self.world.players:
            if not player.dead:
                self.new_players.discard(player)    # In case we missed it somehow
            if player not in self.new_players:
                self.player_team_ticks[PlayerInfo(player)][player.team] += self.unprocessed_ticks
        self.unprocessed_ticks = 0

    def got_player_added(self, player):
        self.new_players.add(player)

    def got_player_removed(self, player, old_id):
        if player not in self.new_players:
            info = PlayerInfo(player, id_=old_id)
            self.player_team_ticks[info][player.team] += self.unprocessed_ticks

    def got_player_respawn(self, player):
        if player in self.new_players:
            self.new_players.remove(player)
            self.player_team_ticks[PlayerInfo(player)][player.team] -= self.unprocessed_ticks

    def got_player_team_set(self, player, old_team):
        # Remove from old team
        if player not in self.new_players:
            self.player_team_ticks[PlayerInfo(player)][old_team] += self.unprocessed_ticks
        # Treat as 'new' until their first respawn on the new team
        self.new_players.add(player)


class TeamPossessionStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.time_ran_out = False
        self.winning_team = None
        self.ticks = 0
        self.possession_by_team = defaultdict(int)
        self.current_possession = {}
        self.possession_changed = True
        self.recalculate_posession()

        self.start_possession = dict(self.current_possession)

    def finalise(self, *, winners, time_ran_out):
        self.winning_team = winners[0] if len(winners) == 1 else None
        self.time_ran_out = time_ran_out

    def get_match_stats(self):
        if self.time_ran_out and self.winning_team:
            current = self.current_possession.get(self.winning_team, 0)
            initial = self.start_possession.get(self.winning_team, 0)
            projection = self.ticks * TICK_PERIOD * (1 - initial) / (current - initial)
            yield 'Time for full conquest', StatType.TIME, projection

    def get_team_stats(self):
        yield 'Av. possession', StatType.PERCENTAGE, dict(self.possession_by_team)
        scale = len(self.world.rooms) / TICK_PERIOD * 60 / self.ticks
        yield 'Conquest/min', StatType.FLOAT, {
            t: (self.current_possession.get(t, 0) - initial) * scale
            for t, initial in self.start_possession.items()
        }

    def doActivate(self):
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)
        self.world.onZoneTagged.addListener(self.got_zone_tagged, lifespan=self.lifespan)

    def recalculate_posession(self):
        zone_count = defaultdict(int)
        total_zones = 0
        for room in self.world.rooms:
            if room.owner:
                zone_count[room.owner] += 1
                total_zones += 1
        self.current_possession = {
            team: count / total_zones for team, count in zone_count.items()}
        self.possession_changed = False

    def got_tick_complete(self):
        self.ticks += 1
        for team in set(self.possession_by_team).union(self.world.teams):
            diff = self.current_possession.get(team, 0) - self.possession_by_team[team]
            self.possession_by_team[team] += diff / self.ticks
        if self.possession_changed:
            self.recalculate_posession()

    def got_zone_tagged(self, *args, **kwargs):
        self.possession_changed = True


class GrapplePercentStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.ticks: dict[PlayerInfo, int] = defaultdict(int)
        self.grapple_ticks: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        yield 'Grapple', StatType.PERCENTAGE, {
            p: self.grapple_ticks[p] / self.ticks[p]
            for p in self.ticks}

    def doActivate(self):
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)

    def got_tick_complete(self):
        for player in self.world.players:
            if not player.dead:
                self.ticks[pi := PlayerInfo(player)] += 1
                if player.grapplingHook.isActive():
                    self.grapple_ticks[pi] += 1


class WalkPercentStatTrigger(StatTrigger):
    '''
    Measures how often each player is walking as a percentage of their
    time moving along the ground.
    '''

    def __init__(self, level):
        super().__init__(level)
        self.ticks: dict[PlayerInfo, int] = defaultdict(int)
        self.walk_ticks: dict[PlayerInfo, int] = defaultdict(int)

    def get_player_stats(self):
        yield 'Walk', StatType.PERCENTAGE, {
            p: self.walk_ticks[p] / self.ticks[p]
            for p in self.ticks}

    def doActivate(self):
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)

    def got_tick_complete(self):
        for player in self.world.players:
            if not player.dead and player.getGroundCollision() and player.xVel != 0:
                intention, direction = player.getGroundIntentionAndDirection()
                if intention < 0:
                    continue
                self.ticks[pi := PlayerInfo(player)] += 1
                if intention == 0:
                    self.walk_ticks[pi] += 1


class ElevationStatTrigger(StatTrigger):
    def __init__(self, level):
        super().__init__(level)
        self.ticks: dict[PlayerInfo, int] = defaultdict(int)
        self.result: dict[PlayerInfo, float] = defaultdict(float)

    def get_player_stats(self):
        yield 'Elevation', StatType.PERCENTAGE, dict(self.result)

    def doActivate(self):
        self.world.onServerTickComplete.addListener(self.got_tick_complete, lifespan=self.lifespan)

    def got_tick_complete(self):
        h = self.world.map.size[1]
        for player in self.world.players:
            if not player.dead:
                self.ticks[pi := PlayerInfo(player)] += 1
                self.result[pi] += (1 - player.pos[1] / h - self.result[pi]) / self.ticks[pi]
