import ctypes
import sys
import warnings
import webbrowser
from typing import Tuple, Callable, Any, Optional

from ..coordinate import to_pygame, CoordinateType
from ..saver import saver
from ...exceptions import OpenGameError, OpenGameWarning, not_created_window


class RichText(object):
    def __init__(self, position: Optional[CoordinateType] = None, font_name: str = 'Arial',
                 font_size: int = 13, size: Tuple[int, int] = (320, 240), file: Optional[str] = None,
                 warned: bool = True):
        if warned:
            warnings.warn(
                'the function is unstable, and it only passes the Windows 10 test',
                OpenGameWarning
            )
            
        if not saver.window:
            raise not_created_window
        self.window = saver.window
        self.window_hwnd = self.window.hwnd
        self.width, self.height = size
        
        if sys.platform != 'win32':
            raise OpenGameError('only supported Windows')
        try:
            import clr
            clr.AddReference('System.Windows.Forms')
            clr.AddReference('System.Drawing')
            clr.AddReference('System')
            
            from System.Windows.Forms import RichTextBox
            from System.Drawing import Font
            from System import String, Single

            self.user32 = ctypes.windll.user32
            self.rich_text_box = RichTextBox
            self.font_type = Font
            self.string_type, self.single_type = String, Single
        except RuntimeError as e:
            raise OpenGameError(f'OS compatibility error [{e}]') from None
        
        self.rtf = self.rich_text_box()
        self.set_font(font_name, font_size)
        self.rtf_hwnd = int(str(self.rtf.Handle))
        self.user32.SetParent(self.rtf_hwnd, self.window_hwnd)
        
        if position:
            self.x, self.y = to_pygame(position)
        else:
            self.x, self.y = 0, 0
        self.move()
        self.when_open_url(webbrowser.open)
        if file:
            self.load(file)
        
    def set_font(self, font_name: str = 'Arial', font_size: int = 13):
        self.font = self.font_type(self.string_type(font_name), self.single_type(font_size))
        self.rtf.font = self.font
        
    def move(self):
        self.user32.MoveWindow(self.rtf_hwnd, self.x, self.y, self.width, self.height, True)
        
    def load(self, rtf_file: str):
        self.rtf.LoadFile(rtf_file)
        
    def open_url(self, _, e):
        self._when_open_url(e.LinkText)

    def when_open_url(self, func: Callable[[str], Any]):
        self._when_open_url = func
        
    def resize(self, size: Tuple[int, int]):
        self.rtf.Width, self.rtf.Height = size
        self.width, self.height = size
