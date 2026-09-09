import pygame
from dataclasses import dataclass
from tower.sprites import Background, Shrub, Enemy, Turret
from tower.grid import TILE_HEIGHT, TILE_WIDTH, get_tile_position
from tower.sprites import layer
from itertools import cycle
from tower import asset_loader
from tower.sprites import Enemy, AnimationState

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
    
    def create_enemy(self, position, orientation = None):
        enemy = Enemy.create_from_surface(
            #!sounds = None,
            groups = [self.layers],
            surface = asset_loader.WALK_FRAMES[0],
            orientation = orientation,
            position = position,
            animation_speed = 6,
        )
        enemy.frames = {
            AnimationState.walking: cycle(asset_loader.WALK_FRAMES),
        }
        enemy.animation_state = AnimationState.walking
        return enemy

    def create_turret(self, position, orientation = None):
        turret = Turret.create_from_surface(
            #!sounds = None,
            groups = [self.layers],
            surface = asset_loader.WALK_FRAMES[0],
            orientation = orientation,
            position = position,
            animation_speed = 6,
        )
        turret.frames = {
            AnimationState.idle:  cycle(asset_loader.TOWER_IDLE_FRAMES),
        }
        turret.animation_state = AnimationState.idle
        return turret

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
