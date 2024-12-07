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

import contextlib
import logging

from twisted.internet import reactor
from twisted.internet.error import CannotListenError

from trosnoth import version
from trosnoth.const import DEFAULT_GAME_PORT
from trosnoth.game import LocalGame
from trosnoth.model.agenthub import LocalHub
from trosnoth.network.base import MsgServer
from trosnoth.network.lobby import UDPMulticaster

from trosnoth.messages import (
    ChatMsg, InitClientMsg,
    ResyncAcknowledgedMsg, BuyUpgradeMsg, ShootMsg, GrapplingHookMsg,
    RespawnRequestMsg, JoinRequestMsg, UpdatePlayerStateMsg, AimPlayerAtMsg,
    PlayerIsReadyMsg, SetSuggestedDurationMsg, SetSuggestedTeamNameMsg,
    SetSuggestedMapMsg, RemovePlayerMsg, ChangeNicknameMsg, CheckSyncMsg,
    ThrowTrosballMsg, PlayerHasUpgradeMsg, PlayerAllDeadMsg, PingMsg,
    SetSuggestedScenarioMsg, EmoteRequestMsg, ChangeHeadMsg, ChangeTeamMsg, SwitchGunMsg,
    BuyAmmoMsg, ContributeToTeamBoostMsg, PlayerTickActionsMsg, SlowPingMsg, AcknowledgeGameOverMsg,
)
from trosnoth.utils import netmsg
from trosnoth.utils.event import Event
from trosnoth.utils.utils import console_locals

log = logging.getLogger(__name__)

agent_tick_messages = netmsg.MessageCollection(
    AimPlayerAtMsg,
    BuyAmmoMsg,
    BuyUpgradeMsg,
    CheckSyncMsg,
    ContributeToTeamBoostMsg,
    EmoteRequestMsg,
    AcknowledgeGameOverMsg,
    GrapplingHookMsg,
    PlayerAllDeadMsg,
    PlayerHasUpgradeMsg,
    RespawnRequestMsg,
    ResyncAcknowledgedMsg,
    ShootMsg,
    SlowPingMsg,
    SwitchGunMsg,
    ThrowTrosballMsg,
    UpdatePlayerStateMsg,
)

# The set of messages that the server expects to receive.
serverMsgs = netmsg.MessageCollection(
    JoinRequestMsg,
    ChatMsg,
    PlayerIsReadyMsg,
    SetSuggestedDurationMsg,
    SetSuggestedTeamNameMsg,
    SetSuggestedMapMsg,
    SetSuggestedScenarioMsg,
    RemovePlayerMsg,
    ChangeNicknameMsg,
    ChangeHeadMsg,
    ChangeTeamMsg,
    PlayerTickActionsMsg,
    PingMsg,
)


class TrosnothServerFactory(MsgServer):
    messages = serverMsgs

    def __init__(
            self, game, noAuth=False, agentCallback=None, *args, **kwargs):
        self.game = game
        self.noAuth = noAuth
        self.agentCallback = agentCallback

        self.connectedClients = set()

        self.onShutdown = Event()       # ()
        self.onConnectionEstablished = Event(['protocol'])
        self.onConnectionLost = Event(['protocol'])

        self.running = True
        self._alreadyShutdown = False
        self.port = None

    def checkGreeting(self, greeting):
        return greeting == b'Trosnoth18'

    def startListening(self, port=DEFAULT_GAME_PORT, interface=''):
        try:
            self.port = reactor.listenTCP(port, self, interface=interface)
        except CannotListenError:
            log.warning('WARNING: Could not listen on port %s', port)
            self.port = reactor.listenTCP(0, self, interface=interface)

    def getTCPPort(self):
        return self.port.getHost().port

    def stopListening(self):
        self.port.stopListening()

    def gotBadString(self, protocol, data):
        log.warning('Server: Unrecognised network data: %r' % (data,))
        log.warning('      : Did you invent a new network message and forget')
        log.warning('      : to add it to '
                    'trosnoth.network.server.serverMsgs?')

    def connectionEstablished(self, protocol):
        '''
        Called by the network manager when a new incoming connection is
        completed.
        '''
        # Remember that this connection's ready for transmission.
        self.connectedClients.add(protocol)
        hub = LocalHub(
            self.game, noAuth=self.noAuth, agentCallback=self.agentCallback)
        hub.connectNode(protocol)

        # Send the setting information.
        protocol.gotServerCommand(InitClientMsg(self._getClientSettings()))

        self.onConnectionEstablished(protocol)

    def _getClientSettings(self):
        '''Returns a byte string representing the settings which must be
        sent to clients that connect to this server.'''

        result = self.game.world.dumpEverything()
        result['serverVersion'] = version.version

        return repr(result).encode('utf-8')

    def connectionLost(self, protocol, reason):
        if protocol in self.connectedClients:
            protocol.hub.disconnectNode()

        self.connectedClients.remove(protocol)
        self.onConnectionLost(protocol)

    def shutdown(self):
        if self._alreadyShutdown:
            return
        self._alreadyShutdown = True

        # Kill server
        self.running = False
        self.game.stop()
        self.stopListening()
        self.onShutdown.execute()
        for protocol in self.connectedClients:
            protocol.transport.loseConnection()


class ListenServer:
    '''
    Interface for running a listen server within the game process.
    '''
    instance = None

    @classmethod
    def is_running(cls):
        return bool(cls.instance)

    @classmethod
    def get_server(cls):
        return cls.instance.server

    @classmethod
    def get_multicast_game_info(cls):
        if not cls.is_running():
            return []
        server = cls.get_server()
        return [{
            'version': version.version,
            'port': server.getTCPPort(),
            'name': cls.instance.game_name,
            'format': server.game.world.game_format,
        }]

    @classmethod
    @contextlib.contextmanager
    def run(cls, level, game_name, **kwargs):
        listen_server = cls(level, game_name, **kwargs)
        listen_server.install()
        multicaster = None
        try:
            multicaster = UDPMulticaster(cls.get_multicast_game_info)
            multicaster.start()
            yield listen_server.server.game
        finally:
            listen_server.server.shutdown()
            if multicaster:
                multicaster.stop()

    def __init__(self, level, game_name='Unnamed game', **kwargs):
        self.game_name = game_name
        game = LocalGame(
            saveReplay=True, gamePrefix='LAN', level=level, onceOnly=True, wait_for_ready=True,
            tweener_can_drive_ticks=False,
            **kwargs,
        )
        self.server = TrosnothServerFactory(game)
        console_locals.get()['server'] = self.server
        self.server.onShutdown.addListener(self._server_shutdown)
        self.server.startListening()
        self.old_instance = None

    def install(self):
        self.old_instance = type(self).instance
        type(self).instance = self

    def _server_shutdown(self):
        console_locals.get()['server'] = None
        if type(self).instance is self:
            type(self).instance = self.old_instance
