from typing import Union

import pygame as pg

from .coordinate import to_pygame, to_opengame, CoordinateType


class Mouse(object):
    
    @property
    def pos(self):
        return to_opengame(pg.mouse.get_pos())
    
    @pos.setter
    def pos(self, pos: CoordinateType):
        pg.mouse.set_pos(to_pygame(pos))
        
    @property
    def x(self):
        return self.pos[0]
    
    @x.setter
    def x(self, x: Union[int, float]):
        y = self.pos[1]
        self.pos = to_pygame((x, y))
        
    @property
    def y(self):
        return self.pos[1]
    
    @y.setter
    def y(self, y: Union[int, float]):
        x = self.pos[0]
        self.pos = to_pygame((x, y))
        
    @property
    def trail(self):
        return pg.mouse.get_rel()
    
    @staticmethod
    def show():
        pg.mouse.set_visible(True)
        
    @staticmethod
    def hide():
        pg.mouse.set_visible(False)
