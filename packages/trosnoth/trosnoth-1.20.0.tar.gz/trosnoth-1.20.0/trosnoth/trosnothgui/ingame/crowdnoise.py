from typing import Optional

from trosnoth import const
from trosnoth.model.zonemechanics import get_teams_with_enough_players_to_capture
from trosnoth.utils.lifespan import LifeSpan
from trosnoth.utils.math import fadeValues, distance


class CrowdNoiseGenerator:
    def __init__(self, app, world):
        self.lifespan = LifeSpan()
        self.app = app
        self.world = world
        self.excitement_driver = None
        self.baseline = 0.03
        self.spike_level = 0.03
        self.current_level = 0.
        self.driver_kind = None

        world.on_before_tick.addListener(self.world_tick, lifespan=self.lifespan)
        world.uiOptions.onChange.addListener(self.ui_options_changed, lifespan=self.lifespan)
        world.on_pause_state_changed.addListener(self.pause_state_changed, lifespan=self.lifespan)

    def stop(self):
        self.lifespan.stop()
        if self.excitement_driver:
            self.excitement_driver.stop()
        self.app.soundPlayer.stop_crowd_noise()

    def pause_state_changed(self):
        if self.world.paused:
            self.app.soundPlayer.stop_crowd_noise(fade_time=2)
            self.current_level = 0.

    def world_tick(self):
        if self.excitement_driver:
            self.excitement_driver.tick()
        self.app.soundPlayer.set_crowd_current_volume(self.current_level)
        self.current_level = fadeValues(self.current_level, self.spike_level, 0.1)
        self.spike_level = fadeValues(self.spike_level, self.baseline, 0.02)

    def ui_options_changed(self):
        if (crowd_kind := self.world.uiOptions.crowd_kind) == const.BOT_GOAL_CAPTURE_MAP:
            driver_kind = MapCaptureDriver
        elif crowd_kind == const.BOT_GOAL_NONE:
            driver_kind = BoringDriver
        else:
            driver_kind = DogFightDriver

        if self.driver_kind == driver_kind:
            return

        if self.excitement_driver:
            self.excitement_driver.stop()
        self.excitement_driver = driver_kind(self)
        self.driver_kind = driver_kind

    def set_baseline(self, baseline):
        self.baseline = min(1, max(0, baseline))

    def spike(self, amazement):
        self.spike_level = fadeValues(self.spike_level, 1, min(1, max(0, amazement)))


class ExcitementDriver:
    def __init__(self, noise_generator):
        self.lifespan = LifeSpan()
        self.noise_generator = noise_generator
        self.world = noise_generator.world

    def stop(self):
        self.lifespan.stop()

    def tick(self):
        pass


class MapCaptureDriver(ExcitementDriver):
    def __init__(self, noise_generator):
        super().__init__(noise_generator)
        self.game_over = False

        self.world.onZoneTagged.addListener(self.orb_tagged, lifespan=self.lifespan)
        self.world.onPlayerKill.addListener(self.player_killed, lifespan=self.lifespan)
        self.world.on_result_set.addListener(self.world_result_set, lifespan=self.lifespan)

        self.recalculate_baseline()

    def tick(self):
        self.recalculate_baseline()

    def orb_tagged(self, zone, player, previous_owner):
        self.noise_generator.spike(0.25)

    def recalculate_baseline(self):
        tag_distance: Optional[float] = None
        room_counts = {t: 0 for t in self.world.teams}
        for room in self.world.rooms:
            if room.owner:
                room_counts[room.owner] += 1
            teams = get_teams_with_enough_players_to_capture(room)
            if teams:
                min_attacker_distance = min(
                    distance(room.orb_pos, p.pos)
                    for p in room.players
                    if p.team in teams and not p.dead)
                if tag_distance is None:
                    tag_distance = min_attacker_distance
                else:
                    tag_distance = min(tag_distance, min_attacker_distance)

        baseline = 0.03
        min_rooms_owned = min(room_counts.values())

        excitement_mark = max(2, min(4, round(len(self.world.rooms) / 6)))
        if min_rooms_owned <= excitement_mark:
            baseline += 0.06 + 0.06 * (excitement_mark - min_rooms_owned) / (excitement_mark - 1)
        else:
            half_rooms = len(self.world.rooms) // 2
            baseline += 0.06 * (half_rooms - min_rooms_owned) / (half_rooms - excitement_mark)

        if tag_distance is not None:
            baseline *= 1 / (tag_distance / 300 + 1) + 1

        clock = self.world.clock
        if clock.counting and not clock.upwards:
            baseline *= 1 / (clock.value / 60 + 1) + 1

        self.noise_generator.set_baseline(baseline)

    def player_killed(self, killer, target, hit_kind):
        self.noise_generator.spike(0.1)

    def world_result_set(self):
        if self.game_over:
            return
        self.game_over = True
        self.noise_generator.spike(1)


class BoringDriver(ExcitementDriver):
    def __init__(self, noise_generator):
        super().__init__(noise_generator)
        noise_generator.set_baseline(0.02)


class DogFightDriver(ExcitementDriver):
    def __init__(self, noise_generator):
        super().__init__(noise_generator)
        self.game_over = False

        self.world.onPlayerKill.addListener(self.player_killed, lifespan=self.lifespan)
        self.world.on_result_set.addListener(self.world_result_set, lifespan=self.lifespan)

        self.recalculate_baseline()

    def tick(self):
        self.recalculate_baseline()

    def recalculate_baseline(self):
        baseline = 0.03
        clock = self.world.clock
        if clock.counting and not clock.upwards:
            baseline += 0.27 / (clock.value / 60 + 1)

        self.noise_generator.set_baseline(baseline)

    def player_killed(self, killer, target, hit_kind):
        self.noise_generator.spike(0.4)

    def world_result_set(self):
        if self.game_over:
            return
        self.game_over = True
        self.noise_generator.spike(1)
