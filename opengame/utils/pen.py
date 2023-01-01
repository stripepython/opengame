from typing import Tuple, List

import pygame as pg
import pygame.gfxdraw as gfx

from ..core.saver import saver
from ..exceptions import not_created_window
from ..core.color import ColorType
from ..core.coordinate import to_pygame, CoordinateType


class Pen(object):
    def __init__(self):
        if not saver.window:
            raise not_created_window
        self.screen = saver.window.screen
        
    def circle(self, color: ColorType, center: CoordinateType, radius: int = 30,
               fill: bool = True, width: int = 1):
        if fill:
            width = 0
        pg.draw.circle(self.screen, color, to_pygame(center), radius, width=width)
        
    def rect(self, color: ColorType, left_top: CoordinateType, size: Tuple[int, int],
             fill: bool = True, width: int = 1):
        if fill:
            width = 0
        pg.draw.rect(self.screen, color, pg.rect.Rect(to_pygame(left_top), size), width=width)
    
    rectangle = rect
    
    def line(self, color: ColorType, start: CoordinateType, end: CoordinateType,
             width: int = 1):
        pg.draw.aaline(self.screen, color, to_pygame(start), to_pygame(end), width)
        
    def polygon(self, color: ColorType, points: List[CoordinateType], fill: bool = True, width: int = 1):
        if fill:
            width = 0
        points = [to_pygame(p) for p in points]
        pg.draw.polygon(self.screen, color, points, width=width)
        
    def ellipse(self, color: ColorType, left_top: CoordinateType, size: Tuple[int, int],
                fill: bool = True, width: int = 1):
        if fill:
            width = 0
        pg.draw.ellipse(self.screen, color, pg.rect.Rect(to_pygame(left_top), size), width=width)
        
    def arc(self, color: ColorType, point: CoordinateType, radius: int, start_degree: float, stop_degree: float):
        x, y = to_pygame(point)
        gfx.arc(self.screen, x, y, radius, start_degree, stop_degree, color)

    def pie(self, color: ColorType, point: CoordinateType, radius: int, start_degree: float, stop_degree: float):
        x, y = to_pygame(point)
        gfx.pie(self.screen, x, y, radius, start_degree, stop_degree, color)
        
    def bezier(self, color: ColorType, points: List[CoordinateType], steps: int = 10):
        points = [to_pygame(p) for p in points]
        gfx.bezier(self.screen, points, steps, color)
