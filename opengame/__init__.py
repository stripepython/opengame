import sys

from . import version

from .core.window import Window
# Import .core.window will hide pygame support prompt
from .core.widgets.sprite import Sprite
from .core.widgets.background import Background
from .core.widgets.label import Label, Font
from .core.widgets.bar import Bar
from .core.widgets.camera import Camera
from .core.widgets.video import Video
from .core.widgets.entry import Entry
from .core.color import Color
from .core.style import styles

from .utils.pen import Pen
from .utils.timer import timer
from .utils.player import MusicPlayer, play_sound
from .utils.rect import RectTool
from .utils.record import recorder
from .utils.glwindow import GLWindow
from .utils import translate, screencap, cs, builtin
from .utils import maths as math

if sys.platform == 'win32':
    from .core.widgets.browser import WebView
    from .core.widgets.richtext import RichText
    from .core.widgets.child import Child
else:
    WebView = RichText = Child = None

from pygame._sdl2.video import messagebox  # pylint: C0413: Import "from pygame._sdl2.video import messagebox" should be placed at the top of the module (wrong-import-position)

del sys
random = math.random


__all__ = ['Window', 'Sprite', 'Background', 'Label', 'Font', 'Bar', 'Color',
           'random', 'Pen', 'timer', 'translate', 'styles', 'math', 'MusicPlayer',
           'play_sound', 'screencap', 'Camera', 'WebView', 'recorder', 'cs',
           'version', 'GLWindow', 'RichText', 'Video', 'builtin', 'Entry', 'RectTool',
           'Child', 'messagebox']
__version__ = version.get_string()
timer.zero()
