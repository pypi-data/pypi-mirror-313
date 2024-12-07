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

from twisted.protocols import amp


class AuthServerError(Exception):
    pass


class NotAuthenticated(AuthServerError):
    pass


class GameDoesNotExist(AuthServerError):
    '''
    Cannot join the given game because it does not exist.
    '''


class GetServerInfo(amp.Command):
    '''
    Gets general information about the server.
    Added in Trosnoth 1.15.0.
    This is always called first, and incompatible client versions will
    then disconnect without making other calls.
    '''
    arguments = []
    response = [
        (b'name', amp.Unicode()),
        (b'version', amp.Unicode()),
        (b'extra', amp.Unicode(optional=True)),
    ]


class ListGames(amp.Command):
    '''
    Returns a list of the Trosnoth games available on this server.
    '''
    arguments = []
    response = [
        (b'games', amp.AmpList([
            (b'id', amp.Integer()),
            (b'name', amp.Unicode(optional=True)),
        ]))
    ]


class ConnectToGame(amp.Command):
    '''
    Requests details with which to join a particular game on the server.
    nick is the preferred nick of the authenticated player.
    '''
    arguments = [
        (b'game_id', amp.Integer()),
        (b'spectate', amp.Boolean()),
    ]
    response = [
        (b'port', amp.Integer()),
        (b'auth_tag', amp.Integer(optional=True)),
        (b'nick', amp.Unicode(optional=True)),
    ]
    errors = {
        NotAuthenticated: b'NO_AUTH',
        GameDoesNotExist: b'NO_GAME',
    }


class PasswordAuthenticate(amp.Command):
    '''
    Authenticates with the server using a password.
    '''
    arguments = [
        (b'username', amp.Unicode()),
        (b'password', amp.Unicode()),
    ]
    response = [
        (b'result', amp.Boolean()),
        (b'token', amp.String()),
    ]


class TokenAuthenticate(amp.Command):
    arguments = [
        (b'username', amp.Unicode()),
        (b'token', amp.String()),
    ]
    response = [
        (b'result', amp.Boolean()),
        (b'token', amp.String()),
    ]


class LocalUsername(amp.Command):
    '''
    Tell the server what the local username is. Usually this is ignored,
    but on camp we often set the server up to just trust this and create
    accounts based on the user's local username.
    '''
    arguments = [
        (b'username', amp.Unicode()),
    ]
    response = []


class GetAuthSettings(amp.Command):
    '''
    Asks the server how users are allowed to authenticate.
    '''
    arguments = []
    response = [
        (b'account_creation', amp.Boolean()),
    ]


class CreateUserWithPassword(amp.Command):
    '''
    Requests to create a user on the server using the given username and
    password.
    On success, a token is returned which may be used for token
    authentication.
    '''
    arguments = [
        (b'username', amp.Unicode()),
        (b'password', amp.Unicode()),
    ]
    response = [
        (b'error', amp.Unicode()),
        (b'token', amp.String()),
    ]
