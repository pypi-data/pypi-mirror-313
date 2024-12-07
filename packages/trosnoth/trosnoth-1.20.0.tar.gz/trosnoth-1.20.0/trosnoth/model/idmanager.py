import logging

log = logging.getLogger(__name__)


class IdManager:
    '''
    Responsible for assigning shot ids, player ids, etc.
    '''

    def __init__(self, world):
        self.world = world
        self.players = BytesIDGenerator()
        self.coins = BytesIDGenerator()
        self.shots = IDGenerator()
        self.projectiles = IDGenerator()

        world.onShotRemoved.addListener(self.shots.mark_id_as_unused)
        world.onCollectableCoinRemoved.addListener(self.coins.mark_id_as_unused)
        world.onPlayerRemoved.addListener(self.seen_player_removed)
        world.on_projectile_removed.addListener(self.projectiles.mark_id_as_unused)

    def stop(self):
        self.world.onShotRemoved.removeListener(self.shots.mark_id_as_unused)
        self.world.onCollectableCoinRemoved.removeListener(self.coins.mark_id_as_unused)
        self.world.onPlayerRemoved.removeListener(self.seen_player_removed)
        self.world.on_projectile_removed.removeListener(self.projectiles.mark_id_as_unused)

    def seen_player_removed(self, player, old_id):
        self.players.mark_id_as_unused(old_id)


class IDGenerator:
    '''
    Generates integer IDs. Never gives out an ID of 0.
    '''

    def __init__(self, upper_bound=1 << 32 - 1):
        self.upper_bound = upper_bound

        self._used_ids = set()
        self._next_id = 1

    def make_id(self):
        new_id = self._next_id
        if len(self._used_ids) >= self.upper_bound:
            return None

        while new_id in self._used_ids:
            new_id = new_id % self.upper_bound + 1
        self._used_ids.add(new_id)
        self._next_id = new_id % self.upper_bound + 1
        return self._pack_id(new_id)

    def mark_id_as_unused(self, id_):
        self._used_ids.discard(self._unpack_id(id_))

    def _pack_id(self, id_):
        return id_

    def _unpack_id(self, id_):
        return id_


class BytesIDGenerator(IDGenerator):
    _unpack_id = ord

    def __init__(self):
        super().__init__(upper_bound=255)

    def _pack_id(self, id_):
        return bytes([id_])
