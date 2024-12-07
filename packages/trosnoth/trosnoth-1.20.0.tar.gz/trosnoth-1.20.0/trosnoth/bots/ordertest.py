import random

from trosnoth.bots.base import Bot
from trosnoth.model.upgrades import Shield


class OrderTestBot(Bot):
    '''
    Not a very sensible bot, just exists to test the system of giving bots
    orders.
    '''
    nick = 'TestingBot'

    def start(self):
        super(OrderTestBot, self).start()

        self.setAggression(False)
        self.setUpgradePolicy(Shield)

        self.orderFinished()

    def orderFinished(self):
        if self.player.dead:
            rooms = [
                r for r in self.world.rooms if r.owner == self.player.team]
            if not rooms:
                rooms = list(self.world.rooms)
            self.respawn(zone=random.choice(rooms))
        else:
            enemies = [
                p for p in self.world.players if p.team != self.player.team and
                not p.dead]
            if enemies:
                enemy = random.choice(enemies)
                # e,self.moveToPoint(enemy.pos)
                self.followPlayer(enemy)
            else:
                # self.world.callLater(1, self.orderFinished)
                self.move_to_orb(self.world.rooms.random())
                # self.move_to_room(self.world.rooms.random())


BotClass = OrderTestBot
