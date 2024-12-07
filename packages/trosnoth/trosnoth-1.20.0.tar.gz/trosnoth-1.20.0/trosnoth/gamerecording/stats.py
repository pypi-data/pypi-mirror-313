from collections import defaultdict
import datetime
import logging

import msgpack
from asgiref.sync import sync_to_async
from twisted.internet import defer

from trosnoth import dbqueue, version
from trosnoth.dbqueue import run_in_synchronous_thread
from trosnoth.const import BOMBER_DEATH_HIT
from trosnoth.levels.base import FrozenLevelStats, PlayerInfo, LevelResult
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.utils.utils import timeNow    # TODO: use game not real time

log = logging.getLogger(__name__)


# TODO: test the accuracy etc. achievements after fixing the stats to fit the
# event-based architecture

class PlayerStatKeeper(object):
    '''Maintains the statistics for a particular player object'''

    def __init__(self, achievement_manager, player):
        self.achievement_manager = achievement_manager
        self.player = player

        # A: Recorded [A]ll game (including post-round)
        # G: Recorded during the main [G]ame only
        # P: Recorded [P]ost-Game only
        self.kills = 0           # G Number of kills they've made
        self.deaths = 0          # G Number of times they've died
        self.zoneTags = 0        # G Number of zones they've tagged
        self.zoneAssists = 0     # G Number of zones they've been in when their
                                 #   team tags it
        self.zoneScore = 0       # G Effective zone capture score,
                                 #   calculated from number of zones
                                 #   captured and neutralised, shared between
                                 #   the players doing the capturing /
                                 #   neutralising
        self.shotsFired = 0      # A Number of shots they've fired
        self.shotsHit = 0        # A Number of shots that have hit a target
        self.coinsEarned = 0     # G Aggregate total of coins earned
        self.coinsUsed = 0       # G Aggregate total of coins used
        self.coinsLost = 0       # G Aggregate total of coins lost in any way
        self.roundsWon = 0       # . Number of rounds won
        self.roundsLost = 0      # . Number of rounds lost

        self.playerDeaths = defaultdict(int)   # A Number of deaths from
                                               #   individual people
        self.upgradesUsed = defaultdict(int)   # G Number of each upgrade used

        self.timeAlive = 0.0     # G Total time alive
        self.timeDead = 0.0      # G Total time dead

        self.killStreak = 0      # G Number of kills made without dying
        self.currentKillStreak = 0
        self.tagStreak = 0       # G Number of zones tagged without dying
        self.currentTagStreak = 0
        self.aliveStreak = 0.0   # G Greatest time alive in one life
        self.lastTimeRespawned = None
        self.lastTimeDied = None
        self.lastTimeSaved = None
        self.paused = True

        self.resume()

    def resume(self):
        if not self.paused:
            return

        self.player.onCoinsSpent.addListener(self.coinsSpent)
        self.player.onShotFired.addListener(self.shotFired)
        self.player.onDied.addListener(self.died)
        self.player.onRespawned.addListener(self.respawned)
        self.player.onKilled.addListener(self.killed)
        self.player.onShotHitSomething.addListener(self.shotHit)
        self.player.onUsedUpgrade.addListener(self.upgradeUsed)
        self.player.onCoinsChanged.addListener(self.coinsChanged)
        self.paused = False

    def stop(self):
        self.pause()

    def pause(self):
        if self.paused:
            return

        self.player.onCoinsSpent.removeListener(self.coinsSpent)
        self.player.onShotFired.removeListener(self.shotFired)
        self.player.onDied.removeListener(self.died)
        self.player.onRespawned.removeListener(self.respawned)
        self.player.onKilled.removeListener(self.killed)
        self.player.onShotHitSomething.removeListener(self.shotHit)
        self.player.onUsedUpgrade.removeListener(self.upgradeUsed)
        self.player.onCoinsChanged.removeListener(self.coinsChanged)
        self.paused = True

    def shotFired(self, shot):
        if not shot.gun_type.shots_hurt_players:
            return
        self.shotsFired += 1

        if self.shotsFired >= 100:
            accuracy = self.accuracy()
            if accuracy >= 0.10:
                self.sendAchievementProgress(b'accuracySmall')
            if accuracy >= 0.15:
                self.sendAchievementProgress(b'accuracyMedium')
            if accuracy >= 0.20:
                self.sendAchievementProgress(b'accuracyLarge')

    def sendAchievementProgress(self, achievementId):
        if self.player.id == -1:
            # Player is no longer in game.
            return
        if not self.achievement_manager:
            return
        self.achievement_manager.triggerAchievement(self.player, achievementId)

    def _updateStreaks(self, updateAlive):
        '''
        updateAlive will be set to True in three situations:
          1. if the player has just died
          2. if the player was alive when the game ended
          3. if the player was alive when they disconnected
        '''
        self.killStreak = max(self.killStreak, self.currentKillStreak)
        self.tagStreak = max(self.tagStreak, self.currentTagStreak)

        time = timeNow()

        if updateAlive and self.lastTimeRespawned:
            lastLife = time - self.lastTimeRespawned
            self.aliveStreak = max(self.aliveStreak, lastLife)
            self.timeAlive += lastLife
            if lastLife >= 180:
                self.sendAchievementProgress(b'aliveStreak')

        elif self.lastTimeDied is not None:
            self.timeDead += time - self.lastTimeDied

        self.currentKillStreak = 0
        self.currentTagStreak = 0

    def died(self, killer, deathType):
        if deathType != BOMBER_DEATH_HIT:
            self.deaths += 1
            if killer is not None:
                self.playerDeaths[killer.identifyingName] += 1

        time = timeNow()

        self._updateStreaks(True)

        self.lastTimeDied = time

        if self.timeAlive >= 1000:
            self.sendAchievementProgress(b'totalAliveTime')

        if self.timeAlive >= 300 and self.timeAlive >= (self.timeAlive +
                self.timeDead) * 0.75:
            self.sendAchievementProgress(b'stayingAlive')

    def respawned(self):
        time = timeNow()

        if self.lastTimeDied is not None:
            self.timeDead += (time - self.lastTimeDied)

        self.lastTimeRespawned = time

    def goneFromGame(self):
        self._updateStreaks(not self.player.dead)

    def gameOver(self, winningTeam):
        self._updateStreaks(not self.player.dead)
        if winningTeam is None:
            # Draw. Do nothing
            pass
        elif self.player.isEnemyTeam(winningTeam):
            self.roundsLost += 1
        else:
            self.roundsWon += 1

    def killed(self, victim, deathType, *args, **kwargs):
        self.kills += 1
        self.currentKillStreak += 1

        self.killStreak = max(self.killStreak, self.currentKillStreak)

    def involvedInZoneCap(self, captureInfo):
        if self.player == captureInfo['player']:
            self.zoneTags += 1
            self.currentTagStreak += 1
            self.tagStreak = max(self.tagStreak, self.currentTagStreak)
        else:
            self.zoneAssists += 1

        self.zoneScore += captureInfo['points'] / len(captureInfo['attackers'])

    def shotHit(self, shot):
        if not shot.gun_type.shots_hurt_players:
            return
        self.shotsHit += 1

    def coinsSpent(self, coins):
        self.coinsUsed += coins

        if self.coinsUsed >= 1000 and self.coinsUsed >= self.coinsEarned * 0.5:
            self.sendAchievementProgress(b'useCoinsEfficiently')

    def coinsChanged(self, oldCoins):
        if self.player.coins < oldCoins:
            self.coinsLost += oldCoins - self.player.coins
        else:
            self.coinsEarned += self.player.coins - oldCoins

    def upgradeUsed(self, upgrade):
        self.upgradesUsed[upgrade.upgradeType] += 1

    def totalPoints(self):
        points = 0
        points += self.kills        * 10
        points += self.deaths       * 1
        points += self.zoneTags     * 20
        points += self.zoneAssists  * 5
        points += self._accuracyPoints()

        return points

    def _accuracyPoints(self):
        if self.shotsFired == 0:
            return 0
        return ((self.shotsHit ** 2.) / self.shotsFired) * 30

    def accuracy(self):
        if self.shotsFired == 0:
            return 0
        return self.shotsHit * 1. / self.shotsFired

    def statDict(self):
        stats = {}
        for val in ('aliveStreak', 'deaths', 'killStreak', 'kills',
                'roundsLost', 'roundsWon', 'shotsFired', 'shotsHit',
                'coinsEarned', 'coinsUsed', 'tagStreak',
                'timeAlive', 'timeDead', 'upgradesUsed', 'zoneAssists',
                'zoneTags', 'zoneScore'):
            stats[val] = getattr(self, val)
        stats['bot'] = self.player.bot
        stats['team'] = self.player.teamId
        stats['username'] = (self.player.user.username if self.player.user
                else None)
        stats['coinsWasted'] = self.coinsLost - self.coinsUsed

        return stats

    def rejoined(self, player):
        self.player = player


class StatKeeper(object):

    def __init__(self, world, achievement_manager):
        self.world = world
        self.achievement_manager = achievement_manager
        self.paused = False

        # A mapping of player ids to statLists
        # (Contains only players currently in the game)
        self.playerStatList = {}
        # A list of all statLists
        # (regardless of in-game status)
        self.allPlayerStatLists = {}
        self.winningTeamId = None

        self.world.onZoneCaptureFinalised.addListener(self.gotZoneCap)
        self.world.onPlayerAdded.addListener(self.playerAdded)
        self.world.onPlayerRemoved.addListener(self.playerRemoved)
        self.world.onStandardGameFinished.addListener(self.gameOver)

        for player in self.world.players:
            self.playerAdded(player)

    def stop(self):
        self.world.onZoneCaptureFinalised.removeListener(self.gotZoneCap)
        self.world.onPlayerAdded.removeListener(self.playerAdded)
        self.world.onPlayerRemoved.removeListener(self.playerRemoved)
        self.world.onStandardGameFinished.removeListener(self.gameOver)
        for playerStats in list(self.allPlayerStatLists.values()):
            playerStats.stop()

    def pause(self):
        self.paused = True
        for playerStats in list(self.allPlayerStatLists.values()):
            playerStats.pause()

    def resume(self):
        self.paused = False
        for playerStats in list(self.allPlayerStatLists.values()):
            playerStats.resume()

    def gotZoneCap(self, captureInfo):
        if self.paused:
            return
        for player in captureInfo['attackers']:
            self.playerStatList[player.id].involvedInZoneCap(captureInfo)

    @defer.inlineCallbacks
    def playerAdded(self, player):
        if not player.join_complete:
            # We want to identify by user rather than nickname if the user
            # is authenticated.
            yield player.onJoinComplete.wait()
            if player.id == -1:
                # Player has already been removed from game
                return

        statkeeper = self.allPlayerStatLists.get(player.identifyingName)
        if statkeeper:
            statkeeper.rejoined(player)
        else:
            statkeeper = PlayerStatKeeper(self.achievement_manager, player)
            if self.paused:
                statkeeper.pause()
            self.allPlayerStatLists[player.identifyingName] = statkeeper
        self.playerStatList[player.id] = statkeeper

    def playerRemoved(self, player, oldId):
        if oldId in self.playerStatList:
            self.playerStatList[oldId].goneFromGame()
            # Just remove this from the list of current players
            # (retain in list of all stats)
            del self.playerStatList[oldId]
        else:
            # Player might still be waiting for onJoinComplete()
            pass

    def gameOver(self, team):
        self.winningTeamId = team.id if team else NEUTRAL_TEAM_ID
        # Only credit current players for game over
        for playerStat in list(self.playerStatList.values()):
            playerStat.gameOver(team)


class ServerGameStats(object):
    def __init__(self, game, arenaId):
        from trosnoth.djangoapp.models import GameRecord

        self.game = game
        self.arenaId = arenaId
        self.world = game.world
        level = game.world.scenarioManager.level
        self.gameRecord = GameRecord(
            started=datetime.datetime.now(),
            serverVersion=version.version,
            blueTeamName=self.world.teams[0].teamName,
            redTeamName=self.world.teams[1].teamName,
            replayName=game.gameRecorder.replay_path.name,
            zoneCount=len(self.world.rooms),
            scenario=level.levelName or level.__class__.__name__,
        )
        self.startGameTime = self.world.getMonotonicTime()

    def stop(self, level_result: LevelResult):
        from trosnoth.djangoapp.models import TrosnothArena, PlayerInGame, TrosnothUser

        if level_result is None:
            finished = False
            stats = self.world.scenarioManager.level.stats.freeze()
            winning_team_id = b''
        else:
            finished = True
            stats = level_result.stats
            winners = level_result.winning_teams
            winning_team_id = winners[0].id if len(winners) == 1 else b''

        self.gameRecord.finished = datetime.datetime.now()
        self.gameRecord.gameSeconds = (
            self.world.getMonotonicTime() - self.startGameTime)
        scoreboard = self.world.scoreboard
        self.gameRecord.teamScoresEnabled = scoreboard.teamScoresEnabled
        self.gameRecord.playerScoresEnabled = scoreboard.playerScoresEnabled
        self.gameRecord.blueTeamName = self.world.teams[0].teamName
        self.gameRecord.redTeamName = self.world.teams[1].teamName
        self.gameRecord.blueTeamScore = scoreboard.teamScores[self.world.teams[0]]
        self.gameRecord.blueTeamScore = scoreboard.teamScores[self.world.teams[1]]
        self.gameRecord.scenario_completed = finished
        self.gameRecord.stats = msgpack.packb(
            FrozenLevelStats.dump(stats, for_db=True),
            use_bin_type=True)

        self.gameRecord.winningTeam = winning_team_id.decode('ascii')
        dbqueue.add(sync_to_async(self.gameRecord.save))

        winning_players = {PlayerInfo(p) for p in level_result.winning_players}
        for i, player_info in enumerate(stats.player_info):
            player_record = PlayerInGame(
                game=self.gameRecord,
                index=i,
                user=TrosnothUser.from_user(
                    username=player_info.username) if player_info.username else None,
                bot=player_info.bot,
                winner=player_info in winning_players,
            )
            dbqueue.add(sync_to_async(player_record.save))

        try:
            arena = run_in_synchronous_thread(TrosnothArena.objects.get, id=self.arenaId)
            if arena.currentTournament:
                @dbqueue.add
                async def add_game_record_to_tournament():
                    await sync_to_async(arena.currentTournament.matches.add)(self.gameRecord)
        except TrosnothArena.DoesNotExist:
            pass

    def queueSaveWithAttrs(self, record, attrs):
        '''
        The Django ORM seems to store the ID of foreign key relationships when
        the attribute is first set, so if you set the relationship before the
        related object is first saved, saving will break. Getting and setting
        again just before the save is good enough to make Django happy.
        '''
        @dbqueue.add
        async def saveEndOfGameStats():
            for attr in attrs:
                setattr(record, attr, getattr(record, attr))
            await sync_to_async(record.save)()
