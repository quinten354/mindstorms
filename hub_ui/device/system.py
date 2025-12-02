import os
from time import sleep as wait

from device import set_led
from .constants import *

def show_error():
    set_led(colors.RED)
    wait(0.2)
    set_led(colors.WHITE)

def print_error(err, message = None):
    tperr = type(err)
    if tperr == None:
        pass
    else:
        print('Type: ' + str(tperr) + ', Data: ' + str(err))

    if message:
        print('Message: ' + message)

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

