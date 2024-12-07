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

import asyncio
import contextlib
import enum
import ipaddress
import logging
import time
from dataclasses import dataclass
from typing import Tuple, Optional, Callable, Dict

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QLabel, QVBoxLayout
from twisted.internet import reactor
from twisted.internet.error import ConnectError
from twisted.protocols import amp

from trosnoth import version
from trosnoth.const import DEFAULT_GAME_PORT
from trosnoth.game import RemoteGame
from trosnoth.gui.app import UserClosedPygameWindow
from trosnoth.levels.base import LevelOptions
from trosnoth.levels.registry import scenario_options
from trosnoth.network import authcommands
from trosnoth.network.client import ConnectionFailed
from trosnoth.network.lobby import (
    get_multicast_servers, get_server_info_and_games, UDPMulticastAsyncGameGetter,
    connect_to_game_server, ask_for_auth_game_details, AuthClientProtocol,
)
from trosnoth.network.server import ListenServer
from trosnoth.run.common import initialise_trosnoth_app
from trosnoth.settings import ClientSettings, ServerCredentials
from trosnoth.trosnothgui.ingame.gameInterface import GameInterface
from trosnoth.utils.aio import (
    as_future, all_completed, create_safe_task, single_entry_task,
)
from trosnoth.utils.event import Event
from trosnoth.utils.utils import (
    UIScreenRunner, parse_server_string, run_in_pygame, format_number,
    clean_garbage,
)
from trosnoth.welcome.messageviewer import WelcomeScreenMessageViewer
from trosnoth.welcome.nonqt import (
    async_callback, run_callback_in_async_loop, STOP_IMAGE_FILE,
    QUESTION_IMAGE_FILE
)
from trosnoth.welcome.settings import SettingsScreen

log = logging.getLogger(__name__)


class Priority(enum.IntEnum):
    TRUSTED_LAN_GAME = 0
    LAN_SERVER = 1
    ADHOC_LAN_GAME = 2
    TRUSTED_SERVER_GAME = 3
    HOST_LAN_GAME = 5
    IP_CONNECT_GAME = 6
    TRUSTED_SERVER_ERROR = 10


@dataclass
class AuthServerGame:
    server_string: str
    ip_address: ipaddress.ip_address
    port: int
    server_name: str
    is_trusted: bool
    server_key_digest: str

    game_id: int
    game_name: str

    auth_settings: Optional[Dict] = None

    @property
    def verification_error(self):
        if not self.credentials:
            return False
        return self.credentials.key_digest != self.server_key_digest

    @property
    def credentials(self):
        if not self.is_trusted:
            return None
        return ClientSettings.get().connection.server_credentials.get(self.server_string)

    async def launch(self, ui_routines, spectate):
        async with AuthClientProtocol.connect(self.ip_address, self.port) as conn:
            if conn.server_key_digest != self.server_key_digest:
                await ui_routines.message_viewer.run(
                    'Error connecting: server identity has changed', 'ok', image=STOP_IMAGE_FILE)
                return

            if self.verification_error:
                proceed = await ui_routines.message_viewer.run(
                    'This server’s public key has changed since last time you connected to it.\n'
                    '\nThe new key fingerprint is '
                    + ':'.join([conn.server_key_digest[i:i + 4] for i in range(0, 20, 4)])
                    + '\n\nDo you wish to proceed?', 'yes', image=STOP_IMAGE_FILE,
                )
                if not proceed:
                    return

            port, auth_tag = await self.get_port_and_auth_tag(conn, ui_routines, spectate)

        if port:
            await connect_to_remote_trosnoth_game(
                ui_routines, spectate, self.ip_address, port, auth_tag)

    async def get_port_and_auth_tag(self, conn, ui_routines, spectate):
        try:
            join_details = await self.request_auth_game_details(conn, ui_routines, spectate)
        except authcommands.NotAuthenticated:
            if self.auth_settings is None:
                self.auth_settings = await as_future(conn.callRemote(authcommands.GetAuthSettings))
            success = await ui_routines.login_user(conn, self)
            if not success:
                return 0, 0

            join_details = await self.request_auth_game_details(conn, ui_routines, spectate)

        port = join_details['port']
        auth_tag = join_details.get('auth_tag') or 0
        nick = join_details.get('nick', None)
        if nick:
            client_settings = ClientSettings.get()
            client_settings.identity.set_nick(nick)
            client_settings.save()

        return (port, auth_tag)

    async def request_auth_game_details(self, conn, ui_routines, spectate):
        # If the server key has changed, do not share the secret token with them
        credentials = None if self.verification_error else self.credentials

        try:
            result = await ask_for_auth_game_details(conn, self.game_id, spectate, credentials)
        except (ConnectionFailed, ConnectError, IOError):
            await ui_routines.message_viewer.run(
                'Could not connect to server.', 'ok', image=STOP_IMAGE_FILE)
        except authcommands.GameDoesNotExist:
            await ui_routines.message_viewer.run(
                'That game no longer exists!', 'ok', image=STOP_IMAGE_FILE)
        else:
            if credentials and result.get('new_token'):
                self.remember_token(credentials.username, result['new_token'])
            return result
        return None

    def remember_token(self, username, token):
        if not self.is_trusted:
            return
        settings = ClientSettings.get()
        settings.connection.server_credentials[self.server_string] = ServerCredentials(
            username=username,
            secret=token,
            key_digest=self.server_key_digest,
        )
        settings.save()


class UIRoutinesAPI(Protocol):
    '''
    This class exists to help with editor type suggestions. It defines
    the function signatures of the various attributes of UIRoutines.
    '''

    message_viewer: WelcomeScreenMessageViewer

    async def login_user(self, auth_connection, auth_server_game: AuthServerGame):
        raise NotImplementedError

    async def host_game(self):
        raise NotImplementedError


@dataclass
class UIRoutines:
    message_viewer: WelcomeScreenMessageViewer
    login_user: Callable
    host_game: Callable
    connect_by_ip: Callable


class GameListItem:
    priority: Priority
    can_play: bool
    can_spectate: bool

    def build_widget(self):
        raise NotImplementedError

    async def play(self, ui_routines: UIRoutinesAPI):
        raise NotImplementedError

    async def spectate(self, ui_routines: UIRoutinesAPI):
        raise NotImplementedError


@dataclass
class GameItem(GameListItem):
    server: str
    game_name: str
    game_format: str

    connection_kind: str
    banner_colour: str
    priority: Priority

    connect_address: Optional[Tuple[ipaddress.ip_address, int]] = None
    auth_game: Optional[AuthServerGame] = None

    server_name: str = ''
    warning: Optional[str] = None

    can_play = True
    can_spectate = True

    def build_widget(self):
        result = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.build_top_banner())
        layout.addWidget(self.build_game_name())
        layout.addWidget(self.build_bottom_banner())
        layout.setSpacing(0)
        result.setLayout(layout)
        result.setStyleSheet('background-color: transparent;')
        return result

    def build_game_name(self):
        result = QLabel(self.game_name)
        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet(f'font-size: 20px; margin: 5px 0;')
        return result

    def build_top_banner(self):
        caption = f'{self.connection_kind}   ·   {self.server}'
        if self.server_name:
            caption += f'   ·   ‘{self.server_name}’'

        result = QLabel(caption)
        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet(f'color: {self.banner_colour}; font-size: 13px;')
        return result

    def build_bottom_banner(self):
        if self.warning:
            result = QLabel(self.warning)
            result.setStyleSheet(f'color: darkred; font-size: 13px;')
        else:
            result = QLabel(f'Format: {self.game_format}')
            result.setStyleSheet(f'color: #444; font-size: 13px;')
        result.setAlignment(Qt.AlignCenter)
        return result

    async def play(self, ui_routines: UIRoutinesAPI):
        await ui_routines.message_viewer.run_task(
            'Connecting to game…',
            self.launch(ui_routines, spectate=False))

    async def spectate(self, ui_routines: UIRoutinesAPI):
        await ui_routines.message_viewer.run_task(
            'Connecting to game…',
            self.launch(ui_routines, spectate=True))

    async def launch(self, ui_routines: UIRoutinesAPI, spectate):
        try:
            if self.connect_address:
                host, port = self.connect_address
                await connect_to_remote_trosnoth_game(ui_routines, spectate, host, port, auth_tag=0)
            elif not self.auth_game:
                raise RuntimeError('No connection or server address given!')
            else:
                await self.auth_game.launch(ui_routines, spectate)
        except LostGameConnection:
            await ui_routines.message_viewer.run(
                'The connection to the game was lost.', 'ok', image=STOP_IMAGE_FILE)

    @classmethod
    def create_auth(cls, auth_server_game: AuthServerGame):
        banner_colour = 'green' if auth_server_game.is_trusted else '#7f4600'
        warning = None
        if auth_server_game.verification_error:
            banner_colour = 'darkred'
            warning = 'Server’s public key has changed!'

        return cls(
            server=auth_server_game.server_string,
            game_name=auth_server_game.game_name,
            server_name=auth_server_game.server_name,
            game_format='variety games',
            connection_kind='Trusted server' if auth_server_game.is_trusted else 'LAN server',
            banner_colour=banner_colour,
            priority=(
                Priority.LAN_SERVER if not auth_server_game.is_trusted else
                Priority.TRUSTED_LAN_GAME if auth_server_game.ip_address.is_private else
                Priority.TRUSTED_SERVER_GAME),
            auth_game=auth_server_game,
            warning=warning,
        )

    @classmethod
    def create_trusted(cls, server, server_info, game_info, ip_address, port):
        return cls.create_auth(AuthServerGame(
            server_string=server,
            server_name=server_info.name,
            server_key_digest=server_info.key_digest,
            ip_address=ip_address,
            port=port,
            is_trusted=True,
            game_id=game_info.id,
            game_name=game_info.name,
        ))

    @classmethod
    def create_lan_server(cls, server_address, server_info, game_info):
        host, port = server_address
        return cls.create_auth(AuthServerGame(
            server_string=str(host),
            server_name=server_info.name,
            server_key_digest=server_info.key_digest,
            ip_address=host,
            port=port,
            is_trusted=False,
            game_id=game_info.id,
            game_name=game_info.name,
        ))

    @classmethod
    def create_lan_adhoc(cls, ip_address, game_name, game_format, connect_address):
        return cls(
            str(ip_address), game_name, game_format=game_format,
            connection_kind='Ad-hoc LAN game', banner_colour='#7f4600',
            priority=Priority.ADHOC_LAN_GAME,
            connect_address=connect_address,
        )


async def connect_to_remote_trosnoth_game(
        ui_routines: UIRoutinesAPI, spectate, host, port, auth_tag):
    try:
        net_client, settings = await connect_to_game_server(host, port)
    except (ConnectionFailed, ConnectError, IOError):
        await ui_routines.message_viewer.run(
            'Could not connect to game.', 'ok', image=STOP_IMAGE_FILE)
        return

    game = None
    try:
        game = RemoteGame(smooth_remote_ticks=True)
        net_client.connectNode(game)
        game.connected(settings)

        await show_game_window(game, auth_tag, spectate)
    finally:
        if game:
            game.stop()
        net_client.disconnect()
        net_client.disconnectNode()


async def host_lan_game(level, game_name, **kwargs):
    with ListenServer.run(level, game_name, **kwargs) as game:
        await show_game_window(game)


class LostGameConnection(Exception):
    pass


@run_in_pygame
async def show_game_window(game, auth_tag=0, spectate=False):
    lost_connection = False
    with initialise_trosnoth_app() as app:

        def connection_was_lost():
            nonlocal lost_connection
            lost_connection = True
            app.stop()

        game_interface = GameInterface(
            app, game, authTag=auth_tag,
            spectate=spectate,
            on_clean_exit=app.stop,
            on_lost_connection=connection_was_lost,
        )
        try:
            app.interface.elements.append(game_interface)
            await app.runner.run()
        finally:
            game_interface.stop()
            clean_garbage()

    if lost_connection:
        raise LostGameConnection


@dataclass
class ErrorItem(GameListItem):
    server: str
    error_text: str
    connection_kind: str
    priority = Priority.TRUSTED_SERVER_ERROR

    can_play = False
    can_spectate = False

    @classmethod
    def create_trusted(cls, server, error_text):
        return cls(server, error_text, connection_kind='Trusted server')

    @classmethod
    def create_lan_adhoc(cls, ip_address, error_text):
        return cls(str(ip_address), error_text, connection_kind='Ad-hoc LAN game')

    def build_widget(self):
        result = QLabel(f'Trusted server   ·   {self.server}   ·   {self.error_text}')
        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet('color: #555; font-size: 13px; margin: 5px;')
        return result

    async def play(self, ui_routines: UIRoutinesAPI):
        raise RuntimeError('Invalid call')

    async def spectate(self, ui_routines: UIRoutinesAPI):
        raise RuntimeError('Invalid call')


class HostGameItem(GameListItem):
    priority = Priority.HOST_LAN_GAME

    can_play = True
    can_spectate = False

    def build_widget(self):
        result = QLabel('Host a LAN game')
        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet(f'color: green; font-size: 20px; margin: 5px 0;')
        return result

    async def spectate(self, ui_routines: UIRoutinesAPI):
        raise RuntimeError('Invalid call')

    async def play(self, ui_routines: UIRoutinesAPI):
        await ui_routines.host_game()


class IPConnectItem(GameListItem):
    priority = Priority.IP_CONNECT_GAME

    can_play = True
    can_spectate = False

    def build_widget(self):
        result = QLabel('Connect to LAN game by IP address')
        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet(f'color: green; font-size: 14px; margin: 5px 0;')
        return result

    async def spectate(self, ui_routines: UIRoutinesAPI):
        raise RuntimeError('Invalid call')

    async def play(self, ui_routines: UIRoutinesAPI):
        await ui_routines.connect_by_ip()


class GamesList:
    def __init__(self):
        self.on_game_added = Event(['game', 'index'])
        self.on_list_cleared = Event([])
        self.on_list_complete = Event([])

        self.games_by_priority = {p: [] for p in Priority}

    def clear_games(self):
        self.games_by_priority = {p: [] for p in Priority}
        self.on_list_cleared()

    def add_game(self, game: GameListItem):
        index = 0
        for p in Priority:
            index += len(self.games_by_priority[p])
            if p == game.priority:
                break
        self.games_by_priority[game.priority].append(game)
        self.on_game_added(game, index)

    def games_list_complete(self):
        self.on_list_complete()


class PlayScreen:
    def __init__(self, parent):
        self.async_manager = parent.async_manager   # Allows async callbacks
        self.window = window = parent.window
        self.login_page = LoginPage(parent)
        self.host_page = HostGamePage(parent)
        self.ip_connect_page = IPConnectPage(self, parent)
        self.ui_routines = UIRoutines(
            message_viewer=parent.message_viewer,
            login_user=self.login_page.run,
            host_game=self.host_page.run,
            connect_by_ip=self.ip_connect_page.run,
        )
        self.loading_message_task = None
        self.games = GamesList()
        self.games_by_widget = {}

        self.parent = parent
        self.game_refresher = None
        self.screen_runner = UIScreenRunner()
        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.play_page = window.findChild(QWidget, 'play_page')
        self.games_table = window.findChild(QWidget, 'games_table')
        self.play_button = window.findChild(QWidget, 'play_play_button')
        self.spectate_button = window.findChild(QWidget, 'spectate_game_button')

        self.games_table.currentCellChanged.connect(
            run_callback_in_async_loop(self.selection_changed))
        self.games_table.cellDoubleClicked.connect(
            run_callback_in_async_loop(self.server_double_clicked))
        self.play_button.clicked.connect(
            run_callback_in_async_loop(self.play_clicked))
        self.spectate_button.clicked.connect(
            run_callback_in_async_loop(self.spectate_clicked))
        window.findChild(QWidget, 'play_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'refresh_games_button').clicked.connect(
            run_callback_in_async_loop(self.refresh_clicked))
        window.findChild(QWidget, 'server_settings_button').clicked.connect(
            run_callback_in_async_loop(self.server_settings_clicked))

        self.update_button_states()

    async def run(self):
        if self.screen_runner.running:
            raise RuntimeError('Already running')

        previous_page_widget = self.main_stack.currentWidget()
        try:
            self.main_stack.setCurrentWidget(self.play_page)
            with self.games.on_list_cleared.subscribe(self.games_list_cleared), \
                    self.games.on_game_added.subscribe(self.game_added), \
                    self.games.on_list_complete.subscribe(self.games_list_complete), \
                    GameRefresher(self.games).run() as refresher:
                self.game_refresher = refresher
                return await self.screen_runner.run()
        finally:
            self.game_refresher = None
            self.main_stack.setCurrentWidget(previous_page_widget)
            if self.loading_message_task and not self.loading_message_task.done():
                self.loading_message_task.cancel()

    def get_current_game_item(self) -> Optional[GameListItem]:
        selected_widget = self.games_table.cellWidget(
            self.games_table.currentRow(), self.games_table.currentColumn())
        return self.games_by_widget.get(selected_widget)

    def update_button_states(self):
        game_item = self.get_current_game_item()
        if game_item is None:
            self.play_button.setEnabled(False)
            self.spectate_button.setEnabled(False)
        else:
            self.play_button.setEnabled(game_item.can_play)
            self.spectate_button.setEnabled(game_item.can_spectate)

    def selection_changed(self, *args):
        self.update_button_states()

    @async_callback
    async def server_double_clicked(self, row_index, column_index):
        game_item = self.get_current_game_item()
        if not game_item:
            return
        if game_item.can_play:
            await self.join_game(game_item)
        elif game_item.can_spectate:
            await self.spectate_game(game_item)

    @async_callback
    async def play_clicked(self):
        await self.join_game(self.get_current_game_item())

    async def join_game(self, game_item):
        try:
            await game_item.play(self.ui_routines)
        except UserClosedPygameWindow:
            pass
        except Exception:
            log.exception('Error connecting to game')
            await self.ui_routines.message_viewer.run(
                'There was an error trying to connect to the game.', 'ok', image=STOP_IMAGE_FILE)

        if self.game_refresher:
            self.game_refresher.refresh()

    @async_callback
    async def spectate_clicked(self):
        await self.spectate_game(self.get_current_game_item())

    async def spectate_game(self, game_item):
        try:
            await game_item.spectate(self.ui_routines)
        except UserClosedPygameWindow:
            pass
        except Exception:
            log.exception('Error connecting to game as spectator')
            await self.ui_routines.message_viewer.run(
                'There was an error trying to connect to the game.', 'ok', image=STOP_IMAGE_FILE)

        if self.game_refresher:
            self.game_refresher.refresh()

    def back_clicked(self):
        self.screen_runner.done(None)

    def refresh_clicked(self):
        if self.game_refresher:
            self.game_refresher.refresh()

    @async_callback
    async def server_settings_clicked(self):
        # Keep the SettingsScreen as a local variable to prevent it
        # being garbage collected during screen.run().
        screen = SettingsScreen(start_tab='servers_tab')
        await screen.run()

    def games_list_cleared(self):
        self.loading_message_task = create_safe_task(self.cycle_loading_message())

    @single_entry_task
    async def cycle_loading_message(self):
        loading_item = QTableWidgetItem('')
        loading_item.setTextAlignment(Qt.AlignCenter)

        self.games_by_widget.clear()
        while self.games_table.rowCount() > 1:
            self.games_table.removeRow(0)
        self.games_table.removeCellWidget(0, 0)
        self.games_table.setItem(0, 0, loading_item)
        self.games_table.setCurrentCell(0, 0, QItemSelectionModel.ClearAndSelect)

        try:
            while True:
                for i in range(4):
                    loading_item.setText('Searching for games' + '.' * i)
                    await asyncio.sleep(.25)
        except asyncio.CancelledError:
            pass

        if self.games_table.rowCount() == 1:
            loading_item.setText('— No games found —')
        else:
            is_selected = loading_item.row() == self.games_table.currentRow()
            self.games_table.removeRow(self.games_table.rowCount() - 1)
            if is_selected:
                self.games_table.setCurrentCell(0, 0, QItemSelectionModel.ClearAndSelect)

    def game_added(self, game: GameListItem, index: int):
        self.games_table.insertRow(index)
        widget = game.build_widget()
        self.games_by_widget[widget] = game
        self.games_table.setCellWidget(index, 0, widget)
        self.games_table.resizeRowsToContents()

    def games_list_complete(self):
        if self.loading_message_task and not self.loading_message_task.done():
            self.loading_message_task.cancel()


class RateLimiter:
    '''
    Limits calls to ping() to a maximum of number calls per period
    seconds. Any additional calls will asynchronously wait until the
    period is over.

    If ping() is called while another call to ping() is waiting, there
    is no guarantee as to the order in which the two calls will return.
    '''

    def __init__(self, number, period):
        self.number = number
        self.period = period
        self.call_times = []

    async def ping(self):
        while True:
            now = time.monotonic()
            cutoff_time = now - self.period
            self.forget_calls_before(cutoff_time)

            if len(self.call_times) < self.number:
                # Not yet rate limited
                self.call_times.append(now)
                return

            # Rate limited. Wait until ready
            await asyncio.sleep(self.call_times[0] - cutoff_time)

    def forget_calls_before(self, cutoff_time):
        # Clear out any calls that are too long ago to worry about
        while self.call_times and self.call_times[0] < cutoff_time:
            self.call_times.pop(0)


class GameRefresher:
    def __init__(self, game_list: GamesList):
        self.game_list = game_list
        self.running_task = None
        self.limiter = RateLimiter(2, 5)
        self.resolved_trusted_servers = {}
        self.trusted_server_set = set()

    @contextlib.contextmanager
    def run(self):
        self.refresh()
        try:
            yield self
        finally:
            if self.running_task and not self.running_task.done():
                self.running_task.cancel()

    def refresh(self):
        self.running_task = create_safe_task(self.refresh_async())

    @single_entry_task
    async def refresh_async(self):
        self.game_list.clear_games()

        tasks = []
        try:
            tasks.append(create_safe_task(self.add_host_lan_game()))

            # Only allow 2 refreshes every 5 seconds
            await self.limiter.ping()

            # 1. Tasks that we can start immediately
            tasks.append(create_safe_task(self.find_adhoc_lan_games()))

            # 2. Resolve the IP address of any trusted servers
            servers = ClientSettings.get().connection.servers
            await self.update_trusted_server_map(servers)

            # 3. Tasks that need to wait for name resolution to complete
            for server in servers:
                tasks.append(create_safe_task(self.get_trusted_server_games(server)))

            tasks.append(create_safe_task(self.find_lan_servers()))

            await asyncio.gather(*tasks)
            self.game_list.add_game(IPConnectItem())
        finally:
            self.game_list.games_list_complete()
            for task in tasks:
                if not task.done():
                    task.cancel()

    async def add_host_lan_game(self):
        await asyncio.sleep(0.1)
        self.game_list.add_game(HostGameItem())

    async def update_trusted_server_map(self, servers):
        servers = list(servers)
        jobs = [self.resolve_server(server) for server in servers]
        addresses = await all_completed(jobs)
        self.resolved_trusted_servers.clear()
        for i, server in enumerate(servers):
            if addresses[i] is not None:
                self.resolved_trusted_servers[server] = addresses[i]
                self.trusted_server_set.add(addresses[i])

    async def resolve_server(self, server_string):
        try:
            host, port = parse_server_string(server_string)
        except ValueError:
            return None
        try:
            ip_address = ipaddress.ip_address(host)
        except ValueError:
            ip_address = ipaddress.ip_address(await as_future(reactor.resolve(host, timeout=2)))
        return ip_address, port

    async def get_trusted_server_games(self, server_string):
        try:
            ip_address, port = self.resolved_trusted_servers[server_string]
        except KeyError:
            return

        try:
            info = await get_server_info_and_games((str(ip_address), port))
        except (ConnectError, IOError, ConnectionError):
            self.game_list.add_game(
                ErrorItem.create_trusted(server_string, 'Could not connect to server.'))
            return
        except (amp.UnknownRemoteError, amp.RemoteAmpError):
            self.game_list.add_game(
                ErrorItem.create_trusted(server_string, 'An error occurred on the server.'))
            return

        if not version.is_compatible(info.version):
            self.game_list.add_game(
                ErrorItem.create_trusted(server_string, f'Incompatible version: {info.version}'))
            return

        for game in info.games:
            self.game_list.add_game(GameItem.create_trusted(
                server=server_string,
                server_info=info,
                game_info=game,
                ip_address=ip_address,
                port=port,
            ))

    async def find_adhoc_lan_games(self):
        async for game in UDPMulticastAsyncGameGetter().get_games():
            ver = game.details.get('version', 'Unknown')
            if isinstance(ver, bytes):
                try:
                    ver = ver.decode('ascii')
                except UnicodeError:
                    ver = 'Unknown'
            elif not isinstance(ver, str):
                ver = 'Unknown'
            if not version.is_compatible(ver):
                item = ErrorItem.create_lan_adhoc(game.ip, f'Incompatible version: {ver}')
            else:
                game_format = game.details.get('format', 'unknown')
                if not isinstance(game_format, str):
                    game_format = 'unknown'
                item = GameItem.create_lan_adhoc(
                    ip_address=game.ip,
                    game_name=game.name,
                    game_format=game_format,
                    connect_address=(game.ip, game.port),
                )
            self.game_list.add_game(item)

    async def find_lan_servers(self):
        async for server in get_multicast_servers():
            if server in self.trusted_server_set:
                # If we a trusted server is on the LAN, don't show it
                # twice.
                continue

            try:
                info = await get_server_info_and_games(server)
            except (
                    ConnectError, IOError, ConnectionError,
                    amp.UnknownRemoteError, amp.RemoteAmpError) as e:
                log.exception(f'Found LAN server {server}, but encountered error: {e}')
                return

            if not version.is_compatible(info.version):
                log.warning(f'LAN server {server} running incompatible version {info.version}')
                return

            for game in info.games:
                self.game_list.add_game(
                    GameItem.create_lan_server(
                        server_address=server,
                        server_info=info,
                        game_info=game,
                    ))


class LoginPage:
    def __init__(self, welcome_screen):
        self.async_manager = welcome_screen.async_manager   # Allows async callbacks
        self.window = window = welcome_screen.window
        self.message_viewer = welcome_screen.message_viewer
        self.auth_connection = None
        self.auth_game = None
        self.screen_runner = UIScreenRunner()
        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.login_page = window.findChild(QWidget, 'login_page')
        self.login_image = window.findChild(QWidget, 'login_image')
        self.error_label = window.findChild(QWidget, 'login_error_label')
        self.header_label = window.findChild(QWidget, 'login_header_label')
        self.server_display = window.findChild(QWidget, 'login_server_display')
        self.username_edit = window.findChild(QWidget, 'login_username_edit')
        self.password_edit = window.findChild(QWidget, 'login_password_edit')
        self.password2_edit = window.findChild(QWidget, 'login_password2_edit')
        self.remember_me = window.findChild(QWidget, 'remember_me_checkbox')

        self.username_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))
        self.password_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))
        self.password2_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))

        self.pixmap = QPixmap(str(QUESTION_IMAGE_FILE))
        self.login_image.setPixmap(self.pixmap)

        self.widgets_hide_unless_creating_account = [window.findChild(QWidget, name) for name in (
            'login_password2_label',
            'login_password2_edit',
        )]
        self.create_account_pane = window.findChild(QWidget, 'create_account_pane')
        self.remember_me_pane = window.findChild(QWidget, 'remember_me_pane')

        window.findChild(QWidget, 'create_account_button').clicked.connect(
            run_callback_in_async_loop(self.create_account_clicked))
        window.findChild(QWidget, 'login_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'login_ok_button').clicked.connect(
            run_callback_in_async_loop(self.ok_clicked))

        self.creating_account = False
        self.is_trusted_server = True
        self.can_create_account = True
        self.transient_message = ''

    async def run(self, auth_connection, auth_game: AuthServerGame):
        self.auth_connection = auth_connection
        self.auth_game = auth_game
        previous_page_widget = self.main_stack.currentWidget()
        try:
            self.reset_form()
            self.main_stack.setCurrentWidget(self.login_page)
            return await self.screen_runner.run()
        finally:
            self.main_stack.setCurrentWidget(previous_page_widget)

    def reset_form(self):
        self.transient_message = ''
        self.is_trusted_server = self.auth_game.is_trusted
        self.can_create_account = self.auth_game.auth_settings['account_creation']
        server_display_name = self.auth_game.server_string
        if self.auth_game.server_name:
            server_display_name += f'   ·   ‘{self.auth_game.server_name}’'
        self.server_display.setText(server_display_name)
        self.creating_account = False
        self.username_edit.setText('')
        self.password_edit.setText('')
        self.password2_edit.setText('')
        self.username_edit.setFocus()
        self.refresh_widget_states()

    def refresh_widget_states(self):
        if self.is_trusted_server:
            self.remember_me_pane.show()
        else:
            self.remember_me_pane.hide()

        if self.creating_account:
            self.header_label.setText('Enter details to create an account on this server.')
            self.create_account_pane.hide()
            for widget in self.widgets_hide_unless_creating_account:
                widget.show()
        else:
            self.header_label.setText('Please log in to this server.')
            for widget in self.widgets_hide_unless_creating_account:
                widget.hide()
            if self.can_create_account:
                self.create_account_pane.show()
            else:
                self.create_account_pane.hide()

        self.error_label.setText(self.transient_message)

    @async_callback
    async def ok_clicked(self):
        try:
            if self.creating_account:
                success = await self.message_viewer.run_task(
                    'Creating account…', self.create_account())
            else:
                success = await self.message_viewer.run_task('Logging in…', self.login())

            if success:
                self.screen_runner.done(True)
        except Exception as e:
            self.screen_runner.error(e)

    async def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        response = await as_future(self.auth_connection.callRemote(
            authcommands.PasswordAuthenticate,
            username=username,
            password=password,
        ))
        success = response['result']
        if success:
            if self.remember_me.isChecked():
                self.auth_game.remember_token(username, response['token'])
            return True
        else:
            self.transient_message = 'Invalid username / password'
            self.refresh_widget_states()
        return False

    async def create_account(self):
        password = self.password_edit.text()
        password2 = self.password2_edit.text()
        if password != password2:
            self.transient_message = 'Passwords do not match'
            self.refresh_widget_states()
            return False

        username = self.username_edit.text()
        response = await as_future(self.auth_connection.callRemote(
            authcommands.CreateUserWithPassword,
            username=username,
            password=password,
        ))
        error_string = response['error']
        if error_string:
            self.transient_message = error_string
            self.refresh_widget_states()
            return False

        self.auth_game.remember_token(username, response['token'])
        return True

    def back_clicked(self):
        self.screen_runner.done(False)

    def create_account_clicked(self):
        self.creating_account = True
        if not self.auth_game.is_trusted:
            self.transient_message = (
                'WARNING: Server is untrusted! Do not use a valuable password.')
        else:
            self.transient_message = ''
        self.username_edit.setFocus()
        self.refresh_widget_states()


class HostGamePage:
    def __init__(self, welcome_screen):
        self.async_manager = welcome_screen.async_manager   # Allows async callbacks
        self.window = window = welcome_screen.window
        self.message_viewer = welcome_screen.message_viewer
        self.screen_runner = UIScreenRunner()
        self.fields_changed = set()

        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.host_page = window.findChild(QWidget, 'host_page')
        self.host_image = window.findChild(QWidget, 'host_image')
        self.game_name_edit = window.findChild(QWidget, 'host_game_name_edit')
        self.scenario_combo = window.findChild(QWidget, 'host_scenario_combo')
        self.teams_combo = window.findChild(QWidget, 'host_teams_combo')
        self.map_combo = window.findChild(QWidget, 'host_map_combo')
        self.duration_edit = window.findChild(QWidget, 'host_duration_edit')
        self.slow_blitz_mode_checkbox = window.findChild(QWidget, 'host_blitz_mode_checkbox')
        self.experimental_widgets = [
            self.slow_blitz_mode_checkbox,
            window.findChild(QWidget, 'blitz_mode_label'),
        ]
        self.warning_label = window.findChild(QWidget, 'host_warning_label')

        self.game_name_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))
        self.game_name_edit.textEdited.connect(
            run_callback_in_async_loop(self.game_name_changed))
        self.duration_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))
        self.duration_edit.textEdited.connect(
            run_callback_in_async_loop(self.duration_changed))
        self.scenario_combo.currentIndexChanged.connect(
            run_callback_in_async_loop(self.update_combo_boxes))

        self.pixmap = QPixmap(str(QUESTION_IMAGE_FILE))
        self.host_image.setPixmap(self.pixmap)

        window.findChild(QWidget, 'host_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'host_ok_button').clicked.connect(
            run_callback_in_async_loop(self.ok_clicked))

        self.scenario_combo.clear()
        for level_class in scenario_options:
            self.scenario_combo.addItem(level_class.levelName)
        self.update_combo_boxes()

    def update_experimental_options(self):
        display_settings = ClientSettings.get().display
        for widget in self.experimental_widgets:
            if display_settings.show_experimental:
                widget.show()
            else:
                widget.hide()

    async def run(self):
        previous_page_widget = self.main_stack.currentWidget()
        try:
            self.update_experimental_options()
            self.main_stack.setCurrentWidget(self.host_page)
            nick = ClientSettings.get().identity.nick
            if nick:
                self.game_name_edit.setText(f'{nick}’s game')
            self.game_name_edit.setFocus()
            self.warning_label.setText(' ')
            return await self.screen_runner.run()
        finally:
            self.main_stack.setCurrentWidget(previous_page_widget)

    def game_name_changed(self, *args):
        self.fields_changed.add('name')
        self.check_validity()

    def duration_changed(self, *args):
        self.fields_changed.add('duration')
        self.check_validity()

    def check_validity(self, force=False):
        if (force or 'name' in self.fields_changed) and not self.check_game_name_validity():
            return False
        if (force or 'duration' in self.fields_changed) and not self.check_duration_validity():
            return False
        self.warning_label.setText(' ')
        return True

    def check_game_name_validity(self):
        game_name = self.game_name_edit.text().strip()
        if not game_name:
            self.warning_label.setText('Please enter a game name.')
            return False
        return True

    def check_duration_validity(self):
        try:
            duration = float(self.duration_edit.text())
        except ValueError:
            self.warning_label.setText('Please enter a valid game duration.')
            return False
        return True

    def update_combo_boxes(self, *args):
        scenario_index = self.scenario_combo.currentIndex()
        level_class = scenario_options[scenario_index]
        self.teams_combo.clear()
        for team_option in level_class.team_selection:
            self.teams_combo.addItem(team_option)
        self.map_combo.clear()
        for map_option in level_class.map_selection:
            self.map_combo.addItem(map_option.name)
        self.duration_edit.setText(format_number(level_class.default_duration / 60))

    @async_callback
    async def ok_clicked(self):
        if not self.check_validity(force=True):
            return

        level_options = LevelOptions(
            team_option_index=self.teams_combo.currentIndex(),
            map_index=self.map_combo.currentIndex(),
            duration=float(self.duration_edit.text()) * 60,
        )
        level_class = scenario_options[self.scenario_combo.currentIndex()]
        level = level_class(level_options=level_options)
        try:
            await host_lan_game(
                level,
                self.game_name_edit.text(),
                slow_dark_conquest=not self.slow_blitz_mode_checkbox.isChecked(),
            )
        except asyncio.CancelledError:
            pass
        except LostGameConnection:
            await self.message_viewer.run(
                'The connection to the game was lost.', 'ok', image = STOP_IMAGE_FILE)
        self.screen_runner.done(True)

    def back_clicked(self):
        self.screen_runner.done(False)


class IPConnectPage:
    def __init__(self, play_screen, welcome_screen):
        self.play_screen = play_screen
        self.async_manager = welcome_screen.async_manager   # Allows async callbacks
        self.window = window = welcome_screen.window
        self.message_viewer = welcome_screen.message_viewer
        self.screen_runner = UIScreenRunner()

        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.ip_connect_page = window.findChild(QWidget, 'ip_connect_page')
        self.ip_connect_image = window.findChild(QWidget, 'ip_connect_image')
        self.address_edit = window.findChild(QWidget, 'ip_connect_address_edit')
        self.port_edit = window.findChild(QWidget, 'ip_connect_port_edit')
        self.warning_label = window.findChild(QWidget, 'ip_connect_warning_label')

        self.address_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))
        self.port_edit.returnPressed.connect(
            run_callback_in_async_loop(self.ok_clicked))

        self.pixmap = QPixmap(str(QUESTION_IMAGE_FILE))
        self.ip_connect_image.setPixmap(self.pixmap)

        window.findChild(QWidget, 'ip_connect_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'ip_connect_ok_button').clicked.connect(
            run_callback_in_async_loop(self.ok_clicked))

    async def run(self):
        previous_page_widget = self.main_stack.currentWidget()
        try:
            self.main_stack.setCurrentWidget(self.ip_connect_page)
            self.address_edit.setText('')
            self.port_edit.setText(str(DEFAULT_GAME_PORT))
            self.address_edit.setFocus()
            self.warning_label.setText(' ')
            return await self.screen_runner.run()
        finally:
            self.main_stack.setCurrentWidget(previous_page_widget)

    def check_port_validity(self):
        try:
            duration = int(self.port_edit.text())
        except ValueError:
            self.warning_label.setText('Please enter a valid port.')
            return False
        return True

    @async_callback
    async def ok_clicked(self):
        if not self.check_port_validity():
            return

        try:
            await self.message_viewer.run_task('Connecting to game…', self.launch())
        except asyncio.CancelledError:
            pass
        except LostGameConnection:
            await self.message_viewer.run(
                'The connection to the game was lost.', 'ok', image = STOP_IMAGE_FILE)
        self.screen_runner.done(True)

    async def launch(self):
        host = self.address_edit.text()
        port = int(self.port_edit.text())
        await connect_to_remote_trosnoth_game(
            self.play_screen.ui_routines, False, host, port, auth_tag=0)

    def back_clicked(self):
        self.screen_runner.done(False)
