import os
from micropython import const

_ISDIR = const(0x4000)

def isdir(path):
    mode = os.stat(path)[0]
    return bool(mode & _ISDIR)

def exists(path):
    try:
        os.stat(path)
    except:
        return False
    return True

def basename(path):
    return path.split('/')[-1]

def dirname(path):
    items = path.split('/')
    if len(items[-1]) == 0:
        del items[-1]
    del items[-1]
    return '/'.join(items)

def split(path):
    return dirname(path), basename(path)

def get_size(path):
    return os.stat(path)[6]

def getctime(path):
    return os.stat(path)[7]

def getmtime(path):
    return os.stat(path)[8]

def getatime(path):
    return os.stat(path)[9]

