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
from configparser import ConfigParser

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QTableWidgetItem

from trosnoth import data
from trosnoth.const import BOT_DIFFICULTY_EASY, BOT_DIFFICULTY_HARD, DEFAULT_BOT_DIFFICULTY
from trosnoth.gui.app import UserClosedPygameWindow
from trosnoth.levels.base import LevelOptions
from trosnoth.model.map import ZoneLayout, ZoneStep
from trosnoth.run.solotest import launch_solo_game_async, SoloGameClosed
from trosnoth.settings import ClientSettings
from trosnoth.triggers.deathmatch import make_small_circles_layout
from trosnoth.utils.utils import (
    UIScreenRunner, format_numbers,
)
from trosnoth.welcome.nonqt import async_callback, run_callback_in_async_loop

TUTORIALS_PROGRESS_FILE = data.user_path / 'tutorials.ini'
COMPLETED_KEY = 'completed'
BEST_SCORE_KEY = 'best_score'

learning_scenarios = []
challenge_scenarios = []


class TutorialsScreen:
    def __init__(self, parent):
        self.async_manager = parent.async_manager   # Allows async callbacks

        self.parent = parent
        self.screen_runner = UIScreenRunner()
        self.window = window = parent.window
        self.main_stack = window.findChild(QWidget, 'main_stack')
        self.tutorials_page = window.findChild(QWidget, 'tutorials_page')

        self.tab_container = window.findChild(QWidget, 'tutorials_tab_container')
        self.tutorials_table = None
        self.tutorials_table_2 = None
        self.tick_font = None
        self.progress = None

        window.findChild(QWidget, 'tutorials_back_button').clicked.connect(
            run_callback_in_async_loop(self.back_clicked))
        window.findChild(QWidget, 'tutorials_play_button').clicked.connect(
            run_callback_in_async_loop(self.play_scenario))

        self.blitz_mode_checkbox = window.findChild(
            QWidget, 'tutorials_blitz_mode_checkbox')

        self.tutorials_table = window.findChild(QWidget, 'tutorials_table')
        self.tutorials_table_2 = window.findChild(QWidget, 'tutorials_table_2')

        self.tables_and_contents = (
            (self.tutorials_table, learning_scenarios),
            (self.tutorials_table_2, challenge_scenarios),
        )
        for tutorials_table, scenarios in self.tables_and_contents:
            tutorials_table.horizontalHeader().sectionResized.connect(
                run_callback_in_async_loop(self.table_section_resized, tutorials_table))
            tutorials_table.cellDoubleClicked.connect(
                run_callback_in_async_loop(self.play_scenario))

            tutorials_table.setColumnWidth(0, 75)
            tutorials_table.setColumnWidth(1, 250)

            title_font = QFont(tutorials_table.item(0, 1).font())
            title_font.setPixelSize(20)
            description_font = QFont(tutorials_table.item(0, 2).font())
            description_font.setPixelSize(16)
            self.tick_font = QFont(tutorials_table.item(0, 2).font())
            self.tick_font.setPixelSize(40)

            tutorials_table.setRowCount(len(scenarios))
            for i, scenario in enumerate(scenarios):
                item = QTableWidgetItem(scenario.name)
                item.setFont(title_font)
                tutorials_table.setItem(i, 1, item)
                item = QTableWidgetItem(scenario.description)
                item.setFont(description_font)
                tutorials_table.setItem(i, 2, item)

            # For some reason, calling resizeRowsToContents right here adds
            # padding to the cells, but using call_soon() does not, and is
            # therefore consistent with what happens on section resize.
            asyncio.get_event_loop().call_soon(self.table_section_resized, tutorials_table)

    def update_progress_indicators(self):
        self.reload_progress()
        best_option_selected = False
        best_tab_index = None
        for tab_index, (tutorials_table, scenarios) in enumerate(self.tables_and_contents):
            for i, scenario in enumerate(scenarios):
                if self.is_scenario_completed(scenario):
                    item = QTableWidgetItem('✓')
                    item.setFont(self.tick_font)
                    tutorials_table.setItem(i, 0, item)
                elif not best_option_selected:
                    best_option_selected = True
                    tutorials_table.setCurrentCell(i, 1)
                    self.tab_container.setCurrentIndex(tab_index)

            if not best_option_selected:
                # Select the first scenario in the challenges list if all are completed
                tutorials_table.setCurrentCell(0, 1)
                self.tab_container.setCurrentIndex(len(self.tables_and_contents) - 1)

    def update_experimental_options(self):
        display_settings = ClientSettings.get().display
        if display_settings.show_experimental:
            self.blitz_mode_checkbox.show()
        else:
            self.blitz_mode_checkbox.hide()

    async def run(self):
        previous_page_widget = self.main_stack.currentWidget()
        try:
            self.update_progress_indicators()
            self.update_experimental_options()
            self.main_stack.setCurrentWidget(self.tutorials_page)
            return await self.screen_runner.run()
        finally:
            self.main_stack.setCurrentWidget(previous_page_widget)

    def back_clicked(self):
        self.screen_runner.done(None)

    def reload_progress(self):
        self.progress = ConfigParser(interpolation=None)
        for scenario in learning_scenarios:
            self.progress.add_section(scenario().get_section_name())
        for scenario in challenge_scenarios:
            self.progress.add_section(scenario().get_section_name())
        self.progress.read(TUTORIALS_PROGRESS_FILE)

    def is_scenario_completed(self, scenario):
        return self.progress[scenario().get_section_name()].getboolean(COMPLETED_KEY, False)

    def get_scenario_best_score(self, scenario):
        return self.progress[scenario().get_section_name()].getfloat(BEST_SCORE_KEY, fallback=None)

    @async_callback
    async def play_scenario(self, *args):
        tab_index = self.tab_container.currentIndex()
        tutorials_table, scenarios = self.tables_and_contents[tab_index]
        current_row = tutorials_table.currentRow()
        scenario = scenarios[current_row]
        previous_best_score = self.get_scenario_best_score(scenario)
        slow_dark_conquest = not self.blitz_mode_checkbox.isChecked()

        if scenario.intro and not self.is_scenario_completed(scenario):
            ok = await self.parent.message_viewer.run(scenario.intro)
            if not ok:
                return

        play_again = True
        scenario_instance = scenario()
        level_instance = None
        while play_again:
            try:
                result = await scenario_instance.run(
                    level=level_instance,
                    slow_dark_conquest=slow_dark_conquest,
                )
            except (UserClosedPygameWindow, SoloGameClosed):
                break

            if not result.a_human_player_won:
                play_again = await self.display_play_again_window(
                    scenario.name, previous_best_score, None)
                if play_again:
                    level_instance = scenario_instance.level.replay()
                continue
            level_instance = None

            if result.tutorial_score is None:
                self.scenario_now_completed(tutorials_table, scenarios, current_row, None)
                break

            best_score = result.tutorial_score if previous_best_score is None else max(
                previous_best_score, result.tutorial_score)
            self.scenario_now_completed(tutorials_table, scenarios, current_row, best_score)

            play_again = await self.display_play_again_window(
                scenario.name, previous_best_score, result.tutorial_score)
            previous_best_score = best_score

    def scenario_now_completed(self, tutorials_table, scenarios, row_index, best_score=None):
        scenario = scenarios[row_index]

        self.reload_progress()
        section_name = scenario().get_section_name()
        self.progress[section_name][COMPLETED_KEY] = '1'
        if best_score is not None:
            self.progress[section_name][BEST_SCORE_KEY] = str(best_score)

        with open(TUTORIALS_PROGRESS_FILE, 'w') as f:
            self.progress.write(f)

        item = QTableWidgetItem('✓')
        item.setFont(self.tick_font)
        tutorials_table.setItem(row_index, 0, item)

    def table_section_resized(self, tutorials_table, *args):
        PADDING = 20
        tutorials_table.resizeRowsToContents()
        for i in range(tutorials_table.rowCount()):
            tutorials_table.setRowHeight(i, tutorials_table.rowHeight(i) + PADDING)

    async def display_play_again_window(self, level_name, best_score, this_score):
        '''
        :param level_name: the name of the scenario
        :param best_score: None if there is no previous best score
        :param this_score: None if level was failed, otherwise best score
        '''
        if this_score is None:
            # Scenario failed
            if best_score is None:
                message = 'Scenario failed.'
            else:
                best_string, = format_numbers([best_score])
                message = f'Scenario failed.\n\nHigh score: {best_string}'
        elif best_score is None:
            this_string, = format_numbers([this_score])
            message = f'Scenario complete.\n\nScore: {this_string}\nOld high score: —'
        else:
            this_string, best_string = format_numbers([this_score, best_score])
            if this_score > best_score:
                message = (
                    f'Congratulations! You got a new high score!\n\n'
                    f'Score: {this_string}\nOld high score: {best_string}'
                )
            elif this_score == best_score:
                message = (
                    f'Congratulations! You equalled your high score.\n\n'
                    f'Score: {this_string}\nHigh score: {best_string}'
                )
            else:
                message = f'Scenario complete.\n\nScore: {this_string}\nHigh score: {best_string}'

        message += f'\n\nPlay {level_name} again?'
        result = await self.parent.message_viewer.run(message, ok_text='play again')
        return result


class TutorialScenario:
    name = NotImplemented
    description = NotImplemented
    section_name = None
    intro = None

    game_prefix = None
    extra_args = {}

    def __init__(self):
        self.level = None

    def get_section_name(self):
        if self.section_name is None:
            return type(self).__name__

    async def run(self, level=None, slow_dark_conquest=True):
        '''
        :return: LevelResult
        '''
        if level is None:
            level = self.build_level()
        self.level = level
        return await launch_solo_game_async(
            game_prefix=self.game_prefix or self.name,
            level=level,
            bot_difficulty=DEFAULT_BOT_DIFFICULTY,
            slow_dark_conquest=slow_dark_conquest,
            **self.extra_args,
        )

    def build_level(self):
        raise NotImplementedError()


@learning_scenarios.append
class CatPigeon(TutorialScenario):
    name = 'Cat among pigeons'
    description = 'Get used to the game controls while shooting bots who don’t shoot back.'
    intro = (
        'Default controls:\n\n'

        'W, A, S, D ~ move player\n'
        'Left mouse ~ shoot\n'
        'Right mouse ~ grappling hook\n\n'

        'Controls can be configured in settings.\n\n'

        'In this scenario, enemy bots will not attack you. Shoot as many of them as you can in '
        'the time limit.'
    )

    def build_level(self):
        from trosnoth.levels.catpigeon import CatPigeonLevel
        return CatPigeonLevel(
            level_options=LevelOptions(duration=120), map_builder=self.build_map)

    def build_map(self):
        zones = ZoneLayout()

        zones.setZoneOwner(zones.firstLocation, 0, dark=True)
        zones.connectZone(zones.firstLocation, ZoneStep.SOUTH, ownerIndex=1, dark=False)

        return zones.createMapLayout(autoOwner=False)


@learning_scenarios.append
class OrbChase(TutorialScenario):
    name = 'Orb chase'
    description = 'Improve your map navigation speed as you try to reach the target orb.'
    intro = (
        'Every time your player touches a red orb in this scenario, you gain one point and a '
        'different orb becomes red.\n\n'

        'Look at the minimap to work out the best route to the red orb.\n\n'

        'You begin this scenario as a ghost. Move the ghost using the mouse. To respawn, move to '
        'a blue room and left click the mouse.\n\n'
    )

    def build_level(self):
        from trosnoth.levels.orbchase import OrbChaseLevel

        return OrbChaseLevel(level_options=LevelOptions(duration=180))


@learning_scenarios.append
class OneOnOneFreeForAll(TutorialScenario):
    name = '1v1 free-for-all'
    description = 'Practise dogfighting with one enemy bot.'
    intro = (
        'In this scenario you will fight against a single enemy bot.\n\n'

        'The winner is the player with the most kills when the timer runs out.\n\n'

        'Every kill earns you money. You can use your money to buy items and weapons. Press tab '
        'to select an item, then press space bar to use it.'
    )

    extra_args=dict(
        bot_count=1,
    )

    def build_level(self):
        from trosnoth.levels.freeforall import FreeForAllLevel

        return FreeForAllLevel(
            level_options=LevelOptions(duration=3 * 60),
            add_one_bot=False, map_builder=make_small_circles_layout)


@learning_scenarios.append
class OneOnOneTrosnothMatch(TutorialScenario):
    name = '1v1 Trosnoth match'
    description = 'Play a Trosnoth match against a single bot. Capture all orbs to win.'
    intro = (
        'The aim of Trosnoth is to capture all enemy rooms.\n\n'

        'To capture a room, touch the orb at the room centre. If the enemy bot is defending the '
        'room, you will need to kill it or chase it away first.\n\n'

        'You can only capture a room that is next to territory you own.'
    )

    game_prefix = '1v1 Trosnoth'
    extra_args = dict(bot_count=1)

    def build_level(self):
        from trosnoth.levels.solo import SoloRulesGame
        return SoloRulesGame()


@learning_scenarios.append
class ThreeOnThreeTrosnothMatch(TutorialScenario):
    name = '3v3 Trosnoth match'
    description = 'You and 2 bots play Trosnoth against 3 bots.'
    intro = (
        'This is a tournament-style 3v3 Trosnoth match, with bots on both teams.\n\n'

        'You can only capture a room if there are more attackers than defenders alive in the '
        'room. E.g.:\n'
        '2 attackers vs. 1 defender = can capture\n'
        '1 attacker vs. 1 defender = cannot capture\n\n'

        'If a team’s territory is divided in two, the team loses the smaller section.'
    )
    game_prefix = '3v3 Trosnoth'
    extra_args = dict(bot_count=5)

    def build_level(self):
        from trosnoth.levels.standard import StandardRandomLevel
        return StandardRandomLevel()


@challenge_scenarios.append
class FreeForAll(TutorialScenario):
    name = 'Four player free-for-all'
    description = 'Practise dogfighting in a 3-bot free-for-all.'
    game_prefix = 'Free-for-all'
    extra_args = dict(bot_count=3)

    def build_level(self):
        from trosnoth.levels.freeforall import FreeForAllLevel
        return FreeForAllLevel(level_options=LevelOptions(duration=300), add_one_bot=False)


@challenge_scenarios.append
class LastStandTrosnothMatch(TutorialScenario):
    name = '3v3 Last stand'
    description = 'Try to win from a losing position.'
    intro = (
        'This is a tournament-style 3v3 Trosnoth match, with bots on both teams.\n\n'

        'However, your team begins the scenario with only 1 or 2 rooms remaining.'
    )
    extra_args = dict(bot_count=5)

    def build_level(self):
        from trosnoth.levels.laststand import LastStandLevel
        return LastStandLevel()


@challenge_scenarios.append
class NonViolentTrosnoth(TutorialScenario):
    name = 'Non-violent Trosnoth'
    description = 'Learn to position your player by playing a Trosnoth match where nobody can ' \
                  'shoot.'
    intro = (
        'This is a regular Trosnoth match, except nobody can fire shots.\n\n'

        'To prevent a room from being captured, you simply need to keep enough defenders in the '
        'room. To capture a room, you need to target a room that is not well defended.\n\n'

        'Pay close attention to the minimap so you will know when to defend and which room to '
        'attack.'
    )
    game_prefix = 'Non-violent'
    extra_args = dict(bot_count=5)

    def build_level(self):
        from trosnoth.levels.positioningdrill import PositioningDrillLevel
        return PositioningDrillLevel()


@challenge_scenarios.append
class PacifistChallenge(TutorialScenario):
    name = 'Pacifist Challenge'
    description = 'Try to win a 3v3 Trosnoth match without firing a single shot.'
    intro = (
        'This is a regular Trosnoth 3v3 match, with a twist.\n\n'

        'In this scenario, everyone can fire shots except you.\n\n'

        'Good luck!'
    )
    extra_args = dict(bot_count=5)

    def build_level(self):
        from trosnoth.levels.pacifistdrill import HumansArePacifistsLevel
        return HumansArePacifistsLevel()


@challenge_scenarios.append
class WingmanChallenge2v2(TutorialScenario):
    name = '2v2 Wingman Challenge'
    description = 'Try to win a 2v2 Trosnoth match without capturing any orbs.'
    intro = (
        'In this 2v2 Trosnoth match, bots can capture rooms but you can’t.\n\n'

        'You’ll need to focus on defending and supporting your team mate.\n\n'

        'Good luck!'
    )
    extra_args = dict(bot_count=3)

    def build_level(self):
        from trosnoth.levels.wingmandrill import HumansAreWingmenLevel
        return HumansAreWingmenLevel()


@challenge_scenarios.append
class WingmanChallenge(TutorialScenario):
    name = '3v3 Wingman Challenge'
    description = 'Try to win a 3v3 Trosnoth match without capturing any orbs.'
    intro = (
        'In this 3v3 Trosnoth match, bots can capture rooms but you can’t.\n\n'

        'You’ll need to focus on defending and supporting your team mates.\n\n'

        'Good luck!'
    )
    extra_args = dict(bot_count=5)

    def build_level(self):
        from trosnoth.levels.wingmandrill import HumansAreWingmenLevel
        return HumansAreWingmenLevel(level_options=LevelOptions(map_index=1))


@challenge_scenarios.append
class WingmanChallenge3v2(TutorialScenario):
    name = '2v3 Wingman Challenge'
    description = 'Play the Wingman Challenge with one player down.'
    intro = (
        'This is the Wingman Challenge again, but this time you only get one team mate.\n\n'

        'Good luck!'
    )
    extra_args = dict(
        stack_teams=True,
        bot_count=3,
        add_bots=((), [('ranger', DEFAULT_BOT_DIFFICULTY)]),
        no_auto_balance=True,
    )

    def build_level(self):
        from trosnoth.levels.wingmandrill import HumansAreWingmenAndMustBeRedLevel
        return HumansAreWingmenAndMustBeRedLevel(level_options=LevelOptions(map_index=1))
