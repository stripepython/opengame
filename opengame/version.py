from collections import namedtuple

__all__ = ['version', 'get_string']

_Version = namedtuple('Version', ['major', 'minor', 'micro'])
version = _Version(1, 0, 2)

def get_string():
    return '.'.join(map(str, version))
