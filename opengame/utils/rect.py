from typing import Union

import pygame as pg

from ..core.window import Window
from ..core.coordinate import to_opengame
from ..exceptions import OpenGameError

__all__ = ['RectTool']


class RectTool(object):
    def __init__(self, obj: Union[pg.sprite.Sprite, Window]):
        if isinstance(obj, Window):
            rect = obj.screen_rect.copy()
        elif isinstance(obj, pg.sprite.Sprite):
            rect = obj.rect.copy()
        else:
            raise OpenGameError('must be a sprite or window')
        self.rect = rect
        
    def _convert(self, x=None, y=None):
        if x and y:
            return to_opengame((x, y))
        if x:
            return to_opengame((x, self.rect.y))[0]
        return to_opengame((self.rect.x, y))[0]
    
    @property
    def x(self):
        return self._convert(x=self.rect.x)
    
    @property
    def y(self):
        return self._convert(y=self.rect.y)
    
    @property
    def center_x(self):
        return self._convert(x=self.rect.centerx)
    
    @property
    def center_y(self):
        return self._convert(y=self.rect.centery)
    
    @property
    def center(self):
        return to_opengame(*self.rect.center)
    
    @property
    def pos(self):
        return self._convert(self.rect.x, self.rect.y)
    
    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height
    
    w = width
    h = height
    
    @property
    def top_left(self):
        return to_opengame(self.rect.topleft)
    
    @property
    def top_right(self):
        return to_opengame(self.rect.topright)
    
    @property
    def top_middle(self):
        return to_opengame(self.rect.midtop)
    
    @property
    def bottom_left(self):
        return to_opengame(self.rect.bottomleft)
    
    @property
    def bottom_right(self):
        return to_opengame(self.rect.bottomright)
    
    @property
    def bottom_middle(self):
        return to_opengame(self.rect.midbottom)
    
    @property
    def left_middle(self):
        return to_opengame(self.rect.midleft)
    
    @property
    def right_middle(self):
        return to_opengame(self.rect.midright)
    
    @property
    def normal(self):
        return self.x, self.y, self.width, self.height
    
    def collide(self, x: float, y: float):
        return self.rect.collidepoint(x, y)
