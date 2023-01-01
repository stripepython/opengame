import math
from typing import Optional, Tuple, Callable, Any

import pygame as pg

from ..saver import saver
from ..coordinate import to_pygame, to_opengame
from ...exceptions import not_created_window


class Sprite(pg.sprite.Sprite):
    def __init__(self, image: str, size: Optional[Tuple[int, int]] = None):
        if not saver.window:
            raise not_created_window
        super().__init__()
        self.window = saver.window
        self.screen = self.window.screen
        self.screen_rect = self.window.screen_rect
        self.path = image
        self.angle = 0
        
        self.image = pg.image.load(image).convert_alpha()
        if size:
            self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.pos = 0, 0
        
        _empty_func = lambda: None
        self._when_click_me = _empty_func
        
    def __str__(self):
        return f'Sprite(image={self.path}, size={self.rect.size})'

    def __copy__(self):
        sprite = Sprite(image=self.path, size=self.rect.size)
        sprite.rect = self.rect.copy()
        sprite.image = self.image.copy()
        return sprite

    clone = copy = __copy__
    
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
        
    def rotate(self, angle: float, image_rotate: bool = True):
        x, y = self.rect.x, self.rect.y
        self.angle = angle
        if image_rotate:
            self.image = pg.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def when_click_me(self, func: Callable[[], Any]):
        self._when_click_me = func
        
    def collide(self, sprite: pg.sprite.Sprite):
        return self.rect.colliderect(sprite.rect)
    
    def collide_point(self, point: Tuple[int, int]):
        return self.rect.collidepoint(to_pygame(point))
    
    def collide_mouse(self):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def collide_left_edge(self):
        return self.rect.left <= 0

    def collide_right_edge(self):
        return self.rect.right >= self.screen_rect.width

    def collide_top_edge(self):
        return self.rect.top <= 0

    def collide_bottom_edge(self):
        return self.rect.bottom >= self.screen_rect.height

    def collide_edge(self):
        return self.collide_left_edge() or self.collide_right_edge() or self.collide_top_edge() or self.collide_bottom_edge()
    
    def show(self):
        self.screen.blit(self.image, self.rect)
        if self.window.event.mouse_down and self.collide_mouse():
            self._when_click_me()
        
    update = show
    
    def forward(self, length: int):
        angle = math.radians(self.angle)
        self.pos = self.x + length * math.cos(angle), self.y - length * math.sin(angle)

    def rebound_if_collide_edge(self):
        if self.collide_edge():
            self.rotate(self.angle)
            
    rice = rebound_if_collide_edge
    
    def save(self, file: str):
        pg.image.save(self.image, file)
    