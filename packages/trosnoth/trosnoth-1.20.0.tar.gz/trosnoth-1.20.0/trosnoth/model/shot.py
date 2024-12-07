import copy
import logging
from math import sin, cos, atan2, sqrt
import random

import pygame

from trosnoth.const import TICK_PERIOD, SHOT_HIT
from trosnoth.messages import PlayerHitMsg
from trosnoth.model.physics import CollisionCircle
from trosnoth.model.unit import (
    Unit, Bouncy, PredictedTrajectory, TrajectoryClickAction,
)
from trosnoth.model.universe_base import NO_PLAYER, NEUTRAL_TEAM_ID
from trosnoth.trosnothgui.common import get_mouse_pos
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen
from trosnoth.utils.collision import collideTrajectory
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)

GRENADE_BLAST_RADIUS = 448


class LocalUnit(Unit):
    '''
    Mixin for representing the local player's shots and grenades.
    These may behave differently from their synchronised counterpart,
    e.g., go slowly until their real counterpart catches up.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nextPos = None
        self.localTicks = 0
        self.realTicks = 0
        self.realShotStarted = False
        self.realShotCaughtUp = False
        self.onRealShotCaughtUp = Event(['sprite'])

    def advance(self):
        if self.realShotCaughtUp:
            super().advance()
            return

        if self.realShotStarted:
            self.realTicks += 1

        if self.nextPos:
            self.pos = self.nextPos
            self.nextPos = None
            self.localTicks += 1
            if self.realTicks >= self.localTicks:
                self.realShotCaughtUp = True
                self.onRealShotCaughtUp(self)
        else:
            super().advance()
            self.nextPos = self.pos
            self.pos = (
                0.5 * self.pos[0] + 0.5 * self.oldPos[0],
                0.5 * self.pos[1] + 0.5 * self.oldPos[1],
            )


class GrenadeShot(Bouncy):
    RADIUS = 5
    DURATION = 2.5
    collision_shape = CollisionCircle(RADIUS)

    def __init__(self, world, player):
        Bouncy.__init__(self, world)
        self.player = player
        self.timeLeft = self.DURATION

        # Place myself.
        self.pos = self.oldPos = player.pos
        angle = player.angleFacing
        self.xVel = self.world.physics.grenadeInitVel * sin(angle)
        self.yVel = -self.world.physics.grenadeInitVel * cos(angle)

    def dump(self):
        return {
            'player': self.player.id if self.player else NO_PLAYER,
            'pos': self.pos,
            'xVel': self.xVel,
            'yVel': self.yVel,
            'timeLeft': self.timeLeft,
        }

    @classmethod
    def rebuild(cls, world, data, **kwargs):
        result = cls(world=world, player=world.getPlayer(data['player']), **kwargs)
        result.timeLeft = data['timeLeft']
        result.pos = result.oldPos = data['pos']
        result.xVel = data['xVel']
        result.yVel = data['yVel']
        return result

    def getGravity(self):
        return self.world.physics.grenadeGravity

    def getMaxFallVel(self):
        return self.world.physics.grenadeMaxFallVel

    def advance(self):
        super(GrenadeShot, self).advance()
        self.timeLeft -= self.world.tickPeriod
        if self.timeLeft <= 0:
            self.removeGrenade()
            self.propagateExplosionEvent()

    def propagateExplosionEvent(self):
        self.world.grenadeExploded(self.player, self.pos, GRENADE_BLAST_RADIUS)

    def removeGrenade(self):
        self.world.removeGrenade(self)


class LocalGrenade(LocalUnit, GrenadeShot):
    def __init__(self, local_state, *args, **kwargs):
        super(LocalGrenade, self).__init__(*args, **kwargs)
        self.localState = local_state

    def propagateExplosionEvent(self):
        pass

    def removeGrenade(self):
        self.localState.grenadeRemoved()


class Shot(Unit):

    GRACE_TIME = 1

    playerCollisionTolerance = 17
    collision_check_buffer = 50

    def __init__(
            self, world, id_, team, player, pos, velocity, gun_type, lifetime,
            *args, **kwargs):
        super().__init__(world, *args, **kwargs)

        self.onRebound = Event(['pos'])
        self.onExpire = Event([])
        self.id = id_
        self.team = None if gun_type.neutral_shots else team
        self.pos = tuple(pos)
        self.futurePositions = []
        self.futureVelocities = []
        self.futureBounces = []
        self.originatingPlayer = player if gun_type.attribute_shots_to_shooter else None
        self.vel = tuple(velocity)
        self.timeLeft = lifetime
        self.gun_type = gun_type
        self.expired = False
        self.justFired = True
        self.hasBounced = False
        self.health = gun_type.shot_health
        self.collision_shape = CollisionCircle(gun_type.shot_rebound_radius)
        self.grace_players = {player: self.GRACE_TIME // TICK_PERIOD}
        self.currently_colliding = False
        self.separate_collisions = 0

    def dump(self):
        return {
            'id': self.id,
            'team': self.team.id if self.team else NEUTRAL_TEAM_ID,
            'pos': self.pos,
            'vel': self.vel,
            'shooter': self.originatingPlayer.id if self.originatingPlayer else 0,
            'time': self.timeLeft,
            'gun_code': self.gun_type.gun_code,
            'health': self.health,
            'colliding': self.currently_colliding,
            'collisions': self.separate_collisions,
            'just_fired': self.justFired,
        }

    @classmethod
    def rebuild(cls, world, data):
        from trosnoth.model.upgrades import gun_type_by_code
        shot = cls(
            world, data['id'], world.getTeam(data['team']),
            world.getPlayer(data['shooter']), tuple(data['pos']),
            tuple(data['vel']), gun_type_by_code[data['gun_code']], data['time'])
        shot.health = data.get('health', 1)
        shot.currently_colliding = data.get('colliding', False)
        shot.separate_collisions = data.get('collisions', 0)
        shot.justFired = data.get('just_fired', False)
        return shot

    def check_collision(self, player):
        if not self.gun_type.shots_hurt_players:
            return False
        if player.is_invulnerable():
            return False
        if player.isFriendsWithTeam(self.team):
            return False
        if player == self.originatingPlayer:
            return False
        if player in self.grace_players:
            return False
        return self.checkCollisionsWithPoints(player.oldPos, player.pos)

    def checkCollisionsWithPoints(self, oldPos, newPos, ticksInFuture=0):
        '''
        Checks whether a player moving between the given points will collide
        with this shot. If futureTicks is given, it is the number of ticks
        in the future (for this shot) that we are checking these points.
        '''
        oldShotPos, newShotPos = self.getFuturePoints(ticksInFuture)
        if oldShotPos is None:
            # Shot has expired
            return False

        # Check both player colliding with us and us colliding with player
        if collideTrajectory(
                newPos, oldShotPos,
                (newShotPos[0] - oldShotPos[0], newShotPos[1] - oldShotPos[1]),
                self.playerCollisionTolerance + self.gun_type.shot_damage_radius):
            return True

        deltaX = newPos[0] - oldPos[0]
        deltaY = newPos[1] - oldPos[1]
        if collideTrajectory(
                newShotPos, oldPos, (deltaX, deltaY),
                self.playerCollisionTolerance + self.gun_type.shot_damage_radius):
            return True
        return False

    def collided_with(self, players):
        # If multiple players are hit in the same tick, the server
        # randomly selects one to die.
        hit_player = random.choice(players)

        if not self.originatingPlayer or self.originatingPlayer.id == -1:
            originating_player_id = NO_PLAYER
        else:
            originating_player_id = self.originatingPlayer.id
        self.world.sendServerCommand(PlayerHitMsg(
            hit_player.id, SHOT_HIT, 1, originating_player_id, shotId=self.id))

    def hitPlayer(self, player, hitpoints):
        self.health -= 1
        if self.health == 0:
            self.expired = True
        player.onHitByShot(self)
        self.grace_players[player] = self.GRACE_TIME // TICK_PERIOD
        if self.originatingPlayer is not None:
            self.originatingPlayer.onShotHitSomething(self)
            if hitpoints:
                self.originatingPlayer.onShotHurtPlayer(player, self)
        if self.health == 0:
            self.onExpire()

    def getFuturePoints(self, ticksInFuture=0):
        '''
        @return: (oldPos, newPos) for a tick the given number of ticks in
            the future, or (None, None) if the shot has expired by that
            time. Calls extendFuturePositions() if needed.
        '''
        if self.expired:
            return None, None
        if ticksInFuture == 0:
            return self.oldPos, self.pos
        ticksLeft = (self.timeLeft + 0.00001) // self.world.tickPeriod
        if ticksInFuture > ticksLeft:
            return None, None

        while len(self.futurePositions) < ticksInFuture:
            if self.futureHasExpired():
                return None, None
            self.extendFuturePositions()

        if ticksInFuture < 2:
            assert ticksInFuture == 1
            oldPos = self.pos
        else:
            oldPos = self.futurePositions[ticksInFuture - 2]
        newPos = self.futurePositions[ticksInFuture - 1]
        if newPos is None:
            oldPos = None
        return oldPos, newPos

    def futureHasExpired(self):
        if self.expired:
            return True
        return self.futurePositions and self.futurePositions[-1] is None

    def getFutureVelocity(self):
        if self.futureVelocities:
            return self.futureVelocities[-1]
        return self.vel

    def extendFuturePositions(self):
        unit = copy.copy(self)
        unit.oldPos, unit.pos = self.getFuturePoints(len(self.futurePositions))
        unit.vel = self.getFutureVelocity()

        deltaT = self.world.tickPeriod
        delta = (unit.vel[0] * deltaT, unit.vel[1] * deltaT)
        final_pos, collision = self.world.physics.getMotion(
            unit, delta, ignoreLedges=True,
            collide_with_zone_boundaries=self.gun_type.shots_rebound_at_zone_boundary)

        bounce_pos = None
        expired = False

        if self.currently_colliding:
            unit.pos = (unit.pos[0] + delta[0], unit.pos[1] + delta[1])
            if not collision:
                self.currently_colliding = False
                self.timeLeft = min(self.gun_type.shot_lifetime / 5, self.timeLeft)

        elif collision and self.separate_collisions < self.gun_type.obstacles_pierced:
            # Move the shot through the obstacle, but notice the collision
            unit.pos = (unit.pos[0] + delta[0], unit.pos[1] + delta[1])
            self.currently_colliding = True
            self.separate_collisions += 1

        else:
            unit.pos = final_pos

            if collision:
                if self.gun_type.shots_rebound:
                    bounce_pos = unit.pos
                    self.separate_collisions += 1
                    self.rebound(unit, collision)
                else:
                    expired = True

        self.futurePositions.append(unit.pos)
        self.futureVelocities.append(unit.vel)
        if expired:
            self.futurePositions.append(None)
            self.futureVelocities.append(unit.vel)
        if bounce_pos is not None:
            # Must be done after all additions to futurePositions, so
            # that len(self.futurePositions) is the correct value.
            self.futureBounces.append((len(self.futurePositions), bounce_pos))

    def advance(self):
        '''
        Called by the universe when this shot should update its position.
        '''
        if self.expired:
            return
        self.justFired = False

        deltaT = self.world.tickPeriod

        oldPos, pos = self.getFuturePoints(ticksInFuture=1)
        if self.futurePositions:
            self.futurePositions.pop(0)
            self.vel = self.futureVelocities.pop(0)
            if self.futureBounces:
                for i, (t, pos) in enumerate(self.futureBounces):
                    self.futureBounces[i] = (max(0, t - 1), pos)

                t, pos = self.futureBounces[0]
                if t == 0:
                    self.futureBounces.pop(0)
                    self.hasBounced = True
                    self.onRebound(pos)

        # Shots have a finite lifetime.
        self.timeLeft = self.timeLeft - deltaT

        if pos is None:
            self.expired = True
            self.onExpire()
        else:
            self.pos = pos

            for player in list(self.grace_players):
                self.grace_players[player] -= 1
                if self.grace_players[player] <= 0:
                    del self.grace_players[player]

    def rebound(self, unit, collision):
        '''
        Shot is a ricochet shot and it's hit an obstacle.
        '''
        obsAngle = collision.angle
        shotAngle = atan2(unit.vel[1], unit.vel[0])
        dif = shotAngle - obsAngle
        final = obsAngle - dif
        speed = sqrt(unit.vel[0] * unit.vel[0] + unit.vel[1] * unit.vel[1])
        unit.vel = (speed * cos(final), speed * sin(final))


class LocalShot(LocalUnit, Shot):
    def advance(self):
        self.justFired = False
        super(LocalShot, self).advance()


class PredictedRicochetTrajectory(PredictedTrajectory):
    click_action = TrajectoryClickAction.SHOOT

    def __init__(self, world, player):
        from trosnoth.model.upgrades import Ricochet
        self.world = world
        self.player = player
        self.collision_shape = CollisionCircle(Ricochet.shot_rebound_radius)

    def predictedTrajectoryPoints(self):
        from trosnoth.model.upgrades import Ricochet
        shot = self.player.createShot(shotClass=LocalShot, gun_type=Ricochet)

        i = 0
        while True:
            _, pos = shot.getFuturePoints(i)
            if pos is None:
                return
            yield pos
            i += 1


class PredictedGhostShotTrajectory(PredictedTrajectory):
    click_action = TrajectoryClickAction.RESPAWN_SHOOT

    def __init__(self, world, player, viewManager):
        self.world = world
        self.player = player
        self.viewManager = viewManager

    def get_target_angle(self, playerPos=None):
        if playerPos is None:
            livePlayer = self.player.clone()
            livePlayer.respawn()
            playerPos = livePlayer.pos

        focus = self.viewManager._focus
        area = self.viewManager.sRect
        playerScreenPos = mapPosToScreen(playerPos, focus, area)
        targetPos = get_mouse_pos()
        return atan2(
            targetPos[0] - playerScreenPos[0],
            -(targetPos[1] - playerScreenPos[1]))

    def predictedTrajectoryPoints(self):
        livePlayer = self.player.clone()
        livePlayer.respawn()
        livePlayer.lookAt(self.get_target_angle(livePlayer.pos))
        shot = livePlayer.createShot(shotClass=LocalShot)

        i = 0
        while True:
            _, pos = shot.getFuturePoints(i)
            if pos is None:
                return
            yield pos
            i += 1
