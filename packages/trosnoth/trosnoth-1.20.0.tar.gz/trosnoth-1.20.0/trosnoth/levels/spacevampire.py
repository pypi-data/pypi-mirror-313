# Trosnoth (Ubertweak Platform Game)
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
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import logging
import random

from trosnoth.const import (
    ACHIEVEMENT_TACTICAL, BOT_GOAL_KILL_THINGS, BOT_GOAL_COWARDLY_CAPTURE,
)
from trosnoth.levels.base import play_level, Level
from trosnoth.levels.maps import LargeMap
from trosnoth.messages import (
    SetPlayerTeamMsg, SetMaxHealthMsg, SetHealthMsg, ChatFromServerMsg,
    SetPlayerCoinsMsg, ZoneStateMsg, UpdateGameInfoMsg,
)
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.model.zonemechanics import ZoneCaptureCalculator
from trosnoth.triggers.base import Trigger
from trosnoth.triggers.coins import SlowlyIncrementLivePlayerCoinsTrigger
from trosnoth.triggers.shotstats import KillDeathRatioStatTrigger, AccuracyStatTrigger
from trosnoth.triggers.timestats import (
    GameDurationStatTrigger, PlayerLivePercentageStatTrigger,
    ScenarioWinPercentStatTrigger,
)
from trosnoth.triggers.zonecaps import StandardZoneCaptureTrigger
from trosnoth.utils.aio import as_future, delay_so_messages_will_apply_immediately
from trosnoth.utils.event import waitForEvents

log = logging.getLogger(__name__)

PLAYER_HEALTH = 5
VAMPIRE_HEALTH_PER_PLAYER = 2
THRALL_HEALTH = 1

VAMPIRE_START_COINS = 1000
TIME_PENALTY_IF_VAMPIRE_LEAVES_GAME = 25
TIME_FOR_VAMPIRE_TO_REJOIN = 25


class SpaceVampireLevel(Level):
    levelName = 'Space Vampire'
    default_duration = 10 * 60
    map_selection = (LargeMap(),)
    level_code = 'vampire'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vampire_team = self.villager_team = None
        self.vampire_player = None
        self.vampire_username = None
        self.vampire_nick = None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        if self.joining_player_is_space_vampire(user, nick):
            return self.vampire_team
        return self.villager_team

    def joining_player_is_space_vampire(self, user, nick):
        if self.vampire_player is not None:
            return False
        if self.vampire_username is None:
            return self.vampire_nick == nick
        return user and self.vampire_username == user.username

    def pre_sync_teams_setup(self):
        self.villager_team, self.vampire_team = self.pre_sync_create_teams([
            ('Space Villagers', (p for p in self.world.players if p != self.vampire_player)),
            ('Space Vampires', (self.vampire_player,) if self.vampire_player else ()),
        ])
        self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    def pre_sync_setup(self):
        if self.world.players:
            self.vampire_player = random.choice([p for p in self.world.players if not p.bot])

        super().pre_sync_setup()

        self.world.uiOptions.highlight_macguffins = [self.world.vampire]

        self.level_options.apply_map_layout(self)
        for room in self.world.rooms:
            room.set_owner(self.vampire_team, dark=False)

        start_room = self.world.rooms.random()
        start_room.set_owner(self.villager_team, dark=True)

        for player in self.world.players:
            player.teleport_to_respawn_point(start_room)

    async def run(self):
        # We might be run from command-line or as a tutorial: give
        # time for bots and local player to join.
        while not self.world.players:
            await self.world.sleep_future(.5)

        # Fill the game up to a minimum number of starting players by
        # adding bots.
        for i in range(max(0, 6 - len(self.world.players))):
            await as_future(self.addBot(self.villager_team, '', botName='ranger'))

        self.set_up_vampire_player()

        for player in self.world.players:
            if player != self.vampire_player:
                self.set_up_villager(player)
        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        SetUpLateJoiningPlayersTrigger(self).activate()
        DeadPlayersBecomeThrallsTrigger(self).activate()

        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.setUserInfo('Space Vampire', (
            '* Space villagers win if they kill the space vampire, or survive the time limit',
            '* The space vampire wins if they kill all space villagers',
            '* When villagers are killed, they join the space vampire as thralls',
        ), BOT_GOAL_COWARDLY_CAPTURE)
        self.world.abilities.set(balanceTeams=False)
        self.villager_team.abilities.set(always_disrupted=True)
        self.vampire_team.abilities.set(dark_zones=False)
        SpaceVampireZoneCaptureTrigger(self).activate()

        self.world.clock.startCountDown(self.level_options.get_duration(self))
        self.world.clock.propagateToClients()

        win_stat = ScenarioWinPercentStatTrigger(self)
        self.stats.add_triggers([
            GameDurationStatTrigger(self),
            win_stat,
            PlayerLivePercentageStatTrigger(self),
            KillDeathRatioStatTrigger(self, deaths=True),
            AccuracyStatTrigger(self),
        ])
        self.stats.resume()

        time_up = self.world.clock.onZero
        player_kill = self.world.onPlayerKill
        player_leave = self.world.onPlayerRemoved
        while True:
            event, args = await waitForEvents([time_up, player_kill, player_leave])
            if event == time_up:
                winners = [self.villager_team]
                break

            if self.vampire_player is None:
                # seen_vampire_leave_game() triggers before this
                if not await self.wait_for_vampire_to_rejoin():
                    # Vampire has not rejoined
                    winners = [self.villager_team]
                    break

                # If vampire has rejoined, continue on to check if
                # vampire has won in the meantime.

            dead_player = args.get('target') or args['player']
            if not any([p for p in self.world.players
                        if p != dead_player and p.team == self.villager_team]):
                winners = [self.vampire_player]
                break

            if dead_player == self.vampire_player:
                if not dead_player.died_from_bomber:
                    winners = [self.villager_team]
                    break

        win_stat.finalise(winners)

        return self.build_level_result(a_human_player_won=True, winners=winners)

    async def wait_for_vampire_to_rejoin(self):
        self.world.sendServerCommand(
            ChatFromServerMsg(True, 'Space vampire has left the game!'.encode('utf-8')))
        time_remaining = self.world.clock.value - TIME_PENALTY_IF_VAMPIRE_LEAVES_GAME
        if time_remaining < 0:
            return False

        self.world.clock.startCountDown(
            TIME_FOR_VAMPIRE_TO_REJOIN, flashBelow=TIME_FOR_VAMPIRE_TO_REJOIN)
        self.world.clock.propagateToClients()

        time_up = self.world.clock.onZero
        player_join = self.world.onPlayerAdded
        while True:
            event, args = await waitForEvents([time_up, player_join])
            if event == time_up:
                return False

            if args['player'].team == self.vampire_team:
                # get_team_to_join() has determined that this is the
                # vampire.
                self.world.sendServerCommand(
                    ChatFromServerMsg(True, 'Space vampire has returned!'.encode('utf-8')))
                self.world.clock.startCountDown(time_remaining)
                self.world.clock.propagateToClients()
                return True

    def set_up_vampire_player(self):
        if not self.vampire_player:
            self.vampire_player = random.choice([p for p in self.world.players if not p.bot])
            self.world.sendServerCommand(
                SetPlayerTeamMsg(self.vampire_player.id, self.vampire_team.id))

        # Remember the vampire details in case they leave the game
        if self.vampire_player.user:
            self.vampire_username = self.vampire_player.user.username
        else:
            self.vampire_nick = self.vampire_player.nick

        # Give the vampire lots of health, coins and the Vampire MacGuffin
        vampire_health = PLAYER_HEALTH + VAMPIRE_HEALTH_PER_PLAYER * (len(self.world.players) - 1)
        self.world.sendServerCommand(SetMaxHealthMsg(self.vampire_player.id, vampire_health))
        self.world.sendServerCommand(SetHealthMsg(self.vampire_player.id, vampire_health))
        self.world.sendServerCommand(
            SetPlayerCoinsMsg(self.vampire_player.id, VAMPIRE_START_COINS))
        self.world.vampire.give_to_player(self.vampire_player)

    def set_up_villager(self, player):
        self.world.sendServerCommand(SetMaxHealthMsg(player.id, PLAYER_HEALTH))
        if player.dead:
            room = random.choice([r for r in self.world.rooms if r.owner == self.villager_team])
            self.world.magically_move_player(player, room.respawn_pos, alive=True)
        else:
            self.world.sendServerCommand(SetHealthMsg(player.id, PLAYER_HEALTH))

    def set_up_thrall(self, player):
        self.world.sendServerCommand(SetMaxHealthMsg(player.id, THRALL_HEALTH))
        self.world.sendServerCommand(SetPlayerTeamMsg(player.id, self.vampire_team.id))
        player.abilities.set(orb_capture=False)

        # Tell thrall bots not to try to conquer the map
        player.agent.messageToAgent(UpdateGameInfoMsg.build('Space Vampire', (
            '* Space villagers win if they kill the space vampire, or survive the time limit',
            '* The space vampire wins if they kill all space villagers',
            '* When villagers are killed, they join the space vampire as thralls',
        ), BOT_GOAL_KILL_THINGS))


class SetUpLateJoiningPlayersTrigger(Trigger):
    '''
    This trigger is specific to this level class.
    '''

    def __init__(self, level: SpaceVampireLevel):
        super().__init__(level)
        self.vampire_team = level.vampire_team
        self.villager_team = level.villager_team
        self.leaving_vampire_health = None
        self.leaving_vampire_max_health = None
        self.leaving_vampire_money = None

    def doActivate(self):
        self.world.onPlayerAdded.addListener(self.seen_player_added, lifespan=self.lifespan)
        self.world.vampire.on_possessor_left_game.addListener(
            self.seen_vampire_leave_game, lifespan=self.lifespan)

    @delay_so_messages_will_apply_immediately
    def seen_player_added(self, player):
        # It's important for messages to be applied immediately because
        # magicallyMovePlayer sends a resync message, and without
        # immediately applying messages, the resync message will be
        # based on the player state before the other messages (e.g. set
        # max health) were applied.
        if player.team == self.vampire_team:
            # Level.get_team_to_join() has already determined that this
            # is the returning space vampire.
            self.level.vampire_player = player
            self.world.vampire.give_to_player(player)
            self.world.sendServerCommand(
                SetMaxHealthMsg(player.id, self.leaving_vampire_max_health))
            self.world.sendServerCommand(SetHealthMsg(player.id, self.leaving_vampire_health))
            self.world.sendServerCommand(SetPlayerCoinsMsg(player.id, self.leaving_vampire_money))
            return

        villagers = len([p for p in self.world.players if p.team == self.villager_team])
        if villagers > len(self.world.players) / 2:
            self.level.set_up_villager(player)
        else:
            self.level.set_up_thrall(player)

    def seen_vampire_leave_game(self):
        self.leaving_vampire_health = self.level.vampire_player.health
        self.leaving_vampire_max_health = self.level.vampire_player.max_health
        self.leaving_vampire_money = self.level.vampire_player.coins
        self.level.vampire_player = None


class DeadPlayersBecomeThrallsTrigger(Trigger):
    '''
    This trigger is specific to this level class.
    '''

    def doActivate(self):
        self.world.onPlayerKill.addListener(self.seen_player_kill, lifespan=self.lifespan)

    def seen_player_kill(self, killer, target, hit_kind):
        if target.team == self.level.villager_team:
            self.level.set_up_thrall(target)


class SpaceVampireZoneCaptureCalculator(ZoneCaptureCalculator):
    def finalise(self, sendNeutraliseEvent=False):
        for team in self.world.teams:
            room_count = len(
                {r for r in self.world.rooms if r.owner == team}.difference(self.capturedZones))
            if room_count == 0:
                # No team may have their final zone captured
                restored = random.choice([r for r in self.capturedZones if r.owner == team])
                del self.capturedZones[restored]

        super().finalise(sendNeutraliseEvent)

    def markZoneCaptured(self, zone, capture_info):
        level = self.world.scenarioManager.level
        if capture_info['team'] == level.vampire_team and capture_info['defenders']:
            # Vampire cannot capture zones unless they are completely empty
            return
        super().markZoneCaptured(zone, capture_info)

    def getTeamSectors(self):
        result = super().getTeamSectors()
        level = self.world.scenarioManager.level
        try:
            # Vampire team cannot have its territory neutralised
            del result[level.vampire_team]
        except KeyError:
            pass
        return result

    def buildMessages(self):
        yield from super().buildMessages()

        # Move neutralised zones to vampire team
        level = self.world.scenarioManager.level
        for zone in self.neutralisedZones:
            yield ZoneStateMsg(zone.id, level.vampire_team.id, False)


class SpaceVampireZoneCaptureTrigger(StandardZoneCaptureTrigger):
    zone_capture_calculator_factory = SpaceVampireZoneCaptureCalculator


if __name__ == '__main__':
    play_level(SpaceVampireLevel(), bot_count=5)
