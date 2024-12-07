import logging
import random

from trosnoth.bots.goalsetter import (
    GoalSetterBot, Goal, RespawnNearZone, MessAroundInZone,
    ZoneMixin, RespawnNearPlayer,
)
from trosnoth.bots.orders import FollowPlayer
from trosnoth.const import (
    BOT_GOAL_HUNT_RABBITS, BOT_GOAL_SCORE_TROSBALL_POINT, BOT_GOAL_CAPTURE_MAP,
    BOT_GOAL_KILL_THINGS, BOT_GOAL_COWARDLY_CAPTURE,
)
from trosnoth.model import upgrades
from trosnoth.model.zonemechanics import (
    get_teams_with_enough_players_to_capture,
    get_teams_fulfilling_all_capture_conditions,
)
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


class ReachCurrentObjective(Goal):
    '''
    Notices what the current level's botGoal is and tries to achieve that goal.
    '''
    def start(self):
        self.bot.player.onRemovedFromGame.addListener(self.removedFromGame)
        self.bot.agent.localState.onGameInfoChanged.addListener(
            self.reevaluate)

    def stop(self):
        super(ReachCurrentObjective, self).stop()
        self.bot.agent.localState.onGameInfoChanged.removeListener(
            self.reevaluate)
        self.bot.player.onRemovedFromGame.removeListener(self.removedFromGame)

    def removedFromGame(self, playerId):
        self.returnToParent()

    def reevaluate(self):
        self.bot.setUpgradePolicy(None)
        if self.bot.game_is_over:
            self.setSubGoal(None)
            return
        botGoal = self.bot.agent.localState.botGoal
        if botGoal == BOT_GOAL_SCORE_TROSBALL_POINT:
            self.setSubGoal(ScoreTrosballPoint(self.bot, self))
        elif botGoal == BOT_GOAL_HUNT_RABBITS:
            # Rabbit hunt
            self.setSubGoal(HuntTheRabbits(self.bot, self))
        elif botGoal == BOT_GOAL_CAPTURE_MAP:
            self.setSubGoal(WinStandardTrosnothGame(self.bot, self))
        elif botGoal == BOT_GOAL_COWARDLY_CAPTURE:
            self.setSubGoal(CaptureZonesButDoNotDie(self.bot, self))
        elif botGoal == BOT_GOAL_KILL_THINGS:
            self.setSubGoal(HuntEnemies(self.bot, self))
        else:
            self.setSubGoal(RunAroundKillingHumans(self.bot, self))


class ScoreTrosballPoint(Goal):
    def start(self):
        self.bot.onOrderFinished.addListener(self.orderFinished)
        self.nextCheck = None
        super(ScoreTrosballPoint, self).start()

    def stop(self):
        self.bot.onOrderFinished.removeListener(self.orderFinished)
        if self.nextCheck:
            self.nextCheck.cancel()
        super(ScoreTrosballPoint, self).stop()

    def orderFinished(self):
        if self.subGoal is None:
            self.reevaluate()

    def reevaluate(self):
        if not self.bot.world.trosballManager.enabled:
            self.returnToParent()
            return
        player = self.bot.player
        world = self.bot.world

        if self.nextCheck:
            self.nextCheck.cancel()
        delay = 2.5 + random.random()
        self.nextCheck = world.callLater(delay, self.reevaluate)

        if player.dead:
            pos = world.trosballManager.getPosition()
            zone = world.rooms.get_at(pos)
            self.setSubGoal(RespawnNearZone(self.bot, self, zone))
        elif player.hasTrosball():
            zoneDef = world.trosballManager.getTargetZoneDefn(player.team)
            self.setSubGoal(None)
            self.bot.move_to_orb(world.zoneWithDef[zoneDef])
        elif world.trosballManager.trosballPlayer:
            self.setSubGoal(None)
            trosballPlayer = world.trosballManager.trosballPlayer
            if player.isFriendsWith(trosballPlayer):
                self.bot.followPlayer(trosballPlayer)
            else:
                self.bot.attackPlayer(trosballPlayer)
        else:
            self.setSubGoal(None)
            self.bot.collectTrosball()


class RunAroundKillingThings(Goal):
    def start(self):
        self.nextCheck = None
        self.scheduleNextCheck()

    def stop(self):
        super(RunAroundKillingThings, self).stop()
        self.cancelNextCheck()

    def scheduleNextCheck(self):
        self.cancelNextCheck()
        delay = 2.5 + random.random()
        self.nextCheck = self.bot.world.callLater(delay, self.reevaluate)

    def cancelNextCheck(self):
        if self.nextCheck:
            self.nextCheck.cancel()
            self.nextCheck = None

    def reevaluate(self, *args, **kwargs):
        self.cancelNextCheck()

        player = self.bot.player

        if player.dead:
            room = self.selectZone()
            if room is None:
                room = player.getZone()
                if room is None:
                    room = self.bot.world.rooms.random()
            self.setSubGoal(RespawnNearZone(self.bot, self, room))
            self.scheduleNextCheck()
            return

        if player.getZone() and self.zoneIsOk(player.getZone()):
            # There are enemies here
            self.setSubGoal(MessAroundInZone(self.bot, self))
            self.scheduleNextCheck()
            return

        room = self.selectZone()
        if room:
            self.setSubGoal(None)
            self.bot.move_to_orb(room)
        else:
            self.setSubGoal(MessAroundInZone(self.bot, self))
        self.scheduleNextCheck()

    def zoneIsOk(self, zone):
        return any(
            (not p.dead and not self.bot.player.isFriendsWith(p))
            for p in zone.players)

    def selectZone(self):
        options = []
        for room in self.bot.world.rooms:
            if self.zoneIsOk(room):
                options.append(room)
        if not options:
            return None
        return random.choice(options)


class RunAroundKillingHumans(RunAroundKillingThings):
    def zoneIsOk(self, zone):
        return any(
            (not p.dead and not self.bot.player.isFriendsWith(p) and not p.bot)
            for p in zone.players)


class HuntingGoal(Goal):
    def start(self):
        self.hunted_player = None
        self.delayed_check = None
        self.bot.onOrderFinished.addListener(self.order_finished)
        self.bot.player.onRespawned.addListener(self.respawned)
        super().start()

    def stop(self):
        self.bot.onOrderFinished.removeListener(self.order_finished)
        self.bot.player.onRespawned.removeListener(self.respawned)
        if self.delayed_check:
            self.delayed_check.cancel()
            self.delayed_check = None
        super().stop()

    def check_again_in(self, delay):
        if self.delayed_check:
            self.delayed_check.cancel()
        self.delayed_check = self.bot.world.callLater(delay, self.reevaluate)

    def order_finished(self):
        if self.subGoal is None:
            self.reevaluate()

    def respawned(self):
        self.reevaluate()

    def reevaluate(self):
        if self.delayed_check:
            self.delayed_check.cancel()
            self.delayed_check = None
        if self.bot.agent.stopped:
            # This test allows us to schedule timed calls to reevaluate
            # without having to worry about accidentally restarting a
            # stopped agent.
            return

        options = [p for p in self.bot.world.players if self.is_potential_target(p)]
        if not options:
            self.no_potential_targets()
            return
        old_target = self.hunted_player
        self.hunted_player = self.select_target(options)
        delay = 10 if (old_target and self.hunted_player != old_target) else 2
        self.check_again_in(delay)

        if self.bot.player.dead:
            self.setSubGoal(RespawnNearPlayer(self.bot, self, self.hunted_player))
            return

        self.setSubGoal(None)
        if isinstance(self.bot.currentOrder, FollowPlayer) \
                and self.bot.currentOrder.targetPlayer == self.hunted_player:
            # We're already attacking this player so no need to reset
            # any pathfinding calculations.
            return

        self.bot.attackPlayer(self.hunted_player)

    def is_potential_target(self, p):
        raise NotImplementedError('{}.is_potential_target'.format(type(self).__name__))

    def no_potential_targets(self):
        raise NotImplementedError('{}.no_potential_targets'.format(type(self).__name__))

    def select_target(self, potentials):
        raise NotImplementedError('{}.select_target'.format(type(self).__name__))


class HuntTheRabbits(HuntingGoal):
    def no_potential_targets(self):
        if self.bot.player.dead:
            self.bot.respawn()
            return

        # All survining rabbits are on this player's team
        self.setSubGoal(RunAway(self.bot, self))

    def is_potential_target(self, p):
        if p.dead:
            return False
        if self.bot.player.isFriendsWith(p):
            return False
        if p.team is None:
            return False
        return True

    def select_target(self, potentials):
        return random.choice(potentials)


class HuntEnemies(HuntingGoal):
    def no_potential_targets(self):
        self.hunted_player = None
        if self.bot.player.dead:
            self.bot.respawn()
        self.check_again_in(1)

    def is_potential_target(self, p):
        if p.dead:
            return False
        if self.bot.player.isFriendsWith(p):
            return False
        return True

    def select_target(self, potentials):
        my_pos = self.bot.player.pos
        scoreboard = self.bot.world.scoreboard
        best_score = -1
        best_target = None
        for player in potentials:
            d = distance(my_pos, player.pos)
            if d == 0:
                return player

            # Select player based on (score ** 2) / distance
            score = scoreboard.playerScores.get(player, 0) ** 2 / d
            if score > best_score:
                best_score = score
                best_target = player
        return best_target


class RunAway(Goal):
    '''
    Used when this is the last rabbit alive. Selects the zone furthest from
    the player and moves to it.
    '''
    def start(self):
        self.bot.onOrderFinished.addListener(self.orderFinished)
        super(RunAway, self).start()

    def stop(self):
        self.bot.onOrderFinished.removeListener(self.orderFinished)
        super(RunAway, self).stop()

    def orderFinished(self):
        self.reevaluate()

    def reevaluate(self):
        if self.bot.player.dead:
            self.returnToParent()
            return

        player_pos = self.bot.player.pos
        target_zone = max(
            self.bot.world.rooms,
            key=lambda r: distance(r.orb_pos or r.centre, player_pos))
        self.bot.move_to_orb(target_zone)


class WinStandardTrosnothGame(Goal):
    '''
    Win the current game of Trosnoth by capturing all the zones.
    '''

    def start(self):
        self.bot.setUpgradePolicy(upgrades.Shield, delay=6)

        self.nextCheck = None
        self.scheduleNextCheck()

    def scheduleNextCheck(self):
        self.cancelNextCheck()
        delay = 2.5 + random.random()
        self.nextCheck = self.bot.world.callLater(delay, self.reevaluate)

    def cancelNextCheck(self):
        if self.nextCheck:
            self.nextCheck.cancel()
            self.nextCheck = None

    def stop(self):
        super(WinStandardTrosnothGame, self).stop()
        self.cancelNextCheck()

    def reevaluate(self, *args, **kwargs):
        '''
        Decide whether to stay in the current zone, or move to another.
        '''
        self.cancelNextCheck()

        player = self.bot.player
        my_zone = None if player.dead else player.getZone()

        # 1. If we're defending a borderline zone, stay in the zone
        if my_zone and my_zone.owner == player.team:
            active_players = my_zone.get_active_players_by_team(sub_player=self.bot.player)
            friendly = len(active_players.get(player.team, []))
            enemy = max(
                (len(players) for team, players in active_players.items() if team != player.team),
                default=0,
            )

            if not (my_zone.dark and self.bot.world.abilities.slow_dark_conquest):
                capture_progress = 1
            else:
                capture_progress = my_zone.get_capture_progress().progress or 0

            if enemy == friendly and capture_progress > .5:
                self.setSubGoal(DefendZone(self.bot, self, my_zone))
                self.scheduleNextCheck()
                return

        # 2. If we're attacking a capturable zone, stay in the zone
        if (
                my_zone and my_zone.owner != player.team
                and player.team in get_teams_fulfilling_all_capture_conditions(
                    my_zone, sub_player=self.bot.player)):
            self.setSubGoal(CaptureZone(self.bot, self, my_zone))
            self.scheduleNextCheck()
            return

        # 3. If we've been cut off, activate bomber
        if (
                my_zone and my_zone.owner != player.team
                and not any(n.owner == player.team for n in my_zone.all_neighbours)):
            if not (self.heading_to_secluded_zone() or self.near_useful_zone(player, my_zone)):
                self.setSubGoal(Explode(self.bot, self))
                self.scheduleNextCheck()
                return

        # 4. Score other zones based on how helpful it would be to be there and
        #    how likely we are to get there in time.

        if my_zone is None:
            zone = self.getMostUrgentZone()
        else:
            zone = self.getMostLikelyUrgentZone(my_zone)

        if zone is None:
            self.returnToParent()
        elif zone.owner == player.team:
            self.setSubGoal(DefendZone(self.bot, self, zone))
        else:
            self.setSubGoal(CaptureZone(self.bot, self, zone))

        self.scheduleNextCheck()

    def near_useful_zone(self, player, current_room):
        # Don't activate bomber if we can quickly get back to a useful
        # zone.
        if len([p for p in player.world.players if p.team == player.team]) == 1:
            threshold = 1000
        else:
            threshold = 1550
        for room in current_room.all_neighbours:
            if any(z.owner == player.team for z in room.open_neighbours):
                if self.weighted_distance_to_orb(player, room) < threshold:
                    return True
        return False

    def weighted_distance_to_orb(self, player, room):
        dx = room.orb_pos[0] - player.pos[0]
        dy = room.orb_pos[1] - player.pos[1]
        if dy < 0:
            # Moving uphill is hard work
            dy *= 1.7
        return (dx ** 2 + dy ** 2) ** 0.5

    def heading_to_secluded_zone(self):
        if not isinstance(self.subGoal, CaptureZone):
            return False
        target_zone = self.subGoal.zone
        player = self.bot.player
        if target_zone.owner == player.team:
            # Can't capture a zone we already own
            return False
        if not any(n.owner == player.team for n in target_zone.all_neighbours):
            # Can't capture a zone with no adjacent friendly zones
            return False
        if any(n.owner == player.team for n in target_zone.open_neighbours):
            # Not secluded: has unblocked connection to friendly zone
            return False
        return True

    def getMostUrgentZone(self):
        best_score = 0
        best_options = []

        for room in self.bot.world.rooms:
            utility = self.getZoneUtility(room)

            if room.owner and not any(r.owner == room.owner for r in room.all_neighbours):
                # This is the last remaining zone
                awesomeness = 10
            else:
                awesomeness = room.consequenceOfCapture()

            score = utility * awesomeness
            if score == best_score:
                best_options.append(room)
            elif score > best_score:
                best_options = [room]
                best_score = score

        if not best_options:
            return None

        return random.choice(best_options)

    def getMostLikelyUrgentZone(self, myZone):
        best_score = 0
        best_options = []
        seen = set()
        pending = [(myZone, 1.0)]
        while pending:
            room, likelihood = pending.pop(0)
            seen.add(room)

            utility = self.getZoneUtility(room)

            if room.owner and not any(r.owner == room.owner for r in room.all_neighbours):
                # This is the last remaining zone
                awesomeness = 5
            else:
                awesomeness = room.consequenceOfCapture()

            score = likelihood * utility * awesomeness
            if score == best_score:
                best_options.append(room)
            elif score > best_score:
                best_options = [room]
                best_score = score

            likelihood *= 0.7
            for other in room.open_neighbours:
                if other not in seen:
                    pending.append((other, likelihood))

        if not best_options:
            return None

        return random.choice(best_options)

    def getZoneUtility(self, zone):
        '''
        How useful would it be to be in this zone?
        '''
        player = self.bot.player
        alreadyHere = player.getZone() == zone and not player.dead

        # Count the number of friendly players and players on the most
        # likely enemy team to tag the zone.
        enemy = friendly = 0
        for count, teams in zone.getPlayerCounts():
            if player.team in teams and friendly == 0:
                friendly = count
            if [t for t in teams if t != player.team] and enemy == 0:
                enemy = count
            if friendly and enemy:
                break

        if zone.owner == player.team:
            if not alreadyHere:
                friendly += 1
            defence = min(3, friendly)
            if enemy == 0:
                utility = 0
            elif enemy > defence:
                # There's a slim chance you could shoot them before they
                # capture the zone.
                utility = 0.2 ** (enemy - defence)
            elif enemy == defence:
                # Being here will stop it being tagged
                utility = 1
            else:
                # There's a slim chance the enemy might shoot them
                utility = 0.2 ** (friendly - enemy)
        elif not any(n.owner == player.team for n in zone.all_neighbours):
            # Cannot capture, have no adjacent zones
            utility = 0

        else:
            defence = min(3, enemy)
            if alreadyHere:
                friendly -= 1
            if friendly > defence:
                # Capturable without player, but there's a slim chance
                # teammates might die
                utility = 0.2 ** (friendly - defence)
            elif friendly == defence:
                # Being here enables the zone tag
                utility = 1
            else:
                # There's a slim chance you could shoot them and capture
                utility = 0.2 ** (enemy - friendly)

        if zone.dark and self.bot.world.abilities.slow_dark_conquest:
            # If the zone will take a while before it can be
            # captured, scale down the utility.
            capture_progress = zone.get_capture_progress()
            utility *= min((capture_progress.progress or 0) + .25, 1)

        return utility


class CaptureZonesButDoNotDie(Goal):
    '''
    This bot goal is used for villagers in the space vampire game mode.
    Bots with this goal are cautious, but do capture zones if it's safe.
    '''

    def __init__(self, bot, parent):
        super().__init__(bot, parent)
        self.next_check = None

    def start(self):
        self.bot.set_dodges_bullets(True)
        self.bot.onOrderFinished.addListener(self.order_finished)
        super().start()
        self.schedule_next_check()

    def stop(self):
        self.cancel_next_check()
        self.bot.onOrderFinished.removeListener(self.order_finished)
        super().stop()

    def schedule_next_check(self):
        self.cancel_next_check()
        delay = 3 + random.random()
        self.next_check = self.bot.world.callLater(delay, self.reevaluate)

    def cancel_next_check(self):
        if self.next_check:
            self.next_check.cancel()
            self.next_check = None

    def order_finished(self):
        self.reevaluate()

    def reevaluate(self):
        self.cancel_next_check()

        my_zone = self.bot.player.getZone()
        if self.bot.player.dead:
            respawn_room = my_zone
            if not respawn_room:
                respawn_room = self.bot.world.rooms.random()
            self.setSubGoal(RespawnNearZone(self.bot, self, respawn_room))
            return

        if not my_zone:
            from trosnoth.bots.silver import MoveIntoMap
            self.setSubGoal(MoveIntoMap(self.bot, self))

        elif self.in_scary_zone():
            if random.random() > .3:
                self.leave_zone(nearest=True)
            else:
                self.leave_zone()

        elif self.enemies_are_in_zone():
            self.setSubGoal(KillEnemyInZone(self.bot, self))

        elif my_zone.owner == self.bot.player.team:
            self.leave_zone()

        elif self.bot.player.team in get_teams_fulfilling_all_capture_conditions(
                my_zone, sub_player=self.bot.player):
            self.setSubGoal(None)
            self.bot.move_to_orb(my_zone)

        else:
            self.setSubGoal(None)
            self.bot.standStill()

        self.schedule_next_check()

    def in_scary_zone(self):
        me = self.bot.player
        here = me.getZone()
        friendly_hitpoints = sum(
            p.health for p in here.players if me.isFriendsWith(p) and not p.dead)
        enemy_hitpoints = sum(
            p.health for p in here.players if not me.isFriendsWith(p) and not p.dead)
        return 1.5 * enemy_hitpoints >= friendly_hitpoints

    def leave_zone(self, nearest=False):
        me = self.bot.player
        here = me.getZone()
        neighbours = list(here.open_neighbours)
        if not neighbours:
            target = here
        elif nearest:
            target = min(neighbours, key=lambda room: distance(room.centre, me.pos))
        else:
            choices = [z for z in neighbours if z.owner != me.team]
            if not choices or random.random() < .3:
                choices = neighbours
            target = random.choice(choices)

        self.setSubGoal(None)
        self.bot.move_to_orb(target)

    def enemies_are_in_zone(self):
        me = self.bot.player
        here = me.getZone()
        return any(not me.isFriendsWith(p) and not p.dead for p in here.players)


class Explode(Goal):
    def start(self):
        self.bot.onTick.addListener(self.tick)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onTick.removeListener(self.tick)

    def reevaluate(self):
        if self.bot.player.dead:
            self.returnToParent()
            return

        if not self.bot.player.bomber:
            self.bot.standStill()
            self.bot.buy_upgrade(upgrades.Bomber)

    def tick(self):
        if self.bot.player.dead:
            self.returnToParent()


class CaptureZone(ZoneMixin, Goal):
    '''
    Respawns if necessary, moves to the given zone, messes around until it's
    capturable, and captures it. If the player dies, respawns and tries again.
    Returns if the zone is captured or becomes uncapturable by virtue of having
    no adjacent zones owned by the team.
    '''

    def __init__(self, bot, parent, zone):
        super(CaptureZone, self).__init__(bot, parent)
        self.zone = zone

    def start(self):
        self.bot.onOrderFinished.addListener(self.orderFinished)
        self.zone.on_capture_progress_complete.addListener(self.reevaluate)
        super(CaptureZone, self).start()

    def stop(self):
        super(CaptureZone, self).stop()
        self.zone.on_capture_progress_complete.removeListener(self.reevaluate)
        self.bot.onOrderFinished.removeListener(self.orderFinished)

    def orderFinished(self):
        self.reevaluate()

    def reevaluate(self, *args, **kwargs):
        player = self.bot.player
        if self.zone.owner == player.team:
            self.returnToParent()
            return

        if not any(n.owner == player.team for n in self.zone.all_neighbours):
            self.returnToParent()
            return

        if player.dead:
            self.setSubGoal(RespawnNearZone(self.bot, self, self.zone))
            return

        player_zone = player.getZone()
        if player_zone == self.zone:
            if player.team in get_teams_fulfilling_all_capture_conditions(
                    self.zone, sub_player=self.bot.player):
                self.setSubGoal(None)
                self.bot.move_to_orb(self.zone)
            elif player.team in get_teams_with_enough_players_to_capture(
                    self.zone, sub_player=self.bot.player):
                self.setSubGoal(MessAroundInZone(self.bot, self))
            else:
                self.setSubGoal(KillEnemyInZone(self.bot, self))
        else:
            self.setSubGoal(None)
            self.bot.move_to_room(self.zone)


class DefendZone(ZoneMixin, Goal):
    '''
    Respawns if necessary, moves to the given zone and messes around there.
    If the player dies, respawns and continues. Returns if the zone is
    captured or neutralised.
    '''

    def __init__(self, bot, parent, zone):
        super(DefendZone, self).__init__(bot, parent)
        self.zone = zone

    def reevaluate(self):
        player = self.bot.player
        if self.zone.owner != player.team:
            self.returnToParent()
            return

        if player.dead:
            self.setSubGoal(RespawnNearZone(self.bot, self, self.zone))
            return

        player_zone = player.getZone()
        if player_zone == self.zone:
            teams_who_can_tag = get_teams_with_enough_players_to_capture(self.zone)
            if teams_who_can_tag:
                # Our only hope is to kill someone
                self.setSubGoal(KillEnemyInZone(self.bot, self))
            else:
                self.setSubGoal(MessAroundInZone(self.bot, self))
        else:
            self.setSubGoal(None)
            self.bot.move_to_orb(self.zone)


class KillEnemyInZone(Goal):
    '''
    Tries to kill the nearest enemy while staying in the current zone.
    Completes if the number of players in the zone changes. Aborts if the
    player dies or leaves the zone.
    '''

    def __init__(self, bot, parent):
        super(KillEnemyInZone, self).__init__(bot, parent)
        self.zone = self.bot.player.getZone()
        self.playersInZone = set(p for p in self.zone.players if not p.dead)
        self.nextCheck = None

    def start(self):
        super(KillEnemyInZone, self).start()
        self.scheduleNextCheck()

    def stop(self):
        super(KillEnemyInZone, self).stop()
        self.cancelNextCheck()

    def scheduleNextCheck(self):
        self.cancelNextCheck()
        delay = 1
        self.nextCheck = self.bot.world.callLater(delay, self.reevaluate)

    def cancelNextCheck(self):
        if self.nextCheck:
            self.nextCheck.cancel()
            self.nextCheck = None

    def reevaluate(self):
        if self.bot.player.dead:
            self.returnToParent()
            return

        zone = self.bot.player.getZone()
        if zone != self.zone:
            self.returnToParent()
            return

        playersInZone = set(p for p in zone.players if not p.dead)
        if playersInZone != self.playersInZone:
            self.returnToParent()
            return

        enemiesInZone = [
            p for p in playersInZone if not p.isFriendsWith(self.bot.player)]
        if not enemiesInZone:
            self.returnToParent()
            return

        target = min(
            enemiesInZone, key=lambda p: distance(p.pos, self.bot.player.pos))
        self.bot.attackPlayer(target)


class RangerBot(GoalSetterBot):
    nick = 'RangerBot'
    generic = True

    MainGoalClass = ReachCurrentObjective


BotClass = RangerBot
