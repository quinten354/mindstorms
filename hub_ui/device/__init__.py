# import modules
import hub as _hub

def get_led():
    return _hub.led()

def set_led(value):
    _hub.led(value)

def get_temp():
    return _hub.temperature()

