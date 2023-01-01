from typing import Tuple

import pygame as pg

from ..saver import saver
from ...exceptions import not_created_window
from ..coordinate import to_pygame, to_opengame


class Background(pg.sprite.Sprite):
    def __init__(self, image: str):
        if not saver.window:
            raise not_created_window
        super().__init__()
        self.window = saver.window
        self.screen_rect = self.window.screen_rect
        self.path = image
        self.image = pg.transform.scale(pg.image.load(image), self.screen_rect.size).convert_alpha()
        self.rect = self.image.get_rect()
        
    def __copy__(self):
        background = Background(self.path)
        background.rect = self.rect.copy()
        background.image = self.image.copy()
        return background
    
    copy = clone = __copy__
    
    def __str__(self):
        return f'Background(image={self.path})'

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

    def scroll_down(self, speed=4):
        x, y = self.rect.x, self.rect.y
        y += speed
        if y > self.screen_rect.height:
            y = -self.screen_rect.height
        self.rect.x, self.rect.y = x, y

    def scroll_up(self, speed=4):
        x, y = self.rect.x, self.rect.y
        y -= speed
        if y < -self.screen_rect.height:
            y = self.screen_rect.height
        self.rect.x, self.rect.y = x, y

    def scroll_left(self, speed=4):
        x, y = self.rect.x, self.rect.y
        x -= speed
        if x < -self.screen_rect.width:
            x = self.screen_rect.width
        self.rect.x, self.rect.y = x, y

    def scroll_right(self, speed=4):
        x, y = self.rect.x, self.rect.y
        x += speed
        if x > self.screen_rect.width:
            x = -self.screen_rect.width
        self.rect.x, self.rect.y = x, y
        
    def show(self):
        self.window.screen.blit(self.image, self.rect)
        
    update = show
