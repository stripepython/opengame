from typing import Tuple

import pygame as pg

from ..coordinate import to_pygame, to_opengame
from ..saver import saver
from ..color import ColorType
from ...exceptions import not_created_window


class Bar(pg.sprite.Sprite):
    def __init__(self, width: int = 240, height: int = 30, border_width: int = 1,
                 proportion: float = 0.0, border_color: ColorType = (0, 0, 0),
                 bar_color: ColorType = (255, 0, 0)):
        if not saver.window:
            raise not_created_window
        super().__init__()
        self.window = saver.window
        self.screen = self.window.screen
        self.screen_rect = self.window.screen_rect
        
        self.width, self.height = width, height
        self.proportion = proportion
        self.realx, self.realy = 0, 0
        self.init_rect()
        
        self.border_color = border_color
        self.bar_color = bar_color
        self.border_width = border_width
        self.pos = 0, 0
        
    def init_rect(self):
        self.rect_border = pg.rect.Rect(self.realx, self.realy, self.width, self.height)
        self.rect_bar = pg.rect.Rect(self.realx, self.realy, self.width * self.proportion, self.height)
        self.rect = self.rect_border

    @property
    def pos(self):
        return to_opengame(self.rect_border.center)

    @pos.setter
    def pos(self, pos: Tuple[int, int]):
        self.realx, self.realy = to_pygame(pos)
        self.realx -= self.rect_border.w // 2
        self.realy -= self.rect_border.h // 2
        self.init_rect()

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, x: int):
        self.pos = x, self.y

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, y: int):
        self.pos = self.x, y

    def pack(self):
        self.window.add(self)

    def unpack(self):
        self.window.sprites.remove(self)
        
    def show(self):
        pg.draw.rect(self.screen, self.bar_color, self.rect_bar)
        pg.draw.rect(self.screen, self.border_color, self.rect_border, width=self.border_width)

    def set_proportion(self, proportion: float):
        if proportion < 0:
            proportion = 0
        self.proportion = proportion
        self.init_rect()
        
    def resize(self, width: int, height: int):
        self.width, self.height = width, height
        self.init_rect()
