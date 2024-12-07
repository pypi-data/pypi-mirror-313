import logging

import pygame

from trosnoth.gui.framework.elements import (
    OptionButtons, make_static_text_button,
)
from trosnoth.model.utils import Rect

from trosnoth.const import HEADS_ORDER
from trosnoth.trosnothgui.ingame.imageradiobutton import RadioButtonGroup, ImageRadioButton

from trosnoth.gui.framework.dialogbox import (
    DialogBox, DialogResult, DialogBoxAttachedPoint,
)
from trosnoth.gui.common import (
    Location, SizedImage, LetterboxedArea, Region, Abs,
)
from trosnoth.gui.framework import elements, prompt

log = logging.getLogger(__name__)


class HeadArea:
    def __init__(self, area, index, total):
        self.area = area
        self.index = index
        self.total = total

    def getRect(self, app):
        full_rect = self.area.getRect(app)
        x0 = full_rect.left
        dx0 = int(full_rect.width * self.index / self.total + 0.5)
        dx1 = int(full_rect.width * (self.index + 1) / self.total + 0.5)
        result = Rect(x0 + dx0, full_rect.top, dx1 - dx0, full_rect.height)
        return result

    def getSize(self, app):
        return self.getRect(app).size


class HeadSelector(RadioButtonGroup):
    def __init__(self, app, area, on_change=None):
        super().__init__(app, on_change=on_change)

        images = [app.theme.sprites.head_pic(head) for head in HEADS_ORDER]
        ratio = len(images) * images[0].get_width() / images[0].get_height()
        full_area = LetterboxedArea(area, ratio)
        for i, head in enumerate(HEADS_ORDER):
            head_area = HeadArea(full_area, i, len(images))
            button = ImageRadioButton(
                app, '', head_area,
                SizedImage(images[i], head_area, alpha=True),
                value=head, border=0)
            self.add(button)


class JoinGameDialog(DialogBox):
    def __init__(self, app, controller, world):
        super().__init__(app, (400, 200), 'Player details')
        self.world = world
        self.result = None
        self.controller = controller
        self.selected_team = None
        self.selected_nick = ''
        self.selected_head = 0

        fonts = self.app.screenManager.fonts
        self.nick_box = None
        self.heads = None
        self.team_buttons = None
        self.team_options = []

        colours = app.theme.colours

        self.elements = []
        self._edge.borderWidth = 1
        self.setColours(
            colours.joinGameBorderColour,
            colours.joinGameTitleColour,
            colours.joinGameBackgroundColour)

    def rebuild(self, nick_selection, team_selection):
        if team_selection and not nick_selection:
            self.setCaption('Select team')
        else:
            self.setCaption('Player details')

        y = 20

        colours = self.app.theme.colours
        fonts = self.app.screenManager.fonts
        self.elements = []

        if nick_selection:
            y += 15
            self.elements.append(elements.TextElement(
                self.app,
                'Nickname:',
                fonts.leaderboardFont,
                Location(DialogBoxAttachedPoint(self, (20, y), 'topleft'), 'bottomleft'),
                colours.in_game_label,
            ))

            self.nick_box = prompt.InputBox(
                self.app,
                Region(
                    topleft=DialogBoxAttachedPoint(self, (20, y), 'topleft'),
                    size=Abs(360, 50),
                ),
                self.app.settings.identity.nick or '',
                font=fonts.gameMenuFont,
                maxLength=30,
                colour=colours.in_game_text_box,
                foreground_colour=colours.in_game_label,
                cursor_colour=colours.in_game_cursor,
                onClick=self.setFocus,
                onTab=lambda sender: self.clearFocus(),
                onEnter=self.ok_clicked,
            )
            self.elements.append(self.nick_box)
            self.setFocus(self.nick_box)
            y += 60

            self.heads = HeadSelector(self.app, Region(
                topleft=DialogBoxAttachedPoint(self, (20, y), 'topleft'),
                size=Abs(360, 50),
            ))
            self.heads.selected(self.app.settings.identity.head)
            self.elements.append(self.heads)
            y += 60

        if team_selection and nick_selection:
            y += 20
            self.elements.append(elements.TextElement(
                self.app,
                'Select team:',
                fonts.leaderboardFont,
                Location(DialogBoxAttachedPoint(self, (20, y), 'topleft'), 'bottomleft'),
                colours.in_game_label,
            ))

        if team_selection:
            self.team_options = [
                self.world.getTeam(team_id)
                for team_id in self.world.uiOptions.team_ids_humans_can_join]

            team_names = []
            team_label_colours = []
            team_selected_colours = []
            for team in self.team_options:
                if team is None:
                    name, colour = 'Rogue', (255, 255, 255)
                else:
                    name, colour = team.teamName, team.colour
                if min(colour) > 192:
                    colour = tuple(component // 2 for component in colour)
                team_names.append(name)
                team_label_colours.append(colour)
                team_selected_colours.append(colour)

            if len(self.team_options) > 1:
                self.team_options.insert(0, None)
                team_names.insert(0, 'Automatic')
                team_label_colours.insert(0, colours.in_game_label)
                team_selected_colours.insert(0, colours.in_game_selection_background)

            self.team_buttons = OptionButtons(
                self.app,
                team_names,
                Location(DialogBoxAttachedPoint(self, (0, y), 'midtop'), 'midtop'),
                team_label_colours, (255, 255, 255),
                colours.in_game_button_hover, team_selected_colours,
                fonts.gameMenuFont, x_padding=20, y_padding=10,
                selected_index=0, vertical=True,
            )
            self.elements.append(self.team_buttons)
            y += self.team_buttons.total_height + 10

        y += 10
        self.elements.extend([
            make_static_text_button(
                self.app,
                Location(DialogBoxAttachedPoint(self, (20, y), 'topleft'), 'topleft'),
                fonts.menuFont,
                'Cancel',
                colours.in_game_button_foreground, colours.in_game_button_background,
                colours.in_game_button_hover, colours.in_game_button_background,
                x_padding=20, y_padding=10,
                on_click=self.cancel,
            ),
            make_static_text_button(
                self.app,
                Location(DialogBoxAttachedPoint(self, (-20, y), 'topright'), 'topright'),
                fonts.menuFont,
                'Ok',
                colours.in_game_button_foreground, colours.in_game_button_background,
                colours.in_game_button_hover, colours.in_game_button_background,
                x_padding=20, y_padding=10,
                hotkey=pygame.K_RETURN,
                on_click=self.ok_clicked,
            ),
        ])
        y += self.elements[-1].stdImage.get_height() + 20

        self.size = (400, y)
        self._edge.auto_position()

    def show(self, nick_selection, team_selection):
        self.rebuild(nick_selection, team_selection)
        super().show()

    def ok_clicked(self, widget):
        if self.nick_box:
            nick = self.nick_box.value.strip()
            if nick == '':
                # Disallow all-whitespace nicks
                return
            self.selected_nick = nick

        if self.team_buttons:
            self.selected_team = self.team_options[self.team_buttons.selected_index]
        if self.heads:
            self.selected_head = self.heads.getSelectedValue()

        self.result = DialogResult.OK
        self.close()

    def cancel(self, sender):
        self.result = DialogResult.Cancel
        self.close()
