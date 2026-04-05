# import modules
import hub
import os

import hub_ui

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

del os

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

del data

hub_ui.main()

