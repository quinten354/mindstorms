# library for connecting to lego 88010 remote

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
    return events['remote'].pressed()

def is_pressed(events, button):
    return button in get_pressed(events)

