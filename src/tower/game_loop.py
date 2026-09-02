import pygame
from dataclasses import dataclass
from tower.state import GameState
from tower.asset_loader import IMAGE_SPRITES

DESIRED_FPS = 60

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
        self.screen.blit(IMAGE_SPRITES[(False, False, "backdrop")], (0, 0))
        while self.state == GameState.main_menu:
            self.handle_events()
            pygame.display.flip()
            pygame.display.set_caption(f"FPS {round(clock.get_fps())}")
            clock.tick(DESIRED_FPS)

class GameEditing(GameLoop):
    pass
