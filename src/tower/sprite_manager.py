import pygame
from dataclasses import dataclass
from tower.sprites import Background

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
            sounds = None,
            groups = [self.layers],
            index = index,
            orientation = orientation,
        )
        return background

    def select_sprites(self, sprites, position = None):
        self.select.add(sprites)
        if position is not None:
            self.move(position)

            