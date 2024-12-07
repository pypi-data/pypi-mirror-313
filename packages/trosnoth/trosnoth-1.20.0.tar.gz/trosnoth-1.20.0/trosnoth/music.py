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
# 02110-1301, USA.

import logging
import random
from contextlib import contextmanager
from typing import ContextManager

from trosnoth.settings import ClientSettings

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

import pygame

from trosnoth import data
from trosnoth.gui.app import get_pygame_runner

log = logging.getLogger(__name__)


# MUSIC_TRACK_COMPLETE must not collide with any pygame events.
MUSIC_TRACK_COMPLETE = 234


def get_music_tracks():
    result = []
    bundled_music_path = data.base_path / 'music'
    result.extend(
        f for f in bundled_music_path.iterdir() if f.is_file() and f.name.endswith('.ogg'))

    user_music_path = data.user_path / 'music'
    if user_music_path.is_dir():
        result.extend(f for f in user_music_path.iterdir() if f.is_file() and (
            f.name.endswith('.ogg') or f.name.endswith('mp3')))

    return result


class MusicPlayerAPI(Protocol):
    '''
    Defines the methods and attributes of the music player which should
    be used outside of the class itself.
    '''

    def run(self) -> ContextManager[None]:
        '''
        :return: A context manager which will cause the music player to
            be running while inside the with statement. When running,
            the music player will play music if the user settings have
            music enabled.
        '''
        raise NotImplementedError


class PygameMusicPlayer:
    instance = None

    def __init__(self):
        self.initialised = False
        self.enabled = True
        self.volume = 1
        self.running = False
        self.previous_track = None

    def apply_saved_settings(self):
        audio_settings = ClientSettings.get().audio
        self.apply_specific_settings(
            audio_settings.music_enabled, audio_settings.music_volume / 100)

    def apply_specific_settings(self, enabled: bool, volume: float) -> None:
        self.enabled = enabled
        self.volume = max(0, min(1, volume))
        if self.running:
            self.refresh()

    @contextmanager
    def run(self):
        if self.running:
            # Already running, so do nothing
            yield
            return

        audio_settings = ClientSettings.get().audio
        self.apply_saved_settings()
        pygame_runner = get_pygame_runner()
        with pygame_runner.on_pygame_event.subscribe(self.process_event), \
                audio_settings.on_change.subscribe(self.apply_saved_settings):
            self.running = True
            try:
                self.refresh()
                yield
            finally:
                self.running = False
                self.stop()

    def process_event(self, event):
        if event.type == MUSIC_TRACK_COMPLETE and self.enabled and self.running:
            self.ensure_started()

    def refresh(self):
        if self.enabled:
            if self.ensure_mixer_initialised():
                pygame.mixer.music.set_volume(self.volume)
                self.ensure_started()
        else:
            self.stop()

    def ensure_started(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            return

        if self.select_next_track():
            pygame.mixer.music.play()

    def ensure_mixer_initialised(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            log.error(f'Could not initialise mixer: {e}')
            return False
        pygame.mixer.music.set_endevent(MUSIC_TRACK_COMPLETE)
        return True

    def select_next_track(self):
        tracks = get_music_tracks()
        if not tracks:
            return False

        random.shuffle(tracks)
        selected_track = tracks[0]
        if selected_track == self.previous_track and len(tracks) > 1:
            selected_track = tracks[1]

        pygame.mixer.music.load(str(selected_track))
        self.previous_track = selected_track

        return True

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.set_endevent()
            pygame.mixer.music.stop()


def get_music_player() -> MusicPlayerAPI:
    '''
    :return: the global pygame runner which can be used to query or
        control the open Pygame window.
    '''
    if PygameMusicPlayer.instance is None:
        PygameMusicPlayer.instance = PygameMusicPlayer()
    return PygameMusicPlayer.instance
