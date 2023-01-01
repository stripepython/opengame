from typing import Optional

import pygame as pg

__all__ = ['MusicPlayer', 'play_sound']


class MusicPlayer(object):
    def __init__(self, sound: str):
        pg.mixer.init()
        self.mixer = pg.mixer.Sound(sound)
        self.path = sound
        
    def __copy__(self):
        return MusicPlayer(self.path)
    
    copy = __copy__
    
    def play(self, loops: int = 0, max_time: int = 0, fade_ms: int = 0):
        self.mixer.play(loops, max_time, fade_ms)
        
    def fadeout(self, time: int):
        self.mixer.fadeout(time)
    
    @staticmethod
    def pause():
        pg.mixer.pause()
    
    @staticmethod
    def unpause():
        pg.mixer.unpause()
        
    @property
    def volume(self):
        return self.mixer.get_volume()
    
    @volume.setter
    def volume(self, vol: int):
        self.mixer.set_volume(vol)
        
    def stop(self):
        self.mixer.stop()
       
    @staticmethod
    def set_mode(frequency: int = 44100, size: int = -16, channels: int = 2, buffer: int = 512,
                 device_name: Optional[str] = None, allowed_changes: int = 5):
        pg.mixer.pre_init(frequency, size, channels, buffer, device_name, allowed_changes)
        pg.mixer.init(frequency, size, channels, buffer, device_name, allowed_changes)
        
        
def play_sound(sound: str, *args, **kwargs):
    MusicPlayer(sound).play(*args, **kwargs)
