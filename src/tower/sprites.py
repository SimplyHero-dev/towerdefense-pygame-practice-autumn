import pygame
import enum
from tower.asset_loader import IMAGE_SPRITES
from itertools import cycle, chain
from pygame.math import Vector2 as Vector


class AnimationState(enum.Enum):
    stopped = "stopped"
    walking = "walking"
    dying = "dying"
    exploding = "exploding"
    idle = "idle"
    
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
        animation_speed = 6,
        path: iter = None,
        angle: iter = None,
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
        self.animation_speed = animation_speed
        self._animation_tick = 0
        self.path = path
        self.angle = angle
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
                self._animation_tick += 1
                if self._animation_tick < self.animation_speed:
                    return
                self._animation_tick = 0
                
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

    def generate_rotation(self):
        return None
    
    def update(self):
        self.animate()

        if self.path is not None:
            pos, path_angle = next(self.path)
            self.move(pos)
            angle = 0
            if self.angle is not None:
                angle = next(self.angle)
            self.rotate(path_angle + angle)


class layer(enum.IntEnum):
    
    background = 0
    turret = 15
    enemy = 20
    shrub = 25
    projectile = 30
    turret_sights = 35
    front = 35

class Background(Sprite):
    
    _layer = layer.background

class Shrub(Sprite):
    
    _layer = layer.shrub

class Logo(Sprite):

    _layer = layer.front

class Enemy(Sprite):
    
    _layer = layer.enemy

class Turret(Sprite):
    
    _layer = layer.turret


def extend(iterable, repeat):
    return (elem for elem in iterable for _ in range(repeat))

def create_turret_sweep(orientation, sweep_degrees, speed = 3):
    half_sweep = sweep_degrees // 2
    return cycle(
        extend(
            chain(
                range(orientation - half_sweep, orientation + half_sweep),
                reversed(range(orientation - half_sweep, orientation + half_sweep)),
            ),
            speed,
        ),
    )

class Vision(Sprite):
    
    _layer = layer.turret_sights
    
    @classmethod
    def create_vision(cls, rect, **kwargs):
        surface = create_surface(size = rect.size)
        surface.fill((0, 0, 128, 128))
        surface.set_colorkey((0, 128, 128), rect, width = 2)
        pygame.draw.rect(surface, (0, 128, 128), rect, width = 2)
        return cls.create_from_surface(surface = surface, **kwargs)
    
    def __init__(self, turret, **kwargs):
        self.turret = turret
        super().__init__(**kwargs)
        self.set_orientation(self.orientation)
        
    def generate_rotation(self):
        return create_turret_sweep(self.orientation, sweep_degrees = 60)
    
    def set_orientation(self, orientation):
        self.orientation = orientation
        self.angle = self.generate_rotation()
        self.rotate(next(self.angle))
        
    def rotate(self, angle):
        new_image = pygame.transform.rotate(self.surface, new_angle)
        turret = self.turret
        v = Vector(
            0,
            (self.surface.get_rect().height // 2 + turret.surface.get_rect().top),
        )
        rv = v.rotate(-new_angle)
        new_rect = new_image.get_rect(center = turret.rect.center + rv)
        self.image = new_image
        self.rect = new_rect
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rotate(next(self.angle))
        
