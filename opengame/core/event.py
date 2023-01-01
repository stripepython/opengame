from typing import Optional, Union

from pygame.event import Event as pgevent
from pygame.locals import *
from pygame import constants

__all__ = ['Event', 'keys']


class _EmptyEvent(object):
    type = None
    button = None
    key = None
    unicode = None
    gain = None
    state = None
    w = None
    h = None
    size = None


class Event(object):
    def __init__(self, event: Optional[pgevent] = None):
        if event is None:
            event = _EmptyEvent()
        self._event = event
    
    def __getitem__(self, item):
        return getattr(self._event, item)
    
    def get_event(self):
        return self._event
    
    @property
    def mouse_down(self):
        return self._event.type == MOUSEBUTTONDOWN
    
    @property
    def mouse_up(self):
        return self._event.type == MOUSEBUTTONUP
    
    @property
    def key_down(self):
        return self._event.type == KEYDOWN
    
    @property
    def key_up(self):
        return self._event.type == KEYUP
    
    @property
    def mouse_moving(self):
        return self._event.type == MOUSEMOTION
    
    @property
    def press_left_button(self):
        if self.mouse_down:
            return self._event.button == 1
        return False
    
    @property
    def press_middle_button(self):
        if self.mouse_down:
            return self._event.button == 2
        return False
    
    @property
    def press_right_button(self):
        if self.mouse_down:
            return self._event.button == 3
        return False
    
    @property
    def active(self):
        return self._event.type == ACTIVEEVENT
    
    @property
    def gain(self):
        if self.active:
            try:
                return bool(self._event.gain)
            except AttributeError:
                return None
        return None
    
    @property
    def state(self):
        if self.active:
            try:
                return bool(self._event.state)
            except AttributeError:
                return None
        return None
    
    @property
    def resizing(self):
        return self._event.type == VIDEORESIZE
    
    @property
    def window_size(self):
        if self.resizing:
            return self._event.size
        return None
    
    @property
    def window_width(self):
        if self.resizing:
            return self._event.w
        return None
    
    @property
    def window_height(self):
        if self.resizing:
            return self._event.h
        return None
    
    def is_down(self, key: Union[int, str]):
        if self.key_down:
            if isinstance(key, int):
                return self._event.key == key
            if isinstance(key, str):
                return keys.get(key) == self._event.key
            return False
        return False
    
    def is_up(self, key: Union[int, str]):
        if self.key_up:
            if isinstance(key, int):
                return self._event.key == key
            if isinstance(key, str):
                return keys.get(key) == self._event.key
            return False
        return False
    
    @property
    def char(self):
        if not (self.key_up or self.key_down):
            return None
        return self._event.unicode


def _get_keys():
    dct = constants.__dict__.copy()
    res = {}
    for key, value in dct.items():
        if key.startswith('K_'):
            key = key.replace('K_', '').lower()
            res[key] = value
    return res


keys = _get_keys()
del constants, _get_keys  #
