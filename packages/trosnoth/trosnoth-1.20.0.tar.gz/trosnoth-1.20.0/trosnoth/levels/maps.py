from trosnoth.model.map import ZoneLayout, ZoneStep
from trosnoth.triggers.deathmatch import make_small_circles_layout, makeCirclesLayout


class MapAPI:
    name: str

    def build(self):
        raise NotImplementedError

    def apply(self, level):
        layout = self.build()
        level.world.setLayout(layout)
        return layout

    @property
    def code(self):
        return type(self).__name__


class StandardMap(MapAPI):
    name = 'Regulation Standard'

    def build(self):
        zones = ZoneLayout.generate(3, 2, 0.95)
        return zones.createMapLayout()


class DefaultLobbyMap(MapAPI):
    name = 'Diamond'

    def build(self):
        zones = ZoneLayout.generate(2, 1, 0.5)
        return zones.createMapLayout()


class SmallMap(MapAPI):
    name = 'Regulation 1v1'

    def build(self):
        zones = ZoneLayout(symmetryEnforced=True)

        zone = zones.connectZone(zones.firstLocation, ZoneStep.SOUTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zones.connectZone(zone, ZoneStep.NORTH)

        return zones.createMapLayout()


class WideMap(MapAPI):
    name = 'Wide'

    def build(self):
        zones = ZoneLayout.generate(5, 1, 0.95)
        return zones.createMapLayout()


class CorridorMap(MapAPI):
    name = 'Corridor'

    def build(self):
        zones = ZoneLayout.generate(5, 0, 0.95)
        return zones.createMapLayout()


class LargeMap(MapAPI):
    name = 'Large'

    def build(self):
        zones = ZoneLayout.generate(5, 3, 0.95)
        return zones.createMapLayout()


class CustomStandardMap(MapAPI):
    name = 'Custom'

    def __init__(self, half_width, height):
        self.half_width = half_width
        self.height = height

    def build(self):
        zones = ZoneLayout.generate(self.half_width, self.height, 0.95)
        return zones.createMapLayout()


class SmallStackMap(MapAPI):
    name = 'Small Stack'

    def build(self):
        zones = ZoneLayout()

        zones.setZoneOwner(zones.firstLocation, 0, dark=True)
        zones.connectZone(zones.firstLocation, ZoneStep.SOUTH, ownerIndex=1, dark=False)

        return zones.createMapLayout(autoOwner=False)


class SmallRingMap(MapAPI):
    name = 'Small Ring'

    def build(self):
        return make_small_circles_layout()


class LargeRingsMap(MapAPI):
    name = 'Large Rings'

    def build(self):
        return makeCirclesLayout()


class LabyrinthMap(MapAPI):
    name = 'Labyrinth'

    def build(self):
        zones = ZoneLayout()

        # Outer ring
        north_spawn_zone = zone = zones.firstLocation
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        east_zone = zone = zones.connectZone(zone, ZoneStep.SOUTH)
        east_spawn_zone = zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        south_west_zone = zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        west_spawn_zone = zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        north_west_zone = zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
        zone = zones.connectZone(zone, ZoneStep.NORTHEAST)

        # Inner swirl
        zone = zones.connectZone(east_zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zones.connectZone(zone, ZoneStep.SOUTH, ownerIndex=0, dark=True)
        zone = zones.connectZone(south_west_zone, ZoneStep.NORTHEAST)
        zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
        zones.connectZone(zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(north_west_zone, ZoneStep.SOUTH)
        zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zones.connectZone(zone, ZoneStep.NORTHEAST)

        # Outer spawn zones
        zones.connectZone(north_spawn_zone, ZoneStep.NORTH, ownerIndex=0, dark=True)
        zones.connectZone(east_spawn_zone, ZoneStep.SOUTHEAST, ownerIndex=0, dark=True)
        zones.connectZone(west_spawn_zone, ZoneStep.SOUTHWEST, ownerIndex=0, dark=True)

        return zones.createMapLayout(autoOwner=False)


class FreeFlowMap(MapAPI):
    name = 'Free Flow'

    def build(self):
        zones = ZoneLayout()

        # Outer ring
        mid_top_zone = zone = zones.firstLocation
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
        zone = zones.connectZone(zone, ZoneStep.NORTHEAST)

        # Inner swirl
        zone = zones.connectZone(mid_top_zone, ZoneStep.SOUTH)
        zones.connect_to_all_neighbours(zone)
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        zones.connect_to_all_neighbours(zone)
        zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zones.connect_to_all_neighbours(zone)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        zones.connect_to_all_neighbours(zone)
        zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zones.connect_to_all_neighbours(zone)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        zones.connect_to_all_neighbours(zone)

        # Spawn zone
        zones.connectZone(mid_top_zone, ZoneStep.NORTH, ownerIndex=0, dark=True)

        return zones.createMapLayout(autoOwner=False)
