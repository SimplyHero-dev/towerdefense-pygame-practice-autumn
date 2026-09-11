import pygame
import random
from dataclasses import dataclass, field
from typing import Tuple, Optional
from pygame.math import Vector2 as Vector
from itertools import pairwise, chain
from tower.movement import interpolate

TILE_HEIGHT = 32
TILE_WIDTH = 32

TILES_Y = 33
TILES_X = 50

START_TILE_ID = "portal"
STOP_TILE_ID = "portal"
MOVABLE_TILE_IDS = "road1", "road2", "road3", "road4", "road5",

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
        
def update_path_finding(tile_map):
    start_position, stop_position = get_portals(tile_map, START_TILE_ID, STOP_TILE_ID)
    paths = []
    while start_position:
        visited = {}
        gx, gy = start_position.pop()
        start_tile = walk_grid(tile_map, visited, gx, gy, MOVABLE_TILE_IDS)
        
        for stop_position in stop_position:
            try:
                paths.append((start_tile, visited[stop_position]))
            except KeyError:
                pass
    return paths

def dfs_find_path(start_tile: GridTile, stop_positions):
    # keep track of visited grid tiles
    visited = {}
    
    def _walk(
        path: list,
        current_tile: Optional[GridTile],
    ):
        if current_tile is None or current_tile.position in visited:
            return []
        visited[current_tile.position] = current_tile
        if current_tile.position in stop_positions:
            return path + [current_tile]
        directions = [
            current_tile.east,
            current_tile.west,
            current_tile.north,
            current_tile.south,
        ]
        random.shuffle(directions)
        for direction in directions:
            subpath = _walk(path + [current_tile], direction)
            if subpath:
                return subpath
        return []
    
    return _walk([], start_tile)

def get_directions(start_tile: GridTile, stop_positions):
    try:
        vectors = []
        for a, b, in pairwise(dfs_find_path(start_tile, stop_positions)):
            v2 = Vector(b.tile.rect.center)
            v1 = Vector(a.tile.rect.center)
            vectors.append(
                (
                    v1,
                    v2,
                )
            )
    except StopIteration:
        pass
    return vectors


def make_enemy_path(start_tile, stop_position, jitter = 10, speed = 40, turn_speed = 8):
    jitter = random.randint(-jitter, jitter)
    jv = Vector(jitter, -30 + jitter)
    for v1, v2 in pairwise(
        chain.from_iterable(
            interpolate(t, speed) for t in get_directions(start_tile, stop_position)
        )
    ):
        if v1 == v2:
            continue
        dot = v1.normalize().dot((v2 - v1).normalize())
        flipx = dot < 0
        yield(
            v2 + jv,
            0,
            flipx,
        )
