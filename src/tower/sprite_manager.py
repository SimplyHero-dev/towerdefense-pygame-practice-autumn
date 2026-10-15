import pygame
from pygame.math import Vector2 as Vector
from dataclasses import dataclass
from tower.sprites import Background, Shrub, Enemy, Turret, Portal, Projectile
from tower.grid import TILE_HEIGHT, TILE_WIDTH, get_tile_position
from tower.sprites import layer, Vision
from itertools import cycle
from tower import asset_loader
from tower.sprites import Enemy, AnimationState
from tower.grid import make_enemy_path
from tower.movement import create_projectile_path


@dataclass
class Spritemanager:

    layers: pygame.sprite.LayeredUpdates
    selected: pygame.sprite.LayeredUpdates
    level: list

    @classmethod
    def create(cls, layers, level):
        return cls(layers = layers, level = level, selected = pygame.sprite.LayeredUpdates())

    def create_background(self, position, orientation = None, index = None):
        background = Background.create_from_tile(
            #!sounds = None,
            groups = [self.layers],
            index = index,
            orientation = orientation,
            position = position,
        )
        return background

    def create_shrub(self, position, orientation = None, index = None):
        shrubs = Shrub.create_from_tile(
            #!sounds = None,
            groups = [self.layers],
            index = index,
            orientation = orientation,
            position = position,
        )
        return shrubs
    
    def create_enemy(self, position, start_tile, stop_positions, orientation = None):
        enemy = Enemy.create_from_surface(
            #!sounds = None,
            groups = [self.layers],
            surface = asset_loader.WALK_FRAMES[0],
            orientation = orientation,
            position = position,
            animation_speed = 6,
        )
        enemy.direction_frames = {
            "side": (asset_loader.WALK_FRAMES, asset_loader.WALK_FRAMES_FLIPPED),
            "up": (asset_loader.WALK_UP_FRAMES, None),
            "down": (asset_loader.WALK_DOWN_FRAMES, None),
        }
        enemy.death_frames = (asset_loader.DEATH_FRAMES, asset_loader.DEATH_FRAMES_FLIPPED)
        enemy.set_direction("side")
        enemy.animation_state = AnimationState.walking
        enemy.path = make_enemy_path(start_tile, stop_positions)
        return enemy

    def create_turret(self, position, orientation = 0):
        turret = Turret.create_from_surface(
            #!sounds = None,
            groups = [self.layers],
            surface = asset_loader.TOWER_IDLE_FRAMES[0],
            orientation = orientation,
            position = position,
            animation_speed = 6,
        )
        turret.frame_source = asset_loader.TOWER_IDLE_FRAMES
        turret.frame_source_flipped = None
        turret.frames = {
            AnimationState.idle:  cycle(range(len(asset_loader.TOWER_IDLE_FRAMES))),
        }
        turret.animation_state = AnimationState.idle
        
        turret.vision = Vision.create_vision(
            rect = pygame.Rect(0, 0, 60, 180),
            turret = turret,
            groups = [self.layers],
            orientation = orientation,
        )
        return turret
    
    def create_projectile(self, turret, enemy, orientation = None):
        start = Vector(turret.rect.center)
        stop = Vector(enemy.rect.center)
        projectile = Projectile.create_from_surface(
            groups = [self.layers],
            surface = asset_loader.PORTAL_IDLE_FRAMES[0],
            orientation = orientation,
            position = start,
        )
        projectile.explode_frames = (asset_loader.EXPLOSION_FRAMES, None)
        projectile.path = create_projectile_path(start, stop, speed = 5, max_distance = 200)
        return projectile

    def create_portal(self, position, orientation = None):
        portal = Portal.create_from_surface(
            #!sounds = None,
            groups = [self.layers],
            surface = asset_loader.PORTAL_IDLE_FRAMES[0],
            orientation = orientation,
            position = position,
            animation_speed = 6,
        )
        portal.frame_source = asset_loader.PORTAL_IDLE_FRAMES
        portal.frame_source_flipped = None
        portal.frames = {
            AnimationState.idle:  cycle(range(len(asset_loader.PORTAL_IDLE_FRAMES))),
        }
        portal.animation_state = AnimationState.idle
        return portal
    
    def select_sprites(self, sprites, position = None):
        self.selected.add(sprites)
        if position is not None:
            self.move(position)

    def move(self, position):
        x, y = position
        for sprite in self.selected:
            if sprite.layer == layer.background:
                gx, gy = (x - (x % TILE_WIDTH), y - (y % TILE_HEIGHT))
                sprite.move((gx, gy), center = False)
            else:
                sprite.move((x, y))

    def place(self, position):
        for sprite in list(self.selected):
            if sprite.layer == layer.background:
                gx, gy = get_tile_position(sprite.rect.topleft)
                self.level[gy][gx] = sprite
            else:
                sprite.move(position)
            self.selected.remove(sprite)

    def kill(self):
        for sprite in list(self.selected):
            sprite.kill()
