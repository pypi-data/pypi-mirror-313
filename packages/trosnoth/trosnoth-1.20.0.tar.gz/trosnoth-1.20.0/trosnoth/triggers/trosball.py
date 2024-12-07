from trosnoth.const import ZONE_CAP_DISTANCE
from trosnoth.triggers.base import Trigger
from trosnoth.utils import math
from trosnoth.utils.event import Event


class StandardTrosballScoreTrigger(Trigger):
    '''
    When the trosball goes through a target orb, trigger an event.
    '''

    def __init__(self, *args, **kwargs):
        super(StandardTrosballScoreTrigger, self).__init__(*args, **kwargs)
        self.onTrosballScore = Event(['room', 'player'])

    def doActivate(self):
        self.world.onUnitsAllAdvanced.addListener(self.units_have_advanced, lifespan=self.lifespan)

    def units_have_advanced(self):
        pos = self.world.trosballManager.getPosition()
        room = self.world.rooms.get_at(pos)

        for team in self.world.teams:
            distance = math.distance(
                pos,
                self.world.trosballManager.getTargetZoneDefn(team).pos)
            if distance < ZONE_CAP_DISTANCE:
                self.onTrosballScore(
                    room, self.world.trosballManager.lastTrosballPlayer)
