from typing import Optional, Tuple, Callable, Any

import pygame as pg
import pygame.freetype as ft

from ..coordinate import to_pygame, to_opengame
from ..saver import saver
from ..color import ColorType
from ...utils.timer import Timer
from ...exceptions import not_created_window, OpenGameError


class Entry(pg.sprite.Sprite):
    timer = Timer()
    
    def __init__(self, default_text: str = '', width: Optional[int] = None, height: int = 40,
                 font_name: str = 'msmincho', font_size: int = 28, auto_start: bool = True,
                 bold: bool = False, foreground: ColorType = (255, 255, 255),
                 background: ColorType = (0, 0, 0), italic: bool = False, font_second: str = 'Arial'):
        if pg.get_sdl_version() < (2, 0, 0):
            raise OpenGameError('must use pygame2')
        if not saver.window:
            raise not_created_window
        super().__init__()
        self.window = saver.window
        self.screen = self.window.screen
        self.screen_rect = self.window.screen_rect
        
        self.rect = pg.Rect(0, 0, self.window.width, height)
        if width:
            self.rect.width = width
        if auto_start:
            self.start()
        self.set_font(font_name, font_size, bold, italic, font_second)
        self.text = default_text
        self.editing_text = ''
        self.position = len(default_text)
        self.editing_pos = 0
        self.editing = False
        
        self.background, self.foreground = background, foreground
        
        self.update = self.show
        self.pos = 0, 0

        _empty_func = lambda: None
        self._when_press_return = _empty_func
    
    def start(self):
        pg.key.start_text_input()
        pg.key.set_text_input_rect(self.rect)
    
    @staticmethod
    def stop():
        pg.key.stop_text_input()
        
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
        
    def set_font(self, font_name: str = 'msmincho', font_size: int = 28, bold: bool = False,
                 italic: bool = False, font_second: str = 'Arial'):
        try:
            self.font = ft.SysFont(font_name, font_size, bold, italic)
        except RuntimeError:
            self.font = ft.SysFont(font_second, font_size, bold, italic)
        
    def when_press_return(self, func: Callable[[], Any]):
        self._when_press_return = func
        
    when_press_enter = when_press_return
        
    @property
    def _event(self):
        return self.window.event.get_event()
    
    def get(self):
        return self.text
    
    def show(self):
        pg.draw.rect(self.screen, self.background, self.rect)
        (key_down, text_editing, text_input, key, text, start, content) = self.window.entry_options()

        if key_down:
            if self.editing:
                if not self.editing_text:
                    self.editing = False
            elif key == pg.K_BACKSPACE:
                self.timer.zero()
                if len(self.text) > 0:
                    self.text = self.text[:self.position - 1] + self.text[self.position:]
                    self.position = max(0, self.position - 1)
            elif key == pg.K_DELETE:
                self.text = self.text[:self.position] + self.text[self.position + 1:]
            elif key == pg.K_LEFT:
                self.position = max(0, self.position - 1)
            elif key == pg.K_RIGHT:
                self.position = min(len(self.text), self.position + 1)
            elif key in {pg.K_RETURN, pg.K_KP_ENTER}:
                self._when_press_return()

        if text_editing:
            self.editing = True
            self.editing_text = text
            self.editing_pos = start

        if text_input:
            self.editing = False
            self.editing_text = ''
            self.text = self.text[:self.position] + content + self.text[self.position:]
            self.position += len(content)

        start_pos = self.rect.copy()
        text_l = self.text[:self.position]
        text_m = self.editing_text[:self.editing_pos] + "|" + self.editing_text[self.editing_pos:]
        text_r = self.text[self.position:]

        rect_textL = self.font.render_to(self.screen, start_pos, text_l, self.foreground)
        start_pos.x += rect_textL.width

        text_m_rect = self.font.render_to(
            self.screen, start_pos, text_m, self.foreground, None, ft.STYLE_UNDERLINE
        )
        start_pos.x += text_m_rect.width
        self.font.render_to(self.screen, start_pos, text_r, self.foreground)
