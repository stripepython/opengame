import wave

from ..exceptions import OpenGameError


__all__ = ['recorder']


class _Recorder(object):
    def __init__(self, save_path: str = 'record.wav', chunk: int = 1024,
                 channels: int = 1, rate: int = 44100, format_: int = 16):
        try:
            from pyaudio import PyAudio, paInt8, paInt16, paInt24, paInt32
        except ImportError:
            raise OpenGameError('cannot import pyaudio, please install it') from None
        _FORMAT_DICT = {
            8: paInt8,
            16: paInt16,
            24: paInt24,
            32: paInt32,
        }  # Define paInt format dict
        
        self.p = PyAudio()
        format_ = _FORMAT_DICT.get(format_, paInt16)
        
        self.stream = self.p.open(
            format=format_,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )
        
        self.chunk = chunk
        self.rate = rate
        self.channels = channels
        self.format = format_
        self.set_file(save_path)
        
        self._running = True
    
    def save(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.file.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
    
    def record(self):
        data = self.stream.read(self.chunk)
        self.file.writeframes(data)
    
    def record_time(self, seconds: float):
        n = int(self.rate / self.chunk * seconds)
        for i in range(n):
            self.record()
    
    def set_file(self, save_path: str):
        self.file = wave.open(save_path, 'wb')
        self.file.setnchannels(self.channels)
        self.file.setsampwidth(self.p.get_sample_size(self.format))
        self.file.setframerate(self.rate)


def recorder(save_path: str = 'record.wav', chunk: int = 1024,
             channels: int = 1, rate: int = 44100, format_: int = 16):
    return _Recorder(save_path, chunk, channels, rate, format_)
