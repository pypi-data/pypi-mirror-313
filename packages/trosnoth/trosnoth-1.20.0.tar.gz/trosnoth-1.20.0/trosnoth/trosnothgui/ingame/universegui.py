'''
Provides a layer between a universe and the GUI, turning
players, shots, grenades into sprites, and drawing rooms.
'''

import logging
import random
import statistics
import time
from math import atan2, sin, cos, pi

import pygame.draw

from trosnoth.const import (
    COLLECTABLE_COIN_LIFETIME, TICK_PERIOD, DEFAULT_COIN_VALUE,
    BOMBER_EXPLOSION_PARTICLE_COUNT,
)
from trosnoth.model.projectile import MineProjectile, LocalMine
from trosnoth.model.universe import Universe
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID, NO_PLAYER
from trosnoth.model.upgrades import allUpgrades
from trosnoth.trosnothgui.ingame.sprites import (
    PlayerSprite, ShotSprite, GrenadeSprite, GrenadeExplosionSprite,
    CollectableCoinSprite, ShoxwaveExplosionSprite, TrosballSprite,
    TrosballExplosionSprite, MineExplosionSprite, MineSprite, BomberExplosionParticle,
)
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen
from trosnoth.utils import globaldebug
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


PROJECTILE_SPRITE_MAP = {
    MineProjectile: MineSprite,
    LocalMine: MineSprite,
}


class UniverseGUI(object):

    # For debugging, displays where the player is server-side too
    SHOW_SERVER_SHADOWS = False

    def __init__(self, app, gameViewer, universe: Universe):
        self.app = app
        self.gameViewer = gameViewer
        self.universe = universe
        self.playerSprites = {}     # playerId -> PlayerSprite
        self.localPlayerId = None
        self.localPlayerSprite = None
        self.shotSprites = {}       # shotId -> ShotSprite
        self.localShotSprites = {}  # shot -> ShotSprite
        self.grenade_sprites = {}    # GrenadeShot -> GrenadeSprite
        self.projectile_sprites = {}
        self.collectableCoinSprites = {}    # coinId -> CollectableCoinSprite
        self.extraSprites = set()
        self._special_animations = set()
        self.trosballSprite = None
        self.tweenFraction = 1
        self.local_player_time = (0, 1)
        self.realTime = time.time()

        app.settings.display.on_detail_level_changed.addListener(
            self.detailLevelChanged)

    def get_screenshot_info(self):
        world = self.universe
        result = {
            'animations': [],
            'coins': [],
            'disabled_upgrades': b''.join(u.upgradeType for u in allUpgrades if not u.enabled),
            'grenades': [
                {
                    'player': grenade_sprite.grenade.player.nick,
                    'pos': grenade_sprite.pos,
                } for grenade_sprite in self.iterGrenades()
            ],
            'macguffins': {
                k: v for k, v in world.macguffin_manager.dump().items() if v != NO_PLAYER},
            'mines': [],
            'players': [player.get_screenshot_info() for player in self.iterPlayers()],
            'shots': [shot.get_screenshot_info() for shot in self.iterShots() if shot.shot],
            'trosball': self.trosballSprite.get_screenshot_info() if self.trosballSprite else None,
            'ui_options': world.uiOptions.dumpState(),
            'world_map': world.map.layout.dumpState() if world.map else None,
            'zones': [
                {
                    'id': zone.id,
                    'teamId': zone.owner.id if zone.owner else NEUTRAL_TEAM_ID,
                    'dark': zone.dark,
                } for zone in world.zones
            ],
        }
        for attr in ('team_ids_humans_can_join', 'team_ids_humans_can_switch_to'):
            result['ui_options'].pop(attr, None)

        if world.clock.showing:
            result['clock'] = round(world.clock.value)
        if world.abilities.renaming:
            result['abilities'] = {'renaming': True}

        if world.scoreboard.playerScoresEnabled:
            result['player_scores'] = {
                p.nick: score for p, score in world.scoreboard.playerScores.items()}
        if world.scoreboard.teamScoresEnabled:
            result['team_scores'] = [world.scoreboard.teamScores[t] for t in world.teams]

        result['teams'] = []
        for team in world.teams:
            team_data = team.abilities.dumpState()
            team_data['name'] = team.teamName
            active_boosts, pending_boosts = [], []
            for boost in team.boosts:
                if boost.activated:
                    active_boosts.append({
                        'code': boost.boost_code,
                        'time': boost.time_remaining,
                    })
                else:
                    pending_boosts.append({
                        'code': boost.boost_code,
                        'cost': boost.remaining_cost,
                    })
            if active_boosts:
                result['active_boosts'] = active_boosts
            if pending_boosts:
                result['pending_boosts'] = pending_boosts
            result['teams'].append(team_data)

        for sprite in self.iter_projectiles():
            if isinstance(sprite, MineSprite):
                mine_data = {
                    'team': sprite.mine.team.teamName if sprite.mine.team else None,
                    'pos': sprite.mine.pos,
                }
                if sprite.mine.stuck_angle is not None:
                    mine_data['stuck_angle'] = sprite.mine.stuck_angle
                    if not sprite.mine.active:
                        mine_data['inactive'] = True
                if sprite.mine.team is None:
                    mine_data['player'] = sprite.mine.player.nick
                # noinspection PyTypeChecker
                result['mines'].append(mine_data)

            else:
                log.error(f'I don’t know how to add {sprite} to screenshot info.')

        for coin_sprite in self.iterCollectableCoins():
            coin_data = {
                'pos': coin_sprite.pos,
                'fading':
                    coin_sprite.coin.creationTick
                    + (COLLECTABLE_COIN_LIFETIME - 2) // TICK_PERIOD
                    <= world.getMonotonicTick(),
            }
            if (coin_value := coin_sprite.coin.value) != DEFAULT_COIN_VALUE:
                coin_data['value'] = coin_value
            # noinspection PyTypeChecker
            result['coins'].append(coin_data)

        bomber_particles = {}
        for sprite in self.extraSprites | self._special_animations:
            if isinstance(sprite, BomberExplosionParticle):
                _, points = bomber_particles.setdefault(sprite.player_id, (sprite.team, []))
                points.append(sprite.pos)
            elif isinstance(sprite, (
                    GrenadeExplosionSprite,
                    TrosballExplosionSprite,
                    ShoxwaveExplosionSprite,
                    MineExplosionSprite)):
                explosion_data = sprite.get_screenshot_info()
                explosion_data['type'] = type(sprite).__name__.rstrip('Sprite')
                # noinspection PyTypeChecker
                result['animations'].append(explosion_data)
            elif isinstance(sprite, TemporalAnomaly):
                # noinspection PyTypeChecker
                result['animations'].append({
                    'type': 'TemporalAnomaly',
                    'team': sprite.team.teamName if sprite.team else None,
                    'start': sprite.start,
                    'player': sprite.local_player.nick,
                })
            else:
                log.error(f'I don’t know how to add {sprite} to screenshot info.')

        # For bomber explosion particles, just record summary statistics
        for bomber_team, particle_set in bomber_particles.values():
            x = statistics.mean(pos[0] for pos in particle_set)
            y = statistics.mean(pos[1] for pos in particle_set)
            distances = list(distance((x, y), pos) for pos in particle_set)
            mean_dist = statistics.mean(distances)
            explosion_data = {
                'type': 'BomberExplosion',
                'team': bomber_team.teamName if bomber_team else None,
                'pos': (x, y),
                'mean_distance': mean_dist,
                'stddev': statistics.pstdev(distances, mu=mean_dist),
            }
            if len(particle_set) != BOMBER_EXPLOSION_PARTICLE_COUNT:
                explosion_data['count'] = len(particle_set)

            # noinspection PyTypeChecker
            result['animations'].append(explosion_data)

        # Remove any empty data
        for key, value in list(result.items()):
            if not value:
                del result[key]

        return result

    def restore_screenshot_info(self, info):
        '''
        By the time this method is called, much of what's in info will
        have already been restored into the Universe object.
        '''
        if self.localPlayerId is not None:
            # Restore the viewing angle that has by now moved to follow
            # the mouse.
            player_sprite = self.getPlayerSprite(self.localPlayerId)
            player_info = [p for p in info['players'] if p['nick'] == player_sprite.player.nick][0]
            player_sprite.player.angleFacing = player_info['angle']

        for player in self.iterPlayers():
            player.drawer.randomise_frame = True

        shot_id = 1
        for shot_info in info.get('shots', []):
            shot = self.universe.getShot(shot_id)
            sprite = self.shotSprites[shot_id] = ShotSprite(self.app, self, shot)
            sprite.restore_screenshot_info(shot_info)
            shot_id += 1

        for mine_sprite in self.iter_projectiles():
            # Randomise mine angle if in air
            mine_sprite.angle = random.random() * 2 * pi

        for coin_sprite in self.iterCollectableCoins():
            # Randomise coin angle
            coin_sprite.animation.start -= random.random() * 10

        if info.get('trosball'):
            self.getTrosballSprite().restore_screenshot_info(info['trosball'])

        single_animation_explosions = {
            'GrenadeExplosion': GrenadeExplosionSprite,
            'TrosballExplosion': TrosballExplosionSprite,
            'ShoxwaveExplosion': ShoxwaveExplosionSprite,
            'MineExplosion': MineExplosionSprite,
        }
        for animation_info in info.get('animations', []):
            animation_type = animation_info['type']
            if animation_type in single_animation_explosions:
                self.extraSprites.add(single_animation_explosions[
                    animation_type].from_screenshot_info(self, animation_info))
            elif animation_type == 'TemporalAnomaly':
                if self.localPlayerSprite \
                        and self.localPlayerSprite.player.nick == animation_info['player']:
                    anomaly = TemporalAnomaly(self, None, self.localPlayerSprite.player)
                    anomaly.remaining_time = .3
                    team_name = animation_info['team']
                    if team_name is None:
                        anomaly.team = None
                    else:
                        anomaly.team = [
                            t for t in self.universe.teams if t.teamName == team_name][0]
                    anomaly.start = animation_info['start']
                    self._special_animations.add(anomaly)
            elif animation_type == 'BomberExplosion':
                team_name = animation_info['team']
                if team_name is None:
                    bomber_team = None
                else:
                    bomber_team = [
                        t for t in self.universe.teams if t.teamName == team_name][0]
                distribution = statistics.NormalDist(
                    animation_info['mean_distance'], animation_info['stddev'])
                particle_count = animation_info.get('count', BOMBER_EXPLOSION_PARTICLE_COUNT)
                for dist in distribution.samples(particle_count):
                    x, y = animation_info['pos']
                    angle = random.random() * 2 * pi
                    x += dist * cos(angle)
                    y += dist * sin(angle)
                    self.extraSprites.add(BomberExplosionParticle((x, y), bomber_team))
            else:
                raise ValueError(f'Unknown animation type {animation_type!r}')

    def stop(self):
        self.app.settings.display.on_detail_level_changed.removeListener(
            self.detailLevelChanged)

    def world_was_reset(self):
        self._special_animations.clear()
        self.extraSprites.clear()
        self.collectableCoinSprites.clear()
        self.projectile_sprites.clear()
        self.grenade_sprites.clear()
        self.localShotSprites.clear()

    def detailLevelChanged(self):
        # Clear everything long-lived
        self.playerSprites = {}
        self.collectableCoinSprites = {}
        self.trosballSprite = None
        if self.localPlayerId is not None:
            self.rebuild_local_player_sprite()

    def set_tween_fraction(self, f):
        self.tweenFraction = f
        self.realTime = time.time()

    def set_local_player_time(self, ticks_and_fraction):
        self.local_player_time = ticks_and_fraction

    def get_local_player_fraction(self):
        ticks, fraction = self.local_player_time
        return fraction

    def getTime(self):
        t = self.universe.getMonotonicTime()
        t -= (1 - self.tweenFraction) * self.universe.tickPeriod
        return t

    def get_local_player_time(self):
        '''
        Used for local player animations.
        '''
        ticks, fraction = self.local_player_time
        return (ticks + fraction) * self.universe.tickPeriod

    def get_tick_portion(self, player=None):
        not_local = self.localPlayerId is None or player is None or self.localPlayerId != player.id
        if not_local:
            return self.tweenFraction * self.universe.tickPeriod

        ticks, fraction = self.local_player_time
        return fraction * self.universe.tickPeriod

    @property
    def zones(self):
        return self.universe.zones

    @property
    def rooms(self):
        return self.universe.rooms

    @property
    def teams(self):
        return self.universe.teams

    @property
    def map(self):
        return self.universe.map

    @property
    def zoneBlocks(self):
        return self.universe.zoneBlocks

    def getTrosballSprite(self):
        if not self.universe.trosballManager.enabled:
            return None
        if self.trosballSprite is None:
            self.trosballSprite = TrosballSprite(self.app, self, self.universe)
        return self.trosballSprite

    def getPlayerSprite(self, playerId, ignoreLocal=False):
        player = self.universe.getPlayer(playerId)
        if player is None:
            return None
        if playerId == self.localPlayerId and not ignoreLocal:
            p = self.localPlayerSprite
            if p.spriteTeam != p.player.team:
                self.rebuild_local_player_sprite()
                if p is self.gameViewer.viewManager.target:
                    self.gameViewer.viewManager.setTarget(
                        self.localPlayerSprite)
                p = self.localPlayerSprite
            return p

        try:
            p = self.playerSprites[playerId]
        except KeyError:
            self.playerSprites[player.id] = p = PlayerSprite(
                self.app, self, player)
            return p

        if p.spriteTeam != player.team:
            # Player has changed teams.
            self.playerSprites[player.id] = p = PlayerSprite(
                self.app, self, player)
        return p

    def overridePlayer(self, player):
        self.localPlayerSprite = PlayerSprite(
            self.app, self, player,
            tweener_function=self.get_local_player_fraction,
            timer=self.get_local_player_time,
        )
        self.localPlayerId = player.id

    def rebuild_local_player_sprite(self):
        p = self.localPlayerSprite
        self.localPlayerSprite = PlayerSprite(
            self.app, self, p.player,
            tweener_function=self.get_local_player_fraction,
            timer=self.get_local_player_time,
        )

    def removeOverride(self):
        self.localPlayerId = None
        self.localPlayerSprite = None

    def iterPlayers(self):
        untouched = set(self.playerSprites.keys())
        for player in self.universe.players:
            untouched.discard(player.id)
            yield self.getPlayerSprite(player.id)
            if self.SHOW_SERVER_SHADOWS and player.id == self.localPlayerId:
                yield self.getPlayerSprite(player.id, ignoreLocal=True)

        # Clean up old players.
        for playerId in untouched:
            del self.playerSprites[playerId]

    def iter_projectiles(self):
        new_sprites = {}

        def sprite(p):
            try:
                sprite = self.projectile_sprites[p]
            except KeyError:
                # TODO: eventually localState.projectiles will also have other
                #   things, such as grenades
                sprite = PROJECTILE_SPRITE_MAP[type(p)](self.app, self, p)
            new_sprites[p] = sprite
            return sprite

        server_projectiles = set(self.universe.projectile_by_id.values())
        for projectile in self.gameViewer.interface.localState.projectiles:
            if not self.SHOW_SERVER_SHADOWS:
                server_projectiles.discard(projectile.server_projectile)
            yield sprite(projectile)
        for projectile in server_projectiles:
            yield sprite(projectile)

        self.projectile_sprites = new_sprites

    def iterGrenades(self):
        untouched = set(self.grenade_sprites.keys())
        for grenade in self.universe.grenades:
            if (
                    grenade.player.id == self.localPlayerId
                    and not self.SHOW_SERVER_SHADOWS):
                continue
            try:
                yield self.grenade_sprites[grenade]
            except KeyError:
                self.grenade_sprites[grenade] = g = (
                    GrenadeSprite(self.app, self, grenade))
                yield g
            else:
                untouched.discard(grenade)

        for grenade in self.gameViewer.interface.localState.local_grenades:
            yield GrenadeSprite(self.app, self, grenade)

        # Clean up old grenades.
        for grenade in untouched:
            del self.grenade_sprites[grenade]

    def iterShots(self):
        untouched = set(self.shotSprites.keys())
        untouchedLocals = set(self.localShotSprites.keys())
        for shot in self.universe.shots:
            if not shot.originatingPlayer and not shot.gun_type.neutral_shots:
                continue
            if (
                    not shot.gun_type.neutral_shots
                    and shot.originatingPlayer.id == self.localPlayerId
                    and not self.SHOW_SERVER_SHADOWS):
                continue
            if shot.justFired:
                continue
            if shot.expired and not globaldebug.enabled:
                continue
            try:
                yield self.shotSprites[shot.id]
            except KeyError:
                self.shotSprites[shot.id] = s = (
                    ShotSprite(self.app, self, shot))
                yield s
            untouched.discard(shot.id)

        for shot in self.gameViewer.interface.localState.shots:
            if shot.justFired:
                continue
            try:
                yield self.localShotSprites[shot]
            except KeyError:
                self.localShotSprites[shot] = s = ShotSprite(
                    self.app, self, shot)
                yield s
            untouchedLocals.discard(shot)

        # Clean up old shots.
        for shotId in untouched:
            s = self.shotSprites[shotId]
            s.noLongerInUniverse()
            if s.shouldRemove():
                del self.shotSprites[shotId]
            else:
                yield s
        for shot in untouchedLocals:
            s = self.localShotSprites[shot]
            s.noLongerInUniverse()
            if s.shouldRemove():
                del self.localShotSprites[shot]
            else:
                yield s

    def iterCollectableCoins(self):
        untouched = set(self.collectableCoinSprites.keys())
        for coin in self.universe.collectableCoins.values():
            if coin.hitLocalPlayer:
                continue
            try:
                yield self.collectableCoinSprites[coin.id]
            except KeyError:
                self.collectableCoinSprites[coin.id] = s = (
                    CollectableCoinSprite(self.app, self, coin))
                yield s
            else:
                untouched.discard(coin.id)

        # Clean up old shots.
        for coinId in untouched:
            del self.collectableCoinSprites[coinId]

    def iterExtras(self):
        for sprite in list(self.extraSprites):
            if sprite.isDead():
                self.extraSprites.remove(sprite)
            yield sprite
        trosball = self.getTrosballSprite()
        if trosball:
            yield trosball

    @property
    def special_animations(self):
        self._special_animations = {a for a in self._special_animations if not a.finished}
        yield from self._special_animations

    def getPlayerCount(self):
        return len(self.universe.players)

    def hasPlayer(self, player):
        return (
            player.id in self.playerSprites or player.id == self.localPlayerId)

    def getPlayersInZone(self, zone):
        result = []
        for p in zone.players:
            ps = self.getPlayerSprite(p.id)
            if ps is not None:
                result.append(ps)
        return result

    def addExplosion(self, pos):
        self.extraSprites.add(GrenadeExplosionSprite(self, pos))

    def addTrosballExplosion(self, pos):
        self.extraSprites.add(TrosballExplosionSprite(self, pos))

    def add_bomber_explosion(self, player, num_particles=BOMBER_EXPLOSION_PARTICLE_COUNT):
        for i in range(num_particles):
            self.extraSprites.add(BomberExplosionParticle(player.pos, player.team, player.id))

    def addShoxwaveExplosion(self, pos):
        self.extraSprites.add(ShoxwaveExplosionSprite(self, pos))

    def add_mine_explosion(self, pos):
        self.extraSprites.add(MineExplosionSprite(self, pos))

    def add_temporal_anomaly(self, real_player, local_player):
        self._special_animations.add(TemporalAnomaly(self, real_player.getZone(), local_player))

    def shot_rebounded(self, shot, pos):
        self.gameViewer.interface.shot_rebounded(pos)


class SpecialAnimation:
    finished: bool

    def draw(self, screen, focus, area):
        raise NotImplementedError


class TemporalAnomaly(SpecialAnimation):
    def __init__(self, world_gui, room, local_player):
        self.local_player = local_player
        self.remaining_time = .3
        self.timer = world_gui.getTime
        self.last_time = self.timer()
        if not room:
            self.remaining_time = 0
            self.start = None
            self.team = None
        else:
            self.team = room.owner
            self.start = room.orb_pos

    @property
    def finished(self):
        return self.remaining_time <= 0

    def draw(self, screen, focus, area):
        now = self.timer()
        self.remaining_time -= now - self.last_time
        self.last_time = now

        start = mapPosToScreen(self.start, focus, area)
        end = mapPosToScreen(self.local_player.pos, focus, area)
        for i in range(5):
            if self.team:
                colour = self.team.shade(random.random(), random.choice([1, 0]))
            else:
                f = round(255 * random.random())
                colour = (f, f, f)
            pygame.draw.lines(screen, colour, False, zigzag(start, end, i), width=10 - 2 * i)


def zigzag(start, end, intermediates):
    result = [start]

    x1, y1 = start
    x2, y2 = end
    angle = atan2(y2 - y1, x2 - x1)
    d = random.choice([True, False])
    for i in range(intermediates):
        amplitude = 30 if d else -30
        d = not d
        x = round(x1 + (x2 - x1) * (i + 1) / (intermediates + 1) + amplitude * sin(angle))
        y = round(y1 + (y2 - y1) * (i + 1) / (intermediates + 1) - amplitude * cos(angle))
        result.append((x, y))

    result.append(end)
    return result