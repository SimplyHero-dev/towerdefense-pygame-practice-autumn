import operator
from itertools import pairwise, accumulate, repeat
from pygame.math import Vector2 as Vector

def lerp(a, b, t):
    return a + (t * (b - a))

def linear(a, b, m, n):
    return a + (m * (b - a) / n)

def interpolate(iterable, n, fn = linear):
    return (fn(a, b, m , n) for a, b in pairwise(iterable) for m in range(0, n + 1))

def create_project_path(start, stop, speed, max_distance):
    vh = (stop - start).normalize() * speed
    path = zip(
        accumulate(
            repeat(vh, max_distance),
            func = operator.add,
            initial = start,
        )
    )
    return path

def path_with_no_rotation(position_iterable):
    return ((pos, 0) for pos in position_iterable)