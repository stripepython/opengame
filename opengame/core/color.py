from typing import Union, Tuple, List

import pygame

__all__ = ['Color', 'ColorType']


def _count_hue(h: int, u: int, e: int):
    e += (
        1 if e < 0
        else -1 if e > 1
        else 0
    )
    if (6 * e) < 1:
        return h + (u - h) * 6 * e
    if (2 * e) < 1:
        return u
    if (3 * e) < 2:
        return h + (u - h) * (2 / 3 - e) * 6
    return h


class Color(pygame.color.Color):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def from_hex(cls, string: Union[int, str], alpha: int = 255):
        if isinstance(string, str):
            string = string.replace('#', '')
            num = int(string, base=16)
        else:
            num = int(string)
        rgba = (
            (num >> 16) & 0xFF,
            (num >> 8) & 0xFF,
            num & 0xFF,
            alpha
        )
        return cls(*rgba)
    
    @classmethod
    def from_hsv(cls, h: int, s: int, v: int, alpha: int = 255):
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        choices = [
            (c, x, 0), (x, c, 0), (0, c, x),
            (0, x, c), (x, 0, c), (c, 0, x)
        ]  # Define cases
        lower, upper = 0, 60
        r1, g1, b1 = 0, 0, 0
        for n in choices:
            if lower < h < upper:
                r1, g1, b1 = n
            lower += 60
            upper += 60
        
        r = (r1 + m) * 255
        g = (g1 + m) * 255
        b = (b1 + m) * 255
        
        return cls(r, g, b, alpha)
    
    @classmethod
    def from_hsl(cls, h: int, s: int, L: int, alpha: int = 255):
        if s == 0:
            r = g = b = L * 255
        else:
            y = L * 6 if L < .5 else (L + s) - (s * L)
            x = 2 * L - y
            r = 255 * _count_hue(x, y, h + 1 / 3)
            g = 255 * _count_hue(x, y, h)
            b = 255 * _count_hue(x, y, h - 1 / 3)
        return cls(r, g, b, alpha)
    
    @classmethod
    def from_cmyk(cls, c: int, m: int, y: int, k: int, alpha: int = 255):
        rk = 255 * (1 - k)
        rgba = (
            (1 - c) * rk,
            (1 - m) * rk,
            (1 - y) * rk,
            alpha
        )
        return cls(*rgba)
    
    @classmethod
    def from_yuv(cls, y: int, u: int, v: int, alpha: int = 255):
        rgba = (
            y + 1.4075 * (v - 128),
            y - .3455 * (u - 128) - .7169 * (v - 128),
            y + 1.7790 * (u - 128),
            alpha
        )
        return cls(*rgba)


ColorType = Union[pygame.color.Color, Tuple[int, int, int], Tuple[int, int, int, int], List[int]]
