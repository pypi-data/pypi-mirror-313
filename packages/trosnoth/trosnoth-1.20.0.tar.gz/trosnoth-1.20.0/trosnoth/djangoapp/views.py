# coding: utf-8

import atexit
import csv
import logging
import operator
import os
import sys

from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
import msgpack

from trosnoth.const import POINT_VALUES, TEAM_1_COLOUR, TEAM_2_COLOUR
from trosnoth.gamerecording.achievementlist import availableAchievements
from trosnoth.levels.base import FrozenLevelStats
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.model.upgrades import upgradeOfType
from trosnoth.triggers.base import StatType
from trosnoth.utils.utils import filename_with_suffix, shade

from .models import (
    TrosnothServerSettings, TrosnothUser, GameRecord, PlayerKills,
    UpgradesUsedInGameRecord, TrosnothArena, Tournament,
    AchievementProgress, PlayerInGame,
)

log = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    context = {
        'settings': TrosnothServerSettings.get(),
    }
    return render(request, 'trosnoth/index.html', context)


@permission_required('trosnoth.manage_arena')
def manageArena(request, arenaId):
    from .forms import ArenaModelForm, ArenaControlForm

    try:
        arenaId = int(arenaId)
        arenaRecord = TrosnothArena.objects.get(id=arenaId)
    except (TypeError, KeyError, TrosnothArena.DoesNotExist):
        raise Http404('Arena not found')

    if request.method == 'POST':
        modelForm = ArenaModelForm(request.POST, instance=arenaRecord)
        controlForm = ArenaControlForm(request.POST)
        if modelForm.is_valid() and controlForm.is_valid():
            # Save the model
            modelForm.save(commit=True).save()

            # Apply control commands
            setArenaInfo(arenaId, {
                'paused': controlForm.cleaned_data['paused'],
                'teamAbilities': {
                    'blue': {
                        'shots': controlForm.cleaned_data['blueShots'],
                        'caps': controlForm.cleaned_data['blueCaps'],
                    },
                    'red': {
                        'shots': controlForm.cleaned_data['redShots'],
                        'caps': controlForm.cleaned_data['redCaps'],
                    },
                },
                'action': 'shutdown' if not arenaRecord.enabled
                    else controlForm.cleaned_data['action'],
            })

            # Redirect to clear the POST data
            return redirect('trosnoth:arena', arenaId=arenaId)

    arenaInfo = getArenaInfo(arenaId)
    if request.method != 'POST':
        modelForm = ArenaModelForm(instance=arenaRecord)
        controlForm = ArenaControlForm(initial={
            'paused': arenaInfo['paused'],
            'blueShots': arenaInfo['blue']['shots'],
            'blueCaps': arenaInfo['blue']['caps'],
            'redShots': arenaInfo['red']['shots'],
            'redCaps': arenaInfo['red']['caps'],
        })

    context = {
        'loneArena': TrosnothArena.objects.count() == 1,
        'settings': TrosnothServerSettings.get(),
        'arena': arenaRecord,
        'info': arenaInfo,
        'controlForm': controlForm,
        'modelForm': modelForm,
    }
    return render(request, 'trosnoth/arena.html', context)


@permission_required('trosnoth.manage_arena')
def newArena(request):
    from .forms import ArenaModelForm

    arenaRecord = TrosnothArena()

    if request.method == 'POST':
        modelForm = ArenaModelForm(request.POST, instance=arenaRecord)
        if modelForm.is_valid():
            # Save the model
            modelForm.save(commit=True).save()

            # Redirect to clear the POST data
            return redirect('trosnoth:arenas')

    if request.method != 'POST':
        modelForm = ArenaModelForm(instance=arenaRecord)

    context = {
        'loneArena': False,
        'settings': TrosnothServerSettings.get(),
        'arena': arenaRecord,
        'modelForm': modelForm,
    }
    return render(request, 'trosnoth/arena.html', context)


@permission_required('trosnoth.manage_arena')
def deleteArena(request, arenaId):
    try:
        arenaId = int(arenaId)
        arenaRecord = TrosnothArena.objects.get(id=arenaId)
    except (TypeError, KeyError, TrosnothArena.DoesNotExist):
        raise Http404('Arena not found')

    if request.method == 'POST':
        if request.POST.get('cancel'):
            return redirect('trosnoth:arena', arenaId=arenaId)
        arenaRecord.delete()
        return redirect('trosnoth:arenas')

    context = {
        'settings': TrosnothServerSettings.get(),
        'heading': 'Delete arena',
        'message': 'Are you sure you want to delete "{}"?'.format(arenaRecord),
        'button': 'Delete',
    }
    return render(request, 'trosnoth/confirm.html', context)


@permission_required('trosnoth:manage_arena')
def startLevel(request, arenaId):
    from .forms import SelectLevelForm

    try:
        arenaId = int(arenaId)
        arenaRecord = TrosnothArena.objects.get(id=arenaId)
    except (TypeError, KeyError, TrosnothArena.DoesNotExist):
        raise Http404('Arena not found')

    if request.method == 'POST':
        if request.POST.get('cancel'):
            return redirect('trosnoth:arena', arenaId=arenaId)

        form = SelectLevelForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['scenario']:
                if form.cleaned_data['duration'] == 0:
                    form.cleaned_data['duration'] = None
                startLevelInArena(arenaId, form.cleaned_data)
            return redirect('trosnoth:arena', arenaId=arenaId)

    else:
        form = SelectLevelForm()

    context = {
        'settings': TrosnothServerSettings.get(),
        'arena': arenaRecord,
        'loneArena': TrosnothArena.objects.count() == 1,
        'form': form,
    }
    return render(request, 'trosnoth/scenario.html', context)


def profile_by_username(request, username):
    try:
        user = TrosnothUser.from_user(username=username)
    except User.DoesNotExist:
        raise Http404('User not found')

    return redirect('trosnoth:profile', userId=user.user.pk, nick=user.nick)


def userProfile(request, userId, nick=None):
    try:
        user = TrosnothUser.from_user(pk=userId)
    except User.DoesNotExist:
        raise Http404('User not found')

    if user.nick != nick:
        return redirect(
            'trosnoth:profile', userId=user.user.pk, nick=user.nick)

    unlockedIds = {a.achievementId for a in AchievementProgress.objects.filter(
        user=user, unlocked=True)}

    unlocked = []
    locked = []

    for achievementClass in availableAchievements.all:
        idString = achievementClass.idstring.decode('Latin-1')
        if finders.find('trosnoth/achievements/{}.png'.format(idString)):
            imageId = idString
        else:
            imageId = 'default'

        info = {
            'name': achievementClass.name,
            'description': achievementClass.description,
            'imageId': imageId,
        }
        if idString in unlockedIds:
            unlockedIds.remove(idString)
            unlocked.append(info)
        else:
            locked.append(info)

    for idString in unlockedIds:
        if finders.find('trosnoth/achievements/{}.png'.format(idString)):
            imageId = idString
        else:
            imageId = 'default'

        unlocked.append({
            'name': idString,
            'description': (
                'This achievement does not exist in this version of Trosnoth'),
            'imageId': imageId,
        })

    unlocked.sort(key=lambda a: a['name'])
    locked.sort(key=lambda a: a['name'])

    context = {
        'settings': TrosnothServerSettings.get(),
        'trosnothUser': user,
        'unlocked': unlocked,
        'locked': locked,
    }
    return render(request, 'trosnoth/user.html', context)


def userList(request):
    context = {
        'settings': TrosnothServerSettings.get(),
        'users': TrosnothUser.objects.order_by('-lastSeen'),
    }
    return render(request, 'trosnoth/userlist.html', context)


def viewGame(request, gameId):
    game = GameRecord.objects.get(pk=gameId)

    data = []

    for player in game.gameplayer_set.all():
        entry = {
            'player': player,
            'nick': player.getNick(),
            'accuracy': (100.0 * player.shotsHit / player.shotsFired
                ) if player.shotsFired else 0.,
            'score': 0,
            'kdr': '{:2.2f}'.format(player.kills / player.deaths
                ) if player.deaths else '∞',
            'adr': '{:2.2f}'.format(player.timeAlive / player.timeDead
                ) if player.timeDead else '∞',
        }

        for stat, weighting in list(POINT_VALUES.items()):
            if stat in entry:
                value = entry[stat]
            else:
                value = getattr(player, stat)
            entry['score'] += value * weighting

        data.append(entry)

    data.sort(key=(lambda entry: entry['score']), reverse=True)

    i = 1
    j = 0
    for entry in data:
        entry['index'] = j
        if entry['player'].bot:
            entry['rank'] = 'B'
        else:
            entry['rank'] = str(i)
            i += 1
        j += 1

    killData = {}
    for pkr in PlayerKills.objects.filter(killee__game=game):
        killData[pkr.killer, pkr.killee] = pkr.count

    killTable = []
    for killerEntry in data:
        killer = killerEntry['player']
        killRow = []
        maxKillCount = maxDeathCount = 0
        maxKill = maxDeath = '-'
        for killeeEntry in data:
            killee = killeeEntry['player']
            count = killData.get((killer, killee), 0)
            killRow.append(count)
            if count > maxKillCount:
                maxKillCount = count
                maxKill = '{} ({})'.format(killeeEntry['nick'], count)
            dieCount = killData.get((killee, killer), 0)
            if dieCount > maxDeathCount:
                maxDeathCount = dieCount
                maxDeath = '{} ({})'.format(killeeEntry['nick'], dieCount)
        killerEntry['maxKill'] = maxKill
        killerEntry['maxDeath'] = maxDeath

        killTable.append({
            'player': killerEntry['player'],
            'nick': killerEntry['nick'],
            'entries': killRow,
        })

    for i in range(len(killTable)):
        killTable[i]['entries'][i] = '-'

    otherKills = [
        killData.get((None, killeeEntry['player']), 0)
        for killeeEntry in data
    ]

    upgradeData = {}
    upgradeCodes = set()
    for ur in UpgradesUsedInGameRecord.objects.filter(gamePlayer__game=game):
        upgradeData[ur.gamePlayer, ur.upgrade] = ur.count
        upgradeCodes.add(ur.upgrade)

    if upgradeCodes:
        nameAndCode = []
        for code in upgradeCodes:
            bytesCode = code.encode('ascii')
            if bytesCode in upgradeOfType:
                name = upgradeOfType[bytesCode].name
            else:
                name = '?{}?'.format(code)
            nameAndCode.append((name, code))

        nameAndCode.sort()
        upgradeList = [name for name, code in nameAndCode]
        upgradeTable = []
        for entry in data:
            entries = []
            maxUpgrade = '-'
            maxUpgradeCount = 0
            for name, code in nameAndCode:
                count = upgradeData.get((entry['player'], code), 0)
                entries.append(count)
                if count > maxUpgradeCount:
                    maxUpgrade = '{} ({})'.format(name, count)
                    maxUpgradeCount = count

            entry['maxUpgrade'] = maxUpgrade

            upgradeTable.append({
                'player': entry['player'],
                'nick': entry['nick'],
                'entries': entries,
            })
    else:
        upgradeList = []
        upgradeTable = []

    if game.teamScoresEnabled and game.playerScoresEnabled:
        teamPlayers = {}
        for player in game.gameplayer_set.all():
            teamPlayers.setdefault(player.team, []).append((
                player.boardScore,
                player.getNick(),
                'team' + player.team + 'player',
            ))

        teams = sorted([
            (game.blueTeamScore, game.blueTeamName, 'A'),
            (game.redTeamScore, game.redTeamName, 'B'),
        ], reverse=True) + [('', 'Rogue', '')]
        scoreboard = []
        for score, name, team in teams:
            players = teamPlayers.get(team)
            if not (players or score):
                continue
            scoreboard.append((score, name, 'team' + team))
            players.sort(reverse=True)
            scoreboard.extend(players)
    elif game.teamScoresEnabled:
        scoreboard = sorted([
            (game.blueTeamScore, game.blueTeamName, 'teamA'),
            (game.redTeamScore, game.redTeamName, 'teamB')], reverse=True)
    elif game.playerScoresEnabled:
        scoreboard = sorted([(
            player.boardScore,
            player.getNick(),
            'team' + player.team + 'player',
        ) for player in game.gameplayer_set.all()], reverse=True)
    else:
        scoreboard = []

    if game.scenario in ('Trosnoth Match', 'Solo Rules Trosnoth') and data:
        winPoints, losePoints = _getMatchTournamentScores( game)
        tournamentPoints = '{:.2f} vs. {:.2f}'.format(winPoints, losePoints)
    else:
        tournamentPoints = ''

    if game.stats is None:
        match_stats = None
        team_stat_titles = None
        team_stats = None
        player_stat_titles = None
        player_stats = None
        scenario_completed = None
        winning_players = []
    else:
        scoreboard = []
        scenario_completed = game.scenario_completed
        stats = msgpack.unpackb(game.stats, raw=False, strict_map_key=False)
        match_data, team_data, player_info_data, player_stat_data = stats
        match_stats = [
            (name, StatType(stat_type).format(value))
            for name, stat_type, value in match_data
        ]
        teams = {
            b'A': (game.blueTeamName, shade(TEAM_1_COLOUR, .5, .5)),
            b'B': (game.redTeamName, shade(TEAM_2_COLOUR, .5, .5)),
            NEUTRAL_TEAM_ID: ('Rogue', (128, 128, 128)),
        }
        team_stat_titles, team_data = FrozenLevelStats.sort_stats(
            team_data, sorted(teams.keys()))
        team_stats = [(*teams[team_id], values) for team_id, values in team_data]

        player_stat_titles, player_data = FrozenLevelStats.sort_stats(
            player_stat_data, range(len(player_info_data)))
        player_stats = [{
            'player': PlayerInGame.objects.get(game=game, index=i),
            'nick': player_info_data[i]['n'],
            'colour': teams[player_info_data[i]['t']][1],
            'stats': values,
        } for i, values in player_data]
        winning_players = [ps for ps in player_stats if ps['player'].winner]

    context = {
        'settings': TrosnothServerSettings.get(),
        'game': game,
        'playerData': data,
        'killTable': killTable,
        'otherKills': otherKills if any(otherKills) else None,
        'upgrades': upgradeList,
        'upgradeTable': upgradeTable,
        'scoreboard': scoreboard,
        'tournamentPoints': tournamentPoints,
        'match_stats': match_stats,
        'team_stat_titles': team_stat_titles,
        'team_stats': team_stats,
        'player_stat_titles': player_stat_titles,
        'player_stats': player_stats,
        'scenario_completed': scenario_completed,
        'winning_players': winning_players,
    }
    return render(request, 'trosnoth/viewgame.html', context)


def _get_zone_scores(match):
    teamTournamentScores = {}

    for player in match.gameplayer_set.all():
        teamTournamentScores[player.team] = teamTournamentScores.get(
            player.team, 0) + player.zoneScore

    blueScore = teamTournamentScores.get('A', 0)
    redScore = teamTournamentScores.get('B', 0)
    if blueScore == redScore == 0:
        # Old game, from before these things were recorded
        return 0, 0

    winZoneScore = max(blueScore, redScore)
    loseZoneScore = min(blueScore, redScore)

    return winZoneScore, loseZoneScore


def _getMatchTournamentScores(match):
    winZoneScore, loseZoneScore = _get_zone_scores(match)
    if winZoneScore == loseZoneScore == 0:
        return 10, 10
    winTournamentPoints = (
        10 + 10 * winZoneScore ** 1.5
        / (winZoneScore ** 1.5 + loseZoneScore ** 1.5))
    loseTournamentPoints = 20 - winTournamentPoints
    return winTournamentPoints, loseTournamentPoints


def tournament(request, tournamentId):
    tournament = Tournament.objects.get(pk=tournamentId)

    mainInfo = {}
    hvmInfo = {}
    noveltyInfo = {}
    gameByGame = []

    for match in tournament.matches.all():
        matchDescription = '?'
        if match.scenario in ('Trosnoth Match', ''):
            winScore, loseScore = _getMatchTournamentScores(match)
            if not match.winningTeam:
                matchDescription = '{} vs. {} [10.0 : 10.0]'.format(
                    match.blueTeamName, match.redTeamName)
            else:
                if match.winningTeam == 'A':
                    winner = match.blueTeamName
                    loser = match.redTeamName
                else:
                    winner = match.redTeamName
                    loser = match.blueTeamName
                matchDescription = '{} vs. {} [{:.1f} : {:.1f}]'.format(
                    winner, loser, winScore, loseScore)

            if {match.blueTeamName, match.redTeamName} == {
                    'Humans', 'Machines'}:
                teams = {'A': match.blueTeamName, 'B': match.redTeamName}
                for teamId, teamName in teams.items():
                    if teamName not in hvmInfo:
                        hvmInfo[teamName] = {
                            'team': teamName,
                            'score': 0,
                            'winCount': 0,
                            'playCount': 0,
                        }
                    record = hvmInfo[teamName]
                    record['playCount'] += 1
                    if teamId == match.winningTeam:
                        record['winCount'] += 1
                        record['score'] += winScore
                    else:
                        record['score'] += loseScore
            else:
                for player in match.gameplayer_set.all():
                    if player.user:
                        playerKey = 'p' + str(player.user.pk)
                    else:
                        playerKey = 'b' + player.botName

                    if playerKey not in mainInfo:
                        mainInfo[playerKey] = {
                            'user': player.user,
                            'nick': player.getNick(),
                            'score': 0,
                            'winCount': 0,
                            'playCount': 0,
                        }
                    record = mainInfo[playerKey]
                    record['playCount'] += 1
                    if player.team == match.winningTeam:
                        record['winCount'] += 1
                        record['score'] += winScore
                    else:
                        record['score'] += loseScore
        elif match.playerScoresEnabled:
            maxScore = 0
            winners = []

            for player in match.gameplayer_set.all():
                if player.boardScore == maxScore:
                    winners.append(player)
                elif player.boardScore > maxScore:
                    winners = [player]
                    maxScore = player.boardScore

            for player in winners:
                if player.user:
                    playerKey = 'p' + str(player.user.pk)
                else:
                    playerKey = 'b' + player.botName

                if playerKey not in noveltyInfo:
                    noveltyInfo[playerKey] = {
                        'user': player.user,
                        'nick': player.getNick(),
                        'score': 0,
                        'scenarios': [],
                    }
                record = noveltyInfo[playerKey]
                record['score'] += 1
                record['scenarios'].append(match.scenario)

            matchDescription = '{} won'.format(
                ', '.join(sorted(w.getNick() for w in winners)))
        else:
            matchDescription = '{} vs {}, {}'.format(
                match.blueTeamName, match.redTeamName, match.getScoreString())
            if match.winningTeam:
                if match.winningTeam == 'A':
                    winner = match.blueTeamName
                    loser = match.redTeamName
                else:
                    winner = match.redTeamName
                    loser = match.blueTeamName

                for player in match.gameplayer_set.all():
                    if player.team != match.winningTeam:
                        continue
                    if player.user:
                        playerKey = 'p' + str(player.user.pk)
                    else:
                        playerKey = 'b' + player.botName

                    if playerKey not in noveltyInfo:
                        noveltyInfo[playerKey] = {
                            'user': player.user,
                            'nick': player.getNick(),
                            'score': 0,
                            'scenarios': [],
                        }
                    record = noveltyInfo[playerKey]
                    record['score'] += 1
                    record['scenarios'].append(match.scenario)

        gameByGame.append({
            'game': match,
            'description': matchDescription,
        })

    mainStandings = sorted(
        mainInfo.values(), key=operator.itemgetter('score'), reverse=True)
    lastRank, lastScore = 1, 0
    for i, record in enumerate(mainStandings):
        if record['score'] == lastScore:
            record['rank'] = lastRank
        else:
            record['rank'] = i + 1
            lastScore = record['score']
            lastRank = record['rank']

    hvmStandings = sorted(
        hvmInfo.values(), key=operator.itemgetter('score'), reverse=True)
    lastRank, lastScore = 1, 0
    for i, record in enumerate(hvmStandings):
        if record['score'] == lastScore:
            record['rank'] = lastRank
        else:
            record['rank'] = i + 1
            lastScore = record['score']
            lastRank = record['rank']

    noveltyStandings = sorted(
        noveltyInfo.values(), key=operator.itemgetter('score'), reverse=True)
    lastRank, lastScore = 1, 0
    for i, record in enumerate(noveltyStandings):
        if record['score'] == lastScore:
            record['rank'] = lastRank
        else:
            record['rank'] = i + 1
            lastScore = record['score']
            lastRank = record['rank']

        scenarioCounts = {}
        bestScenarios = []
        mostRepeats = 0
        for scenario in record['scenarios']:
            n = scenarioCounts[scenario] = scenarioCounts.get(scenario, 0) + 1
            if n > mostRepeats:
                bestScenarios = [scenario]
                mostRepeats = n
            elif n == mostRepeats:
                bestScenarios.append(scenario)
        record['bestScenario'] = ', '.join(sorted(bestScenarios))


    context = {
        'settings': TrosnothServerSettings.get(),
        'tournament': tournament,
        'mainStandings': mainStandings,
        'hvmStandings': hvmStandings,
        'noveltyStandings': noveltyStandings,
        'gameByGame': gameByGame,
    }
    return render(request, 'trosnoth/tournament.html', context)


def gameList(request):
    context = {
        'settings': TrosnothServerSettings.get(),
        'games': GameRecord.objects.order_by('-started'),
        'tournaments': Tournament.objects.all(),
    }
    return render(request, 'trosnoth/gamelist.html', context)


def csv_games_list(request):
    response = HttpResponse(content_type='text/csv')

    team_names = {'A': 'Blue', 'B': 'Red'}

    writer = csv.writer(response)
    writer.writerow([
        'Game ID', 'Date', 'Scenario', 'Duration', 'Size', 'Version',
        'Winner', 'Winner Zone Score', 'Loser Zone Score', 'Winners', 'Losers', 'Tournament(s)'])

    for game in GameRecord.objects.order_by('started'):
        winner_zone_score, loser_zone_score = _get_zone_scores(game)
        winner_players = []
        loser_players = []
        for player in game.gameplayer_set.all():
            name = player.user.user.username if player.user else f'<{player.botName}>'
            if player.team == game.winningTeam:
                winner_players.append(name)
            else:
                loser_players.append(name)

        writer.writerow([
            game.pk,
            game.started,
            game.scenario,
            game.gameSeconds,
            game.zoneCount,
            game.serverVersion,
            team_names.get(game.winningTeam, '—'),
            winner_zone_score,
            loser_zone_score,
            ';'.join(winner_players),
            ';'.join(loser_players),
            ';'.join(t.name for t in game.tournament_set.all()),
        ])
    return response


def getArenaInfo(arenaId):
    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    return threads.blockingCallFromThread(
        reactor, authFactory.getArenaInfo, arenaId)


def setArenaInfo(arenaId, info):
    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    return threads.blockingCallFromThread(
        reactor, authFactory.setArenaInfo, arenaId, info)


def startLevelInArena(arenaId, levelInfo):
    from twisted.internet import reactor
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    return reactor.callFromThread(
        authFactory.startLevel, arenaId, levelInfo)


def tokenAuth(request):
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    if not authFactory.useAdminToken(request.GET['token']):
        return HttpResponse('Invalid token.', content_type='text/plain')

    username = 'autoadmin'
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User(
            username=username,
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        user.save()
    else:
        # Make sure the user hasn't done something silly and locked
        # themselves out.
        if not (user.is_staff and user.is_active and user.is_superuser):
            log.warning('Restoring privileges for autoadmin user.')
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
            user.save()

    login(request, user)

    return redirect('trosnoth:index')


@permission_required('trosnoth.change_trosnothserversetting')
def serverSettings(request):
    from .forms import ServerSettingsForm
    from trosnoth.server.settings import config, CONFIG_PATH

    settingsInstance = TrosnothServerSettings.get()
    if request.method == 'POST':
        form = ServerSettingsForm(request.POST, instance=settingsInstance)
        if form.is_valid():
           # Save the model
            form.save(commit=True).save()

            # Save ini fields
            config.set('web', 'hosts', form.cleaned_data['allowed_hosts'])
            config.set('security', 'key', form.cleaned_data['secret_key'])
            config.set('security', 'debug', str(
                int(form.cleaned_data['debug'])))
            with open(CONFIG_PATH, 'w') as f:
                config.write(f)

            # Redirect to clear the POST data
            return redirect('trosnoth:settings')

    else:
        form = ServerSettingsForm(instance=settingsInstance, initial={
            'allowed_hosts': config.get('web', 'hosts', fallback=''),
            'secret_key': config.get('security', 'key', fallback=''),
            'debug': config.getboolean('security','debug', fallback=False),
        })

    context = {
        'settings': settingsInstance,
        'form': form,
    }
    return render(request, 'trosnoth/settings.html', context)


@permission_required('trosnoth.change_trosnothserversetting')
def auth_logs(request):
    return _show_logs()


@permission_required('trosnoth.change_trosnothserversetting')
def arena_logs(request, arena_id):
    return _show_logs(str(arena_id))


@permission_required('trosnoth.change_trosnothserversetting')
def bot_logs(request, arena_id):
    return _show_logs(f'{arena_id}-bots')


def _show_logs(suffix=''):
    from trosnoth.run.authserver import command_line_log_file

    if not command_line_log_file:
        return HttpResponse('Logging not active on this server.', content_type='text/plain')

    filename = filename_with_suffix(command_line_log_file, suffix)
    try:
        with open(filename) as f:
            return HttpResponse(f.read(), content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse('Log file not found.', content_type='text/plain')


@permission_required('trosnoth.change_trosnothuser')
def manageUsers(request):
    from .forms import ManagePlayerForm

    message = ''
    try:
        username = request.GET['user']
    except KeyError:
        user = None
    else:
        try:
            user = TrosnothUser.from_user(username=username)
        except User.DoesNotExist:
            user = None
            message = 'Player not found'

    if not user:
        context = {
            'heading': 'Manage Players',
            'settings': TrosnothServerSettings.get(),
            'users': TrosnothUser.objects.order_by('nick'),
            'message': message,
        }
        return render(request, 'trosnoth/selectuser.html', context)

    if request.method == 'POST':
        form = ManagePlayerForm(request.POST, instance=user)
        if form.is_valid():
            # Save the model
            form.save(commit=True).save()

            # Update and save the linked user object
            user.user.is_active = form.cleaned_data['active']
            if request.user.is_superuser:
                # Only superusers are allowed to bestow superuser permission
                user.user.is_superuser = form.cleaned_data['superuser']
                user.user.is_staff = form.cleaned_data['superuser']
            user.user.save()

            # Redirect to clear the POST data
            response = redirect('trosnoth:manageusers')
            response['Location'] += '?user={}'.format(
                user.user.username)
            return response
        else:
            message = 'Please correct highlighted fields'
    else:
        form = ManagePlayerForm(instance=user, initial={
            'active': user.user.is_active,
            'superuser': user.user.is_superuser,
        })

    context = {
        'settings': TrosnothServerSettings.get(),
        'selectedUser': user,
        'message': message,
        'form': form,
    }
    return render(request, 'trosnoth/manageuser.html', context)


@permission_required('trosnoth.manage_arena')
def arenas(request):
    allArenas = TrosnothArena.objects.all()
    if len(allArenas) == 1:
        return redirect('trosnoth:arena', arenaId=allArenas[0].pk)

    arenaInfos = []
    for a in allArenas:
        info = getArenaInfo(a.id)
        info.update({
            'name': a.name,
            'id': a.id,
        })
        arenaInfos.append(info)

    context = {
        'heading': 'Manage Players',
        'settings': TrosnothServerSettings.get(),
        'arenas': arenaInfos,
    }
    return render(request, 'trosnoth/arenas.html', context)


@permission_required('trosnoth.shutdown_server')
def shutdown(request):
    from twisted.internet import reactor

    if request.method == 'POST':
        if request.POST.get('cancel'):
            return redirect('trosnoth:index')

        log.warning('Shutting down server due to web request from %s', request.user)

        # Give time for the goodbye page to render before stopping reactor
        reactor.callFromThread(reactor.callLater, 0.5, reactor.stop)

        context = {
            'settings': TrosnothServerSettings.get(),
        }
        return render(request, 'trosnoth/goodbye.html', context)

    context = {
        'settings': TrosnothServerSettings.get(),
        'heading': 'Shut down server',
        'message': 'Are you sure you want to shut down the server?',
        'button': 'Shut down',
    }
    return render(request, 'trosnoth/confirm.html', context)


@permission_required('trosnoth.shutdown_server')
def restart(request):
    from twisted.internet import reactor

    if request.method == 'POST':
        if request.POST.get('cancel'):
            return redirect('trosnoth:index')

        log.warning('Restarting server due to web request from %s', request.user)
        atexit.register(_restart_process)

        # Give time for the goodbye page to render before stopping reactor
        reactor.callFromThread(reactor.callLater, 0.5, reactor.stop)

        context = {
            'settings': TrosnothServerSettings.get(),
            'message': 'The server will restart in a moment.',
        }
        return render(request, 'trosnoth/goodbye.html', context)

    context = {
        'settings': TrosnothServerSettings.get(),
        'heading': 'Restart server',
        'message': 'Are you sure you want to restart the server?',
        'button': 'Restart',
    }
    return render(request, 'trosnoth/confirm.html', context)


def _restart_process():
    if getattr(sys, 'frozen', False):
        argv = sys.argv
    else:
        argv = [sys.executable] + sys.argv
    os.execv(argv[0], argv)
