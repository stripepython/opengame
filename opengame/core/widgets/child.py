import ctypes
import sys
import warnings
from typing import Tuple

from ..saver import saver
from ...exceptions import OpenGameError, not_created_window, OpenGameWarning


class Child(object):
    def __init__(self, hwnd: int, size: Tuple[int, int] = (320, 240), warned: bool = True):
        if warned:
            warnings.warn(
                'the function is unstable, and it only passes the Windows 10 test',
                OpenGameWarning
            )
        if sys.platform != 'win32':
            raise OpenGameError('only supported Windows')
        self.user32 = ctypes.windll.user32
        if not saver.window:
            raise not_created_window
        self.window = saver.window
        self.window_hwnd = self.window.hwnd
        self.x, self.y = 0, 0
        self.width, self.height = size
        self.hwnd = hwnd
        
    def init(self):
        self.user32.MoveWindow(self.hwnd, self.x, self.y, self.width, self.height, None)
        
    def pack(self):
        self.user32.SetParent(self.hwnd, self.window_hwnd)
        self.init()
