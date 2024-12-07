import base64
import contextlib
import logging
import os
import sys
from configparser import ConfigParser
# noinspection PyUnresolvedReferences
from dataclasses import dataclass

import pygame

from trosnoth.const import MAP_TO_SCREEN_SCALE, HEAD_CUEBALL, DEFAULT_SERVER_PORT
from trosnoth.data import user_path, base_path
from trosnoth.gui.app import get_pygame_runner
from trosnoth.utils import unrepr
from trosnoth.utils.event import Event
import trosnoth.version

log = logging.getLogger(__name__)


DISPLAY_SECTION = 'display'
AUDIO_SECTION = 'audio'
IDENTITY_SECTION = 'identity'
SERVERS_SECTION = 'servers'
VERSION_SECTION = 'version'
ALL_SECTIONS = (DISPLAY_SECTION, AUDIO_SECTION, IDENTITY_SECTION, SERVERS_SECTION, VERSION_SECTION)


class PermissiveConfigParser(ConfigParser):
    '''
    Like ConfigParser, but getboolean, getint and getfloat return the
    default if the input is invalid.
    '''
    def getboolean(self, *args, **kwargs):
        try:
            return super().getboolean(*args, **kwargs)
        except ValueError:
            if 'fallback' in kwargs:
                return kwargs['fallback']
            raise

    def getint(self, *args, **kwargs):
        try:
            return super().getint(*args, **kwargs)
        except ValueError:
            if 'fallback' in kwargs:
                return kwargs['fallback']
            raise

    def getfloat(self, *args, **kwargs):
        try:
            return super().getfloat(*args, **kwargs)
        except ValueError:
            if 'fallback' in kwargs:
                return kwargs['fallback']
            raise


def load_old_settings_file(filename):
    '''
    Loads settings files from versions of Trosnoth prior to 1.15. These
    files were saved in a repr-like format.
    '''
    try:
        f = open(user_path / filename)
    except FileNotFoundError:
        return {}

    with f:
        data = unrepr.unrepr(f.read())
    if not isinstance(data, dict):
        return {}
    return data


class ClientSettings:
    instance = None

    def __init__(self, path=None, defaults_path=None):
        if path is None:
            path = user_path / 'client.ini'
        self.path = path
        self.defaults_path = defaults_path or (base_path.parent / 'clientdefaults.ini')
        self.config = PermissiveConfigParser(interpolation=None)
        self.initialise_config()

        self.display = DisplaySettings(self.config[DISPLAY_SECTION])
        self.audio = AudioSettings(self.config[AUDIO_SECTION])
        self.identity = IdentitySettings(self.config[IDENTITY_SECTION])
        self.connection = ConnectionSettings(self.config[SERVERS_SECTION])

        self.migrate()

    def save(self):
        self.display.presave()
        self.audio.presave()
        self.identity.presave()
        self.connection.presave()
        user_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w') as f:
            self.config.write(f)
        self.apply()

    def apply(self):
        self.display.maybe_notify()
        self.audio.maybe_notify()
        self.identity.maybe_notify()
        self.connection.maybe_notify()

    @classmethod
    def get(cls):
        if cls.instance is None or not isinstance(cls.instance, cls):
            cls.instance = cls()
        return cls.instance

    def initialise_config(self):
        for section_name in ALL_SECTIONS:
            self.config.add_section(section_name)
        self.config.read([self.defaults_path, self.path])

    def migrate(self):
        changed = False
        last_version = self.config[VERSION_SECTION].get('saved_by', '').split('.')
        if last_version < ['1', '15']:
            changed = self.migrate_from_repr_files() or changed

        self.config[VERSION_SECTION]['saved_by'] = trosnoth.version.version
        if changed:
            self.save()

    def migrate_from_repr_files(self):
        display_settings = load_old_settings_file('display')
        self.display.size = display_settings.get('size', (0, 0))
        self.display.full_screen_size = display_settings.get('fsSize', (0, 0))
        self.display.full_screen = display_settings.get('fullScreen', False)
        self.display.detail_level = display_settings.get('detailLevel', 'default')
        self.display.show_timings = display_settings.get('showTimings', False)
        self.display.show_range = display_settings.get('showRange', True)

        audio_settings = load_old_settings_file('sound')
        self.audio.sound_enabled = audio_settings.get('playSound', False)
        self.audio.sound_volume = audio_settings.get('musicVolume', 100)
        self.audio.music_enabled = audio_settings.get('playMusic', True)
        self.audio.music_volume = audio_settings.get('musicVolume', 100)

        identity_settings = load_old_settings_file('identity')
        self.identity.nick = identity_settings.get('nick', '')
        self.identity.head = identity_settings.get('head', HEAD_CUEBALL)
        self.identity.first_time = identity_settings.get('firstTime', True)
        self.identity.usernames = identity_settings.get('usernames', {})

        connection_settings = load_old_settings_file('connection')
        if connection_settings == {}:
            self.connection.servers = ['play.trosnoth.org']
        else:
            # Default auth server port has moved, so migrate default port
            # servers to the new default port automatically.
            self.connection.servers = [
                record[0] if record[1] in (6787, DEFAULT_SERVER_PORT) else f'{record[0]}:{record[1]}'
                for record in connection_settings.get('servers', [])
            ]

        return True


class SettingsBase:
    def __init__(self, data):
        self.data = data

    def presave(self):
        '''
        Called before changes are saved to disk. Should be used to
        update self.data if needed.
        '''
        pass

    def maybe_notify(self):
        '''
        Called after changes have been saved. May be used to notify
        event listeners of changes.
        '''
        pass


class DisplaySettings(SettingsBase):
    DETAIL_LEVELS = ['lowest', 'shrunk', 'low', 'default', 'full']

    def __init__(self, data, *args, **kwargs):
        self.on_detail_level_changed = Event([])
        self.on_change = Event([])

        # noinspection PyArgumentList
        super().__init__(data, *args, **kwargs)

        self.size = self.parse_size_string(data.get('size'))
        self.full_screen_size = self.parse_size_string(data.get('full_screen_size'))
        self.full_screen = data.getboolean('full_screen', True)
        self.upscale = data.getboolean('upscale', False)
        self.grab_mouse = data.getboolean('grab_mouse', False)
        self.detail_level = data.get('detail_level', 'default')
        self.sanitise_detail_level()
        self.show_timings = data.getboolean('show_timings', False)
        self.show_range = data.getboolean('show_range', True)
        self.disable_shop_buttons = data.getboolean('disable_shop_buttons', False)
        self.show_experimental = data.getboolean('show_experimental', False)

        self.old_detail_level = self.detail_level
        self.old_data = self.pack_data_for_comparison()

        self.alpha_overlays = True
        self.parallax_backgrounds = True
        self.max_viewport_width = 0
        self.max_viewport_height = 0
        self.antialiased_shots = True
        self.update_detail_flags()

        self._force_windowed = False

    @contextlib.contextmanager
    def keep_windowed(self):
        '''
        For the duration of the with statement, get_size() will return
        the windowed size, even if full screen is selected. If the
        Pygame runner is showing, this will notify it to become windowed
        at the start and end of the with statement.
        '''
        pygame_runner = get_pygame_runner()
        already_forced = self._force_windowed
        self._force_windowed = True
        try:
            if pygame_runner.is_showing() and pygame_runner.is_full_screen():
                pygame_runner.resize_window(*self.get_video_parameters())
            yield
        finally:
            self._force_windowed = already_forced
            if pygame_runner.is_showing():
                pygame_runner.resize_window(*self.get_video_parameters())

    def parse_size_string(self, size_string):
        if size_string and 'x' in size_string:
            try:
                return tuple(int(bit) for bit in size_string.split('x', 1))
            except ValueError:
                return (0, 0)

    def sanitise_detail_level(self):
        if self.detail_level not in self.DETAIL_LEVELS:
            self.detail_level = 'default'

    def pack_data_for_comparison(self):
        return (
            self.full_screen, self.detail_level, self.show_timings, self.show_range, self.size,
            self.full_screen_size, self.disable_shop_buttons, self.grab_mouse, self.upscale,
            self.show_experimental,
        )

    def presave(self):
        self.data['size'] = 'x'.join(str(i) for i in self.size)
        self.data['full_screen_size'] = 'x'.join(str(i) for i in self.full_screen_size)
        self.data['full_screen'] = str(self.full_screen)
        self.data['upscale'] = str(self.upscale)
        self.data['grab_mouse'] = str(self.grab_mouse)
        self.sanitise_detail_level()
        self.data['detail_level'] = self.detail_level
        self.data['show_timings'] = str(self.show_timings)
        self.data['disable_shop_buttons'] = str(self.disable_shop_buttons)
        self.data['show_experimental'] = str(self.show_experimental)
        self.data['show_range'] = str(self.show_range)

    def get_video_parameters(self):
        size = self.size
        grab_mouse = self.grab_mouse and not self._force_windowed
        full_screen = self.full_screen and not self._force_windowed
        if full_screen:
            allowed_modes = self.get_available_resolutions()
            if self.full_screen_size not in allowed_modes:
                size = allowed_modes[0]
            else:
                size = self.full_screen_size
        else:
            size = self.size
            if size == (0, 0):
                size = (1000, 750)

        if self.upscale:
            return (self.max_viewport_width, self.max_viewport_height), False, True, grab_mouse

        return size, full_screen, False, grab_mouse

    def get_available_resolutions(self):
        pygame.display.init()
        return pygame.display.list_modes()

    def maybe_notify(self):
        if self.detail_level != self.old_detail_level:
            self.old_detail_level = self.detail_level
            self.update_detail_flags()
            self.on_detail_level_changed()

        new_data = self.pack_data_for_comparison()
        if new_data != self.old_data:
            self.old_data = new_data
            self.on_change()

    def update_detail_flags(self):
        self.alpha_overlays = True
        self.parallax_backgrounds = True
        self.max_viewport_width = int(1536 * MAP_TO_SCREEN_SCALE + 0.5)
        self.max_viewport_height = int(960 * MAP_TO_SCREEN_SCALE + 0.5)
        self.antialiased_shots = True
        if self.detail_level == 'full':
            return

        if self.detail_level == 'default':
            return

        self.parallax_backgrounds = False
        self.antialiased_shots = False
        if self.detail_level == 'low':
            return

        self.max_viewport_width = 1024
        self.max_viewport_height = 768
        if self.detail_level == 'shrunk':
            return

        # If we're going this low, we really want performance
        self.max_viewport_width = 800
        self.max_viewport_height = 600
        self.alpha_overlays = False


class AudioSettings(SettingsBase):
    def __init__(self, data):
        self.on_change = Event([])
        super().__init__(data)

        self.sound_enabled = data.getboolean('sound', True)
        self.sound_volume = data.getfloat('sound_volume', 50)
        self.music_enabled = data.getboolean('music', True)
        self.music_volume = data.getfloat('music_volume', 50)
        self.crowd_enabled = data.getboolean('crowd', True)
        self.crowd_volume = data.getfloat('crowd_volume', 50)

    def presave(self):
        self.data['sound'] = str(self.sound_enabled)
        self.data['sound_volume'] = str(self.sound_volume)
        self.data['music'] = str(self.music_enabled)
        self.data['music_volume'] = str(self.music_volume)
        self.data['crowd'] = str(self.crowd_enabled)
        self.data['crowd_volume'] = str(self.crowd_volume)

    def maybe_notify(self):
        self.on_change()


class IdentitySettings(SettingsBase):
    def __init__(self, data):
        super().__init__(data)

        self.nick = data.get('nick', '')
        self.head = data.getint('head', HEAD_CUEBALL)
        self.first_time = data.getboolean('first_time', True)
        self.usernames = {}
        self.read_usernames_from_data()

    def read_usernames_from_data(self):
        i = 0
        while True:
            host_key = f'host.{i}'
            name_key = f'username.{i}'
            if not (host_key in self.data and name_key in self.data):
                break
            self.usernames[self.data[host_key]] = self.data[name_key]
            del self.data[host_key]
            del self.data[name_key]
            i += 1

    def presave(self):
        self.data['nick'] = self.nick
        self.data['head'] = str(self.head)
        self.data['first_time'] = str(self.first_time)
        for i, (server, name) in enumerate(self.usernames.items()):
            self.data[f'host.{i}'] = server
            self.data[f'username.{i}'] = name

    def set_info(self, nick, head):
        self.nick = nick
        self.head = head

    def set_nick(self, nick):
        self.nick = nick


@dataclass
class ServerCredentials:
    username: str
    secret: bytes
    key_digest: str


class ConnectionSettings(SettingsBase):
    def __init__(self, data):
        super().__init__(data)
        self.servers = []
        self.server_credentials = {}
        self.server_key_digests = {}
        self.read_servers_from_data()

    def read_servers_from_data(self):
        i = 0
        while True:
            key = f'server.{i}'
            if key not in self.data:
                break
            server_string = self.data[key]
            self.servers.append(server_string)
            del self.data[key]

            username_key = f'username.{i}'
            secret_key = f'secret.{i}'
            pubkey_key = f'key_digest.{i}'
            if username_key in self.data and secret_key in self.data and pubkey_key in self.data:
                credential = ServerCredentials(
                    self.data[username_key],
                    base64.b85decode(self.data[secret_key]),
                    self.data[pubkey_key],
                )
                self.server_credentials[server_string] = credential
                del self.data[username_key]
                del self.data[secret_key]

            i += 1

    def presave(self):
        for i, server in enumerate(self.servers):
            self.data[f'server.{i}'] = server
            try:
                credential = self.server_credentials[server]
            except KeyError:
                pass
            else:
                self.data[f'username.{i}'] = credential.username
                self.data[f'secret.{i}'] = base64.b85encode(credential.secret).decode('ascii')
                self.data[f'key_digest.{i}'] = credential.key_digest

    def get_servers(self):
        for server in self.servers:
            if ':' in server:
                host, port = server.rsplit(':', 1)
                try:
                    port = int(port)
                except ValueError:
                    continue
                return host, port
            yield server, DEFAULT_SERVER_PORT


def getPolicySettings():
    if getattr(sys, 'frozen', False):
        start_path = sys.executable
    else:
        import trosnoth
        start_path = trosnoth.__file__
    path = os.path.join(os.path.dirname(start_path), 'policy.ini')
    config = ConfigParser(interpolation=None)
    config.add_section('privacy')
    config.read(path)
    return config
