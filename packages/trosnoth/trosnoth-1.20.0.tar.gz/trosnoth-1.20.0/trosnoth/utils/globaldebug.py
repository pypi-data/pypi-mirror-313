import logging
import time

log = logging.getLogger(__name__)


enabled = True


# Slows down the universe game loop by this factor
slowMotionFactor = 1

# Maximum number of shots allowed on the map - for debugging shots
# (ignored if falsey)
shotLimit = None

# Opens ticks.csv in working directory and writes tick information
log_ticks = False

# If enabled, pressing the debug key will write screenshot data to
# screenshots.txt in the working directory.
debug_key_screenshots = True


# Displays where the local server thinks sprites are
showSpriteCircles = False

# Displays obstacle locations
showObstacles = False


def getSpriteCircles():
    '''
    Returns a sequence of (point, radius) pairs for positions in the server
    universe where sprites are.
    '''
    if serverUniverse is None:
        return
    for unit in serverUniverse.getCollectableUnits():
        yield (unit.pos, unit.playerCollisionTolerance)

    for player in serverUniverse.playerWithId.values():
        yield (player.pos, 3)


# Updated by other parts of the code
localPlayerId = None
serverUniverse = None

# This flag is set to True when globaldebug is enabled and the middle mouse
# button is being held.
debugKey = False


class TickLogger:
    def __init__(self):
        self.f = open('ticks.csv', 'w') if enabled and log_ticks else None
        self.waiting_ticks = []
        self.tick_data = {}

    def ui_throttler_saw_tick(self, tick_id):
        if self.f is None:
            return
        record = [time.time(), '', '']
        self.tick_data[tick_id] = record
        self.waiting_ticks.append(tick_id)

    def universe_saw_tick(self, world, tick_id):
        if self.f is None:
            return
        if tick_id in self.tick_data:
            self.tick_data[tick_id][1] = time.time()

    def game_interface_saw_tick(self, tick_id):
        if self.f is None:
            return
        if tick_id not in self.tick_data:
            return
        self.tick_data[tick_id][2] = time.time()
        while self.waiting_ticks[0] != tick_id:
            self._write_record(self.waiting_ticks.pop(0))
        self._write_record(self.waiting_ticks.pop(0))

    def _write_record(self, tick_id):
        record = self.tick_data.pop(tick_id)
        self.f.write(', '.join(str(t) for t in record) + '\n')


tick_logger = TickLogger()
