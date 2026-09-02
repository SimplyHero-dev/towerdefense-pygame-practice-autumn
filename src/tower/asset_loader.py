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

def load_all_sounds():
    for channel_id, channel_name in enumerate(channels):
        channels[channel_name] = pygame.mixer.Channel(channel_id)
        # Configure the volume here
        channels[channel_name].set_volume(1.0)

SPRITES = {
    "backdrop": "grass_background.png",
    "road": "FieldsTile_20.png"
}

IMAGE_SPRITES = {}

def load_all_images():
    for sprite_index, sprite_name in SPRITES.items():
        img = import_image(sprite_name)
        for flipped_x in (True, False):
            for flipped_y in (True, False):
                new_img = pygame.transform.flip(img, flip_x = flipped_x, flip_y = flipped_y)
                IMAGE_SPRITES[(flipped_x, flipped_y, sprite_index)] = new_img

