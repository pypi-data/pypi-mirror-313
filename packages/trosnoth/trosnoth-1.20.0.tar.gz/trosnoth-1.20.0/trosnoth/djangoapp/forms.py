import functools

from django import forms

from trosnoth.bots.base import get_available_bot_names, get_bot_class
from trosnoth.const import BOT_DIFFICULTY_EASY, BOT_DIFFICULTY_MEDIUM, BOT_DIFFICULTY_HARD
from trosnoth.djangoapp.models import (
    TrosnothServerSettings, TrosnothUser, TrosnothArena,
)
from trosnoth.levels.base import SELECTABLE_TEAMS, FORCE_RANDOM_TEAMS, HVM_TEAMS
from trosnoth.levels.maps import (
    StandardMap, SmallMap, WideMap, CorridorMap, LargeMap,
    SmallStackMap, SmallRingMap, LargeRingsMap, LabyrinthMap, FreeFlowMap,
)
from trosnoth.levels.registry import scenario_class_by_code, available_scenario_classes


class ServerSettingsForm(forms.ModelForm):
    allowed_hosts = forms.CharField(
        required=False,
        help_text='Comma-separated list of host names that are allowed to be '
                  'used to access the server web interface. Used for security '
                  'purposes. Host names will only be permitted if they are '
                  'in this list, or they are known local IP addresses of '
                  'this machine.')
    secret_key = forms.CharField(
        label='Secret key', max_length=100,
        help_text='Used for cryptographic signing. Should be unique and '
                  'unpredictable. Keep this value secret! Changing this '
                  'value will invalidate active web sessions.')
    debug = forms.BooleanField(
        required=False,
        label='Enable debugging',
        help_text='Show detailed error pages. Never turn this on for a '
                  'public server. ')

    class Meta:
        model = TrosnothServerSettings
        fields = (
            'serverName',
            'welcomeText',
            'elephantName',
            'webPort',
            'serverPort',
            'manholePort',
            'manholePassword',
            'manhole_authorised_keys',
            'trustClientUsernames',
        )
        widgets = {
            'serverName': forms.TextInput,
            'manholePassword': forms.TextInput,
            'elephantName': forms.TextInput,
        }


class ManagePlayerForm(forms.ModelForm):
    active = forms.BooleanField(
        required=False,
        label='Active',
        help_text='Deactivated users cannot log on to this server.',
    )
    superuser = forms.BooleanField(
        required=False,
        label='Superuser',
        help_text='Gives this user full management permissions on this '
                  'server.',
    )

    class Meta:
        model = TrosnothUser
        fields = (
            'nick',
            'ownsElephant',
        )
        widgets = {
            'nick': forms.TextInput,
        }


@functools.lru_cache()
def get_bot_kind_choices():
    result = [('', '(Automatic)')]
    for bot_name in get_available_bot_names():
        bot_class = get_bot_class(bot_name)
        result.append((bot_name, bot_class.nick))
    return tuple(result)


class ArenaModelForm(forms.ModelForm):
    balance_bot_difficulty = forms.TypedChoiceField(
        empty_value=None,
        coerce=int,
        choices=(
            (None, 'Disabled'),
            (BOT_DIFFICULTY_EASY, 'Easy'),
            (BOT_DIFFICULTY_MEDIUM, 'Medium'),
            (BOT_DIFFICULTY_HARD, 'Hard'),
        ),
        required=False,
        label='BalanceBot difficulty',
    )

    machines_difficulty = forms.ChoiceField(
        choices=(
            (BOT_DIFFICULTY_EASY, 'Easy'),
            (BOT_DIFFICULTY_MEDIUM, 'Medium'),
            (BOT_DIFFICULTY_HARD, 'Hard'),
        ),
        required=True,
        label='Humans vs. Machines bot difficulty',
    )

    balance_bot_kind = forms.ChoiceField(choices=get_bot_kind_choices(), required=False)
    machines_bot_kind = forms.ChoiceField(
        choices=get_bot_kind_choices(),
        required=False,
        label='Humans vs. Machines bot kind',
    )

    class Meta:
        model = TrosnothArena
        fields = (
            'name',
            'enabled',
            'autoStartCountDown',
            'require_everyone_ready',
            'balance_bot_difficulty',
            'balance_bot_kind',
            'machines_difficulty',
            'machines_bot_kind',
            'extra_bot_count',
            'force_half_width',
            'force_height',
            'force_duration',
            'gamePort',
            'currentTournament',
            'profileSlowCalls',
        )
        widgets = {
            'name': forms.TextInput,
        }


class ArenaControlForm(forms.Form):
    paused = forms.BooleanField(
        required=False,
        label='Pause game',
    )
    blueShots = forms.BooleanField(
        required=False,
        label='Blue team can shoot',
    )
    blueCaps = forms.BooleanField(
        required=False,
        label='Blue team can capture zones',
    )
    redShots = forms.BooleanField(
        required=False,
        label='Red team can shoot',
    )
    redCaps = forms.BooleanField(
        required=False,
        label='Red team can capture zones',
    )
    action = forms.ChoiceField(
        choices=(
            ('', '------'),
            ('lobby', 'Return to lobby'),
            ('shutdown', 'Restart arena (boots all players)'),
        ),
        required=False,
        help_text='Send a special command to the running game',
    )


class SelectLevelForm(forms.Form):
    level_data = {
        code: {
            'team_options': {
                choice: 1
                for choice in level_class.team_selection
            },
            'size_options': {
                map_object.code: 1
                for map_object in level_class.map_selection
            },
        } for code, level_class in scenario_class_by_code.items()
    }
    scenario = forms.ChoiceField(
        choices=((c.level_code, c.levelName) for c in available_scenario_classes),
        widget=forms.Select(attrs={
            'onchange': "update_fields();",
        }),
    )
    teams = forms.ChoiceField(
        choices=(
            ('Scenario default', 'Scenario default'),
            (SELECTABLE_TEAMS, SELECTABLE_TEAMS),
            (FORCE_RANDOM_TEAMS, FORCE_RANDOM_TEAMS),
            (HVM_TEAMS, HVM_TEAMS),
        ),
    )
    size = forms.ChoiceField(
        choices=tuple(
            (map_class().code, map_class.name) for map_class in [
                StandardMap,
                SmallMap,
                WideMap,
                CorridorMap,
                LargeMap,
                SmallStackMap,
                SmallRingMap,
                LargeRingsMap,
                LabyrinthMap,
                FreeFlowMap,
            ]
        ),
        widget=forms.Select(attrs={
            'onchange': "update_fields();",
        }),
    )
    duration = forms.IntegerField(
        help_text='Duration in minutes. Zero or blank means auto duration.',
        min_value=0,
        required=False,
    )
