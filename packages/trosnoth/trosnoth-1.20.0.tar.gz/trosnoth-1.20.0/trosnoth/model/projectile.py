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
# 02110-1301, USA
import dataclasses
from math import sin, cos, atan2, sqrt
from typing import Optional, TYPE_CHECKING, Tuple

from trosnoth.const import MINE_HIT, TICK_PERIOD
from trosnoth.messages import MineExplodedMsg
from trosnoth.model.physics import CollisionCircle, CollisionShape, SimplePhysicsObject
from trosnoth.model.shot import LocalUnit
from trosnoth.model.unit import Unit
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.utils.math import distance

if TYPE_CHECKING:
    from trosnoth.model.player import Player
    from trosnoth.model.team import Team


class Trajectory:
    def stops(self):
        raise NotImplementedError


@dataclasses.dataclass
class TrajectoryStop:
    pos: Tuple[float, float]
    collision_end: Optional[Tuple[float, float]]
    collision_angle: Optional[float]


class TrajectoryStops:
    def __init__(self, *, iterator=None, expanded=None):
        self.iterator = iterator
        self.expanded = None if expanded is None else [TrajectoryStop(*bits) for bits in expanded]

    def __iter__(self):
        return self

    @classmethod
    def from_iterator(cls, iterator):
        return cls(iterator=iterator)

    @classmethod
    def rebuild(cls, data):
        return cls(expanded=data)

    def dump(self):
        if self.expanded is None:
            self.expanded = list(self)
            self.iterator = None
        return [dataclasses.astuple(stop) for stop in self.expanded]

    def __next__(self):
        if self.expanded is not None:
            if self.expanded:
                return self.expanded.pop(0)
            raise StopIteration()
        pos, collision = next(self.iterator)
        return TrajectoryStop(
            pos=pos,
            collision_end=collision.end if collision else None,
            collision_angle=collision.angle if collision else None,
        )


class ParabolicTrajectory(Trajectory):
    collision_shape: CollisionShape
    max_duration: Optional[float]
    launch_speed: float
    gravity: float
    max_fall_velocity: float
    bounces: bool

    ignore_ledges = True
    bounce_damping_factor = 0.9
    stop_tolerance_distance = 1
    stop_tolerance_ticks = 5

    def __init__(self, world, start_pos, launch_angle):
        super().__init__()
        self.world = world
        self.start_pos = start_pos
        self.launch_angle = launch_angle

    def stops(self):
        stationary_ticks = 0
        # If no max duration is specified, go for 4 seconds, not forever
        time_left = self.max_duration if self.max_duration is not None else 4
        pos = old_pos = self.start_pos
        angle = self.launch_angle
        x_vel = self.launch_speed * sin(angle)
        y_vel = -self.launch_speed * cos(angle)
        delta_t = self.world.tickPeriod
        collision = None

        while time_left > 0:
            yield pos, collision

            delta = (x_vel * delta_t, y_vel * delta_t)

            old_pos = pos
            pos, collision = self.world.physics.getMotion(
                SimplePhysicsObject(pos, self.collision_shape),
                delta,
                ignoreLedges=self.ignore_ledges)

            if distance(pos, old_pos) < self.stop_tolerance_distance:
                stationary_ticks += 1
                if stationary_ticks > self.stop_tolerance_ticks:
                    yield pos, collision
                    return
            else:
                stationary_ticks = 0

            if collision:
                if not self.bounces:
                    yield pos, collision
                    return

                shotAngle = atan2(y_vel, x_vel)
                dif = shotAngle - collision.angle
                final = collision.angle - dif
                speed = sqrt(x_vel ** 2 + y_vel ** 2) * self.bounce_damping_factor
                x_vel = speed * cos(final)
                y_vel = speed * sin(final)

            v_final = y_vel + self.gravity * delta_t
            y_vel = min(self.max_fall_velocity, v_final)

            time_left -= self.world.tickPeriod


projectile_type_registry = {}


class Projectile(Unit):
    trajectory_shape: Trajectory
    team: Optional['Team']
    player: Optional['Player']

    projectile_kind_code: Optional[bytes] = None

    triggered_by_explosion = False
    collides_with_players = False   # If true, class must implement InteractingUnit
    triggered_by_detonation_beam = False    # If true, class must implement hit_by_shot()

    def __init__(self, *args, id_, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id_

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Save the subclass in projectile_type_registry if
        # projectile_kind_code is set.
        if not cls.projectile_kind_code:
            return
        if cls.projectile_kind_code in projectile_type_registry:
            other_type = projectile_type_registry[cls.projectile_kind_code]
            # noinspection PyTypeHints
            if issubclass(cls, other_type):
                cls.projectile_kind_code = None
            else:
                raise KeyError(
                    f'kind code {cls.projectile_kind_code} already used by {other_type}')
        else:
            projectile_type_registry[cls.projectile_kind_code] = cls

    @property
    def collision_shape(self):
        return self.trajectory_shape.collision_shape

    def caught_in_explosion(self):
        # Only needs to be implemented if triggered_by_explosion is True
        pass

    def dump(self):
        if self.projectile_kind_code is None:
            raise RuntimeError('Cannot dump Projectile class without projectile_kind_code set')
        return {
            'id': self.id,
            'kind': self.projectile_kind_code,
        }

    @staticmethod
    def build_from_data(world, data):
        subclass = projectile_type_registry[data['kind']]
        return subclass.rebuild(data)

    @classmethod
    def rebuild(cls, world, data, *args, **kwargs):
        return cls(world, id_=data['id'], *args, **kwargs)


class GrenadeTrajectory(ParabolicTrajectory):
    collision_shape = CollisionCircle(radius=5)
    max_duration = 2.5
    launch_speed = 500
    gravity = 300
    max_fall_velocity = 700
    blast_radius = 448
    bounces = True


class GrenadeProjectile:
    trajectory_shape = GrenadeTrajectory


class MineTrajectory(ParabolicTrajectory):
    collision_shape = CollisionCircle(0.25)
    max_duration = None
    launch_speed = 600
    gravity = 734.4
    max_fall_velocity = 700
    blast_radius = 25
    bounces = False
    ignore_ledges = False


class MineProjectile(Projectile):
    projectile_kind_code = b'mine'

    TRIGGER_RADIUS = 40
    BLAST_RADIUS = 115
    ACTIVATION_DELAY = 1    # s

    trajectory_shape = MineTrajectory
    triggered_by_explosions = True
    triggered_by_detonation_beam = True
    collides_with_players = True
    collision_check_buffer = 20 + TRIGGER_RADIUS

    def __init__(self, world, *args, player=None, rebuild_data=None, **kwargs):
        assert player is None or rebuild_data is None
        super().__init__(world, *args, **kwargs)

        # These are not sent over the wire to clients
        self.detonation_beam_hits = 0
        self.ticks_since_detonation_beam_hit = 0
        self.last_detonation_beam_player = None

        if rebuild_data is not None:
            self.player = world.getPlayer(rebuild_data['player'])
            self.team = world.getTeam(rebuild_data['team'])
            self.initial_angle = rebuild_data['throw_angle']
            self.stops = TrajectoryStops.rebuild(rebuild_data['stops'])
            self.pos = rebuild_data['pos']
            self.stuck_angle = rebuild_data['stuck_angle']
            self.active_countdown = rebuild_data['countdown']
        else:
            self.player = player
            self.team = player.team
            self.initial_angle = player.angleFacing
            self.stops = TrajectoryStops.from_iterator(
                self.trajectory_shape(world, player.pos, player.angleFacing).stops())
            self.pos = next(self.stops).pos
            self.stuck_angle = None
            self.active_countdown = round(self.ACTIVATION_DELAY / TICK_PERIOD)

        # We do this here instead of as a class attribute to avoid a
        # circular import.
        from trosnoth.model.upgrades import DetonationBeam
        self.required_detonation_beam_hits = round(
            DetonationBeam.time_to_detonate_mine / TICK_PERIOD)

    def dump(self):
        result = super().dump()
        result.update({
            'player': self.player.id,
            'team': self.team.id if self.team else NEUTRAL_TEAM_ID,
            'throw_angle': self.initial_angle,
            'stops': self.stops.dump(),
            'pos': self.pos,
            'stuck_angle': self.stuck_angle,
            'countdown': self.active_countdown,
        })
        return result

    @classmethod
    def rebuild(cls, world, data, **kwargs):
        mine = super().rebuild(world, data, rebuild_data=data, **kwargs)
        return mine

    @property
    def active(self):
        return self.stuck and self.active_countdown <= 0

    @property
    def stuck(self):
        return self.stuck_angle is not None

    def advance(self):
        if self.stuck:
            if self.world.isServer and self.id is not None and self.active_countdown == 1:
                self.check_for_nearby_mines()
            self.active_countdown = max(0, self.active_countdown - 1)
        else:
            try:
                stop = next(self.stops)
            except StopIteration:
                return
            if stop.collision_angle is None:
                self.pos = stop.pos
            else:
                self.pos = stop.collision_end
                self.stuck_angle = stop.collision_angle

        if self.world.isServer:
            if self.last_detonation_beam_player is None \
                    or not self.last_detonation_beam_player.one_tick_freeze:
                # If the firing player has lag, don't reset the count
                self.ticks_since_detonation_beam_hit += 1
            if self.ticks_since_detonation_beam_hit >= 2:
                self.ticks_since_detonation_beam_hit = 2
                self.detonation_beam_hits = 0
                self.last_detonation_beam_player = None

    def is_player_friendly(self, player):
        return player.isFriendsWithTeam(self.team) or player == self.player

    def check_collision(self, player):
        if not self.active:
            return False
        if not player.dead and not self.is_player_friendly(player):
            if distance(player.pos, self.pos) < self.TRIGGER_RADIUS:
                return True
        return False

    def collided_with(self, players):
        self.send_explosion()

    def hit_by_shot(self, shot):
        self.detonation_beam_hits += 1
        self.ticks_since_detonation_beam_hit = 0
        self.last_detonation_beam_player = shot.originatingPlayer

        if self.detonation_beam_hits >= self.required_detonation_beam_hits:
            self.detonation_beam_hits = 0
            self.last_detonation_beam_player = None
            self.send_explosion()

    def check_for_nearby_mines(self):
        for projectile in self.world.projectile_by_id.values():
            if not isinstance(projectile, MineProjectile):
                continue
            if not projectile.active:
                continue
            if projectile.team == self.team and self.team is not None:
                continue
            if projectile.player == self.player and self.player is not None:
                continue
            if distance(projectile.pos, self.pos) < self.TRIGGER_RADIUS:
                self.world.callLater(0.05, projectile.caught_in_explosion)

    def send_explosion(self):
        assert self.world.isServer and self.id is not None
        self.world.sendServerCommand(MineExplodedMsg(self.id))
        self.world.send_explosion_kills(
            killer=self.player,
            killer_team=self.team,
            pos=self.pos,
            radius=self.BLAST_RADIUS,
            kill_type=MINE_HIT,
            dentonate_friendly_projectiles=True,
        )

    def caught_in_explosion(self):
        if self.world.projectile_by_id.get(self.id) is not self:
            # We may have been removed before this callback
            return
        self.send_explosion()


class LocalMine(LocalUnit, MineProjectile):
    def __init__(self, local_state, *args, **kwargs):
        super().__init__(id_=None, *args, **kwargs)
        self.local_state = local_state
        self.server_projectile = None

    def check_collision(self, player):
        return False

    def match_projectile(self, server_projectile):
        self.server_projectile = server_projectile
        self.realShotStarted = True
