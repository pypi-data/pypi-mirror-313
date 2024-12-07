# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2012 Joshua D Bartlett
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
import getpass
import hashlib
import ipaddress
import logging
import socket
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import List, Optional

import simplejson
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from twisted.internet.ssl import ClientContextFactory

from trosnoth.const import MULTICAST_PROTOCOL_NAME
from trosnoth.network import authcommands
from trosnoth.network.client import TrosnothClientProtocol
from trosnoth.network.networkDefines import (
    multicastPort, multicastGroup,
)
from trosnoth.settings import getPolicySettings, ServerCredentials
from trosnoth.utils.aio import SimpleAsyncIterator, as_future
from trosnoth.utils.unrepr import unrepr
from twisted.internet.error import CannotListenError
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator, DatagramProtocol
from twisted.protocols import amp
from trosnoth.utils.twist import WeakCallLater

log = logging.getLogger(__name__)


async def connect_to_game_server(host, port, timeout=5):
    cc = ClientCreator(reactor, TrosnothClientProtocol)

    trosnoth_client = await as_future(cc.connectTCP(str(host), port, timeout=timeout))
    settings = await as_future(trosnoth_client.getSettings())

    return (trosnoth_client, settings)


async def ask_for_auth_game_details(
        amp_client, game_id, spectate, credentials: Optional[ServerCredentials]):
    logged_in = False
    new_token = None
    try:
        # 1. Ask for details to connect
        return await as_future(amp_client.callRemote(
            authcommands.ConnectToGame, game_id=game_id, spectate=spectate,
        ))
    except authcommands.NotAuthenticated:
        # 2. Attempt to log in using the ‘remember me’ token
        if credentials:
            result = await as_future(amp_client.callRemote(
                authcommands.TokenAuthenticate,
                username=credentials.username,
                token=credentials.secret))
            logged_in = result['result']
            if logged_in:
                new_token = result['token']

        # 3. Attempt to log in using this computer’s username (if configured to)
        if not logged_in and getPolicySettings().get('privacy', 'sendusername', fallback=False):
            logged_in = await as_future(amp_client.callRemote(
                authcommands.LocalUsername, username=getpass.getuser()))

        # 4. Propagate the exception so the caller can do the logging in
        if not logged_in:
            raise

    # If login was successful, try the call again
    result = await as_future(amp_client.callRemote(
        authcommands.ConnectToGame, game_id=game_id, spectate=spectate,
    ))
    if new_token:
        result['new_token'] = new_token
    return result


class AuthGame:
    def __init__(self, game_id, name):
        self.id = game_id
        self.name = name


class NonAuthGame:
    def __init__(self, ip_address, port, details=None):
        self.ip = ip_address
        self.port = port
        self.details = details or {}
        self.name = details.get('name', 'Unnamed game')


class AuthClientProtocol(amp.AMP):
    server_name = None
    server_version = None
    server_key_digest = None

    @classmethod
    @asynccontextmanager
    async def connect(cls, host, port, timeout=5):
        if isinstance(host, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            host = str(host)
        elif not isinstance(host, str):
            raise TypeError(f'host must be ip_address or str, not {type(host)}')

        protocol = await as_future(ClientCreator(reactor, cls).connectSSL(
            host, port, ClientContextFactory(), timeout=timeout))
        try:
            info = await as_future(protocol.callRemote(authcommands.GetServerInfo))
            public_key = protocol.transport.getPeerCertificate().get_pubkey().to_cryptography_key()

            protocol.server_name = info['name']
            protocol.server_version = info['version']
            protocol.server_key_digest = hashlib.sha256(
                public_key.public_bytes(Encoding.DER, PublicFormat.PKCS1)).hexdigest()

            yield protocol
        finally:
            if protocol.transport and protocol.transport.connected:
                protocol.transport.loseConnection()


@dataclass
class ServerInfoAndGames:
    name: str
    version: str
    games: List[AuthGame]
    key_digest: RSAPublicKey


async def get_server_info_and_games(server, timeout=4):
    '''
    Connects to an authentication server and asks it for its name,
    version, and a list of available games.

    :param server: A tuple of (host, port)
    :param timeout: seconds before attempt is canceled
    '''
    host, port = server
    async with AuthClientProtocol.connect(host, port, timeout) as conn:
        result = ServerInfoAndGames(
            conn.server_name, conn.server_version, [], conn.server_key_digest)

        data = await as_future(conn.callRemote(authcommands.ListGames))
        for item in data['games']:
            result.games.append(AuthGame(item['id'], item['name']))

        return result


class UDPMulticaster(object):
    def __init__(self, gameGetter):
        self.logging_expects_success = True
        self.stopped = True
        self.port = None
        self.listener = UDPMulticastListener(gameGetter)
        self.tryListening()

    def stop(self):
        if self.port is not None:
            self.port.stopListening()
        self.stopped = True

    def start(self):
        if self.stopped:
            self.stopped = False
            self.tryListening()

    def tryListening(self):
        if self.stopped:
            return
        try:
            self.port = reactor.listenMulticast(multicastPort, self.listener)
            if not self.logging_expects_success:
                self.logging_expects_success = True
                log.warning('Multicast list succeeded')
        except CannotListenError as e:
            # Cannot listen to the multicast, possibly because another
            # instance is running on this computer.
            if self.logging_expects_success:
                self.logging_expects_success = False
                log.warning(f'{e}: retrying every 5 seconds')

            # Try listening again in 5 seconds.
            WeakCallLater(5, self, 'tryListening')


class UDPMulticastListener(DatagramProtocol):
    def __init__(self, gameGetter):
        '''
        gameGetter must be callable, and return a sequence of game information
        dicts, each of which must contain:
            ['port'] - the port this game is listening on
            ['version'] - the version string
            ['name'] - the game name
        '''
        self.getGames = gameGetter

    def startProtocol(self):
        # Join the correct multicast group.
        self.transport.joinGroup(multicastGroup)

    def datagramReceived(self, datagram, address):
        '''
        A multicast datagram has been received.
        '''
        if datagram == b'%s:GetGames' % (MULTICAST_PROTOCOL_NAME,):
            for game in self.getGames():
                self.transport.write(
                    b'%s:Game:%s' % (MULTICAST_PROTOCOL_NAME, repr(game).encode('utf-8'),),
                    address)


class UDPMulticastAsyncGameGetter(DatagramProtocol):
    def __init__(self):
        self.port = None
        self.iter = None

    async def get_games(self, timeout=3):
        self.port = reactor.listenUDP(0, self)
        try:
            try:
                self.transport.write(
                    b'%s:GetGames' % MULTICAST_PROTOCOL_NAME, (multicastGroup, multicastPort))
            except socket.error as e:
                log.info('Could not request games from multicast: %s', e)
                return

            async for game in self.wait_for_responses(timeout):
                yield game
        finally:
            self.port.stopListening()

    def wait_for_responses(self, timeout):
        self.iter = SimpleAsyncIterator()
        asyncio.get_running_loop().call_later(timeout, self.iter.done)
        return self.iter

    def datagramReceived(self, datagram, address):
        '''
        A reply to our query has been received.
        '''
        if not datagram.startswith(b'%s:Game:' % (MULTICAST_PROTOCOL_NAME,)):
            return

        info_string = datagram[len(b'%s:Game:' % (MULTICAST_PROTOCOL_NAME,)):]
        try:
            game_info = unrepr(info_string)
        except SyntaxError:
            log.warning(f'Received ill-formatted LAN game datagram: {datagram}')
            return

        if not isinstance(game_info, dict) or 'port' not in game_info:
            log.warning(f'Received invalid LAN game info: {game_info}')
            return
        port = game_info.pop('port')
        if not isinstance(port, int):
            log.warning(f'Received invalid LAN game port: {port}')
            return
        ip_address = ipaddress.ip_address(address[0])
        self.iter.next(NonAuthGame(ip_address, port, game_info))


class UDPMulticastManyServerGetter(DatagramProtocol):
    def __init__(self):
        self.port = None
        self.iter = None

    async def get_servers(self, timeout=3):
        self.port = reactor.listenUDP(0, self)
        try:
            try:
                self.transport.write(
                    b'%s:GetServer' % MULTICAST_PROTOCOL_NAME, (multicastGroup, multicastPort))
            except socket.error as e:
                log.info('Could not request servers from multicast: %s', e)
                return

            async for server in self.wait_for_responses(timeout):
                yield server
        finally:
            self.port.stopListening()

    def wait_for_responses(self, timeout):
        self.iter = SimpleAsyncIterator()
        asyncio.get_running_loop().call_later(timeout, self.iter.done)
        return self.iter

    def datagramReceived(self, datagram, address):
        '''
        A reply to our query has been received.
        '''
        if not datagram.startswith(b'%s:Server:' % (MULTICAST_PROTOCOL_NAME,)):
            return

        auth_port = simplejson.loads(datagram[len(b'%s:Server:' % (MULTICAST_PROTOCOL_NAME,)):])
        if not isinstance(auth_port, int):
            return
        server = (ipaddress.ip_address(address[0]), auth_port)
        self.iter.next(server)


def get_multicast_servers(timeout=1):
    return UDPMulticastManyServerGetter().get_servers(timeout)
