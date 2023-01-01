import ctypes
import sys
import threading
import warnings
from typing import Tuple, Callable, Any, Optional

from ..coordinate import to_pygame, CoordinateType
from ..saver import saver
from ...exceptions import OpenGameError, OpenGameWarning, not_created_window


class _form(object):
    ...


class WebView(object):
    def __init__(self, size: Tuple[int, int] = (450, 250), position: Optional[CoordinateType] = None,
                 url: str = '', script_errors_suppressed: bool = True, menu_enabled: bool = True,
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
            clr.AddReference('System.Threading')

            from System.Windows.Forms import Application, WebBrowser
            
            self.user32 = ctypes.windll.user32
            self.app = Application
            self.web_browser = WebBrowser
        except RuntimeError as e:
            raise OpenGameError(f'OS compatibility error [{e}]') from None
        
        form = _form()
        threading.Thread(target=self._get_web, args=(form, self.width, self.height)).start()

        while True:
            try:
                self.ie = getattr(form, 'web')
                break
            except AttributeError:
                continue
                
        self.ie.ScriptErrorsSuppressed = script_errors_suppressed
        self.ie_hwnd = int(str(self.ie.Handle))
        if position:
            self.x, self.y = to_pygame(position)
        else:
            self.x, self.y = 0, 0
        self.user32.SetParent(self.ie_hwnd, self.window_hwnd)
        self.move()
        
        if url != '':
            self.ie.Navigate(url)

        self.ie.IsWebBrowserContextMenuEnabled = menu_enabled
        self.ie.NewWindow += self._before_window
        
        self.url = url

    def _get_web(self, form: _form, width: int, height: int):
        web = self.web_browser()
        form.web = web
        web.Width = width
        web.Height = height

    def move(self):
        self.user32.MoveWindow(self.ie_hwnd, self.x, self.y, self.width, self.height, True)

    def _before_window(self, sender, e):
        href = sender.Document.ActiveElement.GetAttribute('href')
        self.set_url(href)
        e.Cancel = True
        
    def set_url(self, url: str):
        self.url = url
        self.ie.Navigate(url)

    def show_url(self, func: Callable[[], Any]):
        self.ie.Navigating += func

    def resize(self, width: int, height: int):
        self.width, self.height = width, height
        self.ie.Width = width
        self.ie.Height = height

    def destroy(self):
        self.ie.Dispose()
