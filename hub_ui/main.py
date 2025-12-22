# import modules
import hub
import os
import builtins
import uasyncio as asyncio
from time import time

import hub_ui

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
try:
    data = eval(data)
except:
    data = {}
file.close()
del file

try:
    power_off_timeout = data['power_off_timeout']
except:
    power_off_timeout = 300000

# set timeout
hub.power_off(timeout = power_off_timeout)
hub.config['powerdown_timeout'] = power_off_timeout

del data

events = {'stop': False, 'run': None, 'program_runner': False, 'sensor_data': False, 'program_input': [], 'power_off_timeout': power_off_timeout, 'remote': None, 'remote_connect': None, 'remote_value': [0, 0, 0, 0, 0, 0], 'refresh_ui': False, 'last_activity': time()}

async def setup_ui(events):
    await hub_ui.main(events)

async def setup_io(events):
    await hub_ui.io(events)

async def setup_program_runner(events):
    await hub_ui.program_runner(events)

async def setup_sensor_data(events):
    await hub_ui.sensor_data(events)

async def setup_controller(events):
    while True:
        if events['remote_connect'] == 'connect':
            remote = hub_ui.Remote()
            connect = remote.connect()
            events['remote'] = remote
            while True:
                try:
                    connect.__next__()
                except builtins.StopIteration:
                    break
                if events['remote_connect'] == 'disconnect':
                    events['remote'].cancel()
                    events['remote'] = None
                    events['remote_connect'] = None
                    break
                await asyncio.sleep(0)

        if events['remote_connect'] == 'disconnect':
            events['remote'].cancel()
            events['remote'] = None
            events['remote_connect'] = None 

        await asyncio.sleep(1)

async def main():
    asyncio.create_task(setup_ui(events))
    asyncio.create_task(setup_io(events))
    asyncio.create_task(setup_program_runner(events))
    asyncio.create_task(setup_sensor_data(events))
    asyncio.create_task(setup_controller(events))
    while True:
        await asyncio.sleep(16)

file = open('/etc/hostname')
hub.config['hostname'] = file.read()
file.close()

hub.config['device_get_can_return_float'] = True

asyncio.run(main())

