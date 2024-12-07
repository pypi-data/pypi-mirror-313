import functools
import logging
import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Callable

import pygame

from trosnoth.const import (
    MAP_TO_SCREEN_SCALE,
    ACTION_SETTINGS_MENU, ACTION_QUIT_MENU,
    ACTION_REALLY_QUIT, ACTION_PAUSE_GAME, ACTION_MAIN_MENU,
    ACTION_TERMINAL_TOGGLE, ACTION_FOLLOW, ACTION_RADIAL_UPGRADE_MENU, ACTION_USE_UPGRADE,
    ACTION_RESPAWN,
    ACTION_READY, ACTION_CLEAR_UPGRADE, ACTION_CHAT,
    ACTION_JUMP, ACTION_RIGHT, ACTION_LEFT, ACTION_DOWN,
    ACTION_HOOK, ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY, ACTION_EMOTE,
    MAX_EMOTE, ACTION_NEXT_WEAPON, ACTION_PREVIOUS_WEAPON, ACTION_BUY_AMMO, MOUSE_UP,
    ACTION_NEXT_TEAM_BOOST, KEY_UP, ACTION_CONTRIBUTE_TO_TEAM_BOOST, ACTION_TOGGLE_FULLSCREEN,
    ACTION_GUN_SLOTS,
)
from trosnoth.gui.app import get_pygame_runner
from trosnoth.gui.framework import framework
from trosnoth.gui.framework.declarative import (
    DeclarativeElement, Rectangle, Text, PygameSurface,
    Button, ComplexDeclarativeThing, Graphic,
)
from trosnoth.gui.common import (
    Location, FullScreenAttachedPoint, ScaledSize, Area,
)
from trosnoth.gui.keyboard import shortcutName
from trosnoth.messages import (
    RespawnRequestMsg, EmoteRequestMsg,
    PlayerIsReadyMsg, ThrowTrosballMsg,
)
from trosnoth.model.player import Player
from trosnoth.model.shot import (
    PredictedGhostShotTrajectory,
)
from trosnoth.model.trosball import PredictedTrosballTrajectory
from trosnoth.model.unit import PredictedTrajectory, PredictedProjectileTrajectory
from trosnoth.model.upgrades import (
    allUpgrades, gun_types, TeamBoost, GunType, SelectableShopItem, Upgrade,
)
from trosnoth.settings import ClientSettings
from trosnoth.trosnothgui.ingame.messagebank import FormattedMessageBank
from trosnoth.trosnothgui.ingame import mainMenu
from trosnoth.trosnothgui.ingame.gamevote import GameVoteMenu
from trosnoth.trosnothgui.ingame.gauges import (
    ItemCostGauge, GaugeAppearance, IconGauge, ReloadAmmoGauge,
)
from trosnoth.trosnothgui.ingame.chatBox import ChatBox
from trosnoth.trosnothgui.ingame.universegui import UniverseGUI
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen

from trosnoth.trosnothgui.ingame.upgradeinterface import RadialUpgradeMenu
from trosnoth.utils.aio import create_safe_task
from trosnoth.welcome.keygrab import hidden_qt_toplevels, KeyGrabberElement

log = logging.getLogger(__name__)


class LogMessage(Enum):
    GAME_PAUSED = 'Game paused'
    GAME_RESUMED = 'Game resumed'
    CANNOT_PAUSE = 'You can only pause games from the server', 'errorMessageColour'
    PROJECTILE_LAUNCHED = '{player} has launched a {upgrade}'
    UPGRADE_USED = '{player} is using a {upgrade}'
    NINJA_USED = '{player} has become a {upgrade}'
    ACHIEVEMENT = '{player} has achieved {achievement}', 'achievementMessageColour'
    PLAYER_JOINED = '{player} has joined {team}'
    PLAYER_LEFT = '{player} has left the game'
    ELEPHANT_GAINED = '{player} now has {elephant}'
    SERVER_CHAT = '{message}', 'errorMessageColour'
    TROSBALL_DROPPED = 'The ball has been dropped!'
    TROBSALL_GAINED = '{player} now has the ball!'
    NEW_JUGGERNAUT = '{player} is the new juggernaut'
    PLAYER_KILLED = '{killer} killed {target}'
    PLAYER_DIED = '{target} was killed'
    BOMBER_DEATH = '{player} head asplode'
    TROSBALL_DEATH = '{player} was killed by the Trosball'
    TEMPORAL_ANOMALY = 'You were unspawned in a temporal anomaly', 'errorMessageColour'
    RESPAWNED = '{player} is back in the game'
    CAPPED = '{player} captured zone {zone}'

    GAME_FULL = 'The game is full!', 'errorMessageColour'
    NICK_IN_USE = 'That name is already being used!', 'errorMessageColour'
    BAD_NICK = 'That name is not allowed!', 'errorMessageColour'
    UNAUTHORISED = 'You are not authorised to join this game!', 'errorMessageColour'
    ALREADY_JOINED = 'Cannot join the same game twice!', 'errorMessageColour'
    JOIN_FAILED = 'Join failed ({code})', 'errorMessageColour'

    NOT_ENOUGH_COINS = 'You do not have enough coins.', 'errorMessageColour'
    CANNOT_REACTIVATE = 'You already have that item.', 'errorMessageColour'
    NO_UPGRADE_WHILE_DEAD = 'You cannot buy an upgrade while dead.', 'errorMessageColour'
    UPGRADES_DISABLED = 'Upgrades can’t be bought at this time.', 'errorMessageColour'
    TROSBALL_EXCLUDES_UPGRADES = (
        'You cannot activate items while holding the Trosball.', 'errorMessageColour')
    TOO_CLOSE_TO_EDGE = 'You are too close to the zone edge.', 'errorMessageColour'
    TOO_CLOSE_TO_ORB = 'You are too close to the orb.', 'errorMessageColour'
    NOT_IN_DARK_ZONE = 'You are not in a dark friendly zone.', 'errorMessageColour'
    UNRECOGNISED_UPGRADE = 'Upgrade not recognised by server.', 'errorMessageColour'
    UPGRADE_DISABLED = 'That upgrade is currently disabled.', 'errorMessageColour'
    UPGRADE_UNAVAILABLE = 'You cannot buy that item at this time.', 'errorMessageColour'

    GAME_NOT_STARTED = 'The game has not started yet.', 'errorMessageColour'
    ALREADY_ALIVE = 'You are already alive.', 'errorMessageColour'
    BE_PATIENT = 'You cannot respawn yet.', 'errorMessageColour'
    MOVE_TO_FRIENDLY_ZONE = 'Cannot respawn outside friendly zone.', 'errorMessageColour'
    ZONE_FROZEN = 'That zone has been frozen!', 'errorMessageColour'
    CANNOT_RESPAWN = 'You cannot respawn here.', 'errorMessageColour'

    def __init__(self, message, colour_name='grey'):
        self.message = message
        self.colour_name = colour_name

    def format(self, *args, **kwargs):
        return self.message.format(*args, **kwargs)


class DetailsInterface(framework.CompoundElement):
    '''Interface containing all the overlays onto the screen:
    chat messages, player lists, gauges, coins, etc.'''
    def __init__(self, app, gameInterface):
        super(DetailsInterface, self).__init__(app)
        self.gameInterface = gameInterface
        self.settings_screen_task = None
        self.settings_screen = None
        self.cycle_team_boost = False
        self.team_boost_contributor = TeamBoostContributor(gameInterface.current_boost_purchase)

        # Maximum number of messages viewable at any one time
        maxView = 10

        self.world = gameInterface.world
        self.player = None
        font = app.screenManager.fonts.messageFont
        self.message_log = FormattedMessageBank(
            self.app, maxView, 60,
            Location(FullScreenAttachedPoint(ScaledSize(-40, -40), 'bottomright'), 'bottomright'),
            'right', 'bottom', font,
            record_kind=LogMessage,
        )

        self.currentUpgrade = None

        self.chatBox = ChatBox(app, self.world, self.gameInterface)

        menuloc = Location(FullScreenAttachedPoint((0,0), 'bottomleft'),
                'bottomleft')
        self.menuManager = mainMenu.MainMenu(self.app, menuloc, self,
                self.gameInterface.keyMapping)
        self.trajectoryOverlay = TrajectoryOverlay(app, gameInterface.gameViewer.viewManager, self)
        self.radialUpgradeMenu = RadialUpgradeMenu(app, self.player, self.set_current_upgrade)
        self.radialUpgradeMenu.start()
        self.gameVoteMenu = GameVoteMenu(app, self.world, on_change=self._castGameVote)
        self._gameVoteUpdateCounter = 0
        self.elements = [
            self.message_log,
            DeclarativeElement(app, (0, -1), UpgradePanel(self)),
            self.gameVoteMenu, self.chatBox,
            self.trajectoryOverlay, self.menuManager,
            DeclarativeElement(app, (0, 1), BottomPanel(self)),
            self.radialUpgradeMenu,
        ]

        self.upgradeMap = dict((upgradeClass.action, upgradeClass) for
                upgradeClass in allUpgrades)
        self.gun_map = {gun_type.action: gun_type for gun_type in gun_types}

    def stop(self):
        self.radialUpgradeMenu.stop()
        self.elements = []

    def sendRequest(self, msg):
        return self.gameInterface.sendRequest(msg)

    def tick(self, delta_t):
        super(DetailsInterface, self).tick(delta_t)

        self._updateGameVoteMenu()
        self.team_boost_contributor.tick(delta_t)

    def _castGameVote(self, msg):
        self.sendRequest(msg)

    def _updateGameVoteMenu(self):
        show_vote_menu = self.world.uiOptions.showReadyStates and self.player is not None
        self.gameVoteMenu.set_active(show_vote_menu)
        self.gameInterface.gameInfoDisplay.set_active(not show_vote_menu)

        if show_vote_menu:
            if self._gameVoteUpdateCounter <= 0:
                self.gameVoteMenu.update(self.player)
                self._gameVoteUpdateCounter = 25
            else:
                self._gameVoteUpdateCounter -= 1

    def setPlayer(self, player):
        if self.player is not None:
            self.player.onPrivateChatReceived.removeListener(self.privateChat)

        self.player = player
        if player:
            self.player.onPrivateChatReceived.addListener(self.privateChat)

        self.radialUpgradeMenu.set_player(player)

    def show_settings(self):
        from trosnoth.welcome.settings import SettingsScreen
        if self.settings_screen_task and not self.settings_screen_task.done():
            self.settings_screen.raise_to_top()
            return
        self.settings_screen = SettingsScreen(self.grab_hotkey)
        self.settings_screen_task = create_safe_task(self._show_settings_then_update_key_map())

    async def _show_settings_then_update_key_map(self):
        try:
            await self.settings_screen.run()
        finally:
            self.gameInterface.updateKeyMapping()

    async def grab_hotkey(self, parent_window, prompt, title=None):
        with hidden_qt_toplevels():
            return await KeyGrabberElement(self.app, prompt).show()

    def set_current_upgrade(self, upgradeType):
        self.currentUpgrade = upgradeType

    def _requestUpgrade(self):
        if self.player.hasTrosball():
            self.sendRequest(ThrowTrosballMsg())
        elif self.currentUpgrade is not None and self.currentUpgrade.is_buyable(self.player):
            self.currentUpgrade.please_use(self.player)

    def doAction(self, action):
        '''
        Activated by hotkey or menu.
        action corresponds to the action name in the keyMapping.
        '''
        if action == ACTION_SETTINGS_MENU:
            self.show_settings()
        elif action == ACTION_QUIT_MENU:
            self.menuManager.showQuitMenu()
        elif action == ACTION_REALLY_QUIT:
            # Disconnect from the server.
            self.gameInterface.disconnect()
        elif action == ACTION_TOGGLE_FULLSCREEN:
            settings = ClientSettings.get()
            settings.display.full_screen = not settings.display.full_screen
            settings.save()
            get_pygame_runner().resize_window(*settings.display.get_video_parameters())
        elif action == ACTION_PAUSE_GAME:
            if self.world.isServer:
                self.world.pauseOrResumeGame()
                if self.world.paused:
                    self.new_message(LogMessage.GAME_PAUSED)
                else:
                    self.new_message(LogMessage.GAME_RESUMED)
            else:
                self.new_message(LogMessage.CANNOT_PAUSE)
        elif action == ACTION_MAIN_MENU:
            # Return to main menu and show or hide the menu.
            self.menuManager.escape()
        elif action == ACTION_TERMINAL_TOGGLE:
            self.gameInterface.toggleTerminal()
        elif self.gameInterface.is_spectating():
            # Replay-specific actions
            if action in (ACTION_FOLLOW, ACTION_USE_UPGRADE):
                # Follow the game action
                self.gameInterface.gameViewer.setTarget(None)
        else:
            # All actions after this line should require a player.
            if self.player is None:
                return

            paused = self.world.paused
            if action == ACTION_RESPAWN:
                if not paused:
                    self.sendRequest(RespawnRequestMsg())
            elif action == ACTION_READY:
                if self.player.readyToStart:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, False))
                else:
                    self._castGameVote(PlayerIsReadyMsg(self.player.id, True))
            elif action in self.upgradeMap:
                self.set_current_upgrade(self.upgradeMap[action])
            elif action == ACTION_CLEAR_UPGRADE:
                self.set_current_upgrade(None)
                self.menuManager.manager.reset()
            elif action in ACTION_GUN_SLOTS:
                index = ACTION_GUN_SLOTS.index(action)
                guns = list(self.player.guns)
                if index < len(guns):
                    self.player.guns.please_select(guns[index])
            elif action in self.gun_map:
                gun_type = self.gun_map[action]
                gun = self.player.guns.get(gun_type)
                cost = gun.get_required_coins(self.player)
                if gun.ammo > 0 or gun.max_ammo == 0:
                    self.player.guns.please_select(gun)
                else:
                    self.set_current_upgrade(gun_type)
            elif action == ACTION_CHAT:
                self.chat()
                self.menuManager.manager.reset()
            elif action == ACTION_USE_UPGRADE:
                if not paused:
                    self._requestUpgrade()
            elif action == ACTION_BUY_AMMO:
                self.player.current_gun.please_buy_ammo()
            elif action == ACTION_EMOTE:
                self.sendRequest(EmoteRequestMsg(emoteId=random.randrange(MAX_EMOTE + 1)))
            elif action == ACTION_RADIAL_UPGRADE_MENU:
                self.radialUpgradeMenu.toggle()
            elif action == ACTION_NEXT_WEAPON:
                self.player.guns.scroll_selection(1)
            elif action == ACTION_PREVIOUS_WEAPON:
                self.player.guns.scroll_selection(-1)
            elif action == ACTION_NEXT_TEAM_BOOST:
                self.cycle_team_boost = True
            elif action == ACTION_CONTRIBUTE_TO_TEAM_BOOST:
                self.team_boost_contributor.start()
            elif action == ACTION_CONTRIBUTE_TO_TEAM_BOOST + KEY_UP:
                self.team_boost_contributor.stop()
            elif action.endswith(KEY_UP):
                pass
            elif action not in (
                    ACTION_JUMP, ACTION_RIGHT, ACTION_LEFT, ACTION_DOWN,
                    ACTION_HOOK, ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY):
                log.warning('Unknown action: %r', action)

    def new_message(self, log_message, **kwargs):
        self.message_log.newMessage(log_message, **kwargs)

    def privateChat(self, text, sender):
        # Destined for the one player
        text = " (private): " + text
        self.newChat(text, sender)

    def newChat(self, text, sender: Optional[Player]):
        if sender is None:
            self.chatBox.newServerMessage(text)
        else:
            colour = sender.team.shade(0.5, 1) if sender.team else (192, 192, 192)
            self.chatBox.newMessage(text, sender.nick, colour)

    def chat(self):
        if not self.player:
            return

        if self.chatBox.isOpen():
            self.chatBox.close()
        else:
            pygame.key.set_repeat(300, 30)
            self.chatBox.open()
            self.chatBox.setPlayer(self.player)

    def upgradeUsed(self, player, upgradeCode):
        upgradeClass = player.world.getUpgradeType(upgradeCode)
        message = upgradeClass.getActivateNotification(player.nick)

        self.new_message(message, player=player.nick, upgrade=upgradeClass.name)

    def player_bought_ammo(self, gun_type):
        if gun_type == self.currentUpgrade:
            self.set_current_upgrade(None)


def arrange_horizontal_elements(frame, children, y=0):
    x_offset = 80
    x = -0.5 * (len(children) - 1) * x_offset
    for child in children:
        frame.add(child, at=(x, y))
        x += x_offset


@dataclass(frozen=True)
class InProgressUpgradeDisplay(ComplexDeclarativeThing):
    player: Player
    world_gui: UniverseGUI

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        items = sorted(self.player.items.getAll(), key=lambda i: (i.sort_order, i.upgradeType))
        children = [SingleActiveUpgradeDisplay(i, self.player, self.world_gui) for i in items]
        arrange_horizontal_elements(frame, children)


@dataclass(frozen=True)
class InProgressTeamBoostsDisplay(ComplexDeclarativeThing):
    player: Player
    world_gui: UniverseGUI

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if self.player.team is None:
            return
        boosts = sorted(
            self.player.team.boosts.get_active(), key=lambda b: (b.sort_order, b.boost_code))
        children = [SingleActiveTeamBoostDisplay(i, self.world_gui) for i in boosts]
        arrange_horizontal_elements(frame, children)


@dataclass(frozen=True)
class SingleActiveUpgradeDisplay(ComplexDeclarativeThing):
    upgrade: Upgrade
    player: Player
    world_gui: UniverseGUI

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        colours = frame.app.theme.colours

        if self.upgrade.totalTimeLimit == 0:
            ratio = 1
        else:
            tick_portion = self.world_gui.get_tick_portion(player=self.player)
            time_remaining = self.upgrade.timeRemaining - tick_portion
            ratio = time_remaining / self.upgrade.totalTimeLimit

        frame.add(
            IconGauge(
                icon=type(self.upgrade).get_icon(frame.app.theme.sprites),
                size=(40, 10),
                ratio=ratio,
                foreground=colours.gaugeGood,
                border_width=0.5,
            )
        )


@dataclass(frozen=True)
class SingleActiveTeamBoostDisplay(ComplexDeclarativeThing):
    boost: TeamBoost
    world_gui: UniverseGUI

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        colours = frame.app.theme.colours

        if self.boost.time_limit == 0:
            ratio = 1
        else:
            remaining = self.boost.time_remaining - self.world_gui.get_tick_portion()
            ratio = remaining / self.boost.time_limit

        frame.add(
            IconGauge(
                icon=type(self.boost).get_icon(frame.app.theme.sprites),
                size=(40, 10),
                ratio=ratio,
                foreground=colours.gaugeGood,
                border_width=0.5,
            )
        )


@dataclass(frozen=True)
class BottomPanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if not (player := self.details_interface.player):
            return
        world_gui = self.details_interface.gameInterface.gameViewer.worldgui
        if player.dead:
            frame.add(RespawnGaugeDisplay(player, world_gui=world_gui), at=(0, -75))
        else:
            frame.add(GunReloadDisplay(player, world_gui=world_gui), at=(0, -75))
        frame.add(GunsPanel(self.details_interface))


@dataclass(frozen=True)
class RespawnGaugeDisplay(ComplexDeclarativeThing):
    player: Player
    world_gui: UniverseGUI

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        time_till_respawn = self.player.timeTillRespawn - self.world_gui.get_tick_portion(
            self.player)
        frame.add(IconGauge(
            icon=frame.app.theme.sprites.ghostIcon(self.player.team).getImage(),
            size=(100, 30),
            ratio=(ratio := 1 - (time_till_respawn / self.player.total_respawn_time)),
            foreground=colours.gaugeGood if ratio >= 1 else colours.gaugeBad,
            border_width=1.5,
        ))


@dataclass(frozen=True)
class GunReloadDisplay(ComplexDeclarativeThing):
    player: Player
    world_gui: UniverseGUI

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        player = self.player
        tick_portion = self.world_gui.get_tick_portion(player)
        override = player.current_gun.get_reload_ratio_and_colour(
            frame.app.theme.colours, tick_portion)
        reload_time = player.guns.reload_time - tick_portion
        if override is not None:
            ratio, colour = override
        elif reload_time > 0:
            ratio = 1 - reload_time / player.guns.reload_from
            colour = colours.gaugeBad
        else:
            ratio = 1
            colour = colours.gaugeGood
        frame.add(IconGauge(
            icon=frame.app.theme.sprites.gunIcon.getImage(),
            size=(100, 30),
            ratio=ratio,
            foreground=colour,
            border_width=1.5,
        ))


@dataclass(frozen=True)
class GunsPanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        gun_slots = []
        for i, gun in enumerate(self.details_interface.player.guns):
            gun_slots.append(GunSlot(self.details_interface, gun, i))

        arrange_horizontal_elements(frame, gun_slots, y=-20)


@dataclass(frozen=True)
class GunSlot(ComplexDeclarativeThing):
    details_interface: DetailsInterface
    gun: GunType
    slot_index: int

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if self.slot_index < len(ACTION_GUN_SLOTS):
            try:
                slot_key = self.details_interface.gameInterface.keyMapping.getkey(
                    ACTION_GUN_SLOTS[self.slot_index])
            except KeyError:
                hotkey_name = ''
            else:
                hotkey_name = shortcutName(slot_key)
        else:
            hotkey_name = ''

        frame.add(GunSlotAppearance(
            gun_type=type(self.gun),
            hotkey_name=hotkey_name,
            ammo_ratio=1 if self.gun.max_ammo == 0 else self.gun.ammo / self.gun.max_ammo,
            selected=self.details_interface.player.guns.selected == self.gun,
        ))


@dataclass(frozen=True)
class GunSlotAppearance(ComplexDeclarativeThing):
    gun_type: Type[GunType]
    hotkey_name: str
    ammo_ratio: float
    selected: bool

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        if self.selected:
            background = colours.gun_panel_selected_background
        else:
            background = colours.gun_panel_background
        frame.add(
            Rectangle(
                80, 40,
                colour=background,
                border_width=1, border=colours.gun_panel_border,
            ),
        )

        frame.add(
            Graphic(f'sprites/{self.gun_type.icon_path}', width=40, height=40),
            at=(-20, 0),
            alpha=0.9,
        )

        frame.add(
            GaugeAppearance(
                size=(42, 10),
                ratio=self.ammo_ratio,
                border_width=0.5,
                foreground=colours.gauge_ammo,
            ),
            at=(17, -5),
        )

        frame.add(
            Text(
                self.gun_type.name,
                height=12,
                max_width=60,
                font='FreeSans.ttf',
                text_colour=colours.gun_text,
                shadow_colour=colours.gun_text_shadow,
                shadow_offset=(0.5, 0.5),
                truncate=True,
            ),
            at=(10, 14),
        )

        if self.hotkey_name:
            frame.add(
                Text(
                    self.hotkey_name,
                    height=20,
                    max_width=30,
                    font='FreeSans.ttf',
                    text_colour=colours.gun_text,
                    shadow_colour=colours.gun_text_shadow,
                    shadow_offset=(1, 1),
                ),
                at=(-35, 0),
            )


@dataclass(frozen=True)
class UpgradePanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        if not (player := self.details_interface.player):
            return
        world_gui = self.details_interface.gameInterface.gameViewer.worldgui
        frame.add(MoneyDisplayPanel(self.details_interface), at=(-219, 0))
        frame.add(UpgradeDisplayPanel(self.details_interface), at=(-144, 0))
        frame.add(RefillAmmoPanel(self.details_interface), at=(-90, 0))
        frame.add(InProgressUpgradeDisplay(player, world_gui), at=(-132, 110))
        if player.team:
            pending_boosts = any(player.team.boosts.get_pending())
            if pending_boosts:
                frame.add(TeamBoostPurchasePanel(self.details_interface), at=(141, 0))
            frame.add(
                InProgressTeamBoostsDisplay(player, world_gui),
                at=(153, 110 if pending_boosts else 30))


@dataclass(frozen=True)
class MoneyDisplayPanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {'coins': 0}

    def draw(self, frame, state):
        target_coins = self.details_interface.player.coins
        diff = target_coins - state['coins']
        if diff > 0:
            diff = round(max(0.1 * diff, min(diff, 500 * frame.delta_t)))
        elif diff < 0:
            diff = round(min(0.1 * diff, max(diff, -500 * frame.delta_t)))
        state['coins'] += diff
        coins = state['coins']
        coins -= round(self.details_interface.gameInterface.current_boost_purchase.coins)

        colours = frame.app.theme.colours
        frame.add(
            Rectangle(
                90, 82,
                colour=colours.upgrade_panel_background,
                border_width=1, border=colours.upgrade_panel_border,
            ),
            at=(0, 41),
        )
        frame.add(
            Text(
                f'${coins:,}'.replace(',', '\N{hair space}'),
                height=30,
                max_width=70,
                font='FreeSans.ttf',
                text_colour=frame.app.theme.colours.coinsDisplayColour,
                shadow_offset=(1, 1),
            ),
            at=(0, 40),
        )

        try:
            shop_key = self.details_interface.gameInterface.keyMapping.getkey(
                ACTION_RADIAL_UPGRADE_MENU)
        except KeyError:
            subcaption = None
        else:
            subcaption = f'({shortcutName(shop_key)})'

        frame.add(
            Button(
                'SHOP',
                subcaption=subcaption,
                pos=(0, 65),
                size=(86, 29),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                on_click=self.details_interface.radialUpgradeMenu.toggle,
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=frame.app.settings.display.disable_shop_buttons,
            ),
        )


@dataclass(frozen=True)
class IconWithButton(ComplexDeclarativeThing):
    details_interface: DetailsInterface
    icon: Optional[pygame.Surface]
    button_text: str
    action: str
    button_disabled: bool

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        frame.add(
            Rectangle(
                48, 82,
                colour=colours.upgrade_panel_background,
                border_width=1, border=colours.upgrade_panel_border,
            ),
            at=(0, 41),
        )
        if self.icon:
            frame.add(
                PygameSurface(self.icon, width=38, height=38),
                at=(0, 20),
            )

        try:
            use_key = self.details_interface.gameInterface.keyMapping.getkey(self.action)
        except KeyError:
            subcaption = None
        else:
            subcaption = f'({shortcutName(use_key)})'

        button_disabled = self.button_disabled or frame.app.settings.display.disable_shop_buttons
        frame.add(
            Button(
                self.button_text,
                subcaption=subcaption,
                pos=(0, 65),
                size=(44, 29),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                on_click=functools.partial(self.details_interface.doAction, self.action),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=button_disabled,
            ),
        )


@dataclass(frozen=True)
class UpgradeDisplayPanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        player = self.details_interface.player
        upgrade = self.details_interface.currentUpgrade

        if player.hasTrosball():
            image = frame.app.theme.sprites.trosball_image()
            use_text = 'THROW'
            show_gauge = False
            button_disabled = False
        elif upgrade:
            image = upgrade.get_icon(frame.app.theme.sprites)
            use_text = upgrade.get_use_text(player)
            show_gauge = True
            button_disabled = not upgrade.is_buyable(player)
        else:
            image = None
            use_text = 'BUY'
            show_gauge = False
            button_disabled = True

        frame.add(IconWithButton(
            details_interface=self.details_interface,
            icon=image,
            button_text=use_text,
            action=ACTION_USE_UPGRADE,
            button_disabled=button_disabled,
        ))
        if show_gauge:
            frame.add(
                ItemCostGauge(
                    player=self.details_interface.player,
                    upgrade=upgrade,
                    size=(44, 8),
                ),
                at=(0, 45),
            )


@dataclass(frozen=True)
class RefillAmmoPanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {}

    def draw(self, frame, state):
        player = self.details_interface.player
        if player.current_gun.max_ammo > 0:
            image = player.current_gun.get_icon(frame.app.theme.sprites)
            gun = player.current_gun
        else:
            image = None
            gun = None

        frame.add(IconWithButton(
            details_interface=self.details_interface,
            icon=image,
            button_text='RELOAD',
            action=ACTION_BUY_AMMO,
            button_disabled=not player.current_gun.is_buyable(player),
        ))
        if gun:
            frame.add(
                ReloadAmmoGauge(
                    player=self.details_interface.player,
                    gun=gun,
                    size=(44, 8),
                ),
                at=(0, 45),
            )


class TeamBoostContributor:
    def __init__(self, tracker):
        self.tracker = tracker
        self.running = False
        self.boost_class = None

    def switch(self, boost_class):
        if boost_class == self.boost_class:
            return
        self.stop()
        self.boost_class = boost_class

    def start(self, boost_class=None):
        self.stop()
        if boost_class is not None:
            self.boost_class = boost_class
        if self.boost_class is not None:
            self.running = True
            self.tracker.start_boost_purchase(self.boost_class)

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.boost_class == self.tracker.boost_class:
            self.tracker.complete_purchase()

    def is_active(self):
        if not self.running:
            return False
        return self.boost_class == self.tracker.boost_class

    def tick(self, delta_t):
        if self.is_active():
            self.tracker.contribute(500 * delta_t)
            if self.tracker.get_boost_progress_ratio() >= 1:
                self.stop()


@dataclass(frozen=True)
class TeamBoostPurchasePanel(ComplexDeclarativeThing):
    details_interface: DetailsInterface

    def build_state(self, renderer):
        return {'order': [], 'current': 0}

    def draw(self, frame, state):
        if self.details_interface.cycle_team_boost:
            self.next_clicked(state)
            self.details_interface.cycle_team_boost = False

        new_order = []
        selected_index = 0
        if self.details_interface.player.team is None:
            pending = set()
        else:
            pending = {type(b) for b in self.details_interface.player.team.boosts.get_pending()}

            new_i = 0
            for i, boost_class in enumerate(state['order']):
                if boost_class in pending:
                    pending.remove(boost_class)
                    new_order.append(boost_class)
                    if i == state['current']:
                        selected_index = new_i
                    new_i += 1

        contributor = self.details_interface.team_boost_contributor
        if pending and not contributor.is_active():
            # Select the new upgrade
            selected_index = len(new_order)
        state['order'] = new_order + list(pending)
        state['current'] = selected_index
        if not state['order']:
            contributor.switch(None)
            return
        contributor.switch(state['order'][state['current']])

        boost_class = state['order'][selected_index]

        if contributor.is_active():
            coins = contributor.tracker.get_total_contributed_coins()
        else:
            boost = self.details_interface.player.team.boosts.get(boost_class)
            coins = boost.total_cost - boost.remaining_cost

        try:
            contribute_key = self.details_interface.gameInterface.keyMapping.getkey(
                ACTION_CONTRIBUTE_TO_TEAM_BOOST)
        except KeyError:
            contribute_key_name = None
        else:
            contribute_key_name = shortcutName(contribute_key)
        frame.add(TeamBoostPurchaseAppearance(
            boost_class=boost_class,
            index=selected_index + 1,
            count=len(state['order']),
            coins=coins,
            button_disabled=frame.app.settings.display.disable_shop_buttons,
            contribute_key=contribute_key_name,
            on_contribute_click=functools.partial(self.contribute_clicked, state),
            on_next_click=functools.partial(self.next_clicked, state),
            on_prev_click=functools.partial(self.prev_clicked, state),
        ))
        frame.register_listener(MOUSE_UP, self.seen_mouse_up)

    def contribute_clicked(self, state):
        self.details_interface.team_boost_contributor.start(state['order'][state['current']])

    def seen_mouse_up(self, state, pos, button):
        contributor = self.details_interface.team_boost_contributor
        if button == 1 and contributor.running:
            contributor.stop()
            return True
        return False

    def next_clicked(self, state):
        if not state['order']:
            return
        state['current'] += 1
        state['current'] %= len(state['order'])
        self.details_interface.team_boost_contributor.switch(state['order'][state['current']])

    def prev_clicked(self, state):
        if not state['order']:
            return
        state['current'] -= 1
        state['current'] %= len(state['order'])
        self.details_interface.team_boost_contributor.switch(state['order'][state['current']])


@dataclass(frozen=True)
class TeamBoostPurchaseAppearance(ComplexDeclarativeThing):
    boost_class: Type[TeamBoost]
    index: int
    count: int
    coins: float
    button_disabled: bool
    contribute_key: str
    on_next_click: Callable
    on_prev_click: Callable
    on_contribute_click: Callable

    def draw(self, frame, state):
        colours = frame.app.theme.colours
        frame.add(
            Rectangle(
                150, 82,
                colour=colours.upgrade_panel_background,
                border_width=1, border=colours.upgrade_panel_border,
            ),
            at=(0, 41),
        )
        extra_text = f' ({self.index}/{self.count})' if self.count > 1 else ''
        frame.add(
            Text(
                text=f'BUYING TEAM BOOST{extra_text}',
                height=9,
                font='FreeSans.ttf',
                max_width=140,
                text_colour=(0, 0, 0),
                shadow_offset=(1, 1),
                shadow_colour=(225, 225, 225),
            ),
            at=(0, 13),
        )
        frame.add(
            Text(
                text=self.boost_class.name,
                height=15,
                font='FreeSans.ttf',
                max_width=140,
                text_colour=(0, 0, 0),
                shadow_offset=(1, 1),
                shadow_colour=(240, 240, 240),
            ),
            at=(0, 28),
        )
        image = self.boost_class.get_icon(frame.app.theme.sprites)
        frame.add(
            PygameSurface(image, width=34, height=34),
            at=(-59, 45),
        )
        frame.add(
            GaugeAppearance(
                size=(114, 20),
                ratio=self.coins / self.boost_class.total_cost,
                foreground=colours.gaugeGood,
                border_width=1,
            ),
            at=(15, 45),
        )

        frame.add(
            Button(
                'Contribute' + f' ({self.contribute_key})' if self.contribute_key else '',
                pos=(0, 71),
                size=(106, 18),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=self.button_disabled,
                on_click=self.on_contribute_click,
            ),
        )
        frame.add(
            Button(
                '«',
                pos=(-64, 71),
                size=(18, 18),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=self.count <= 1,
                on_click=self.on_next_click,
            ),
        )
        frame.add(
            Button(
                '»',
                pos=(64, 71),
                size=(18, 18),
                font='FreeSans.ttf',
                font_height=14,
                mouse_pos=frame.get_mouse_pos(),
                background_colour=colours.upgrade_panel_button,
                disabled_background=colours.upgrade_panel_disabled,
                disabled_text=colours.upgrade_panel_border,
                disabled=self.count <= 1,
                on_click=self.on_prev_click,
            ),
        )


class TrajectoryOverlay(framework.Element):
    def __init__(self, app, viewManager, details_interface):
        super(TrajectoryOverlay, self).__init__(app)
        self.viewManager = viewManager
        self.details_interface = details_interface
        self.enabled = False

    def setEnabled(self, enable):
        self.enabled = enable

    def isActive(self):
        return self.getTrajectory() is not None

    def getTrajectory(self) -> Optional[PredictedTrajectory]:
        if not self.enabled:
            return None

        player = self.viewManager.getTargetPlayer()
        if player.dead:
            if not player.inRespawnableZone():
                return None
            return PredictedGhostShotTrajectory(
                player.world, player, self.viewManager)

        if player.hasTrosball():
            return PredictedTrosballTrajectory(player.world, player)

        selected_upgrade = self.details_interface.currentUpgrade
        if selected_upgrade and selected_upgrade.projectile_kind:
            required_coins = selected_upgrade.get_required_coins(player)
            if required_coins is not None and player.coins >= required_coins:
                return PredictedProjectileTrajectory(player, selected_upgrade.projectile_kind)

        return player.current_gun.build_trajectory(player)

    def draw(self, surface):
        trajectory = self.getTrajectory()
        if trajectory is None:
            return

        focus = self.viewManager._focus
        area = self.viewManager.sRect

        points = list(trajectory.predictedTrajectoryPoints())
        numPoints = len(points)
        if numPoints == 0:
            return
        greenToYellow = [(i, 255, 0) for i in range(
            0, 255, 255 // (numPoints // 2 + numPoints % 2))]
        yellowToRed = [(255, i, 0) for i in range(
            255, 0, -255 // (numPoints // 2))]

        colours = [(0, 255, 0)] + greenToYellow + yellowToRed

        lastPoint = None
        for item in zip(points, colours):
            point = item[0]
            colour = item[1]
            # Set first point
            if lastPoint is None:
                lastPoint = point
                adjustedPoint = mapPosToScreen(point, focus, area)
                pygame.draw.circle(surface, colour, adjustedPoint, 2)
                continue


            adjustedPoint = mapPosToScreen(point, focus, area)
            adjustedLastPoint = mapPosToScreen(lastPoint, focus, area)

            pygame.draw.line(surface, colour, adjustedLastPoint, adjustedPoint, 5)

            lastPoint = point

        # noinspection PyUnboundLocalVariable
        pygame.draw.circle(surface, colour, adjustedPoint, 2)

        radius = int(trajectory.explosionRadius() * MAP_TO_SCREEN_SCALE)
        if radius > 0:
            pygame.draw.circle(surface, (0,0,0), adjustedPoint, radius, 2)
