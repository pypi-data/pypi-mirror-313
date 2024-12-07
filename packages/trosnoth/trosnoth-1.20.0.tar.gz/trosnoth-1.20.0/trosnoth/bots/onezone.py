import random

from trosnoth.bots.goalsetter import (
    GoalSetterBot, MessAroundInZone, Goal, RespawnNearZone,
)


class OneZoneBot(GoalSetterBot):
    nick = 'Bothersome'
    generic = True

    class MainGoalClass(Goal):
        def reevaluate(self):
            if self.bot.player.dead:
                room = self.bot.player.getZone()
                if room is None:
                    room = self.bot.world.rooms.random()
                self.setSubGoal(RespawnNearZone(self.bot, self, room))
            else:
                self.setSubGoal(MessAroundInZone(self.bot, self))


    def start(self):
        super(OneZoneBot, self).start()

        self.set_dodges_bullets(False)
        self.setUpgradePolicy(None)


BotClass = OneZoneBot
