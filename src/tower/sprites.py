import pygame
from tower.asset_loader import IMAGE_SPRITES
import enum

class AnimationState(enum.Enum):
    stopped = "stopped"
    walking = "walking"
    dying = "dying"
    exploding = "exploding"
    
    @classmethod
    def state_kill_sprite(cls, state):
        return state in (cls.exploding, cls.dying)

class Sprite(pygame.sprite.Sprite):
    @classmethod
    def create_from_tile(
        cls,
        index,
        groups,
        image_tiles = IMAGE_SPRITES,
        flipped_x = False,
        flipped_y = False,
        **kwargs,
    ):
        image = image_tiles[(flipped_x, flipped_y, index)]
        rect = image.get_rect()
        return cls(
            image = image,
            image_tiles = image_tiles,
            index = index,
            groups = groups,
            rect = rect,
            **kwargs,
        )
    
    @classmethod
    def create_from_surface(
        cls,
        groups,
        surface,
        **kwargs,
    ):
        rect = surface.get_rect()
        return cls(
            groups = groups,
            image = surface,
            index = None,
            rect = rect,
            **kwargs,
        )
        
    def __init__(
        self,
        groups,
        image_tiles = None,
        index = None,
        rect = None,
        image = None,
        orientation = 0,
        position = (0, 0),
        flipped_x = False,
        flipped_y = False,
        animation_state = AnimationState.stopped,
        frames = None,
    ):
        super().__init__(groups)
        self.image = image
        self.image_tiles = image_tiles
        self.index = index
        self.rect = rect
        self.orientation = orientation
        self.flipped_x = flipped_x
        self.flipped_y = flipped_y
        self._last_angle = None
        self.animation_state = animation_state
        self.frames = frames
        if self.image is not None:
            self.mask = pygame.mask.from_surface(self.image)
            self.surface = self.image.copy()
            self.rotate(self.orientation)
        if self.rect is not None and position is not None:
            self.move(position)
        
    def move(self, position, center: bool = True):
        if center:
            self.rect.center = position
        else:
            self.rect.topleft = position
        
    def rotate(self, angle):
        # do not rotate if the desired angle is the same as the last
        # angle we rotated to.
        if angle == self._last_angle:
            return
        new_image = pygame.transform.rotate(self.surface, angle % 360)
        new_rect = new_image.get_rect(center = self.rect.center)
        self.image = new_image
        self.rect = new_rect
        self.mask = pygame.mask.from_surface(self.image)
        self._last_angle = angle
        
    def set_sprite_index(self, index):
        self.image = self.image_sprites[(self.flipped_x, self.flipped_y, index)]
        self.surface = self.image.copy()
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.index = index
        self.rotate(self.orientation)
        
    def animate(self):
        if self.frames is not None:
            roll = self.frames.get(self.animation_state, None)
            if roll is not None:
                try:
                    next_frame_index = next(roll)
                    if next_frame_index != self.index:
                        self.set_frame(next_frame_index)
                except StopIteration:
                    if AnimationState.state_kill_sprite(self.animation_state):
                        self.kill()
                    self.animation_state = AnimationState.stopped
    
    def set_frame(self, surface):
        self.image = surface
        self.surface = surface.copy()
        self.rect = surface.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.animate()


class layer(enum.IntEnum):
    
    background = 0
    enemy = 20
    shrub = 25
    projectile = 30
    front = 35

class Background(Sprite):
    
    _layer = layer.background

class Shrub(Sprite):
    
    _layer = layer.shrub

class Logo(Sprite):

    _layer = layer.front

class Enemy(Sprite):
    
    _layer = layer.enemy
