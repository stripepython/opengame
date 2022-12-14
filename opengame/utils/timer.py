import time

import pygame as pg

__all__ = ['timer', 'Timer']


class Timer(object):
    def __init__(self):
        self._start_time = time.time()
    
    def __str__(self):
        return 'Timer()'
    
    def __int__(self):
        return int(self.time)
    
    def __float__(self):
        return self.time
    
    @property
    def time(self):
        return time.time() - self._start_time
    
    def zero(self):
        self._start_time = time.time()
    
    def get(self, digits: int = 2):
        return round(self.time, digits)
    
    @staticmethod
    def sleep(seconds: int):
        pg.time.delay(int(seconds * 1000))
    

timer = Timer()
