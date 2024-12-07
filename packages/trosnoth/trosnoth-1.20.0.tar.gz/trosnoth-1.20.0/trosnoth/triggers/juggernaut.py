import random

from trosnoth.messages import AwardPlayerCoinMsg
from trosnoth.triggers.base import Trigger
from trosnoth.utils.event import Event


class ReachScoreVictoryTrigger(Trigger):
    '''
    Trigger the end of the game when a score threshold is reached
    '''

    def __init__(self, level, required_score):
        super().__init__(level)
        self.on_victory = Event([])
        self.required_score = required_score

    def doActivate(self):
        self.world.scoreboard.on_change.addListener(
            self.got_scoreboard_change, lifespan=self.lifespan)

    def got_scoreboard_change(self, target, new_score):
        if target and new_score >= self.required_score:
            self.on_victory()


class AwardCoinsOnHitTrigger(Trigger):
    '''
    When a player is hurt, award coins to the attacker.
    '''

    def __init__(self, level, damage_coins):
        super().__init__(level)
        self.level = level
        self.damage_coins = damage_coins

    def doActivate(self):
        self.world.on_player_health_decreased.addListener(
            self.player_health_decreased, lifespan=self.lifespan)

    def player_health_decreased(self, player, hitter, damage):
        if hitter is not None:
            if player.health <= 0:
                damage -= 1
            if damage > 0:
                self.world.sendServerCommand(
                    AwardPlayerCoinMsg(hitter.id, self.damage_coins * damage))


class JuggernautTransferTrigger(Trigger):
    '''
    When the juggernaut dies or leaves the game, one of the players who
    hurt the juggernaut becomes the new juggernaut.
    '''

    def __init__(self, level, give_juggernaut_function):
        super().__init__(level)
        self.give_juggernaut = give_juggernaut_function
        self.juggernaut_candidates = []

    def doActivate(self):
        self.world.juggernaut.on_death_of_possessor.addListener(
            self.select_new_juggernaut, lifespan=self.lifespan)
        self.world.juggernaut.on_possessor_left_game.addListener(
            self.select_new_juggernaut, lifespan=self.lifespan)
        self.world.on_player_health_decreased.addListener(
            self.player_health_decreased, lifespan=self.lifespan)

    def player_health_decreased(self, player, hitter, damage):
        if player.is_juggernaut() and hitter is not None:
            self.juggernaut_candidates.append(hitter)

    def select_new_juggernaut(self, *args, **kwargs):
        candidates = [
            p for p in self.juggernaut_candidates
            if p != self.world.juggernaut.possessor and not p.dead]
        self.juggernaut_candidates = []

        if not candidates:
            self.give_juggernaut(None)
        else:
            self.give_juggernaut(random.choice(candidates))
