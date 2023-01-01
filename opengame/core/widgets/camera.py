from typing import Optional, Union, Tuple, List, Dict

import pygame as pg

from ..coordinate import to_pygame, to_opengame
from ..saver import saver
from ...exceptions import not_created_window, OpenGameError


class Camera(pg.sprite.Sprite):
    def __init__(self, device: Optional[str] = None, size: Union[Tuple[int, int], List[int]] = (320, 180),
                 color_mode: str = 'RGB', auto_start: bool = False, backend: Optional[str] = None):
        if not saver.window:
            raise not_created_window
        self.window = saver.window
        super().__init__()
        try:
            import pygame.camera
            self.cra = pygame.camera
            self.cra.init(backend)
        except RuntimeError:
            raise OpenGameError('only supports Linux (V4L2) and Windows (MSMF) cameras')
        if not self.cra.list_cameras():
            raise OpenGameError('no cameras available')
        
        if not device:
            device = self.cra.list_cameras()[0]
        self.set_mode(device, size, color_mode)
        self.backend = backend
        self.image = pg.surface.Surface(size)
        self.last = self.image.copy()

        if auto_start:
            self.start()
            
    def __copy__(self):
        return Camera(self.device, self.size, self.color_mode, False, self.backend)
    
    copy = __copy__
    
    def set_mode(self, device: Optional[str] = None, size: Union[Tuple[int, int], List[int]] = (320, 180),
                 color_mode: str = 'RGB'):
        if not device:
            device = self.cra.list_cameras()[0]
        self.device = device
        self.size = size
        self.color_mode = color_mode
        self.camera = self.cra.Camera(device, size, color_mode)
        self.rect = pg.rect.Rect((0, 0), self.size)
        self.pos = 0, 0

    def pack(self):
        self.window.add(self)

    def unpack(self):
        self.window.sprites.remove(self)

    def start(self):
        self.camera.start()
        
    def stop(self):
        self.camera.stop()

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

    @property
    def controls(self):
        hflip, vfilp, brightness = self.camera.get_controls()
        return {'hfilp': hflip, 'vfilp': vfilp, 'brightness': brightness}

    @controls.setter
    def controls(self, values: Dict[str, Union[bool, int]]):
        self.camera.set_controls(**values)

    def flip_horizontally(self):
        self.camera.set_controls(hflip=True)

    def flip_vertically(self):
        self.camera.set_controls(vflip=True)

    def set_brightness(self, brightness: int):
        self.camera.set_controls(brightness=brightness)
        
    @property
    def raw(self):
        return self.camera.get_raw()
    
    def save(self, save_path: str = 'camera.jpg', mode: str = 'wb', **kwargs):
        with open(save_path, mode, **kwargs) as img:
            img.write(self.raw)
        return save_path
    
    def record(self, raise_for_stopped: bool = False):
        try:
            self.image = self.camera.get_image()
            self.last = self.image.copy()
        except pg.error as err:
            if raise_for_stopped:
                err = OpenGameError(str(err))
                raise err from None
            self.image = self.last

    def show(self):
        self.window.screen.blit(self.image, self.rect)
        
    update = show
