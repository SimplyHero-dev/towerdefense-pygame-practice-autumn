import tower
import importlib.resources

def load(module_path, name):
    return importlib.resources.path(module_path, name)

def import_image(asset_name: str):
    with load("tower.assets.gfx", asset_name) as resource:
        return pygame.image.load(resource).convert_alpha()
    