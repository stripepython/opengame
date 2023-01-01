from typing import Optional, Tuple

import cv2

from ..core.saver import saver
from ..exceptions import not_created_window

__all__ = ['encodings', 'Screencap']


class encodings(object):
    I420 = 'I420'
    XVID = 'XVID'
    PIM1 = 'PIM1'
    THEO = 'THEO'
    FLV1 = 'FLV1'
    AVC1 = 'ACV1'
    DIV3 = 'DIV3'
    DIVX = 'DIVX'
    MP42 = 'MP42'
    MJPG = 'MJPG'
    U263 = 'U263'
    I263 = 'I263'
    

class Screencap(object):
    def __init__(self):
        if not saver.window:
            raise not_created_window
        self.window = saver.window
        self.images = []
        
    def record(self, temp_file: str = 'temp.png'):
        self.window.screenshot(temp_file)
        array = cv2.imread(temp_file)
        self.images.append(array)
        
    def save(self, video_path: str = 'screencap.avi', encoding: str = encodings.I420,
             fps: Optional[float] = None, size: Optional[Tuple[int, int]] = None):
        if not fps:
            fps = self.window.fps
        if not size:
            size = self.window.size
        fourcc = cv2.VideoWriter_fourcc(*encoding)
        writer = cv2.VideoWriter(video_path, fourcc, fps, size)
        
        for img in self.images:
            if img is not None:
                frame = cv2.resize(img, size)
                writer.write(frame)
                
        writer.release()
        cv2.destroyAllWindows()
        
    @property
    def arrays(self):
        yield from self.images
