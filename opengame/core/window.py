import os
import sys
from typing import Tuple, Optional, Union, Callable, Any

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame as pg
    from pygame.locals import *
except ImportError:
    raise ImportError('pygame missing') from None

from .event import Event
from .saver import saver
from .mouse import Mouse
from .style import styles, Style
from .color import ColorType
from ..exceptions import OpenGameError


__all__ = ['Window']


def _init_all():
    pg.init()
    pg.mixer.init()
    pg.font.init()
    
    
_DEFAULT_ICON = os.path.join(os.path.dirname(__file__), 'favicon.png')


class Window(object):
    def __init__(self, title: str = 'OpenGame Window', size: Tuple[int, int] = (480, 360), style: Style = styles.normal,
                 favicon: Optional[str] = _DEFAULT_ICON, fps: Union[int, float] = 60, on_center: bool = False,
                 window_pos: Optional[Tuple[int, int]] = None, depth: int = 0, vsync: bool = False):
        if on_center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        if window_pos:
            x, y = window_pos
            os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
            del x, y
            
        _init_all()
        
        self.set_mode(size, style, depth, vsync)
        pg.display.set_caption(title)
        
        if favicon:
            icon = pg.image.load(favicon)
            pg.display.set_icon(icon)
        
        self.clock = pg.time.Clock()
        self.fps = fps
        self.event = Event()
        self.mouse = Mouse()
        self.sprites = []
        self.counter = 0
        
        self._key_down = self._text_input = self._text_editing = False
        self._key = None
        self._text = self._start = self._content = None
        
        _empty_func = lambda: None
        self._when_mouse_down = _empty_func
        self._when_mouse_up = _empty_func
        self._when_key_down = _empty_func
        self._when_key_up = _empty_func
        self._when_mouse_move = _empty_func
        self._when_draw = _empty_func
        self._when_resize = _empty_func
        self._when_active = _empty_func
        
        saver.window = self
        
    def set_mode(self, size: Tuple[int, int], style: Style = styles.normal, depth: int = 0, vsync: bool = False):
        self.width, self.height = size
        self.style = style
        self.depth = depth
        self.vsync = vsync
        self.screen = pg.display.set_mode(size, flags=style.style, depth=depth, vsync=vsync)
        self.screen_rect = self.screen.get_rect()
        
    def resize(self, width: int, height: int):
        self.set_mode((width, height), self.style, self.depth, self.vsync)
    
    @property
    def size(self):
        return self.screen_rect.size
    
    @staticmethod
    def destroy(status: int = 0, exit_all: bool = True):
        pg.quit()
        if exit_all:
            sys.exit(status)
        
    @staticmethod
    def update():
        pg.display.update()
        
    def show(self, status: int = 0, escape_quit: bool = False, quit_disable: bool = False):
        while True:
            self.screen.fill((255, 255, 255))
            for sprite in self.sprites:
                sprite.show()
            self._when_draw()
            
            for event in pg.event.get():
                if event.type == QUIT and (not quit_disable):
                    self.destroy(status)
                if escape_quit and event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.destroy(status)
                    self._key_down = True
                    self._key = event.key
                if event.type == TEXTEDITING:
                    self._text_editing = True
                    self._text = event.text
                    self._start = event.start
                if event.type == TEXTINPUT:
                    self._text_input = True
                    self._content = event.text
                self.event_handler(event)
            
            self.update()
            self.counter += 1
            self.clock.tick(self.fps)

    def when_mouse_down(self, func: Callable[[], Any]):
        self._when_mouse_down = func

    def when_mouse_up(self, func: Callable[[], Any]):
        self._when_mouse_up = func

    def when_mouse_move(self, func: Callable[[], Any]):
        self._when_mouse_move = func

    def when_key_down(self, func: Callable[[], Any]):
        self._when_key_down = func

    def when_key_up(self, func: Callable[[], Any]):
        self._when_key_up = func

    def when_draw(self, func: Callable[[], Any]):
        self._when_draw = func

    def when_resize(self, func: Callable[[], Any]):
        self._when_resize = func

    def when_active(self, func: Callable[[], Any]):
        self._when_active = func
        
    set_mouse_down = when_mouse_down
    set_mouse_up = when_mouse_up
    set_mouse_move = when_mouse_move
    set_key_down = when_key_down
    set_key_up = when_key_up
    set_draw = when_draw
    set_resize = when_resize
    set_active = when_active

    def event_handler(self, event: pg.event.Event):
        self.event = Event(event)
        if self.event.mouse_down:
            self._when_mouse_down()
        elif self.event.mouse_up:
            self._when_mouse_up()
        elif self.event.key_up:
            self._when_key_up()
        elif self.event.key_down:
            self._when_key_down()
        elif self.event.mouse_moving:
            self._when_mouse_move()
        elif self.event.resizing:
            self._when_resize()
        elif self.event.active:
            self._when_active()
            
    @property
    def hwnd(self):
        try:
            return pg.display.get_wm_info()['window']
        except KeyError:
            raise OpenGameError('getting hwnd did not support in this OS') from None
    
    @property
    def title(self):
        return pg.display.get_caption()
    
    @title.setter
    def title(self, title: str):
        pg.display.set_caption(title)
        
    def clear(self):
        self.screen.fill((255, 255, 255))
        
    def rates(self, mod: int):
        return self.counter % mod == 0
    
    def add(self, sprite):
        self.sprites.append(sprite)

    def screenshot(self, file: str = 'screenshot.png'):
        pg.image.save(self.screen, file)
        return file
    
    def entry_options(self):
        res = (self._key_down, self._text_editing, self._text_input,
               self._key, self._text, self._start, self._content)
        self._key_down = self._text_input = self._text_editing = False
        self._key = None
        self._text = self._start = self._content = None
        return res
    
    def fill(self, color: ColorType):
        self.screen.fill(color)
