import warnings
from typing import Optional, Tuple, Union

import pygame as pg
import cv2

from ..saver import saver
from ..coordinate import to_pygame, to_opengame
from ...exceptions import not_created_window, OpenGameError, OpenGameWarning


class Video(pg.sprite.Sprite):
    def __init__(self, video_path: Union[int, str] = 0, size: Optional[Tuple[int, int]] = None,
                 auto_set_fps: bool = True, warned: bool = True):
        if not saver.window:
            raise not_created_window
        super().__init__()
        if video_path == 0 and warned:
            warnings.warn('not recommended set video_path to 0, use opengame.Camera() widget', OpenGameWarning)
        self.video_path = video_path
        self.video = cv2.VideoCapture(video_path)
        
        self.window = saver.window
        self.screen = self.window.screen
        self.screen_rect = self.window.screen_rect
        
        ret, frame = self.video.read()
        if not (ret and self.video.isOpened()):
            raise OpenGameError('cannot red this video')
        frame = cv2.transpose(frame)
        if not size:
            size = frame.shape[0], frame.shape[1]
        frame = cv2.resize(frame, size)
        self.size = size
        self.width, self.height = self.size
        
        self.image = pg.surfarray.make_surface(frame)
        self.last = self.image.copy()
        self.rect = self.image.get_rect()
        
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        if auto_set_fps:
            self.set_fps()
            
        self.update = self.show
            
    def set_fps(self):
        self.window.fps = self.fps
        
    def resize(self, width: int, height: int):
        self.rect.width, self.rect.height = width, height
        self.width, self.height = width, height
        self.size = self.width, self.height

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
        
    def show(self):
        self.screen.blit(self.image, self.rect)
        
    def read(self, quit_if_over: bool = False, raise_if_over: bool = False, *args, **kwargs):
        ret, frame = self.video.read()
        if ret:
            frame = cv2.transpose(cv2.resize(frame, self.size))
            self.image = pg.surfarray.make_surface(frame)
            self.last = self.image.copy()
        else:
            if quit_if_over:
                self.window.destroy(*args, **kwargs)
            if raise_if_over:
                raise OpenGameError('video play over')
            self.video.release()
            self.image = self.last
