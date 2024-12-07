import logging
import random

from trosnoth.gui.framework.menu import MenuDisplay
from trosnoth.gui.menu.menu import MenuManager, Menu, MenuItem
from trosnoth.gui.common import Abs, Location, Region, Canvas
from trosnoth.gui.framework.dialogbox import (
    DialogBox, DialogResult,
)
from trosnoth.gui.framework.elements import (
    TextButton, SolidRect, TextElement, OptionButtons,
)
from trosnoth.gui.framework.framework import CompoundElement
from trosnoth.gui.framework.prompt import InputBox, intValidator
from trosnoth.levels.registry import scenario_options
from trosnoth.messages import (
    PlayerIsReadyMsg, SetSuggestedTeamNameMsg, SetSuggestedDurationMsg,
    SetSuggestedMapMsg, SetSuggestedScenarioMsg, ChangeNicknameMsg, ChangeHeadMsg, ChangeTeamMsg,
)
from trosnoth.trosnothgui.ingame.dialogs import HeadSelector
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)

Y_PADDING = 10
X_PADDING = 20
BACKGROUND_COLOUR = (255, 255, 255)


class GameVoteMenu(CompoundElement):
    def __init__(self, app, world, on_change=None):
        super().__init__(app)
        self.world = world
        self.player = None
        self.last_config_info = (False, False, False)

        self.on_change = Event()
        if on_change is not None:
            self.on_change.addListener(on_change)

        main_font = app.screenManager.fonts.gameMenuFont
        label_font = app.screenManager.fonts.leaderboardFont
        input_font = app.screenManager.fonts.gameMenuFont
        menu_font = app.screenManager.fonts.game_options_font
        colours = app.theme.colours

        self.ready_options = OptionButtons(
            app,
            ['Ready', 'Not ready'],
            (2 * X_PADDING, 2 * Y_PADDING),
            colours.in_game_button_foreground, BACKGROUND_COLOUR, colours.in_game_button_hover,
            colours.in_game_selection_background,
            main_font, x_padding=X_PADDING, y_padding=Y_PADDING,
            selected_index=1,
            on_change=self.ready_state_changed,
        )
        menu_width = self.ready_options.total_width + 2 * X_PADDING

        y = self.ready_options.total_height + 3 * Y_PADDING

        nickname_label = TextElement(
            app, 'Nickname:', label_font, (2 * X_PADDING, y), colours.in_game_label)
        y += nickname_label.image.getSize(app)[1]

        self.last_nickname = ''
        self.nickname_box = InputBox(
            app,
            Region(
                top=Abs(y),
                left=Abs(2 * X_PADDING),
                width=Abs(self.ready_options.total_width),
                height=Abs(self.ready_options.total_height)),
            app.settings.identity.nick or '',
            font=input_font,
            colour=colours.in_game_text_box,
            foreground_colour=colours.in_game_label,
            cursor_colour=colours.in_game_cursor,
            onClick=app.focus.set_focus,
            onEnter=self.nickname_enter_pressed,
        )
        y += self.ready_options.total_height + Y_PADDING

        self.heads = HeadSelector(app, Region(
            top=Abs(y),
            left=Abs(2 * X_PADDING),
            width=Abs(self.ready_options.total_width),
            height=Abs(self.ready_options.total_height)),
            on_change=self.head_selected,
        )
        self.heads.selected(app.settings.identity.head)
        y += self.ready_options.total_height + Y_PADDING

        self.more_menu = Menu(name='More…', items=[])
        manager = MenuManager()
        manager.setDefaultMenu(self.more_menu)
        self.menu_display = MenuDisplay(
            app, Location(Abs(X_PADDING, y), 'topleft'), Abs(menu_width, 0),
            menu_font, manager,
            colours.in_game_button_foreground,
            colours.in_game_button_foreground,
            colours.in_game_button_hover,
            backColour=BACKGROUND_COLOUR,
            autosize=True, hidable=True, hidden=True, x_padding=X_PADDING,
            y_padding=Y_PADDING,

        )
        self.menu_display.ACCELERATION = 2000

        self.scenario_menu = ScenarioMenu(self)
        self.team_name_menu = TeamNameMenu(self)
        self.map_menu = MapMenu(self)
        self.duration_menu = DurationMenu(self)

        self.elements = [
            SolidRect(app, BACKGROUND_COLOUR, None, Region(
                topleft=Abs(X_PADDING, Y_PADDING),
                width=Abs(menu_width),
                height=Abs(y - Y_PADDING))),
            self.ready_options,
            nickname_label,
            self.nickname_box,
            self.heads,
            self.menu_display,
        ]
        self.update_menu_contents()

    def update(self, player):
        self.player = player
        self.ready_options.set_index(0 if player.readyToStart else 1)
        if self.last_nickname != player.nick:
            self.last_nickname = player.nick
            self.nickname_box.setValue(player.nick)
        self.heads.selected(player.head)
        self.update_menu_contents()

    def update_menu_contents(self):
        if self.menu_display.manager.menu != self.more_menu:
            self.menu_display.manager.menu.update()

        scenario_voting = self.world.uiOptions.allow_scenario_voting
        team_switching = bool(self.world.uiOptions.team_ids_humans_can_switch_to)
        team_suggestions = self.world.uiOptions.team_name_suggestions
        can_force = self.world.isServer
        key = scenario_voting, team_switching, can_force, team_suggestions
        if key == self.last_config_info:
            return
        self.last_config_info = key

        while self.more_menu.items:
            self.more_menu.popItem(0)

        if team_switching:
            self.more_menu.appendItem(MenuItem('Change teams', listener=self.change_teams_clicked))
        if team_suggestions:
            self.more_menu.appendItem(MenuItem('Suggest team name', listener=self.show_team_menu))
        if scenario_voting:
            self.more_menu.appendItem(
                MenuItem('Suggest scenario', listener=self.show_scenario_menu))
            self.more_menu.appendItem(MenuItem('Suggest map', listener=self.show_map_menu))
            self.more_menu.appendItem(
                MenuItem('Suggest duration', listener=self.show_duration_menu))
        if can_force:
            self.more_menu.appendItem(MenuItem('Force start now', listener=self.start_game_now))

        self.menu_display.set_active(bool(self.more_menu.items))

    def ready_state_changed(self, new_index):
        ready = (new_index == 0)
        if self.player and self.player.readyToStart != ready:
            self.on_change.execute(PlayerIsReadyMsg(self.player.id, ready))

    def nickname_enter_pressed(self, widget):
        self.on_change.execute(ChangeNicknameMsg(self.player.id, widget.value.encode()))
        self.app.focus.clear_focus()

    def change_teams_clicked(self, menu_item):
        options = set(self.world.uiOptions.team_ids_humans_can_switch_to)
        if not self.player or not options:
            return
        options.discard(self.player.teamId)
        self.on_change.execute(ChangeTeamMsg(self.player.id, random.choice(list(options))))

    def show_team_menu(self, menu_item):
        self.team_name_menu.update()
        self.menu_display.manager.showMenu(self.team_name_menu)

    def show_scenario_menu(self, menu_item):
        self.scenario_menu.update()
        self.menu_display.manager.showMenu(self.scenario_menu)

    def show_map_menu(self, menu_item):
        self.map_menu.update()
        self.menu_display.manager.showMenu(self.map_menu)

    def show_duration_menu(self, menu_item):
        self.duration_menu.update()
        self.menu_display.manager.showMenu(self.duration_menu)

    def start_game_now(self, menu_item):
        self.world.make_everyone_ready()

    def head_selected(self, selected_index):
        head = self.heads.getSelectedValue()
        if self.player and head != self.player.head:
            self.on_change.execute(ChangeHeadMsg(self.player.id, self.heads.getSelectedValue()))


class CountedMenuItem(MenuItem):
    def __init__(self, caption, action=None, listener=None):
        self.caption = caption
        self.count = 0
        self.selected = False
        super().__init__(caption, action, listener)

    def set_count(self, count):
        self.count = count
        self.refresh_name()

    def set_selected(self, selected):
        self.selected = selected
        self.refresh_name()

    def refresh_name(self):
        self.name = f'{self.caption} ({self.count})' + (' ⇐' if self.selected else '')


class SelectionMenu(Menu):
    def __init__(self, gvm, name, items):
        super().__init__(name, items, listener=self.item_selected)
        self.gvm = gvm

    def item_selected(self, value):
        raise NotImplementedError

    def update(self):
        pass

    def cancel_menu(self, *args):
        self.gvm.menu_display.manager.cancel()


class ScenarioMenu(SelectionMenu):
    def __init__(self, gvm):
        options = [
            CountedMenuItem('No preference', (None, False)),
        ]
        for option in scenario_options:
            options.append(CountedMenuItem(option.levelName, (option, False)))
            if option.hvm_level_name:
                options.append(CountedMenuItem(option.hvm_level_name, (option, True)))
        options.extend([
            MenuItem('---', None),
            MenuItem('Back', None, listener=self.cancel_menu),
        ])
        super().__init__(gvm, 'Scenario…', options)

    def item_selected(self, level_data):
        if level_data is None:
            return
        scenario_class, hvm = level_data
        self.gvm.on_change.execute(
            SetSuggestedScenarioMsg.from_scenario_class(self.gvm.player.id, scenario_class, hvm))
        self.cancel_menu()

    def update(self):
        values = {}
        for player in self.gvm.world.players:
            if not player.bot:
                key = (player.suggested_scenario_class, player.suggested_scenario_hvm)
                values[key] = values.get(key, 0) + 1

        for item in self.items:
            if item.action is not None:
                item.set_count(values.get(item.action, 0))
                key = (
                    self.gvm.player.suggested_scenario_class,
                    self.gvm.player.suggested_scenario_hvm)
                item.set_selected(key == item.action)


class TeamNameMenu(SelectionMenu):
    def __init__(self, gvm):
        super().__init__(gvm, 'Team name…', items=[
            CountedMenuItem('No preference', ''),
            MenuItem('Other…', None, listener=self.other_clicked),
            MenuItem('---', None),
            MenuItem('Back', None, listener=self.cancel_menu),
        ])

    def other_clicked(self, item):
        prompt = TeamNameBox(self.gvm.app)

        @prompt.onClose.addListener
        def custom_value_entered():
            if prompt.result == DialogResult.OK:
                self.gvm.on_change.execute(SetSuggestedTeamNameMsg(prompt.value.encode('utf-8')))

        prompt.show()
        self.cancel_menu()

    def item_selected(self, team_name):
        if team_name is None:
            return
        self.gvm.on_change.execute(SetSuggestedTeamNameMsg(team_name.encode('utf-8')))
        self.cancel_menu()

    def update(self):
        values = {'': 0}
        for player in self.gvm.world.players:
            if not player.bot:
                team_name = player.suggested_team_name
                values[team_name] = values.get(team_name, 0) + 1

        for item in list(self.items):
            if item.action is None:
                continue
            if item.action in values:
                item.set_count(values.pop(item.action))
                item.set_selected(self.gvm.player.suggested_team_name == item.action)
            else:
                self.removeItem(item)

        for team_name, count in values.items():
            item = CountedMenuItem(team_name, team_name)
            item.set_count(count)
            item.set_selected(self.gvm.player.suggested_team_name == item.action)
            self.insertItem(-3, item)


class MapMenu(SelectionMenu):
    def __init__(self, gvm):
        super().__init__(gvm, 'Map…', [
            CountedMenuItem('No preference', ''),
            MenuItem('---', None),
            MenuItem('Back', None, listener=self.cancel_menu),
        ])

    def item_selected(self, map_name):
        if map_name is None:
            return
        self.gvm.on_change.execute(SetSuggestedMapMsg(self.gvm.player.id, map_name.encode()))
        self.cancel_menu()

    def update(self):
        for item in list(self.items):
            if item.action:
                self.removeItem(item)

        level_class = self.gvm.player.suggested_scenario_class
        if level_class is None:
            options = {m.code: m.name for lc in scenario_options for m in lc.map_selection}
        else:
            options = {m.code: m.name for m in level_class.map_selection}

        counts = {'': 0}
        for player in self.gvm.world.players:
            if not player.bot:
                map_code = player.suggested_map
                counts[map_code] = counts.get(map_code, 0) + 1

        sorted_options = sorted(options.items(), key=lambda i: i[1])
        if 'StandardMap' in options:
            item = ('StandardMap', options['StandardMap'])
            sorted_options.remove(item)
            sorted_options.insert(0, item)

        for code, name in sorted_options:
            item = CountedMenuItem(name, code)
            item.set_count(counts.get(code, 0))
            item.set_selected(self.gvm.player.suggested_map == code)
            self.insertItem(-2, item)

        self.items[0].set_count(counts.get('', 0))
        self.items[0].set_selected(self.gvm.player.suggested_map == '')


class DurationMenu(SelectionMenu):
    def __init__(self, gvm):
        super().__init__(gvm, 'Duration…', [
            CountedMenuItem('No preference', 0),
            MenuItem('Other…', None, listener=self.other_clicked),
            MenuItem('---', None),
            MenuItem('Back', None, listener=self.cancel_menu),
        ])

    def other_clicked(self, item):
        prompt = GameDurationBox(self.gvm.app)

        @prompt.onClose.addListener
        def custom_value_entered():
            if prompt.result == DialogResult.OK:
                duration = int(prompt.value) * 60
                self.gvm.on_change.execute(SetSuggestedDurationMsg(self.gvm.player.id, duration))

        prompt.show()
        self.cancel_menu()

    def item_selected(self, duration):
        if duration is None:
            return
        self.gvm.on_change.execute(SetSuggestedDurationMsg(self.gvm.player.id, duration))
        self.cancel_menu()

    def update(self):
        values = {0: 0}
        for player in self.gvm.world.players:
            if not player.bot:
                duration = player.suggested_duration
                values[duration] = values.get(duration, 0) + 1

        for item in list(self.items):
            if item.action is None:
                continue
            if item.action in values:
                item.set_count(values.pop(item.action))
                item.set_selected(self.gvm.player.suggested_duration == item.action)
            else:
                self.removeItem(item)

        for duration, count in values.items():
            item = CountedMenuItem('%d min' % (int(duration/60+0.5),), duration)
            item.set_count(count)
            item.set_selected(self.gvm.player.suggested_duration == item.action)
            self.insertItem(-3, item)


class EntryDialog(DialogBox):
    def __init__(self, app, title, label, validator=None):
        DialogBox.__init__(self, app, Canvas(400, 230), title)

        self.result = None
        self.value = None

        labelFont = app.screenManager.fonts.bigMenuFont
        labelColour = app.theme.colours.dialogBoxTextColour
        btnFont = app.screenManager.fonts.bigMenuFont
        btnColour = app.theme.colours.dialogButtonColour
        highlightColour = app.theme.colours.black
        inputFont = app.screenManager.fonts.defaultTextBoxFont
        inputColour = app.theme.colours.grey

        self.inputBox = InputBox(
            app,
            Region(topleft=self.Relative(0.1, 0.4), bottomright=self.Relative(0.9, 0.6)),
            font=inputFont, colour=inputColour, onClick=self.setFocus,
            onEnter=self.okClicked, onEsc=self.cancelClicked,
            validator=validator)

        self.elements = [
            TextElement(
                app, label,
                labelFont, Location(self.Relative(0.1, 0.2), 'midleft'),
                labelColour),
            self.inputBox,

            TextButton(
                app,
                Location(self.Relative(0.3, 0.9), 'center'),
                'Ok', btnFont, btnColour, highlightColour,
                onClick=self.okClicked),
            TextButton(
                app,
                Location(self.Relative(0.7, 0.9), 'center'),
                'Cancel', btnFont, btnColour, highlightColour,
                onClick=self.cancelClicked),
        ]

        self.setFocus(self.inputBox)

    def okClicked(self, element):
        self.result = DialogResult.OK
        self.value = self.inputBox.value
        self.close()

    def cancelClicked(self, element):
        self.result = DialogResult.Cancel
        self.value = self.inputBox.value
        self.close()


class TeamNameBox(EntryDialog):
    def __init__(self, app):
        EntryDialog.__init__(self, app, 'Custom Team', 'Team name:')


class GameDurationBox(EntryDialog):
    def __init__(self, app):
        EntryDialog.__init__(self, app, 'Custom Duration', 'Duration (mins):', intValidator)
