import pygame
import random
from dataclasses import dataclass
from tower.state import GameState
from tower.asset_loader import IMAGE_SPRITES
from tower.sprites import Background, Shrub

DESIRED_FPS = 60

BUSH_INDICES = ["shrub1", "shrub2", "shrub3", "shrub4", "shrub5", "shrub6"]

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
    def loop(self):
        clock = pygame.time.Clock()
        background = create_surface(self.game.screen_rect.size)
        background.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))
        group = pygame.sprite.LayeredUpdates()
        logo = Background.create_from_tile(
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

        rotation = 0
        while self.state == GameState.main_menu:
            self.handle_events()
            #repaint background
            self.screen.blit(background, (0, 0))
            #rotation += 1
            #logo.rotate(rotation % 360)
            # Instruct all sprites to update
            group.update()
            # Tell the group where to draw
            group.draw(self.screen)
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

class GameEditing(GameLoop):
    pass
