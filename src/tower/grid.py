import pygame
from dataclasses import dataclass, field
from typing import Tuple, Optional

TILE_HEIGHT = 32
TILE_WIDTH = 32

TILES_Y = 33
TILES_X = 50

START_TILE_ID = ""
STOP_TILE_ID = ""

def get_grid_rect(gx, gy):

    return pygame.Rect(gx * TILE_WIDTH, gy * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)

def tile_positions():

    for y in range(TILES_Y):
        for x in range(TILES_X):
            yield (y, x, x * TILE_WIDTH, y * TILE_HEIGHT)

def get_tile_position(position):

    x, y = position
    return x // TILE_WIDTH, y // TILE_HEIGHT

def create_tile_map(default_value = None) -> list:

    return [[default_value for _ in range(TILES_X)] for _ in range(TILES_Y)]

@dataclass
class GridTile:
    
    tile: pygame.sprite.Sprite
    position: Tuple[int, int]
    east: Optional["GridTile"] = field(repr = False, default = None)
    west: Optional["GridTile"] = field(repr = False, default = None)
    north: Optional["GridTile"] = field(repr = False, default = None)
    south: Optional["GridTile"] = field(repr = False, default = None)
    
def get_portals(tile_map, start_tile_index, stop_tile_index):
    start_position = set()
    stop_position = set()
    for (gy, gx, _, _) in tile_positions():
        tile = tile_map[gy][gx]
        if tile.index == start_tile_index:
            start_position.add((gx, gy))
        elif tile.index == stop_tile_index:
            stop_position.add((gx, gy))
    return start_position, stop_position

def walk_grid(tile_map, visited, gx, gy, valid_tile_indices):
    if not 0 <= gx < TILES_X or not 0 <= gy < TILES_Y:
        return None
    if tile := visited.get((gx, gy)):
        return tile
    if tile.index in valid_tile_indices or tile.index in (
        STOP_TILE_ID,
        START_TILE_ID,
    ):
        tile = GridTile(tile = tile, position = (gx, gy))
        visited[(gx, gy)] = tile
        # Recursively check each cardinal direction
        tile.east = walk_grid(tile_map, visited, gx + 1, gy, valid_tile_indices)
        tile.west = walk_grid(tile_map, visited, gx - 1, gy, valid_tile_indices)
        tile.north = walk_grid(tile_map, visited, gx, gy - 1, valid_tile_indices)
        tile.south = walk_grid(tile_map, visited, gx, gy + 1, valid_tile_indices)
        