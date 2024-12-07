import logging

from trosnoth.trosnothgui.ingame.dialogs import JoinGameDialog
from trosnoth.gui.framework.dialogbox import DialogResult

log = logging.getLogger(__name__)


class JoinGameController(object):
    '''
    Shows and hides the join game dialog.
    '''

    def __init__(self, app, gameInterface, game):
        self.app = app
        self.world = game.world
        self.interface = gameInterface

        self.previous_nickname_was_rejected = False

        self.join_game_dialog = JoinGameDialog(self.app, self, self.world)
        self.join_game_dialog.onClose.addListener(self.join_dialog_closed)

    ### External API calls

    def established_connection_to_game(self):
        self.try_to_join_game(just_connected=True)

    def lost_connection_to_game(self):
        self.hide_dialog_if_showing()

    def successfully_joined_game(self):
        self.hide_dialog_if_showing()

    def now_spectating_game(self):
        self.hide_dialog_if_showing()

    def spectator_requests_join(self):
        self.try_to_join_game()

    def user_should_try_a_different_name(self):
        '''
        Called by the game interface when a join has failed with a
        reason that’s related to the selected nickname.
        '''
        # Try again immediately (this time the dialog will show, even
        # if the previous attempt was automatic).
        self.previous_nickname_was_rejected = True
        self.try_to_join_game()

    def world_was_reset(self):
        '''
        Called by the game interface whenever a world reset is received.
        '''
        if self.join_game_dialog.showing:
            # We might no longer need to choose a team
            self.join_game_dialog.close()
            self.try_to_join_game()

    ### Internal functions

    def hide_dialog_if_showing(self):
        if self.join_game_dialog.showing:
            self.join_game_dialog.close()

    def try_to_join_game(self, just_connected=False):
        if self.interface.player:
            return

        options = self.world.uiOptions
        game_is_local = self.interface.world.isServer
        require_nick = (
            self.previous_nickname_was_rejected
            or (just_connected and not game_is_local)
            or not self.app.settings.identity.nick)

        can_switch_later = not bool(
            set(options.team_ids_humans_can_join)
            - set(options.team_ids_humans_can_switch_to))
        if options.allow_scenario_voting and can_switch_later and not require_nick:
            # Just join the game, player can switch teams once in
            select_team = False
        else:
            select_team = len(options.team_ids_humans_can_join) > 1

        self.previous_nickname_was_rejected = False
        if select_team or require_nick:
            self.join_game_dialog.show(require_nick, select_team)
        else:
            self.attempt_join_game(
                self.app.settings.identity.nick, self.app.settings.identity.head)

    def join_dialog_closed(self):
        if self.join_game_dialog.result is None:
            # Closed by us not the user
            return
        if self.join_game_dialog.result != DialogResult.OK:
            self.interface.spectate()
        else:
            if self.join_game_dialog.selected_nick:
                nick = self.join_game_dialog.selected_nick
                head = self.join_game_dialog.selected_head
                self.app.settings.identity.set_info(nick, head)
                self.app.settings.save()
            else:
                nick = self.app.settings.identity.nick
                head = self.app.settings.identity.head

            team = self.join_game_dialog.selected_team
            self.attempt_join_game(nick, head, team)

    def attempt_join_game(self, nick, head, team=None):
        self.interface.joinGame(nick, head, team)
