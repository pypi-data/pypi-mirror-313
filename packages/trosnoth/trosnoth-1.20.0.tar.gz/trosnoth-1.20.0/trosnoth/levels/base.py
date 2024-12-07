import asyncio
import dataclasses
import logging
import random
from typing import Optional, List, Iterable

import msgpack
from twisted.internet import defer

from trosnoth.const import (
    GAME_FULL_REASON, PRIVATE_CHAT, BOT_GOAL_NONE, DEFAULT_BOT_DIFFICULTY, DEFAULT_TEAM_NAME_1,
    DEFAULT_TEAM_NAME_2, BOT_GOAL_KILL_THINGS,
)
from trosnoth.levels.hvm import HumansVsMachinesBotManager
from trosnoth.levels.maps import MapAPI, DefaultLobbyMap
from trosnoth.messages import (
    ChatMsg, PlaySoundMsg, UpdateGameInfoMsg, ChatFromServerMsg,
    SetTeamNameMsg, RemovePlayerMsg, RemoveProjectileMsg, SetPlayerCoinsMsg,
)
from trosnoth.model.player import Player
from trosnoth.model.team import Team
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.base import StatTrigger, StatType, Trigger
from trosnoth.triggers.lobby import (
    AddBotsForLobbyTrigger, MakeNewPlayersNeutralTrigger,
    StartGameWhenReadyTrigger,
)
from trosnoth.utils.aio import as_future
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)

SELECTABLE_TEAMS = 'Flexible teams'
FORCE_RANDOM_TEAMS = 'Random teams (no choice)'
HVM_TEAMS = 'Humans vs. Machines'


def preferred_team_otherwise_smallest(preferred_team, universe, include_bots=False):
    if preferred_team is not None:
        return preferred_team

    team_sizes = {t: 0 for t in universe.teams}
    for player in universe.players:
        if player.team in team_sizes and (include_bots or not player.bot):
            team_sizes[player.team] = team_sizes[player.team] + 1

    smallest_size = min(team_sizes.values())
    options = [t for t, v in team_sizes.items() if v == smallest_size]
    return random.choice(options)


class BotController:
    '''
    This class exists as an interface between the level and a PuppetBot. At
    the moment it just proxies orders through to the bot, but ultimately the
    bot will be running in a separate process.
    '''

    def __init__(self, agent):
        self.agent = agent
        self._bot = agent.ai
        self.onOrderFinished = self._bot.onOrderFinished

    @property
    def player(self):
        return self._bot.player

    def standStill(self):
        return self._bot.standStill()

    def moveToPoint(self, pos):
        return self._bot.moveToPoint(pos)

    def move_to_room(self, room):
        return self._bot.move_to_room(room)

    def move_to_orb(self, room):
        return self._bot.move_to_orb(room)

    def attackPlayer(self, player):
        return self._bot.attackPlayer(player)

    def followPlayer(self, player):
        return self._bot.followPlayer(player)

    def collectTrosball(self):
        return self._bot.collectTrosball()

    def respawn(self, zone=None):
        return self._bot.respawn(zone)

    def setAggression(self, aggression):
        return self._bot.setAggression(aggression)

    def set_dodges_bullets(self, dodges_bullets):
        return self._bot.set_dodges_bullets(dodges_bullets)

    def setUpgradePolicy(self, upgrade, coinBuffer=0, delay=0):
        return self._bot.setUpgradePolicy(upgrade, coinBuffer, delay)


@dataclasses.dataclass
class LevelOptions:
    team_option_index: int = 0
    map_index: int = 0
    duration: Optional[float] = None

    def get_duration(self, level):
        return self.duration if self.duration is not None else level.default_duration

    def get_team_option(self, level):
        return level.team_selection[self.team_option_index]

    def get_map(self, level) -> MapAPI:
        return level.map_selection[self.map_index]

    def apply_map_layout(self, level):
        return self.get_map(level).apply(level)


RESERVED_TEAM_NAMES = {'machines'}


def get_preferred_team_name(players, default=None):
    preferences = {}
    for p in players:
        if p.suggested_team_name and not p.bot:
            suggestion = p.suggested_team_name.strip()
            if suggestion.lower() in RESERVED_TEAM_NAMES:
                continue
            preferences[suggestion] = preferences.get(suggestion, 0) + 1

    if not preferences:
        return default

    return max(preferences, key=preferences.get)


def get_preferred_scenario(game, players):
    counts = {}
    for player in players:
        choice = player.suggested_scenario_class
        if choice is None:
            continue
        hvm = player.suggested_scenario_hvm
        counts[choice, hvm] = counts.get((choice, hvm), 0) + 1

    if counts:
        level_class, hvm = max(counts, key=counts.get)
    else:
        from trosnoth.levels.registry import scenario_options
        from trosnoth.levels.standard import StandardRandomLevel
        if random.random() >= .5:
            level_class = StandardRandomLevel
        else:
            level_class = random.choice(scenario_options)

        if HVM_TEAMS in level_class.team_selection:
            hvm = random.random() > .7
        else:
            hvm = False

    level_options = LevelOptions(
        duration=get_preferred_duration(game, players),
        map_index=get_preferred_map_index(level_class, players),
    )
    if hvm:
        level_options.team_option_index = level_class.team_selection.index(HVM_TEAMS)
    return level_class(level_options=level_options)


def get_preferred_duration(game, players):
    lobby_settings = game.lobbySettings
    forced_duration = lobby_settings.get_forced_duration() if lobby_settings else None
    if forced_duration:
        return forced_duration * 60

    counts = {}
    for player in players:
        duration = player.suggested_duration
        counts[duration] = counts.get(duration, 0) + 1

    if not counts:
        return None

    return max(counts, key=counts.get) or None


def get_preferred_map_index(level_class, players):
    index_by_code = {map_class.code: i for i, map_class in enumerate(level_class.map_selection)}
    counts = {}
    for player in players:
        if player.suggested_map in index_by_code:
            index = index_by_code[player.suggested_map]
            counts[index] = counts.get(index, 0) + 1

    if not counts:
        return 0
    return max(counts, key=counts.get)


HUMANS_TEAM_NAME = 'Humans'
MACHINES_TEAM_NAME = 'Machines'


class LevelStats:
    def __init__(self, level):
        self.level = level
        self.paused = True
        self.triggers = []
        self.player_info_tracker = None

    def add_triggers(self, triggers: Iterable[StatTrigger]):
        for trigger in triggers:
            self.add_stat_trigger(trigger)

    def add_stat_trigger(self, trigger: StatTrigger):
        self.triggers.append(trigger)
        if self.paused and trigger.active:
            trigger.deactivate()
        elif not (self.paused or trigger.active):
            trigger.activate()

    def pause(self):
        self.paused = True
        for trigger in self.triggers:
            trigger.deactivate()
        if self.player_info_tracker:
            self.player_info_tracker.deactivate()

    def resume(self):
        self.paused = False
        for trigger in self.triggers:
            trigger.activate()
        if self.player_info_tracker is None:
            self.player_info_tracker = PlayerInfoTracker(self.level)
        self.player_info_tracker.activate()

    def freeze(self):
        if self.player_info_tracker:
            player_info = self.player_info_tracker.dump_player_info()
        else:
            player_info = set()
        match_stats = []
        team_stats = []
        player_stats = []
        for trigger in self.triggers:
            try:
                for item in trigger.get_match_stats():
                    match_stats.append(item)
            except Exception:
                log.exception('Error freezing match stats')

            try:
                for item in trigger.get_team_stats():
                    team_stats.append(item)
            except Exception:
                log.exception('Error freezing team stats')

            try:
                for item in trigger.get_player_stats():
                    player_stats.append(item)
            except Exception:
                log.exception('Error freezing player stats')

        return FrozenLevelStats(match_stats, team_stats, player_info, player_stats)


class PlayerInfoTracker(Trigger):
    def __init__(self, level):
        super().__init__(level)
        self.player_info = set()

    def doActivate(self):
        self.world.on_player_join_complete.addListener(
            self.got_player_join_complete, lifespan=self.lifespan)
        self.world.onPlayerRemoved.addListener(self.got_player_removed, lifespan=self.lifespan)
        for player in self.world.players:
            self.update_player(player)

    def dump_player_info(self):
        for player in self.world.players:
            self.update_player(player)
        return set(self.player_info)

    def got_player_join_complete(self, player):
        self.update_player(player)

    def got_player_removed(self, player, old_id):
        self.update_player(player, id_=old_id)

    def update_player(self, player, id_=None):
        info = PlayerInfo(player, id_=id_)
        self.player_info.discard(info)
        self.player_info.add(info)


class PlayerInfo:
    def __init__(self, player, id_=None, nick=None, team=None, bot=None, username=None):
        if player is None:
            self.key = (None, nick)
            self.nick = nick
            self.team = team
            self.bot = bot
            self.username = username
        else:
            if player.user:
                self.key = (player.user, None)
                self.username = player.user.username
            else:
                self.key = (None, nick or player.nick)
                self.username = None
            self.nick = player.nick
            self.team = player.team
            self.bot = player.bot

    @classmethod
    def rebuild(cls, world, data, id_):
        nick, team_id, username, bot = data
        return cls(
            None,
            id_=id_,
            nick=nick,
            team=world.getTeam(team_id),
            bot=bot,
            username=username,
        )

    def __eq__(self, other):
        return type(self) == type(other) and self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f'{type(self).__name__}(nick={self.nick!r}, team={self.team!r})'

    def __repr__(self):
        return f'{type(self).__name__}(key={self.key!r}, nick={self.nick!r}, team={self.team!r})'

    def dump(self, *, for_db=False):
        if for_db:
            return {
                'n': self.nick,
                't': self.team.id if self.team else NEUTRAL_TEAM_ID,
                'u': self.username,
                'b': self.bot,
            }
        return [
            self.nick,
            self.team.id if self.team else NEUTRAL_TEAM_ID,
            self.username,
            self.bot,
        ]


@dataclasses.dataclass
class FrozenLevelStats:
    match_stats: list[tuple[str, StatType, float]]
    team_stats: list[tuple[str, StatType, dict[Team, float]]]
    player_info: set[PlayerInfo]
    player_stats: list[tuple[str, StatType, dict[PlayerInfo, float]]]

    @staticmethod
    def dump(instance, *, for_db=False):
        if instance is None:
            return None
        player_list = []
        player_index = {}
        for info in instance.player_info:
            player_index[info] = len(player_list)
            player_list.append(info.dump(for_db=for_db))
        return (
            [(name, int(stat_type), value) for name, stat_type, value in instance.match_stats],
            [(name, int(stat_type), {team.id: value for team, value in stats.items()})
                for name, stat_type, stats in instance.team_stats],
            player_list,
            [(name, int(stat_type), {
                player_index[player_info]: value for player_info, value in stats.items()})
                for name, stat_type, stats in instance.player_stats],
        )

    @classmethod
    def rebuild(cls, world, data):
        if data is None:
            return None
        match_data, team_data, player_info_data, player_stat_data = data
        match_stats = [(name, StatType(stat_type), value) for name, stat_type, value in match_data]
        team_stats = [
            (name, StatType(stat_type), {
                world.getTeam(team_id): value for team_id, value in stats.items()})
            for name, stat_type, stats in team_data
        ]
        player_list = [
            PlayerInfo.rebuild(world, data, i)
            for i, data in enumerate(player_info_data)]

        player_stats = [
            (name, StatType(stat_type), {
                player_list[index]: value for index, value in stats.items()})
            for name, stat_type, stats in player_stat_data
        ]
        return cls(match_stats, team_stats, set(player_list), player_stats)

    @staticmethod
    def sort_stats(sub_stats, all_keys):
        def team_sort_key(key):
            return tuple(-1e6 if (s := stat_dict.get(key)) is None else s
                for name, kind, stat_dict in sub_stats)

        teams = sorted(all_keys, key=team_sort_key, reverse=True)

        best_stats = {}

        titles = []
        for i, (stat_name, kind, stat_dict) in enumerate(sub_stats):
            titles.append(stat_name)
            best_stats[i] = 0.995 * max(stat_dict.values()) if stat_dict else 0

        rows = []
        for team in teams:
            row = []
            rows.append((team, row))
            for i, (stat_name, stat_kind, stat_dict) in enumerate(sub_stats):
                value = stat_dict.get(team)
                row.append((
                    value,
                    StatType(stat_kind).format(value),
                    value is not None and value >= best_stats[i],
                ))

        return titles, rows


@dataclasses.dataclass
class LevelResult:
    scenario_name: str
    a_human_player_won: bool
    winning_players: List[Player]
    winning_teams: List[Team]
    tutorial_score: Optional[float] = None
    stats: Optional[FrozenLevelStats] = None

    def dump(self, world):
        data = {
            'name': self.scenario_name,
            'human_won': self.a_human_player_won,
            'tut_score': self.tutorial_score,
            'win_players': None if self.winning_players is None
                else [p.id for p in self.winning_players],
            'win_teams': None if self.winning_teams is None
                else [t.id for t in self.winning_teams],
            'stats': FrozenLevelStats.dump(self.stats),
        }
        return msgpack.packb(data, use_bin_type=True)

    @classmethod
    def rebuild(cls, world, data_string):
        data = msgpack.unpackb(data_string, raw=False, strict_map_key=False)
        return cls(
            scenario_name=data['name'],
            a_human_player_won=bool(data['human_won']),
            tutorial_score=None if (d := data['tut_score']) is None else float(d),
            winning_players=[world.getPlayer(p_id) for p_id in data['win_players']]
                if data['win_players'] is not None else None,
            winning_teams=[world.getTeam(t_id) for t_id in data['win_teams']]
                if data['win_teams'] is not None else None,
            stats=FrozenLevelStats.rebuild(world, data['stats']),
        )


class Level(object):
    '''
    Base class for all standard and custom levels. A level provides
    server-only instructions about how a particular game is set up and
    operates.

    NOTE that clients know nothing about what level is being used, so any
    events that affect world state need to be carried out through the
    message-passing API in order that clients stay in sync with the server.
    '''

    recordGame = True
    resetPlayerCoins = True
    levelName = None

    default_duration: float
    team_selection = ('Scenario default',)
    map_selection = (None,)

    # Any level that can be selected in-game or in the server web
    # interface must define a string level_code value.
    level_code = None

    # If hvm_level_name is set, it will show up in the level options
    # lists. If it's not set, Humans vs. Machines will not be avalaible
    # for this level kind.
    hvm_level_name = None

    coins_for_kills_factor = 1
    coins_for_caps_factor = 1
    respawn_time_factor = 1

    def __init__(self, *args, level_options=None, **kwargs):
        super(Level, self).__init__(*args, **kwargs)
        self.world = None
        self._winner = None
        self.activeTriggers = set()
        self.level_options = level_options or LevelOptions()
        self.on_got_world = Event(['world'])
        self.stats = LevelStats(self)

    def replay(self, **kwargs):
        return type(self)(level_options=self.level_options, **kwargs)

    def set_world(self, world):
        self.world = world
        self.on_got_world(world)

    def begin_hvm(self):
        if self.world.botManager:
            raise RuntimeError('Another BotManager is active')
        if self.world.teams[0].teamName == HUMANS_TEAM_NAME:
            reverse = False
        elif self.world.teams[0].teamName == MACHINES_TEAM_NAME:
            reverse = True
        else:
            reverse = random.randrange(2)
        self.world.botManager = HumansVsMachinesBotManager(self.world, reverse)
        self.world.botManager.startingSoon()

    def pre_sync_setup(self):
        '''
        Called before all world state is synced to clients. This is
        typically used to set up the map, team names, and sometimes team
        allocations.

        The default implementation selects teams based on the selected
        team options. If a scenario is going to generate teams in some
        other way, it should override this method. I.e., it should not call
        super().pre_sync_setup().
        '''
        self.pre_sync_teams_setup()
        self.world.abilities.respawn_time_factor = self.respawn_time_factor

    def pre_sync_teams_setup(self):
        team_option = self.level_options.get_team_option(self)
        if team_option == FORCE_RANDOM_TEAMS:
            self.pre_sync_randomise_teams()
        elif team_option == HVM_TEAMS:
            self.pre_sync_create_hvm_teams()
        else:
            self.pre_sync_create_preferred_teams()

    async def run_lobby_period(self):
        '''
        When hosting a LAN game, this is called after the world state is
        synced to clients. It should take care of setting up and tearing
        down the lobby period, and should call wait_for_ready_players()
        or equivalent to wait until everyone selects ready.

        The default implementation will return all players to ghosts in
        their own territory before returning.
        '''
        self.setUserInfo('Waiting for players…', (
            '* Select "Ready" to start',
        ), BOT_GOAL_KILL_THINGS)
        await self.wait_for_ready_players()

        self.return_players_to_own_territory(alive=False)
        self.remove_all_projectiles()
        self.reset_coins_to_zero()

    def return_players_to_own_territory(self, alive=None):
        for p in self.world.players:
            pos = self.world.select_good_respawn_zone_for_team(p.team).centre
            self.world.magically_move_player_now(p, pos, alive=alive)

    def remove_all_projectiles(self):
        for projectile_id in list(self.world.projectile_by_id):
            self.world.sendServerCommand(RemoveProjectileMsg(projectile_id))

    def reset_coins_to_zero(self):
        for p in self.world.players:
            self.world.sendServerCommand(SetPlayerCoinsMsg(p.id, 0))

    async def wait_for_ready_players(self):
        with self.world.uiOptions.modify(showReadyStates=True), \
                self.world.abilities.modify(
                    leaveFriendlyZones=True, zoneCaps=False, renaming=True):
            while True:
                humans = [p for p in self.world.players if not p.bot]
                if humans and all(p.readyToStart for p in humans):
                    break

                await as_future(self.world.sleep(3))

    def pre_sync_create_teams(self, team_info, neutral_players=(), remove_others=True):
        '''
        Sets team names and players on teams.
        Only call this from pre_sync_setup() as it does not sync changes
        to clients.

        :param team_info: sequence of (team_name, players) for each team
        :param neutral_players: if provided, these players will become
            neutral
        :param remove_others: whether or not to remove players who are
            not mentioned in team_info or neutral_players (default True)
        :return: sequence of teams
        '''
        unseen_players = set(self.world.players)

        team_objects = self.world.teams
        for team, (team_name, players) in zip(team_objects, team_info):
            team.teamName = team_name
            for player in players:
                player.team = team
                unseen_players.discard(player)

        for player in neutral_players:
            player.team = None
            unseen_players.discard(player)

        if remove_others:
            for player in unseen_players:
                self.world.delPlayer(player)

        return self.world.teams

    def pre_sync_randomise_teams(self, set_team_names=True):
        players = list(self.world.players)
        random.shuffle(players)
        group1, group2 = players[:len(players) // 2], players[len(players) // 2:]

        if set_team_names:
            name1 = get_preferred_team_name(group1, DEFAULT_TEAM_NAME_1)
            name2 = get_preferred_team_name(group2, DEFAULT_TEAM_NAME_2)
            if name2 == name1:
                if name1 == DEFAULT_TEAM_NAME_2:
                    name1 = DEFAULT_TEAM_NAME_1
                else:
                    name2 = DEFAULT_TEAM_NAME_2
        else:
            name1 = self.world.teams[0].teamName
            name2 = self.world.teams[1].teamName

        self.pre_sync_create_teams([(name1, group1), (name2, group2)])

    def pre_sync_create_hvm_teams(self):
        config = [(HUMANS_TEAM_NAME, self.world.players), (MACHINES_TEAM_NAME, ())]
        random.shuffle(config)
        self.pre_sync_create_teams(config)

    def pre_sync_create_preferred_teams(self):
        name1 = get_preferred_team_name(self.world.players, DEFAULT_TEAM_NAME_1)
        name2 = get_preferred_team_name(
            (p for p in self.world.players if p.suggested_team_name != name1),
            DEFAULT_TEAM_NAME_1 if name1 == DEFAULT_TEAM_NAME_2 else DEFAULT_TEAM_NAME_2)

        players1 = set()
        players2 = set()
        others = []
        for p in self.world.players:
            if p.suggested_team_name == name1:
                players1.add(p)
            elif p.suggested_team_name == name2:
                players2.add(p)
            else:
                others.append(p)

        random.shuffle(others)
        while others:
            p = others.pop()
            if len(players1) < len(players2):
                players1.add(p)
            elif len(players2) < len(players1):
                players2.add(p)
            else:
                random.choice([players1, players2]).add(p)

        self.pre_sync_create_teams([(name1, players1), (name2, players2)])

    def tearDownLevel(self):
        '''
        Called when a new level is selected, or the server terminates. This
        could be used to tear down event handlers which have been set up.
        '''
        while self.activeTriggers:
            trigger = self.activeTriggers.pop()
            try:
                trigger.deactivate()
            except Exception:
                log.exception('Error tearing down %s', trigger)

    async def run(self) -> LevelResult:
        '''
        Called when the level starts. By this point the Game and World have
        been completely instantiated. When this coroutine returns without any
        errors, the level is deemed to be completed, and the server will
        return to the lobby.
        '''
        # Never return. Levels will override this.
        await asyncio.get_event_loop().create_future()
        return self.build_level_result()

    def build_level_result(self, *, winners=None, **kwargs):
        winning_teams = {t for t in winners if isinstance(t, Team)}
        winning_player_ids = {p.id for p in winners if isinstance(p, Player)}
        winning_players = [
            p for p in self.world.players
            if p.id in winning_player_ids or p.team in winning_teams]
        if 'a_human_player_won' not in kwargs:
            kwargs['a_human_player_won'] = any(not p.bot for p in winning_players)
        return LevelResult(
            scenario_name=self.levelName or self.__class__.__name__,
            stats=self.stats.freeze(),
            winning_players=winning_players,
            winning_teams=list(winning_teams),
            **kwargs,
        )

    def findReasonPlayerCannotJoin(self, game, team_id, user, bot):
        '''
        Checks whether or not another player with the given details can join
        the game. By default, this will respect game.maxTotalPlayers, and
        game.maxPerTeam.

        @param game: the LocalGame object of the current game
        @param team_id: the id of the team that the player will join if
            permitted (calculated from call to getIdOfTeamToJoin().
        @param user: the authentication server user object if this game is
            being run on an authentication server, or None otherwise.
        @param bot: whether or not the requested join is from a bot.

        @return: None if the player can join the game, or a reason constant
            otherwise (e.g. GAME_FULL_REASON, or UNAUTHORISED_REASON).
        '''
        if len(game.world.players) >= game.maxTotalPlayers:
            return GAME_FULL_REASON

        if team_id != NEUTRAL_TEAM_ID:
            if sum(1 for p in game.world.players if p.teamId == team_id) >= game.maxPerTeam:
                return GAME_FULL_REASON

        return None

    def get_team_to_join(self, preferred_team, user, nick, bot):
        '''
        When a player asks to join a game, this method is called to
        decide which team to put them on, assuming that they are allowed
        to join.

        :param preferred_team: the team that the player would like to
            join if possible, or None if the player does not care
        :param user: the authentication server user object if this game
            is being run on an authentication server, or None otherwise.
        :param nick: the player's nick
        :param bot: whether or not the requested join is from a bot.

        :return: a team
        '''

        # Default team selection defers to bot manager
        if self.world.botManager:
            return self.world.botManager.getTeamToJoin(preferred_team, bot)
        if self.level_options.get_team_option(self) == FORCE_RANDOM_TEAMS:
            preferred_team = None
        result = preferred_team_otherwise_smallest(preferred_team, self.world, include_bots=bot)

        if not bot:
            # Restrict to teams humans are allowed to join
            allowed_team_ids = self.world.uiOptions.team_ids_humans_can_join
            team_id = result.id if result else NEUTRAL_TEAM_ID
            if allowed_team_ids and team_id not in allowed_team_ids:
                team_id = random.choice(allowed_team_ids)
                result = self.world.getTeam(team_id)

        return result

    def getWinner(self):
        '''
        Called when the server is saving the stats record for this game.
        Should return the team that has won, or None if the game has drawn.
        If the game is still in progress the Level may return None, or may
        return who is currently in the lead: this will only ever be used if
        the stats are saved half-way through the game and not saved at the
        end (e.g. server crashed).
        '''
        return self._winner

    @defer.inlineCallbacks
    def addBot(self, team, nick, botName='puppet', difficulty=DEFAULT_BOT_DIFFICULTY):
        '''
        Utility function that adds a bot to the game, but bypasses the call
        to findReasonPlayerCannotJoin(), because it is this level that has
        requested the join. By default, creates a PuppetBot which does
        nothing until told.
        '''

        game = self.world.game
        agent = yield game.addBot(
            botName, team=team, fromLevel=True, nick=nick, difficulty=difficulty)
        if agent and agent.player is None:
            yield agent.onPlayerSet.wait()

        defer.returnValue(agent)

    async def addControllableBot(self, team, nick, difficulty=DEFAULT_BOT_DIFFICULTY):
        '''
        Adds a PuppetBot to the game, which does nothing until told.
        '''
        game = self.world.game
        agent = await as_future(game.addBot(
            'puppet', team=team, fromLevel=True, nick=nick, forceLocal=True,
            difficulty=difficulty))
        if agent.player is None:
            await agent.onPlayerSet.wait_future()
        return BotController(agent)

    async def waitForHumans(self, number):
        '''
        Utility function that waits until at least number human players have
        joined the game, then returns a collection of the human players in
        the game.
        '''
        while True:
            humans = [p for p in self.world.players if p.join_complete and not p.bot]
            if len(humans) >= number:
                return humans

            await self.world.onPlayerAdded.wait_future()

    def sendPrivateChat(self, fromPlayer, toPlayer, text):
        fromPlayer.agent.sendRequest(
            ChatMsg(PRIVATE_CHAT, toPlayer.id, text=text.encode()))

    def playSound(self, filename):
        '''
        Utility function to play a sound on all clients. The sound file must
        exist on the client system.
        '''
        self.world.sendServerCommand(PlaySoundMsg(filename.encode('utf-8')))

    def setUserInfo(self, user_title, user_info, bot_goal):
        '''
        Utility function to set the tip that all players get to tell them
        their current objectives. Note that this function sets this tip
        globally for all players.
        '''
        self.world.uiOptions.setDefaultUserInfo(user_title, user_info, bot_goal)
        self.world.uiOptions.set(crowd_kind=bot_goal)
        self.world.sendServerCommand(
            UpdateGameInfoMsg.build(user_title, user_info, bot_goal))

    def notifyAll(self, message, error=False):
        '''
        Sends a notification message to all players and observers.
        '''
        self.world.sendServerCommand(
            ChatFromServerMsg(text=message.encode('utf-8'), error=error))

    def setTeamName(self, team, name):
        self.world.sendServerCommand(SetTeamNameMsg(team.id, name.encode()))


class LobbySettings(object):
    def getAutoStartCountDown(self) -> Optional[float]:
        '''
        :return: Number of seconds before game will automatically start,
            or None for no auto start.
        '''
        raise NotImplementedError(
            '{}.getAutoStartCountDown'.format(self.__class__.__name__))

    def get_forced_size(self):
        raise NotImplementedError('{}.get_forced_size'.format(type(self).__name__))

    def get_forced_duration(self):
        raise NotImplementedError('{}.get_forced_duration'.format(type(self).__name__))

    def get_require_everyone_ready(self):
        raise NotImplementedError(f'{type(self).__name__}.get_require_everyone_ready')


class ServerLobbySettings(LobbySettings):
    def __init__(self, arenaManager):
        super(ServerLobbySettings, self).__init__()
        self.arenaManager = arenaManager

    def getAutoStartCountDown(self):
        record = self.arenaManager.getArenaRecord()
        result = record.autoStartCountDown
        if result < 0:
            return None
        return result

    def get_require_everyone_ready(self):
        record = self.arenaManager.getArenaRecord()
        return record.require_everyone_ready

    def get_forced_duration(self):
        record = self.arenaManager.getArenaRecord()
        return record.force_duration

    def get_forced_size(self):
        record = self.arenaManager.getArenaRecord()
        half_width = record.force_half_width
        height = record.force_height
        if half_width is not None and height is not None:
            return half_width, height
        return None


class LocalLobbySettings(LobbySettings):
    def getAutoStartCountDown(self):
        return None

    def get_forced_duration(self):
        return None

    def get_forced_size(self):
        return None

    def get_require_everyone_ready(self):
        return False


class LobbyLevel(Level):
    recordGame = False
    resetPlayerCoins = False
    levelName = 'Lobby'
    default_duration = None

    def __init__(self, lobbySettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if lobbySettings is None:
            lobbySettings = LocalLobbySettings()
        self.lobbySettings = lobbySettings
        self.require_everyone_ready = False

    def replay(self, **kwargs):
        return super().replay(lobbySettings=self.lobbySettings, **kwargs)

    def pre_sync_teams_setup(self):
        # Keep the existing map, but make all players neutral
        self.pre_sync_create_teams(
            [(DEFAULT_TEAM_NAME_1, ()), (DEFAULT_TEAM_NAME_2, ())],
            neutral_players=self.world.players,
        )
        self.world.uiOptions.team_ids_humans_can_join = [NEUTRAL_TEAM_ID]

    async def run(self):
        MakeNewPlayersNeutralTrigger(self).activate()
        self.world.uiOptions.set(
            showReadyStates=True,
            allow_scenario_voting=True,
            team_name_suggestions=True,
            team_ids_humans_can_join=[NEUTRAL_TEAM_ID],
        )
        AddBotsForLobbyTrigger(self).activate()
        StartGameWhenReadyTrigger(self).activate()
        autoStartTime = self.lobbySettings.getAutoStartCountDown()
        self.require_everyone_ready = self.lobbySettings.get_require_everyone_ready()

        title = 'Lobby'
        userInfo = (
            '* Free for all',
            '* A match will start when enough players select "ready"',
        )
        self.setUserInfo(title, userInfo, BOT_GOAL_NONE)

        self.world.abilities.set(zoneCaps=False, renaming=True)
        self.world.onChangeVoiceChatRooms([], [])

        if autoStartTime is not None:
            self.world.clock.startCountDown(autoStartTime)
            self.world.clock.propagateToClients()
            await self.world.clock.onZero.wait_future()
            self.start_some_game_now()

        # Lobby never finishes until it is canceled because a new level is
        # started.
        await asyncio.get_event_loop().create_future()

        # For the lobby, this result is never actually used
        return self.build_level_result()

    def start_new_game_if_ready(self):
        players = [p for p in self.world.players if not p.bot]
        if not players:
            return
        ready_players = [p for p in players if p.readyToStart]
        ratio = 1 if self.require_everyone_ready else 0.7
        if len(ready_players) < ratio * len(players):
            return

        # Remove players who are not ready
        for p in list(self.world.players):
            if p.bot or not p.readyToStart:
                self.world.sendServerCommand(RemovePlayerMsg(p.id))

        level = get_preferred_scenario(self.world.game, ready_players)
        self.world.scenarioManager.startLevel(level)

    def start_some_game_now(self):
        level = get_preferred_scenario(
            self.world.game, [p for p in self.world.players if not p.bot])
        self.world.scenarioManager.startLevel(level)


class StandardLobbyLevel(LobbyLevel):
    def pre_sync_setup(self):
        super().pre_sync_setup()
        DefaultLobbyMap().apply(self)


def play_level(level, withLogging=True, **kwargs):
    '''
    For testing new Levels - launches Trosnoth in single player mode with
    the given level.
    '''
    import sys
    from trosnoth.run.solotest import launch_solo_game
    from trosnoth.welcome.common import initialise_qt_application

    initialise_qt_application()

    if withLogging:
        from trosnoth.utils.utils import initLogging
        initLogging()

    if '--profile' in sys.argv[1:]:
        import cProfile
        from trosnoth.utils.profiling import KCacheGrindOutputter
        prof = cProfile.Profile()

        try:
            prof.runcall(launch_solo_game, level=level, **kwargs)
        except (SystemExit, asyncio.CancelledError):
            pass
        finally:
            kg = KCacheGrindOutputter(prof)
            with open('{}.log'.format(level.__class__.__name__), 'w') as f:
                kg.output(f)
    else:
        try:
            launch_solo_game(level=level, **kwargs)
        except asyncio.CancelledError:
            pass


def run_bot_match(
        level, ai_class1, ai_class2,
        difficulty1=DEFAULT_BOT_DIFFICULTY, difficulty2=DEFAULT_BOT_DIFFICULTY,
        team_size=3, with_logging=True,
        **kwargs):
    from trosnoth.run.solotest import launch_solo_game

    if with_logging:
        from trosnoth.utils.utils import initLogging
        initLogging()

    bot_teams = (
        [(ai_class1, difficulty1)] * team_size,
        [(ai_class2, difficulty2)] * team_size,
    )
    launch_solo_game(
        level=level, bots_only=True, add_bots=bot_teams,
        return_when_level_completes=True,
        **kwargs)
