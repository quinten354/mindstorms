# library for connecting to lego 88010 remote
from time import time_ns as time

def connect(events):
    events['remote_connect'] = 'connect'
    while True:
        if events['remote']:
            return events['remote']

def disconnect(events):
    events['remote_connect'] = 'disconnect'

def get_remote(events):
    return events['remote']

def get_pressed(events):
    try:
        return events['remote'].pressed()
    except AttributeError:
        return

def is_pressed(events, button):
    if type(button) != str:
        raise TypeError('button must be str')
    pressed = get_pressed(events)
    if type(pressed) == tuple:
        return button in pressed

def get_value(events):
    pressed = get_pressed(events)
    if 'LEFT_PLUS' in pressed and events['remote_value'][2] == 0:
        events['remote_value'][0] = events['remote_value'][0] + 1
        events['remote_value'][2] = time()
    elif 'LEFT_PLUS' in pressed and (time() - 750000000) > events['remote_value'][2] and events['remote_value'][2] > 0:
        events['remote_value'][0] = events['remote_value'][0] + 0.1
    else:
        events['remote_value'][2] = 0

    if 'LEFT' in pressed:
        events['remote_value'][0] = 0

    if 'LEFT_MINUS' in pressed and events['remote_value'][3] == 0:
        events['remote_value'][0] = events['remote_value'][0] - 1
        events['remote_value'][3] = time()
    elif 'LEFT_MINUS' in pressed and (time() - 750000000) > events['remote_value'][3] and events['remote_value'][3] > 0:
        events['remote_value'][0] = events['remote_value'][0] + 0.1
    else:
        events['remote_value'][3] = 0

    if 'RIGHT_PLUS' in pressed and events['remote_value'][4] == 0:
        events['remote_value'][1] = events['remote_value'][1] + 1
        events['remote_value'][4] = time()
    elif 'RIGHT_PLUS' in pressed and (time() - 750000000) > events['remote_value'][4] and events['remote_value'][4] > 0:
        events['remote_value'][1] = events['remote_value'][1] + 0.1
    else:
        events['remote_value'][4] = 0

    if 'RIGHT' in pressed:
        events['remote_value'][1] = 0

    if 'RIGHT_MINUS' in pressed and events['remote_value'][5] == 0:
        events['remote_value'][1] = events['remote_value'][1] - 1
        events['remote_value'][5] = time()
    elif 'RIGHT_MINUS' in pressed and (time() - 750000000) > events['remote_value'][5] and events['remote_value'][5] > 0:
        events['remote_value'][1] = events['remote_value'][1] + 0.1
    else:
        events['remote_value'][5] = 0

    return events['remote_value'][0], events['remote_value'][1]

