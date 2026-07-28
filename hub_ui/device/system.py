import hub
import os
from time import sleep as wait
import sys
import io

import device
import device.port
from device import set_led
from .constants import *

def show_error():
    set_led(rgb_colors.RED)
    wait(0.2)
    set_led(rgb_colors.WHITE)

def print_error(error, message = None, log_file = None, event_loop = True):
    buf = io.StringIO()
    sys.print_exception(error, buf)
    error_string = buf.getvalue()
    buf.close()
    if event_loop:
        if message:
            print({'type': 'error', 'name': 'ExecuteError', 'errmessage': str(error_string), 'message': str(message)})
        else:
            print({'type': 'error', 'name': 'ExecuteError', 'errmessage': str(error_string), 'message': None})
    else:
        print(error_string)

    if log_file:
        file = open(log_file, mode = 'w')
        file.write('\n\n' + str(error_string))
        file.close()

def reset():
    set_led(rgb_colors.WHITE)
    for port in 'A', 'B', 'C', 'D', 'E', 'F':
        dev_type = device.port.get_type(port)
        if dev_type == 47 or dev_type == 75:
            device.port.motor.float(port)
        if dev_type == 64:
            device.port.devices.light_matrix.clear(port)

# continue event loop
def cel():
    hub.config['cel']()

