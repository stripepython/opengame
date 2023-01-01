from typing import Union, Tuple, Sequence

from pygame.math import Vector2, Vector3

from opengame.exceptions import not_created_window
from .saver import saver

__all__ = ['CoordinateType', 'parse', 'to_pygame', 'to_opengame']

CoordinateType = Union[Tuple[Union[int, float], Union[int, float]], Sequence[Union[int, float]], complex, Vector2, Vector3]


def parse(pos: CoordinateType):
    if isinstance(pos, complex):
        return pos.real, pos.imag
    if isinstance(pos, Vector2):
        return tuple(pos.xy)
    if isinstance(pos, Vector3):
        x, y, z = pos.xyz
        return x / z, -y / z
    return tuple(pos)


def to_opengame(pos: CoordinateType):
    x, y = parse(pos)
    if not saver.window:
        raise not_created_window
    cx, cy = saver.window.screen_rect.center
    return x - cx, -y + cy


def to_pygame(pos: CoordinateType):
    x, y = parse(pos)
    if not saver.window:
        raise not_created_window
    cx, cy = saver.window.screen_rect.center
    return x + cx, cy - y
