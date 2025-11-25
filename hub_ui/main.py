# import modules
import hub
import os

import hub_ui
import uasyncio as asyncio

restart = lambda: hub.power_off(restart = True)

# get listdir on hub
listdir = os.listdir('/')

# check directorys /etc, /tmp, /var and /programs
if 'var' not in listdir:
    os.mkdir('/var')

if 'etc' not in listdir:
    os.mkdir('/etc')

if 'tmp' not in listdir:
    os.mkdir('/tmp')

if 'programs' not in listdir:
    os.mkdir('/programs')

# check file .program_info
if '.program_info' not in listdir:
    open('/.program_info', mode = 'x').close()

del listdir

# clear /tmp
for item in os.listdir('/tmp'):
    os.remove('/tmp/' + item)

# set settings in /etc/config
file = open('/etc/config')
data = file.read()
data = data.split('\\n')
file.close()
del file

try:
    power_off_timeout = data['power_off_timeout']
except:
    power_off_timeout = 300000

# set timeout
hub.power_off(timeout = power_off_timeout)

del data

events = {'stop': False, 'run': None, 'program_runner': False, 'sensor_data': False}

# button press
def center_button_change(time):
    hub.power_off(timeout = power_off_timeout)
    if time > 600:
        events['stop_ui'] = True
        hub.button.center.was_pressed()

def button_change(time):
    hub.power_off(timeout = power_off_timeout)

def bluetooth_button_change(time):
    hub.power_off(timeout = power_off_timeout)

hub.button.center.on_change(center_button_change)
hub.button.left.on_change(button_change)
hub.button.right.on_change(button_change)
hub.button.connect.on_change(bluetooth_button_change)

async def setup_ui(events):
    await hub_ui.main(events)

async def setup_io(events):
    await hub_ui.io(events)

async def setup_program_runner(events):
    await hub_ui.program_runner(events)

async def setup_sensor_data(events):
    await hub_ui.sensor_data(events)

async def main():
    asyncio.create_task(setup_ui(events))
    asyncio.create_task(setup_io(events))
    while True:
        await asyncio.sleep(16)

hub_ui.sync_programs()

asyncio.run(main())

