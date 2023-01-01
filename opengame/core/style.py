from pygame import constants

__all__ = ['styles', 'Style']


class Style(object):
    def __init__(self, style: int):
        self.style = style
        if isinstance(style, Style):
            self.style = style.style
        self.help_docs = ''
    
    def __str__(self):
        return f'Style(style={self.style})'
    
    def __add__(self, other):
        if isinstance(other, int):
            return Style(self.style | other)
        if isinstance(other, Style):
            return Style(self.style | other.style)
        return self
    
    __or__ = __add__
    
    def help(self):
        return self.help_docs


class styles(object):
    normal = Style(0)  # Normal mode
    fullscreen = Style(constants.FULLSCREEN)  # Window full screen display
    resizable = Style(constants.RESIZABLE)  # Window resizeable
    no_frame = Style(constants.NOFRAME)  # Window without borders or controls
    hidden = Style(constants.HIDDEN)  # Window opens in hidden mode
    shown = Style(constants.SHOWN)  # Window opens in shown mode
    scaled = Style(constants.SCALED)  # Window resolution depends on desktop size and zoom shape
    
    # Define help documents
    normal.help_docs = 'The normal mode'
    fullscreen.help_docs = 'Window full screen display'
    resizable.help_docs = 'Window resizeable'
    no_frame.help_docs = 'Window without borders or controls'
    hidden.help_docs = 'Window opens in hidden mode'
    shown.help_docs = 'Window opens in shown mode'
    scaled.help_docs = 'Window resolution depends on desktop size and zoom shape'
