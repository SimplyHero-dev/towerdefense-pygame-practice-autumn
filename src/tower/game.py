import pygame
from dataclasses import dataclass, field
from tower.state import GameState, StateError
from tower.game_loop import GameLoop, GameMenu

width = 1280
height = 720

SCREENRECT = pygame.Rect(0, 0, width, height)

@dataclass
class TowerGame:
    screen: pygame.Surface
    screen_rect: pygame.Rect
    fullscreen: bool
    state: GameState
    game_menu: GameLoop = field(init=False, default = None)
    
    @classmethod
    def create(cls, fullscreen=False):
        game = cls(
            screen=None,
            screen_rect = SCREENRECT,
            fullscreen = fullscreen,
            state = GameState.initializing,
        )
        game.init()
        return game
    
    def set_state(self, new_state):
        self.state = new_state
        
    def assert_state_is(self, *expected_states: GameState):
        if self.state not in expected_states:
            raise StateError(
                f"Expected the state to be one of {expected_states} not {self.state}"
            )
        
    def init(self):
        self.assert_state_is(GameState.initializing)
        pygame.init()
        window_style = pygame.FULLSCREEN if self.fullscreen else 0
        
        bit_depth = pygame.display.mode_ok(self.screen_rect.size, window_style, 32)
        screen = pygame.display.set_mode(self.screen_rect.size, window_style, bit_depth)
        pygame.mixer.pre_init(
            frequency = 44100,
            size = 32,
            channels = 2,
            buffer = 512,
        )
        pygame.font.init()
        self.screen = screen

        from tower.asset_loader import load_all_images, load_all_sounds
        load_all_images()
        load_all_sounds()

        self.set_state(GameState.initialized)
        self.game_menu = GameMenu(game = self)
        self.set_state(GameState.initialized)
        
    def start_game(self):
        self.assert_state_is(GameState.initialized)
        self.set_state(GameState.main_menu)
        self.loop()
        
    def loop(self):
        while self.state != GameState.quitting:
            if self.state == GameState.main_menu:
                self.game_menu.loop()
            elif self.state == GameState.map_editing:
                self.game_menu.loop()
            elif self.state == GameState.game_playing:
                self.game_menu.loop()
        self.quit()
            
    def quit(self):
        pygame.quit()
