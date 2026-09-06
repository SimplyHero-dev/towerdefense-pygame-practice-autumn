import pygame
from dataclasses import dataclass
from tower.sprites import Background, Shrub
from tower.grid import TILE_HEIGHT, TILE_WIDTH, get_tile_position
from tower.sprites import layer

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
