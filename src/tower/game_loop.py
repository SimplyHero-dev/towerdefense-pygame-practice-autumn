import pygame
import random
from dataclasses import dataclass
from tower.state import GameState
from tower.asset_loader import IMAGE_SPRITES
from tower.sprites import Background, Shrub, Logo
from tower.grid import create_tile_map, tile_positions
from tower.sprite_manager import Spritemanager

DESIRED_FPS = 60

BUSH_INDICES = ["shrub1", "shrub2", "shrub3", "shrub4", "shrub5", "shrub6"]
TILE_INDICES = ["road1", "road2", "road3", "road4", "road5"]

def create_surface(size, flags = pygame.SRCALPHA):
    return pygame.Surface(size, flags = flags)

@dataclass
class GameLoop:
    game: "TowerGame"
    
    def handle_events(self):
        
        for event in pygame.event.get():
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ) or event.type == pygame.QUIT:
                self.set_state(GameState.quitting)
            
            self.handle_event(event)
            
    def loop(self):
        while self.state != GameState.quitting:
            self.handle_events()
            
    def handle_event(self, event):
        pass
        
    def set_state(self, new_state):
        self.game.set_state(new_state)
    
    @property
    def screen(self):
        return self.game.screen
    
    @property
    def state(self):
        return self.game.state
    
class GameMenu(GameLoop):

    def create_level(self):
        background_tiles = create_tile_map()
        for (gy, gx, x, y) in tile_positions():
            background_tile = Background.create_from_tile(
                groups = [],
                index = "blank",
            )
            background_tile.rect.topleft = (x, y)
            background_tiles[gy][gx] = background_tile
        return background_tiles

    def draw_background(self):
        self.background.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))
        for (gy, gx, x, y) in tile_positions():
            background_tile = self.level[gy][gx]
            self.background.blit(background_tile.image, (x, y))

    def loop(self):
        clock = pygame.time.Clock()
        self.background = create_surface(self.game.screen_rect.size)

        self.level = self.create_level()
        self.draw_background()

        group = pygame.sprite.LayeredUpdates()
        logo = Logo.create_from_tile(
            groups = [group],
            index = "game_logo",
            orientation = 0,
            position = self.game.screen_rect.center,
        )
        screen_width, screen_height = self.game.screen_rect.size
        self.bushes = []
        for _ in range(15):
            position = (
                random.randint(0, screen_width),
                random.randint(0, screen_height),
            )
            bush = Shrub.create_from_tile(
                groups = [group],
                index = random.choice(BUSH_INDICES),
                orientation = 0,
                position = position,
            )
            self.bushes.append(bush)

        #!rotation = 0
        while self.state == GameState.main_menu:
            self.handle_events()
            #repaint background
            self.screen.blit(self.background, (0, 0))
            #!rotation += 1
            #!logo.rotate(rotation % 360)
            # Instruct all sprites to update
            group.update()
            # Tell the group where to draw
            group.draw(self.screen)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.game.game_editing.level = self.level
            self.game.game_editing.sprite_manager.level = self.level
            self.set_state(GameState.map_editing)

@dataclass
class GameEditing(GameLoop):
    layers: pygame.sprite.LayeredUpdates
    sprite_manager: Spritemanager
    level: list
    spawn: callable = None
    bush_index: int = 0
    tile_index: int = 0

    @property
    def mouse_position(self):
        return pygame.mouse.get_pos()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.sprite_manager.move(self.mouse_position)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button in (
            pygame.BUTTON_LEFT,
            pygame.BUTTON_RIGHT,
        ):
            if event.button == pygame.BUTTON_LEFT:
                self.sprite_manager.place(self.mouse_position)
                if self.spawn:
                    self.spawn()
            elif event.button == pygame.BUTTON_RIGHT:
                self.sprite_manager.kill()
                self.spawn = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.sprite_manager.kill()
                self.spawn = lambda: self.sprite_manager.select_sprites(
                    self.sprite_manager.create_background(
                        index = TILE_INDICES[self.tile_index],
                        position = self.mouse_position,
                    ),
                    position = self.mouse_position,
                )
                self.spawn()
            elif event.key == pygame.K_2:
                self.sprite_manager.kill()
                self.spawn = lambda: self.sprite_manager.select_sprites(
                    self.sprite_manager.create_shrub(
                        index = BUSH_INDICES[self.bush_index],
                        position = self.mouse_position,
                    ),
                    position = self.mouse_position,
                )
                self.spawn()
            elif event.key == pygame.K_TAB:
                if self.spawn is not None:
                    self.bush_index = (self.bush_index + 1) % len(BUSH_INDICES)
                    self.tile_index = (self.tile_index + 1) % len(TILE_INDICES)
                    self.sprite_manager.kill()
                    self.spawn()

    def loop(self):
        background = create_surface(self.game.screen_rect.size)
        background.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))

        while self.state == GameState.map_editing:
            self.handle_events()
            self.screen.blit(background, (0, 0))
            self.layers.update()
            self.layers.draw(self.screen)
            pygame.display.flip()

