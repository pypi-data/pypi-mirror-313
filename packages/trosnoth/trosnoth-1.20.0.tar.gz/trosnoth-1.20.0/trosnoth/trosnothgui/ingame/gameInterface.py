import math
from dataclasses import dataclass
from functools import partial
import logging
import random
from typing import Optional, TYPE_CHECKING

import pygame
from trosnoth.gui.framework.framework import CompoundElement
from twisted.internet import defer, reactor

from trosnoth.const import (
    TROSBALL_DEATH_HIT, OPEN_CHAT, PRIVATE_CHAT, TEAM_CHAT,
    NOT_ENOUGH_COINS_REASON, PLAYER_DEAD_REASON, CANNOT_REACTIVATE_REASON,
    GAME_NOT_STARTED_REASON, TOO_CLOSE_TO_EDGE_REASON, PLAYER_HAS_TROSBALL_REASON,
    TOO_CLOSE_TO_ORB_REASON, NOT_IN_DARK_ZONE_REASON, INVALID_UPGRADE_REASON,
    DISABLED_UPGRADE_REASON, ALREADY_ALIVE_REASON, BE_PATIENT_REASON,
    ENEMY_ZONE_REASON, FROZEN_ZONE_REASON, BOMBER_DEATH_HIT,
    ACTION_CLEAR_UPGRADE, GAME_FULL_REASON, NICK_USED_REASON, BAD_NICK_REASON, UNAUTHORISED_REASON,
    USER_IN_GAME_REASON, ALREADY_JOINED_REASON, LEFT_STATE, RIGHT_STATE, TICK_PERIOD,
)
from trosnoth.gui.framework import framework, hotkey, console
from trosnoth.gui.framework.declarative import (
    DeclarativeElement, Text, Rectangle,
    ComplexDeclarativeThing, FadeIn, FullScreenRectangle, Button,
)
from trosnoth.gui.framework.collapsebox import CollapseBox
from trosnoth.gui import keyboard
from trosnoth.gui.common import (
    Region, Screen, Canvas,
)

from trosnoth.gamerecording.achievementlist import availableAchievements
from trosnoth.levels.base import FrozenLevelStats

from trosnoth.model.agent import ConcreteAgent, LocalPlayerSmoother
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.model.upgrades import Shoxwave

from trosnoth.trosnothgui.ingame import viewmanager
from trosnoth.trosnothgui.ingame.achievementdisplay import (
    AchievementDisplay, RecentAchievements,
)
from trosnoth.trosnothgui.ingame.crowdnoise import CrowdNoiseGenerator
from trosnoth.trosnothgui.ingame.replayInterface import ViewControlInterface
from trosnoth.trosnothgui.ingame.joincontroller import JoinGameController
from trosnoth.trosnothgui.ingame.detailsInterface import DetailsInterface, LogMessage
from trosnoth.trosnothgui.ingame.playerInterface import PlayerInterface

from trosnoth import keymap

from trosnoth.data import user, getPath

from trosnoth.utils import globaldebug
from trosnoth.utils.event import Event
from trosnoth.utils.twist import WeakLoopingCall

from trosnoth.messages import (
    ChatFromServerMsg, ChatMsg, PingMsg,
    ShotFiredMsg, RespawnMsg, CannotRespawnMsg, TickMsg,
    CannotJoinMsg, AddPlayerMsg, PlayerHasUpgradeMsg, RemovePlayerMsg,
    PlayerCoinsSpentMsg, CannotBuyUpgradeMsg, ConnectionLostMsg,
    AchievementUnlockedMsg, SetPlayerTeamMsg, PlaySoundMsg,
    FireShoxwaveMsg, AwardPlayerCoinMsg,
    PlayerHasTrosballMsg, SlowPingMsg, BuyAmmoMsg, ScenarioCompleteMsg,
)
from trosnoth.utils.utils import console_locals

if TYPE_CHECKING:
    from trosnoth.model.player import Player

log = logging.getLogger(__name__)


class GameInterface(framework.CompoundElement, ConcreteAgent):
    '''Interface for when we are connected to a game.'''

    local_player_driver_class = LocalPlayerSmoother
    achievementDefs = availableAchievements

    def __init__(
            self, app, game, on_clean_exit=None,
            on_lost_connection=None, replay=False, authTag=0, spectate=False):
        super(GameInterface, self).__init__(app, game=game)
        self.localState.onShoxwave.addListener(self.localShoxwaveFired)
        self.localState.onGameInfoChanged.addListener(self.gameInfoChanged)
        self.world.onOpenChatReceived.addListener(self.openChat)
        self.world.onTeamChatReceived.addListener(self.teamChat)
        self.world.onReset.addListener(self.worldReset)
        self.world.onGrenadeExplosion.addListener(self.grenadeExploded)
        self.world.onTrosballExplosion.addListener(self.trosballExploded)
        self.world.onBomberExplosion.addListener(self.bomber_exploded)
        self.world.on_mine_explosion.addListener(self.mine_exploded)
        self.world.onZoneTagged.addListener(self.orb_tagged)
        self.world.elephant.on_transfer.addListener(self.elephant_transferred)
        self.world.juggernaut.on_transfer.addListener(self.juggernaut_transferred)
        self.timingsLoop = WeakLoopingCall(self, '_sendPing')
        self.crowd_noise = CrowdNoiseGenerator(app, self.world)

        self.current_boost_purchase = TeamBoostTransactionTracker(self)

        self.subscribedPlayers = set()
        self.recent_achievements = RecentAchievements()

        self.on_scenario_complete = Event(['result'])

        self.on_clean_exit = Event()
        if on_clean_exit is not None:
            self.on_clean_exit.addListener(on_clean_exit)

        self.on_lost_connection = Event()
        if on_lost_connection is not None:
            self.on_lost_connection.addListener(on_lost_connection)
        self.game = game

        self.keyMapping = keyboard.KeyboardMapping(keymap.default_game_keys)
        self.runningPlayerInterface = None
        self.updateKeyMapping()
        self.gameViewer = viewmanager.GameViewer(self.app, self, game, replay)
        if replay or spectate:
            self.joinController = None
        else:
            self.joinController = JoinGameController(self.app, self, self.game)
        self.detailsInterface = DetailsInterface(self.app, self)
        self.timing_info = TimingInfo()
        self.gameInfoDisplay = GameInfoDisplay(
            app, self,
            Region(topleft=Screen(0.01, 0.05), size=Canvas(330, 200)))
        self.hotkeys = hotkey.Hotkeys(
            self.app, self.keyMapping, self.detailsInterface.doAction)
        self.terminal = None
        self.end_screen = None
        self.connection_was_lost = False

        self.vcInterface = None
        if replay:
            self.vcInterface = ViewControlInterface(self.app, self)

        self.ready = False
        if self.joinController:
            defer.maybeDeferred(game.addAgent, self, authTag=authTag).addCallback(self.addedAgent)

        self.setElements()

        if spectate:
            self.spectate()

        self.timingsLoop.start(1, now=False)

    def _sendPing(self):
        if self.connection_was_lost:
            return
        for i in range(3):
            data = bytes([random.randrange(256)])
            if data not in self.localState.pings:
                self.sendRequest(PingMsg(data))
                break

        for i in range(3):
            data = bytes([random.randrange(256)])
            if data not in self.localState.slow_pings:
                self.sendRequest(SlowPingMsg(data))
                break

    def gameInfoChanged(self):
        self.gameInfoDisplay.refreshInfo()

    def addedAgent(self, result):
        self.ready = True
        if self.joinController:
            self.joinController.established_connection_to_game()

    def spectatorWantsToJoin(self):
        if self.runningPlayerInterface or not self.joinController:
            return
        self.joinController.spectator_requests_join()

    def sendRequest(self, msg):
        if not self.ready:
            # Not yet completely connected to game
            return
        super(GameInterface, self).sendRequest(msg)

    def worldReset(self, *args, **kwarsg):
        if self.ready and self.joinController:
            self.joinController.world_was_reset()
        self.gameViewer.reset()

    def updateKeyMapping(self):
        # Set up the keyboard mapping.
        try:
            # Try to load keyboard mappings from the user's personal settings.
            with open(getPath(user, 'keymap'), 'r') as f:
                config = f.read()
            self.keyMapping.load(config)
            if self.runningPlayerInterface:
                self.runningPlayerInterface.keyMappingUpdated()
        except IOError:
            pass

    def detached(self):
        super().detached()
        self.connectionLost(None)

    @ConnectionLostMsg.handler
    def connectionLost(self, msg):
        self.connection_was_lost = True
        self.cleanUp()
        if self.joinController:
            self.joinController.lost_connection_to_game()

        if not self.end_screen:
            if self.gameViewer.replay:
                self.on_clean_exit()
            else:
                self.on_lost_connection()

    def joined(self, player):
        '''Called when joining of game is successful.'''
        pygame.key.set_repeat()
        self.gameViewer.worldgui.overridePlayer(self.localState.player)
        self.runningPlayerInterface = pi = PlayerInterface(self.app, self)
        self.detailsInterface.setPlayer(pi.player)
        self.setElements()

        self.joinController.successfully_joined_game()
        self.gameViewer.leaderboard.update()

    def spectate(self):
        '''
        Called by join controller if user selects to only spectate.
        '''
        self.vcInterface = ViewControlInterface(self.app, self)
        self.setElements()

        # Regenerate leaderboard so names are clickable
        self.gameViewer.leaderboard.update()

        if self.joinController:
            self.joinController.now_spectating_game()

    def stop(self):
        super(GameInterface, self).stop()
        self.localState.onShoxwave.removeListener(self.localShoxwaveFired)
        self.localState.onGameInfoChanged.removeListener(self.gameInfoChanged)
        self.world.juggernaut.on_transfer.removeListener(self.juggernaut_transferred)
        self.world.elephant.on_transfer.removeListener(self.elephant_transferred)
        self.world.onOpenChatReceived.removeListener(self.openChat)
        self.world.onTeamChatReceived.removeListener(self.teamChat)
        self.world.onReset.removeListener(self.worldReset)
        self.world.onGrenadeExplosion.removeListener(self.grenadeExploded)
        self.world.onTrosballExplosion.removeListener(self.trosballExploded)
        self.world.onBomberExplosion.removeListener(self.bomber_exploded)
        self.world.on_mine_explosion.removeListener(self.mine_exploded)
        self.world.onZoneTagged.removeListener(self.orb_tagged)
        self.timingsLoop.stop()
        self.gameViewer.stop()
        self.detailsInterface.stop()
        self.crowd_noise.stop()
        self.app.soundPlayer.stop_looping_sounds()
        if self.runningPlayerInterface is not None:
            self.runningPlayerInterface.stop()
        if self.end_screen:
            self.end_screen.stop()

        self.elements = []
        self.detailsInterface = None
        self.runningPlayerInterface = None
        self.gameViewer = None

    def setElements(self):
        if self.end_screen:
            joined = True
            if self.end_screen.fully_showing:
                self.elements = [self.end_screen]
            else:
                self.elements = [
                    self.gameViewer,
                    self.gameInfoDisplay,
                    self.end_screen,
                    DeclarativeElement(self.app, (0, 0.725), AchievementDisplay(
                        self.recent_achievements, self.detailsInterface.player)),
                ]
        elif self.runningPlayerInterface:
            joined = True
            self.elements = [
                self.gameViewer, self.runningPlayerInterface,
                self.gameInfoDisplay, self.hotkeys, self.detailsInterface,
                DeclarativeElement(self.app, (0, 0.65), MaybeShowUpscaleMessage()),
                DeclarativeElement(self.app, (0, 0.725), AchievementDisplay(
                    self.recent_achievements, self.detailsInterface.player)),
                DeclarativeElement(
                    self.app, (0, 0), GameTipDisplay(self.detailsInterface.player))
            ]
        else:
            joined = False
            self.elements = [
                self.gameViewer,
                self.gameInfoDisplay,
            ]
            if self.vcInterface is not None:
                self.elements.append(self.vcInterface)
            if self.joinController:
                self.elements.append(DeclarativeElement(self.app, (-1, 1), JoinDisplay(self)))
            self.elements.extend([
                self.hotkeys,
                self.detailsInterface,
            ])

        self.elements.append(
            DeclarativeElement(self.app, (-0.4, 1), TimingDisplay(self, self.timing_info)))

        self.detailsInterface.menuManager.set_mode(
            joined=joined, can_join=bool(self.joinController))

    def is_spectating(self):
        '''
        :return: True for replays or observer mode.
        '''
        return not self.runningPlayerInterface

    def toggleTerminal(self):
        if self.terminal is None:
            locs = {'app': self.app}
            try:
                locs.update(console_locals.get())
            except LookupError:
                pass
            self.terminal = console.TrosnothInteractiveConsole(
                self.app,
                self.app.screenManager.fonts.consoleFont,
                Region(size=Screen(1, 0.4), bottomright=Screen(1, 1)),
                locals=locs)
            self.terminal.interact().addCallback(self._terminalQuit)

        from trosnoth.utils.utils import timeNow
        if self.terminal in self.elements:
            if timeNow() > self._termWaitTime:
                self.elements.remove(self.terminal)
        else:
            self._termWaitTime = timeNow() + 0.1
            self.elements.append(self.terminal)
            self.setFocus(self.terminal)

    def _terminalQuit(self, result):
        if self.terminal in self.elements:
            self.elements.remove(self.terminal)
        self.terminal = None

    def disconnect(self):
        self.cleanUp()
        self.on_clean_exit()

    def joinGame(self, nick, head, team, timeout=10):
        if team is None:
            teamId = NEUTRAL_TEAM_ID
        else:
            teamId = team.id

        self.sendJoinRequest(teamId, nick, head)

    def setPlayer(self, player):
        if not player:
            self.gameViewer.worldgui.removeOverride()
            self.lostPlayer()

        super(GameInterface, self).setPlayer(player)

        if player:
            if __debug__ and globaldebug.enabled:
                globaldebug.localPlayerId = player.id

            self.joined(player)

    @CannotJoinMsg.handler
    def joinFailed(self, msg):
        args = {}
        if msg.reasonId == GAME_FULL_REASON:
            message = LogMessage.GAME_FULL
        elif msg.reasonId == NICK_USED_REASON:
            message = LogMessage.NICK_IN_USE
            self.joinController.user_should_try_a_different_name()
        elif msg.reasonId == BAD_NICK_REASON:
            message = LogMessage.BAD_NICK
            self.joinController.user_should_try_a_different_name()
        elif msg.reasonId == UNAUTHORISED_REASON:
            message = LogMessage.UNAUTHORISED
        elif msg.reasonId == USER_IN_GAME_REASON:
            message = LogMessage.ALREADY_JOINED
        elif msg.reasonId == ALREADY_JOINED_REASON:
            message = LogMessage.ALREADY_JOINED
        else:
            # Unknown reason.
            message = LogMessage.JOIN_FAILED
            args = dict(code=msg.reasonId)
            message = 'Join failed (%r)' % (msg.reasonId,)

        self.detailsInterface.new_message(message, **args)
        self.detailsInterface.newChat(message.format(**args), None)

    def cleanUp(self):
        if self.gameViewer.timerBar is not None:
            self.gameViewer.timerBar = None
        pygame.key.set_repeat(300, 30)

    @PlayerCoinsSpentMsg.handler
    def discard(self, msg):
        pass

    @AwardPlayerCoinMsg.handler
    def playerAwardedCoin(self, msg):
        if not self.localState.player:
            return
        if msg.sound and msg.playerId == self.localState.player.id:
            self.play_sound('gotCoin')

    def elephant_transferred(self, old_possessor, new_possessor):
        if new_possessor:
            self.detailsInterface.new_message(
                LogMessage.ELEPHANT_GAINED,
                player=new_possessor.nick,
                elephant=self.world.uiOptions.elephantName,
            )

    def juggernaut_transferred(self, old_possessor, new_possessor):
        if new_possessor:
            self.detailsInterface.new_message(
                LogMessage.NEW_JUGGERNAUT, player=new_possessor.nick)

    @PlayerHasTrosballMsg.handler
    def gotTrosball(self, msg, _lastTrosballPlayer=[None]):
        player = self.world.playerWithId.get(msg.playerId)

        if player != _lastTrosballPlayer[0]:
            _lastTrosballPlayer[0] = player
            if player is None:
                self.detailsInterface.new_message(LogMessage.TROSBALL_DROPPED)
            else:
                self.detailsInterface.new_message(LogMessage.TROBSALL_GAINED, player=player.nick)

    @AddPlayerMsg.handler
    def addPlayer(self, msg):
        player = self.world.getPlayer(msg.playerId)
        if player and player not in self.subscribedPlayers:
            self.subscribedPlayers.add(player)
            team_name = str(player.team) if player.team else self.world.rogueTeamName
            self.detailsInterface.new_message(
                LogMessage.PLAYER_JOINED, player=player.nick, team=team_name)
            player.onDied.addListener(partial(self.player_died, player))

    @SetPlayerTeamMsg.handler
    def changeTeam(self, msg):
        self.defaultHandler(msg)    # Make sure the local player changes team
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.new_message(
                LogMessage.PLAYER_JOINED,
                player=player.nick, team=self.world.getTeamName(msg.teamId))

    @RemovePlayerMsg.handler
    def handle_RemovePlayerMsg(self, msg):
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.new_message(LogMessage.PLAYER_LEFT, player=player.nick)
            self.subscribedPlayers.discard(player)

    def lostPlayer(self):
        if self.runningPlayerInterface:
            self.runningPlayerInterface.stop()
        self.runningPlayerInterface = None
        self.detailsInterface.setPlayer(None)
        self.setElements()

    @CannotBuyUpgradeMsg.handler
    def notEnoughCoins(self, msg):
        if msg.reasonId == NOT_ENOUGH_COINS_REASON:
            message = LogMessage.NOT_ENOUGH_COINS
        elif msg.reasonId == CANNOT_REACTIVATE_REASON:
            message = LogMessage.CANNOT_REACTIVATE
        elif msg.reasonId == PLAYER_DEAD_REASON:
            message = LogMessage.NO_UPGRADE_WHILE_DEAD
        elif msg.reasonId == GAME_NOT_STARTED_REASON:
            message = LogMessage.UPGRADES_DISABLED
        elif msg.reasonId == PLAYER_HAS_TROSBALL_REASON:
            message = LogMessage.TROSBALL_EXCLUDES_UPGRADES
        elif msg.reasonId == TOO_CLOSE_TO_EDGE_REASON:
            message = LogMessage.TOO_CLOSE_TO_EDGE
        elif msg.reasonId == TOO_CLOSE_TO_ORB_REASON:
            message = LogMessage.TOO_CLOSE_TO_ORB
        elif msg.reasonId == NOT_IN_DARK_ZONE_REASON:
            message = LogMessage.NOT_IN_DARK_ZONE
        elif msg.reasonId == INVALID_UPGRADE_REASON:
            message = LogMessage.UNRECOGNISED_UPGRADE
        elif msg.reasonId == DISABLED_UPGRADE_REASON:
            message = LogMessage.UPGRADE_DISABLED
        else:
            message = LogMessage.UPGRADE_UNAVAILABLE
        self.detailsInterface.new_message(message)
        self.defaultHandler(msg)

    @PlayerHasUpgradeMsg.handler
    def gotUpgrade(self, msg):
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.upgradeUsed(player, msg.upgradeType)
            upgradeClass = self.world.getUpgradeType(msg.upgradeType)
            existing = player.items.get(upgradeClass)
            if not existing:
                if (self.detailsInterface.player is None or
                        self.detailsInterface.player.isFriendsWith(player)):
                    self.play_sound('buyUpgrade')

        self.defaultHandler(msg)

    @ChatFromServerMsg.handler
    def gotChatFromServer(self, msg):
        self.detailsInterface.new_message(
            LogMessage.SERVER_CHAT, message=msg.text.decode('utf-8'))

    def orb_tagged(self, zone, player, previous_owner):
        zone_label = zone.defn.label

        if player is None:
            self.play_sound('orb-power-down', zone.orb_pos)
        else:
            nick = player.nick
            self.detailsInterface.new_message(LogMessage.CAPPED, player=nick, zone=zone_label)
            self.play_sound('orb-change' if previous_owner else 'orb-power-up', zone.orb_pos)

    def player_died(self, target, killer, death_type):
        if death_type == TROSBALL_DEATH_HIT:
            self.detailsInterface.new_message(LogMessage.TROSBALL_DEATH, player=target.nick)
        elif death_type == BOMBER_DEATH_HIT:
            self.detailsInterface.new_message(LogMessage.BOMBER_DEATH, player=target.nick)
            thisPlayer = self.detailsInterface.player
            if thisPlayer and target.id == thisPlayer.id:
                self.detailsInterface.doAction(ACTION_CLEAR_UPGRADE)
        else:
            self.play_sound('killed-by-shot', pos=target.pos)
            if killer is None:
                self.detailsInterface.new_message(LogMessage.PLAYER_DIED, target=target.nick)
            else:
                self.detailsInterface.new_message(
                    LogMessage.PLAYER_KILLED, killer=killer.nick, target=target.nick)

    @RespawnMsg.handler
    def playerRespawn(self, msg):
        if msg.phantom:
            if self.player and msg.playerId == self.player.id:
                self.detailsInterface.new_message(LogMessage.TEMPORAL_ANOMALY)
                self.gameViewer.worldgui.add_temporal_anomaly(self.player, self.localState.player)
            return
        player = self.world.getPlayer(msg.playerId)
        if player:
            self.detailsInterface.new_message(LogMessage.RESPAWNED, player=player.nick)

    @CannotRespawnMsg.handler
    def respawnFailed(self, msg):
        if msg.reasonId == GAME_NOT_STARTED_REASON:
            message = LogMessage.GAME_NOT_STARTED
        elif msg.reasonId == ALREADY_ALIVE_REASON:
            message = LogMessage.ALREADY_ALIVE
        elif msg.reasonId == BE_PATIENT_REASON:
            message = LogMessage.BE_PATIENT
        elif msg.reasonId == ENEMY_ZONE_REASON:
            message = LogMessage.MOVE_TO_FRIENDLY_ZONE
        elif msg.reasonId == FROZEN_ZONE_REASON:
            message = LogMessage.ZONE_FROZEN
        else:
            message = LogMessage.CANNOT_RESPAWN
        self.detailsInterface.new_message(message)

    def sendPrivateChat(self, player, targetId, text):
        self.sendRequest(ChatMsg(PRIVATE_CHAT, targetId, text=text.encode()))

    def sendTeamChat(self, player, text):
        self.sendRequest(
            ChatMsg(TEAM_CHAT, player.teamId, text=text.encode()))

    def sendPublicChat(self, player, text):
        self.sendRequest(ChatMsg(OPEN_CHAT, text=text.encode()))

    def openChat(self, text, sender):
        text = ': ' + text
        self.detailsInterface.newChat(text, sender)

    def teamChat(self, team, text, sender):
        player = self.detailsInterface.player
        if player and player.isFriendsWithTeam(team):
            text = ' (team): ' + text
            self.detailsInterface.newChat(text, sender)

    @AchievementUnlockedMsg.handler
    def achievementUnlocked(self, msg):
        self.recent_achievements.add(msg)
        player = self.world.getPlayer(msg.playerId)
        if not player:
            return

        achievementName = self.achievementDefs.getAchievementDetails(
            msg.achievementId)[0]
        self.detailsInterface.new_message(
            LogMessage.ACHIEVEMENT, player=player.nick, achievement=achievementName)

    @ShotFiredMsg.handler
    def shotFired(self, msg):
        self.defaultHandler(msg)
        try:
            shot = self.world.getShot(msg.shot_id)
        except KeyError:
            return

        self.play_sound(shot.gun_type.firing_sound, pos=shot.pos)

    def grenadeExploded(self, pos, radius):
        self.gameViewer.worldgui.addExplosion(pos)
        self.play_sound('explodeGrenade', pos=pos)

    def trosballExploded(self, player):
        self.gameViewer.worldgui.addTrosballExplosion(player.pos)
        self.play_sound('explodeGrenade', pos=player.pos)

    def bomber_exploded(self, player):
        self.gameViewer.worldgui.add_bomber_explosion(player)
        self.play_sound('bomber-explode', pos=player.pos)

    def shot_rebounded(self, pos):
        self.play_sound('shot-rebound', pos=pos)

    @FireShoxwaveMsg.handler
    def shoxwaveExplosion(self, msg):
        self.defaultHandler(msg)
        self.play_sound(Shoxwave.firing_sound, pos=(msg.xpos, msg.ypos))
        localPlayer = self.localState.player
        if localPlayer and msg.playerId == localPlayer.id:
            return
        self.gameViewer.worldgui.addShoxwaveExplosion((msg.xpos, msg.ypos))

    def localShoxwaveFired(self):
        localPlayer = self.localState.player
        self.gameViewer.worldgui.addShoxwaveExplosion(localPlayer.pos)

    def mine_exploded(self, pos):
        self.gameViewer.worldgui.add_mine_explosion(pos)
        self.play_sound('explodeGrenade', pos=pos)

    def play_sound(self, action, pos=None):
        self.app.soundPlayer.play(action, self.gameViewer.viewManager.getTargetPoint(), pos)

    @PlaySoundMsg.handler
    def playSoundFromServerCommand(self, msg):
        self.app.soundPlayer.playFromServerCommand(
            msg.filename.decode('utf-8'))

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        super(GameInterface, self).handle_TickMsg(msg)
        self.timing_info.seen_tick()

        looping_sound_positions = {}
        for shot in self.world.shots:
            if sound_name := shot.gun_type.looping_sound:
                looping_sound_positions.setdefault(sound_name, []).append(shot.pos)
        self.app.soundPlayer.set_looping_sound_positions(
            self.gameViewer.viewManager.getTargetPoint(), looping_sound_positions)

        if __debug__ and globaldebug.enabled:
            globaldebug.tick_logger.game_interface_saw_tick(msg.tickId)
            if globaldebug.debug_key_screenshots and globaldebug.debugKey:
                log.error('Saving screenshot info…')
                import pprint
                with open('screenshots.txt', 'a') as f:
                    try:
                        from trosnoth.tools.screenshots import get_screenshot_data
                        pprint.pprint(get_screenshot_data(self), f)
                    except Exception:
                        log.exception('Error saving screenshot info')

    @BuyAmmoMsg.handler
    def handle_BuyAmmoMsg(self, msg):
        if self.player and self.player.id == msg.player_id:
            self.detailsInterface.player_bought_ammo(msg.gun_type)

    @ScenarioCompleteMsg.handler
    def handle_ScenarioCompleteMsg(self, msg):
        self.end_screen = GameEndScreen(self.app, self)
        self.setElements()
        self.play_sound('game-over')
        self.defaultHandler(msg)

    def stats_screen_closed(self):
        result = self.end_screen.scenario_result
        self.end_screen.stop()
        self.end_screen = None
        self.setElements()
        self.on_scenario_complete(result)
        if self.connection_was_lost:
            self.on_clean_exit()


@dataclass(frozen=True)
class GameTipDisplay(ComplexDeclarativeThing):
    player: 'Player'

    def build_state(self, renderer):
        return {
            'count': 0,
        }

    def draw(self, frame, state):
        left_key = self.player.checkMotionKey(LEFT_STATE)
        right_key = self.player.checkMotionKey(RIGHT_STATE)
        left_key, right_key = left_key and not right_key, right_key and not left_key
        right_mouse = self.player.isFacingRight()

        if not self.player.world.paused:
            if self.player.dead:
                state['count'] = 0
            elif left_key and right_mouse or right_key and not right_mouse:
                state['count'] += frame.delta_t
            elif left_key or right_key:
                state['count'] = 0

            if self.player.guns.reload_time > 0:
                # Don't display the hint if you've been looking behind you to fire
                state['count'] = 0

        if state['count'] >= 3:
            x = -200 if right_mouse else 200
            frame.add(
                Rectangle(
                    width=300, height=60, colour=(255, 224, 192),
                    border=(255, 192, 128), border_width=1.5),
                alpha=0.8,
                at=(x, 0),
            )
            frame.add(
                Text(
                    'Watch where you’re going',
                    height=18,
                    font='FreeSans.ttf',
                    text_colour=(255, 192, 128),
                    shadow_offset=(1, 1),
                ),
                at=(x, -8),
            )
            frame.add(
                Text(
                    'You can move more quickly when you',
                    height=14,
                    font='FreeSans.ttf',
                    text_colour=(64, 64, 64),
                ),
                at=(x, 9),
            )
            frame.add(
                Text(
                    'are moving towards your mouse pointer',
                    height=14,
                    font='FreeSans.ttf',
                    text_colour=(64, 64, 64),
                ),
                at=(x, 26),
            )



class GameEndScreen(CompoundElement):
    def __init__(self, app, game_interface, wait_time=2, fade_time=3):
        super().__init__(app)
        self.game_interface = game_interface
        self.scenario_result = game_interface.world.scenario_result
        self.fully_showing = False
        self.fade_time = fade_time
        self.timeout = reactor.callLater(wait_time, self._wait_complete)
        self.elements = []

    def _wait_complete(self):
        self.timeout = reactor.callLater(self.fade_time, self._fade_complete)
        self.elements = [
            DeclarativeElement(self.app, (0, 0), FadeIn(
                duration=3,
                contents=StatisticsScreen(self),
            )),
        ]

    def _fade_complete(self):
        self.timeout = None
        self.fully_showing = True
        self.game_interface.setElements()

    def stop(self):
        self.game_interface = None
        if self.timeout:
            self.timeout.cancel()

    def draw(self, screen):
        if not self.active:
            return
        if self.fully_showing:
            pygame.draw.rect(screen, (255, 255, 255, 128), screen.get_rect())
        super().draw(screen)


@dataclass(frozen=True)
class StatisticsScreen(ComplexDeclarativeThing):
    end_screen: GameEndScreen

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        frame.add(StatsTables(self.end_screen))

        frame.add(Button(
            caption='done',
            pos=(438, 345),
            size=(100, 50),
            font='FreeSans.ttf',
            font_height=20,
            mouse_pos=frame.get_mouse_pos(),
            on_click=self.end_screen.game_interface.stats_screen_closed,
            background_colour=(192, 255, 192),
            hover_colour=(64, 192, 64),
        ))


@dataclass(frozen=True)
class StatsTables(ComplexDeclarativeThing):
    end_screen: GameEndScreen

    def draw(self, frame, state):
        scenario_result = self.end_screen.scenario_result
        stats = scenario_result.stats
        self.draw_title(frame, scenario_result.winning_teams, scenario_result.winning_players)

        y = -278
        y = self.draw_match_stats(frame, scenario_result.scenario_name, stats, y)
        if stats and stats.team_stats:
            y = self.draw_team_stats(frame, stats, y)
        if stats and stats.player_stats:
            self.draw_player_stats(frame, stats, y)

    def draw_title(self, frame, winning_teams, winning_players):
        if winning_teams:
            colour = winning_teams[0].shade(.5, .6)
            background_colour = winning_teams[0].shade(.3, 1)
            if len(winning_teams) == 1:
                message = f'Winner: {winning_teams[0].teamName}'
            else:
                message = f'Winners: {", ".join(t.teamName for t in winning_teams)}'
        elif winning_players:
            team = winning_players[0].team
            colour = team.shade(.5, .6) if team else (64, 64, 64)
            background_colour = team.shade(.3, 1) if team else (204, 204, 204)
            if len(winning_players) == 1:
                message = f'Winner: {winning_players[0].nick}'
            else:
                message = f'Winners: {", ".join(p.nick for p in winning_players)}'
        else:
            colour = (64, 64, 64)
            background_colour = (204, 204, 204)
            message = 'Game drawn'

        frame.add(FullScreenRectangle(colour=(255, 255, 255)))
        frame.add(Rectangle(
            width=976,
            height=60,
            colour=background_colour,
            border=colour,
            border_width=1,
        ), at=(0, -330))
        frame.add(Text(
            text=message,
            height=36,
            font='Junction.ttf',
            text_colour=colour,
            max_width=966,
        ), at=(0, -310))

    def draw_match_stats(self, frame, scenario_name, stats, y):
        def write_row(left_column, right_column):
            nonlocal y
            frame.add(Text(
                left_column,
                height=20,
                font='Junction.ttf',
                text_colour=(64, 64, 64),
                max_width=472,
                align=Text.A_right,
            ), at=(-16, y))
            frame.add(Text(
                right_column,
                height=20,
                font='FreeSans.ttf',
                text_colour=(128, 128, 128),
                max_width=472,
                align=Text.A_left
            ), at=(16, y))
            y += 28

        y += 28
        write_row('Scenario', scenario_name)
        for stat_name, stat_kind, value in stats.match_stats:
            write_row(stat_name, stat_kind.format(value))
        return y

    def draw_team_stats(self, frame, stats, y):
        titles, rows = FrozenLevelStats.sort_stats(
            stats.team_stats, self.end_screen.game_interface.world.teams)

        col_width = 976 / (1.5 + len(stats.team_stats))
        y += 28
        for i, stat_name in enumerate(titles):
            frame.add(Text(
                stat_name,
                height=20,
                font='Junction.ttf',
                text_colour=(64, 64, 64),
                max_width=col_width * .95,
            ), at=((i + 2) * col_width - 488, y))

        for team, team_stats in rows:
            y += 34
            frame.add(Text(
                team.teamName,
                height=26,
                text_colour=team.shade(.5, .5),
                max_width=2 * col_width,
                align=Text.A_left,
                font='Junction.ttf',
            ), at=(-488, y))
            for i, (value, formatted_value, is_best) in enumerate(team_stats):
                frame.add(Text(
                    formatted_value,
                    height=20,
                    text_colour=(64, 192, 64) if is_best else (128, 128, 128),
                    max_width=col_width * .95,
                    font='FreeSans.ttf',
                ), at=((i + 2) * col_width - 488, y))

        y += 34
        return y

    def draw_player_stats(self, frame, stats, y):
        titles, rows = FrozenLevelStats.sort_stats(stats.player_stats, stats.player_info)

        col_width = 976 / (1.5 + len(stats.player_stats))
        y += 28
        for i, stat_name in enumerate(titles):
            frame.add(Text(
                stat_name,
                height=20,
                font='Junction.ttf',
                text_colour=(64, 64, 64),
                max_width=col_width * .95,
            ), at=((i + 2) * col_width - 488, y))

        for p, player_stats in rows:
            y += 34
            colour = p.team.shade(.5, .5) if p.team else (128, 128, 128)
            frame.add(Text(
                p.nick,
                height=26,
                text_colour=colour,
                max_width=2 * col_width,
                align=Text.A_left,
                font='Junction.ttf',
            ), at=(-488, y))
            for i, (value, formatted_value, is_best) in enumerate(player_stats):
                frame.add(Text(
                    formatted_value,
                    height=20,
                    text_colour=(64, 192, 64) if is_best else (128, 128, 128),
                    max_width=col_width * .95,
                    font='FreeSans.ttf',
                ), at=((i + 2) * col_width - 488, y))


@dataclass(frozen=True)
class MaybeShowUpscaleMessage(ComplexDeclarativeThing):
    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        display = frame.app.settings.display
        if display.upscale:
            return
        if display.size[1] < display.max_viewport_height * 1.06:
            return
        frame.add(UpscaleMessage())


@dataclass(frozen=True)
class UpscaleMessage(ComplexDeclarativeThing):
    def draw(self, frame, state):
        frame.add(Rectangle(
            width=600,
            height=50,
            colour=(208, 200, 192, 192),
        ))
        frame.add(Text(
            'For a better experience on ultra high definition displays,',
            height=20,
            font='Junction.ttf',
            text_colour=(0, 0, 0),
            max_width=580,
            align=Text.A_center,
        ), at=(0, 0))
        frame.add(Text(
            'consider enabling up-scaling in display settings',
            height=20,
            font='Junction.ttf',
            text_colour=(0, 0, 0),
            max_width=580,
            align=Text.A_center,
        ), at=(0, 20))


@dataclass(frozen=True)
class JoinDisplay(ComplexDeclarativeThing):
    game_interface: GameInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if self.game_interface.joinController.join_game_dialog.showing:
            return
        frame.add(Rectangle(
            width=320,
            height=128,
            colour=(255, 255, 255),
        ), at=(160, -64))
        frame.add(Text(
            'You are spectating',
            height=24,
            font='Junction.ttf',
            text_colour=(64, 64, 64),
            max_width=300,
            align=Text.A_center,
        ), at=(160, -80))
        frame.add(Button(
            caption='Quit',
            pos=(80, -40),
            size=(100, 50),
            font='FreeSans.ttf',
            font_height=20,
            mouse_pos=frame.get_mouse_pos(),
            on_click=self.game_interface.disconnect,
            background_colour=(192, 255, 192),
            hover_colour=(64, 192, 64),
        ))
        frame.add(Button(
            caption='Join',
            pos=(240, -40),
            size=(100, 50),
            font='FreeSans.ttf',
            font_height=20,
            mouse_pos=frame.get_mouse_pos(),
            on_click=self.game_interface.spectatorWantsToJoin,
            background_colour=(192, 255, 192),
            hover_colour=(64, 192, 64),
        ))


class TimingInfo():
    def __init__(self):
        self.frames_seen = 0
        self.ticks_seen = 0
        self.time_passed = 0.

    def reset(self):
        self.frames_seen = 0
        self.ticks_seen = 0
        self.time_passed = 0.

    def seen_tick(self):
        self.ticks_seen += 1

    def seen_frame(self, delta_t):
        self.time_passed += delta_t
        self.frames_seen += 1


class TeamBoostTransactionTracker:
    def __init__(self, interface):
        self.coins = 0
        self.interface = interface
        self.boost_class = None

    def start_boost_purchase(self, boost_class):
        self.boost_class = boost_class
        if self.interface.player.team.boosts.get(boost_class):
            self.coins = 50
        else:
            self.coins = boost_class.deposit_cost
        self.constrain_coins()

    def contribute(self, delta):
        self.coins += delta
        self.constrain_coins()

    def constrain_coins(self):
        boost = self.interface.player.team.boosts.get(self.boost_class)
        if boost:
            remaining = boost.remaining_cost
        else:
            remaining = self.boost_class.total_cost
        self.coins = min(self.coins, self.interface.player.coins, remaining)

    def get_total_contributed_coins(self):
        boost = self.interface.player.team.boosts.get(self.boost_class)
        self.constrain_coins()
        if boost:
            progress = boost.total_cost - boost.remaining_cost + self.coins
        else:
            progress = self.coins
        return progress

    def get_boost_progress_ratio(self):
        return self.get_total_contributed_coins() / self.boost_class.total_cost

    def complete_purchase(self):
        coins = self.coins
        self.interface.please_contribute_to_team_boost(self.boost_class, round(coins))

        self.coins = 0
        self.boost_class = None


@dataclass(frozen=True)
class TimingDisplay(ComplexDeclarativeThing):
    interface: GameInterface
    info: TimingInfo

    def build_state(self, renderer):
        return {'fps': None, 'tps': None}

    def draw(self, frame, state):
        if not frame.app.settings.display.show_timings:
            return
        self.info.seen_frame(frame.delta_t)
        if self.info.time_passed > 3:
            state['fps'] = self.info.frames_seen / self.info.time_passed
            state['tps'] = self.info.ticks_seen / self.info.time_passed
            self.info.reset()

        frame.add(TimingPanel(
            fps=state['fps'],
            tps=state['tps'],
            ping=self.interface.localState.lastPingTime,
            smooth=self.interface.localState.slow_ping_time,
            jitter=self.interface.app.jitterLogger.jitter,
        ))


@dataclass(frozen=True)
class TimingPanel(ComplexDeclarativeThing):
    fps: Optional[float]
    tps: Optional[float]
    ping: Optional[float]
    smooth: Optional[float]
    jitter: Optional[float]

    def draw(self, frame, state):
        lines = []
        if self.fps is not None:
            lines.append(f'FPS: {self.fps:.1f}')
        if self.tps is not None:
            lines.append(f'TPS: {self.tps:.1f}')
        if self.ping is not None:
            lines.append(f'Ping: {round(1000 * self.ping)} ms')
        if self.smooth is not None:
            lines.append(f'Smooth: {round(1000 * self.smooth)} ms')
        if self.jitter is not None:
            lines.append(f'Jitter: {round(1000 * self.jitter)} ms')

        height = 10 * len(lines) + 6
        frame.add(
            Rectangle(
                width=84,
                height=height,
                colour=(255, 255, 255, 128),
            ),
            at=(0, -height / 2)
        )

        y = 4 - height
        for line in lines:
            y += 10
            frame.add(
                Text(
                    line,
                    height=10,
                    font='Junction.ttf',
                    text_colour=(0, 0, 0),
                    max_width=80,
                    align=Text.A_left,
                ),
                at=(-40, y),
            )


class GameInfoDisplay(CollapseBox):
    def __init__(self, app, gameInterface, region):
        colours = app.theme.colours
        fonts = app.screenManager.fonts
        self.interface = gameInterface
        super(GameInfoDisplay, self).__init__(
            app,
            region=region,
            titleFont=fonts.gameInfoTitleFont,
            font=fonts.gameInfoFont,
            titleColour=colours.gameInfoTitle,
            hvrColour=colours.gameInfoHover,
            colour=colours.gameInfoColour,
            backColour=colours.gameInfoBackColour,
            title='',
        )
        self.refreshInfo()

    def refreshInfo(self):
        localState = self.interface.localState
        self.setInfo(localState.userInfo, localState.userTitle)

    def get_screenshot_scenario(self):
        local_state = self.interface.localState
        user_info = list(local_state.userInfo)
        if self.hidden:
            user_info = []
        if (user_title := local_state.userTitle) or user_info:
            return [user_title] + user_info
        return []

    def restore_screenshot_scenario(self, data):
        local_state = self.interface.localState
        local_state.userTitle = data[0] if data else ''
        local_state.userInfo = tuple(data[1:])

        self.refreshInfo()
        self.hidden = not local_state.userInfo

        # Skip any resize animation and just jump to the intended size
        self.rect.height = self.targetRect.height
        self.updateElements()
