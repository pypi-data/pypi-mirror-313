import logging

import pygame

import trosnoth.data.sound as sound
from trosnoth.data import getPath
from trosnoth.utils.math import distance


log = logging.getLogger(__name__)


def get_sound_volume(dist, loud_radius=500):
    return max(0, 1 / max(1, dist / loud_radius) ** 2 - 0.01)


def get_distance(origin, pos, x_offset=0):
    x, y = origin
    x += x_offset
    return distance((x, y), pos)


class SoundAction(object):
    def __init__(self, filename, channel):
        self.channel = channel
        if not pygame.mixer.get_init():
            return

        try:
            self.sound = pygame.mixer.Sound(getPath(sound, filename))
        except Exception:
            self.sound = None
            log.exception('Error loading sound file')
        self.master_volume = 1

    def play(self, origin=None, pos=None):
        if self.sound is None or not pygame.mixer.get_init():
            return
        if origin is None or pos is None:
            l_volume = r_volume = 1
        else:
            l_volume = get_sound_volume(get_distance(origin, pos, x_offset=-250))
            r_volume = get_sound_volume(get_distance(origin, pos, x_offset=250))

        l_volume *= self.master_volume
        r_volume *= self.master_volume
        if l_volume < 0.01 and r_volume < 0.01:
            return

        if self.channel:
            channel = pygame.mixer.Channel(self.channel)
            channel.play(self.sound)
        else:
            channel = self.sound.play()

        if channel:
            channel.set_volume(l_volume, r_volume)

    def set_master_volume(self, val):
        self.master_volume = val


class LoopingSound:
    def __init__(self, filename, channels, master_volume=1.):
        if not pygame.mixer.get_init():
            return
        self.channels = [pygame.mixer.Channel(c) for c in channels]
        self.master_volume = master_volume

        try:
            self.sound = pygame.mixer.Sound(getPath(sound, filename))
        except Exception:
            self.sound = None
            log.exception('Error loading sound file')

    def set_master_volume(self, master_volume):
        self.master_volume = master_volume

    def set_positions(self, origin, positions):
        if not pygame.mixer.get_init():
            return

        for i, pos in enumerate(sorted(positions, key=lambda p: distance(origin, p))):
            if i >= len(self.channels):
                break
            channel = self.channels[i]
            l_volume = get_sound_volume(get_distance(origin, pos, x_offset=-250), loud_radius=300)
            r_volume = get_sound_volume(get_distance(origin, pos, x_offset=250), loud_radius=300)
            if l_volume <= 0 >= r_volume:
                channel.stop()
            else:
                channel.set_volume(l_volume, r_volume)
                if not channel.get_busy():
                    channel.play(self.sound, loops=-1)

        for channel in self.channels[len(positions):]:
            channel.stop()

    def stop(self):
        for channel in self.channels:
            channel.fadeout(200)


class CrowdSound:
    def __init__(self, channel, filename='crowd.ogg', master_volume=1.):
        if not pygame.mixer.get_init():
            return
        self.channel = pygame.mixer.Channel(channel)
        self.master_volume = master_volume
        self.stopped = True

        try:
            self.sound = pygame.mixer.Sound(getPath(sound, filename))
        except Exception:
            self.sound = None
            log.exception('Error loading sound file')

    def set_master_volume(self, master_volume):
        self.master_volume = master_volume

    def stop(self, fade_time):
        self.channel.fadeout(round(fade_time * 1000))
        self.stopped = True

    def set_volume(self, volume):
        if not pygame.mixer.get_init():
            return
        self.channel.set_volume(self.master_volume * volume)
        if self.stopped or not self.channel.get_busy():
            self.channel.play(self.sound, loops=-1)
            self.stopped = False


class SoundPlayer(object):
    def __init__(self):
        self.sounds = {}
        self.looping_sounds = {}
        self.sfx_volume = 1
        crowd_channel = 1
        self.crowd_sound = CrowdSound(channel=crowd_channel)
        self._reservedChannels = crowd_channel + 1
        if pygame.mixer.get_init():
            pygame.mixer.set_num_channels(32)

    def addSound(self, filename, action, channel=None):
        if not pygame.mixer.get_init():
            return

        if channel is not None and channel >= self._reservedChannels:
            self._reservedChannels = channel + 1
            pygame.mixer.set_reserved(self._reservedChannels)

        self.sounds[action] = SoundAction(filename, channel)

        # In case a sound is added after the volume has been set:
        self.sounds[action].set_master_volume(self.sfx_volume)

    def add_looping_sound(self, filename, name, channels, positional=True):
        self._reservedChannels = max(self._reservedChannels, max(channels) + 1)
        pygame.mixer.set_reserved(self._reservedChannels)
        self.looping_sounds[name] = LoopingSound(filename, channels, self.sfx_volume)

    def set_looping_sound_positions(self, origin, looping_sound_positions):
        for sound_name in self.looping_sounds:
            looping_sound_positions.setdefault(sound_name, [])
        for sound_name, positions in looping_sound_positions.items():
            self.looping_sounds[sound_name].set_positions(origin, positions)

    def stop_looping_sounds(self):
        for looping_sound in self.looping_sounds.values():
            looping_sound.stop()

    def play(self, action, origin=None, pos=None):
        if not pygame.mixer.get_init():
            return

        self.sounds[action].play(origin, pos)

    def playFromServerCommand(self, filename):
        action = 'custom:' + filename
        if action not in self.sounds:
            self.addSound(filename, action, channel=0)
        self.play(action)

    def set_sfx_volume(self, val):
        self.sfx_volume = val
        for action in self.sounds.values():
            action.set_master_volume(val)
        for looping_sound in self.looping_sounds.values():
            looping_sound.set_master_volume(val)

    def set_crowd_master_volume(self, val):
        self.crowd_sound.set_master_volume(val)

    def set_crowd_current_volume(self, val):
        self.crowd_sound.set_volume(val)

    def stop_crowd_noise(self, fade_time=0.5):
        self.crowd_sound.stop(fade_time)
