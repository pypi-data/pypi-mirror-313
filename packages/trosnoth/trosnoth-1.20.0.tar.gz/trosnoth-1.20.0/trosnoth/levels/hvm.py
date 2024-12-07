# Trosnoth (UberTweak Platform Game)
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

import random
import logging

from twisted.internet import defer

from trosnoth.const import DEFAULT_BOT_DIFFICULTY
from trosnoth.levels.maps import SmallMap

log = logging.getLogger(__name__)


BOTS_PER_HUMAN = 1  # Option exists for debugging with many bots


class HumansVsMachinesBotManager(object):
    '''
    Injects bots into the game as needed for a humans vs. machines game.
    '''
    def __init__(self, universe, reverse):
        self.universe = universe

        self.enabled = False
        self.botSurplus = 0
        self.detachingAgents = set()

        if reverse:
            self.botTeam = universe.teams[0]
            self.humanTeam = universe.teams[1]
        else:
            self.botTeam = universe.teams[1]
            self.humanTeam = universe.teams[0]

        self.agents = set()

    @defer.inlineCallbacks
    def startingSoon(self):
        self.enabled = True
        bots = len([p for p in self.universe.players if p.bot])
        humans = len(self.universe.players) - bots
        self.botSurplus = bots - humans * BOTS_PER_HUMAN
        yield self._addBots()

    @defer.inlineCallbacks
    def playerAdded(self, player):
        if not self.enabled:
            return
        if player.bot:
            if player.agent not in self.agents:
                # Someone's directly added a different bot
                self.botSurplus += 1
                self._removeBots()
        else:
            self.botSurplus -= BOTS_PER_HUMAN
            yield self._addBots()

    @defer.inlineCallbacks
    def removingPlayer(self, player):
        if not self.enabled:
            return

        if player.bot:
            if player.agent in self.agents:
                # Bot was booted, not by us
                self.agents.discard(player.agent)
                player.agent.stop()
                self.universe.game.detachAgent(player.agent)

            if player.agent in self.detachingAgents:
                self.detachingAgents.discard(player.agent)
            else:
                self.botSurplus -= 1
                yield self._addBots()
        else:
            self.botSurplus += BOTS_PER_HUMAN
            self._removeBots()

    @defer.inlineCallbacks
    def _addBots(self):
        game = self.universe.game
        bot_name = ''
        if game.serverInterface:
            difficulty = game.serverInterface.get_machines_difficulty()
            bot_name = game.serverInterface.get_machines_bot_name()
            extra_bot_count = game.serverInterface.get_extra_bot_count()
        else:
            difficulty = DEFAULT_BOT_DIFFICULTY
            extra_bot_count = 0

        if not bot_name:
            bot_name = self._get_default_bot_name()

        while self.botSurplus < extra_bot_count:
            agent = yield game.addBot(bot_name, team=self.botTeam, difficulty=difficulty)
            self.agents.add(agent)
            self.botSurplus += 1

    def _get_default_bot_name(self):
        from trosnoth.levels.standard import StandardLevel
        level = self.universe.scenarioManager.level
        if isinstance(level, StandardLevel):
            map_object = level.level_options.get_map(level)
            if isinstance(map_object, SmallMap):
                # If we're on a 1v1 map, use SilverBot instead of RangerBot
                return 'silver'
        return 'ranger'

    def _removeBots(self):
        game = self.universe.game
        extra_bot_count = game.serverInterface.get_extra_bot_count() if game.serverInterface else 0

        while self.botSurplus > extra_bot_count:
            if not self.agents:
                return
            agent = random.choice(list(self.agents))
            self.agents.discard(agent)
            self.detachingAgents.add(agent)
            self.botSurplus -= 1
            agent.stop()
            game.detachAgent(agent)

    def getTeamToJoin(self, preferredTeam, bot):
        if bot:
            return self.botTeam
        return self.humanTeam

    def stop(self):
        self.enabled = False
        while self.agents:
            agent = self.agents.pop()
            agent.stop()
            self.universe.game.detachAgent(agent)
