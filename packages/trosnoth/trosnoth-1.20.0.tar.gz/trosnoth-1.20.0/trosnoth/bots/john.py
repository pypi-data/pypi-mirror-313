from trosnoth.bots.base import Bot

from trosnoth.messages import TickMsg
from trosnoth.model.upgrades import LaunchGrenade
from trosnoth.utils.math import distance


class JohnBot(Bot):
    '''
    This is not the original JohnAI, as the bot API has changed substantially
    since JohnAI was written. Instead, this bot is inspired by version 1.1.3 of
    JohnAI, last edited 2010-12-28. It maintains the following behaviours of
    the original JohnAI:
     - Chases and shoots at nearby enemies.
     - Uses grenades when there are 3 or more enemies in the zone
    '''

    nick = 'JohnBot'
    generic = True

    def start(self):
        super(JohnBot, self).start()

        self.orderFinished()

    def orderFinished(self):
        if self.player.dead:
            if self.player.inRespawnableZone():
                self.respawn()
            else:
                self.moveToFriendlyZone()

        else:
            self.startMoving()

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        super(JohnBot, self).handle_TickMsg(msg)

        if self.player.dead:
            return
        zone = self.player.getZone()
        if not zone:
            return

        enemyPlayers = len([
            p for p in zone.players
            if not (p.dead or self.player.isFriendsWith(p))])
        if enemyPlayers >= 3:
            self.setUpgradePolicy(LaunchGrenade)
        else:
            self.setUpgradePolicy(None)

    def moveToFriendlyZone(self):
        rooms = [
            room for room in self.world.rooms if
            self.player.isZoneRespawnable(room)]
        if not rooms:
            self.world.callLater(3, self.orderFinished)
            return

        player_pos = self.player.pos
        best_room = min(rooms, key=lambda r: distance(r.centre, player_pos))
        self.move_to_room(best_room)

    def startMoving(self):
        enemies = [
            p for p in self.world.players
            if not (p.dead or self.player.isFriendsWith(p))]
        player_pos = self.player.pos

        if enemies:
            nearest_enemy = min(enemies, key=lambda p: distance(p.pos, player_pos))
            self.attackPlayer(nearest_enemy)
        else:
            rooms = [
                r for r in self.world.rooms
                if r.owner != self.player.team and
                any(n.owner == self.player.team for n in r.all_neighbours)]
            if rooms:
                nearest_room = min(
                    rooms, key=lambda r: distance(r.centre, player_pos))
                self.move_to_orb(nearest_room)
            else:
                self.world.callLater(3, self.orderFinished)


BotClass = JohnBot
