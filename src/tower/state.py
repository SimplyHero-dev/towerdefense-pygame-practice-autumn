import enum

class GameState(enum.Enum):
    unknown = "unknown"
    initializing = "initializing"
    initialized = "initialized"
    map_ediitng = "map_editing"
    game_playing = "game_playing"
    main_menu = "main_menu"
    game_ending = "game_ended"
    quitting = "quitting"
    
class StateError(Exception):
    pass
