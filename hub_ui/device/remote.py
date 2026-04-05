# library for connecting to lego 88010 remote
from time import time_ns as time
from hub_ui import remote as remote_lib

OFF = const(0x00)
PINK = const(0x01)
PURPLE = const(0x02)
BLUE = const(0x03)
LIGHTBLUE = const(0x04)
LIGHTGREEN = const(0x05)
GREEN = const(0x06)
YELLOW = const(0x07)
ORANGE = const(0x08)
RED = const(0x09)
WHITE = const(0x0A)

colors = [OFF, PINK, PURPLE, BLUE, LIGHTBLUE, LIGHTGREEN, GREEN, YELLOW, ORANGE, RED, WHITE]

remote = remote_lib.Remote()

def connect(cancel_func):
    connector = remote.connect()
    while True:
        try:
            next(connector)
        except:
            break
        if cancel_func():
            disconnect()
            break

def disconnect():
    remote.cancel()

def get_pressed():
    return remote.pressed()

def is_pressed(button):
    if type(button) != str:
        raise TypeError('button must be str')
    pressed = get_pressed()
    if type(pressed) == tuple:
        return button in pressed

def set_color(color):
    col = colors[color]
    remote.color(col)

def was_pressed(button):
    if button in remote.__was_pressed:
        remote.__was_pressed.remove(button)
        return True
    else:
        return False

