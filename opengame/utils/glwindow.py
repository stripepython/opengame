from typing import Tuple, Optional, Union

import pygame as pg

from ..core.window import Window
from ..core.style import Style, styles
from ..exceptions import OpenGameError

__all__ = ['GLWindow']


class GLWindow(Window):
    def __init__(self, title: str = 'OpenGame GL Window', size: Tuple[int, int] = (480, 360),
                 style: Style = styles.normal, favicon: Optional[str] = None, fps: Union[int, float] = 60,
                 on_center: bool = False, window_pos: Optional[Tuple[int, int]] = None,
                 depth: int = 0, vsync: bool = False, gl_version: Optional[Tuple[int, int]] = None):
        try:
            from OpenGL import GL, GLU, GLUT
            self.gl, self.glu, self.glut = GL, GLU, GLUT
        except ImportError:
            raise OpenGameError('cannot import pyopengl, please install it') from None
        
        self.init_gl(gl_version)
        super().__init__(title, size, style, favicon, fps, on_center,
                         window_pos, depth, vsync)
        
    @staticmethod
    def init_gl(gl_version: Optional[Tuple[int, int]] = None):
        pg.init()
        if not gl_version:
            gl_version = (
                pg.display.gl_get_attribute(pg.GL_CONTEXT_MAJOR_VERSION),
                pg.display.gl_get_attribute(pg.GL_CONTEXT_MINOR_VERSION),
            )
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
        
    def set_mode(self, size: Tuple[int, int] = (480, 360), style: Style = styles.normal, depth: int = 0, vsync: bool = False):
        self.screen = pg.display.set_mode(size, flags=pg.OPENGL | pg.DOUBLEBUF | style.style, depth=depth, vsync=vsync)
        self.width, self.height = size
            
    def clear(self):
        self.gl.glClear(self.gl.GL_DEPTH_BUFFER_BIT | self.gl.GL_COLOR_BUFFER_BIT)

    def show(self, status: int = 0, escape_quit: bool = False, quit_disable: bool = False,
             wait_seconds: float = 0.005):
        while True:
            self.clear()
            
            for event in pg.event.get():
                if event.type == pg.QUIT and (not quit_disable):
                    self.destroy(status)
                if escape_quit and event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.destroy(status)
                self.event_handler(event)
            
            self.gl.glFlush()
            self._when_draw()
            pg.display.flip()
            self.counter += 1
            pg.time.wait(int(wait_seconds * 1000))
