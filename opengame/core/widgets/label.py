from typing import Optional, Tuple

import pygame as pg

from ..coordinate import to_pygame, to_opengame
from ..saver import saver
from ..color import ColorType
from ...exceptions import not_created_window


class Font(object):
    def __init__(self, font: Optional[str] = None, size: int = 24):
        self.font = pg.font.Font(font, size)
        self.f, self.s = font, size
        
    def __str__(self):
        return f'Font(font={self.f}, size={self.s})'
        
    @classmethod
    def from_system(cls, name: str, size: int = 25, bold: bool = False, italic: bool = False):
        res = cls()
        res.font = pg.font.SysFont(name, size, bold, italic)
        return res
    
    @staticmethod
    def get_fonts():
        return pg.font.get_fonts()
    
    @staticmethod
    def get_default_font():
        return pg.font.get_default_font()


class Label(pg.sprite.Sprite):
    def __init__(self, text: str = '', font: Optional[Font] = None, antialias: bool = True,
                 color: ColorType = (0, 0, 0)):
        if not saver.window:
            raise not_created_window
        super().__init__()
        if font is None:
            font = Font()
        self.window = saver.window
        self.screen = self.window.screen
        self.screen_rect = self.window.screen_rect
        
        self.text = text
        self.font = font
        self.antialias = antialias
        self.color = color
        self.set_text(text)
        
        self.rect.center = self.screen_rect.center
        
    def __str__(self):
        return f'Label(text={self.text}, font={self.font}, antialias={self.antialias}, color={self.color})'
    
    def __copy__(self):
        label = Label(self.text, self.font, self.antialias, self.color)
        label.image = self.image.copy()
        label.rect = self.rect.copy()
        return label

    @property
    def pos(self):
        return to_opengame(self.rect.center)

    @pos.setter
    def pos(self, pos: Tuple[int, int]):
        self.rect.centerx, self.rect.centery = to_pygame(pos)

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
        
    def set_text(self, text: str = ''):
        if hasattr(self, 'rect'):
            x, y = self.rect.x, self.rect.y
        else:
            x, y = self.screen_rect.center
        self.text = str(text)
        self.image = self.font.font.render(self.text, self.antialias, self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
    def show(self):
        self.screen.blit(self.image, self.rect)
        
    def save(self, file: str):
        pg.image.save(self.image, file)
        
    update = show
