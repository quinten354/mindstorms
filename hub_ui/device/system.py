import os
from time import sleep as wait

import device
import device.port
from device import set_led
from .constants import *

def show_error():
    set_led(rgb_colors.RED)
    wait(0.2)
    set_led(rgb_colors.WHITE)

def print_error(error, message = None):
    if message:
        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': str(message)})
    else:
        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': None})

def sync_programs():
    listdir = os.listdir('/programs')
    programs = []
    for item in listdir:
        programs.append({'name': item.split('.py')[0], 'nickname': item.split('.py')[0]})

    file = open('/.program_info')
    try:
        data = eval(file.read())
    except:
        data = []

    file.close()

    for item in data:
        exist = False
        for program in programs:
            if item['name'] == program['name']:
                exist = True

        if not exist:
            data.remove(item)

    for program in programs:
        exist = False
        for item in data:
            if item['name'] == program['name']:
                exist = True

        if not exist:
            data.append(program)

    file = open('/.program_info', mode = 'w')
    file.write(str(data))
    file.close()

def reset():
    set_led(rgb_colors.WHITE)
    for port in 'A', 'B', 'C', 'D', 'E', 'F':
        dev_type = device.port.get_type(port)
        if dev_type == 47 or dev_type == 75:
            device.port.motor.float(port)
        if dev_type == 64:
            device.port.devices.light_matrix.clear(port)

