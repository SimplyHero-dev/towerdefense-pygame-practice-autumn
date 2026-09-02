import pygame
from dataclasses import dataclass
from tower.game import TowerGame
from tower.state import GameState

@dataclass
class GameLoop:
    game: TowerGame
    
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
    def screen(self):
        return self.game.state
    
class GameMenu(GameLoop):
    pass

class GameEditing(GameLoop):
    pass
