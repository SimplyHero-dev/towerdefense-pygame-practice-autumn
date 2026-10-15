import pygame
import importlib.resources

def load(module_path, name):
    ref = importlib.resources.files(module_path) / name
    return importlib.resources.as_file(ref)

def import_image(asset_name: str):
    with load("tower.assets.gfx", asset_name) as resource:
        return pygame.image.load(resource).convert_alpha()

def import_sound(asset_name: str):
    with load("tower.assets.audio", asset_name) as resource:
        return pygame.mixer.Sound(resource)

channels = {
    "score": None,
}

def import_spritesheet(asset_name: str, frame_width: int, frame_height: int):
    """
    Loads a spritesheet and slices it into individual frame Surfaces, reading left-to-right, top-to-bottom.
    """
    with load ("tower.assets.gfx", asset_name) as resource:
        sheet = pygame.image.load(resource).convert_alpha()
        
    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height)).copy()
            frames.append(frame)
    return frames

def load_all_sounds():
    for channel_id, channel_name in enumerate(channels):
        channels[channel_name] = pygame.mixer.Channel(channel_id)
        # Configure the volume here
        channels[channel_name].set_volume(1.0)

SPRITES = {
    "backdrop": "grass_background.png",
    "road1": "FieldsTile_20.png",
    "road2": "FieldsTile_10.png",
    "road3": "FieldsTile_12.png",
    "road4": "FieldsTile_24.png",
    "road5": "FieldsTile_22.png",
    "game_logo": "game_logo.png",
    "shrub1": "6.png",
    "shrub2": "5.png",
    "shrub3": "4.png",
    "shrub4": "3.png",
    "shrub5": "2.png",
    "shrub6": "1.png",
    "blank": "blank.png",
    "portal_start": "FieldsTile_start.png",
    "portal_stop": "FieldsTile_end.png",
}

IMAGE_SPRITES = {}

def load_all_images():
    for sprite_index, sprite_name in SPRITES.items():
        img = import_image(sprite_name)
        for flipped_x in (True, False):
            for flipped_y in (True, False):
                new_img = pygame.transform.flip(img, flip_x = flipped_x, flip_y = flipped_y)
                IMAGE_SPRITES[(flipped_x, flipped_y, sprite_index)] = new_img
 
WALK_FRAMES = []
WALK_FRAMES_FLIPPED = []
TOWER_IDLE_FRAMES = []
PORTAL_IDLE_FRAMES = []
WALK_UP_FRAMES = []
WALK_DOWN_FRAMES = []
DEATH_FRAMES = []
DEATH_FRAMES_FLIPPED = []
DEATH_UP_FRAMES = []
DEATH_UP_FRAMES = []
EXPLOSION_FRAMES = []
                
def load_all_animations():
    global WALK_FRAMES, WALK_FRAMES_FLIPPED, WALK_UP_FRAMES, WALK_DOWN_FRAMES
    global TOWER_IDLE_FRAMES, PORTAL_IDLE_FRAMES
    global DEATH_FRAMES, DEATH_FRAMES_FLIPPED, DEATH_UP_FRAMES, DEATH_DOWN_FRAMES, EXPLOSION_FRAMES
    #enemy
    WALK_FRAMES_FLIPPED = import_spritesheet("S_Walk.png", frame_width = 48, frame_height = 48)
    WALK_FRAMES = [pygame.transform.flip(frame, True, False) for frame in WALK_FRAMES_FLIPPED]
    WALK_UP_FRAMES = import_spritesheet("U_Walk.png", frame_width = 48, frame_height = 48)
    WALK_DOWN_FRAMES = import_spritesheet("D_Walk.png", frame_width = 48, frame_height = 48)
    DEATH_FRAMES_FLIPPED = import_spritesheet("S_Death.png", frame_width = 48, frame_height = 48)
    DEATH_FRAMES = [pygame.transform.flip(frame, True, False) for frame in DEATH_FRAMES_FLIPPED]
    DEATH_UP_FRAMES = import_spritesheet("U_Death.png", frame_width = 48, frame_height = 48)
    DEATH_DOWN_FRAMES = import_spritesheet("D_Death.png", frame_width = 48, frame_height = 48)
    #nonliving
    TOWER_IDLE_FRAMES = import_spritesheet("level7toweridle.png", frame_width = 70, frame_height = 130)
    PORTAL_IDLE_FRAMES = import_spritesheet("PORTAL BLUE-Sheet.png", frame_width = 64, frame_height = 64)
    EXPLOSION_FRAMES = import_spritesheet("PORTAL BLUE-Sheet.png", frame_width = 64, frame_height = 64)


