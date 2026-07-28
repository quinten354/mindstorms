import serial
import os
import multiprocessing
from time import sleep as wait

from .data_reader import get_data_from_hub
from .io import main as io
from .sensor_data import main as sensor_data_start, update as sensor_data_update
from .cmd import main as cmd
from .functions import find_device

# connect with the hub's event-loop
class Hub_connect_event_loop:
    '''
    Connect with the hub using serial.Serial(device).
    This can only if you have installed the software on the hub via Hub_connect_pyboard.install.

    Connect to the hub
    hub = Hub_connect_event_loop(device)

    Close connection
    hub.close()
    '''
    
    # setup connection
    def __init__(self, device = None):
        # find device
        if not device:
            device = find_device()

        self.device = device

        # connect with hub
        self._serial = serial.Serial(device)
        self._serial.write(b'\n')

        # setup manager
        self._manager = multiprocessing.Manager()
        self._data = self._manager.dict()
        self._to_kill = self._manager.list()
        self._io = self._manager.dict()
        self._cmd_output = self._manager.list()
        self._cmd_errors = self._manager.list()
        self._cmd_event = self._manager.Event()
        self._sdwidgets = {}
        self._sdevent = self._manager.Event()
        self._sdpid = None
        self._sdsend = False

        # set waitings dict, here come all requests to the hub while we wait for answer
        self._io['output'] = ''
        self._io['sensor_data'] = ''

        # start function as a new process
        get_data_from_hub(self)

    # upload a file to the hub
    def upload_file(self, path_computer, path_hub):
        # read file on computer
        file = open(path_computer, mode = 'r')
        data = file.read()
        file.close()

        # send content of file to hub
        self.send({'type': 'upload_file', 'path': str(path_hub), 'content': data})

    # download a file from the hub
    def download_file(self, path_hub, path_computer):
        # add computer path to waitings, so if the program receive the file, it knows where it must download it
        self._data[path_hub] = path_computer
        # send request to download the file
        self.send({'type': 'download_file', 'path': str(path_hub)})

    def upload_program(self, path_computer, name = None):
        # get name
        if not name:
            if os.name == 'nt':
                name = path_computer.split('\\')[-1].split('.py')[0]
            else:
                name = path_computer.split('/')[-1].split('.py')[0]

        # delete invalid characters
        for char in ['/', '\\']:
            name.replace(char, '')

        # delete first character if it is a number
        if name[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            name = name[1:]

        if name in ['.', '..']:
            print('Warning: invalid name; change name to \'' + name + '_' + '\'.')
            name = name + '_'

        if not name:
            if os.name == 'nt':
                name = path_computer.split('\\')[-1].split('.py')[0]
            else:
                name = path_computer.split('/')[-1].split('.py')[0]

        self.upload_file(path_computer, '/programs/' + name)
        self.reset_ui()

        return name

    def run_tmp(self, path_computer):
        name = path_computer.split('.py')
        file = open(path_computer)
        data = file.read()
        file.close()
        self.send({'type': 'run_tmp', 'name': name, 'data': data})

    def upload_and_run(self, path_computer, name = None, nickname = None, animation = None):
        name = self.upload_program(path_computer, name, nickname, animation)
        self.run(name)

    def run(self, name):
        self.send({'type': 'run', 'name': name})

    def run_file(self, path):
        self.send({'type': 'run_file', 'path': path})

    def get_programs(self):
        self.send({'type': 'get_programs'})

    def delete_program(self, name):
        self.send({'type': 'delete_program', 'name': name})

    def stop(self):
        self.send({'type': 'stop'})

    def start_send_sensor_data(self):
        self.send({'type': 'start_send_sensor_data'})
        self._sdsend = True
        sensor_data_update(self)

    def stop_send_sensor_data(self):
        self.send({'type': 'stop_send_sensor_data'})
        self._sdsend = False
        sensor_data_update(self)

    def send(self, dict_):
        for string in cut_string(str(dict_) + '\n'):
            string = str(string).encode()
            self._serial.write(string)
            self._serial.flush()
            wait(0.1)

    def exec(self, command):
        self.send({'type': 'execute', 'command': str(command)})

    def send_program_input(self, value):
        self.send({'type': 'program_input', 'value': str(value)})

    def power_off(self, fast = False):
        self.send({'type': 'power_off', 'fast': fast})
        self.close()

    def restart(self, fast = False):
        '''
        Restart the hub
        '''

        self.send({'type': 'restart', 'fast': fast})
        self.close()

    def ls(self, dir):
        self.send({'type': 'ls', 'dir': dir})

    def touch(self, path):
        self.send({'type': 'touch', 'path': path})

    def remove(self, path):
        self.send({'type': 'remove', 'path': path})

    def mkdir(self, dir):
        self.send({'type': 'mkdir', 'dir': dir})

    def rmdir(self, dir):
        self.send({'type': 'rmdir', 'dir': dir})

    def reset_ui(self):
        self.send({'type': 'reset_ui'})

    def get_output(self):
        output = self._io['output']
        self._io['output'] = ''
        return output

    def get_last_sended_sensor_data(self):
        return self._io['sensor_data']

    def stat(self, path):
        self.send({'type': 'stat', 'path': path})

    def fsstat(self):
        self.send({'type': 'fsstat'})

    def isdir(self, path):
        self.send({'type': 'isdir', 'path': path})

    def get_runtime_data(self):
        self.send({'type': 'get_runtime_data'})

    def get_sensor_data(self):
        self.send({'type': 'get_sensor_data'})

    def start_sensor_data_viewer(self):
        sensor_data_start(self)

    def startstop_send_sensor_data(self):
        if self._sdsend:
            self.stop_send_sensor_data()
        else:
            self.start_send_sensor_data()

    def start_io(self):
        io(self)

    def start_cmd(self):
        cmd(self)

    def exec_cmd(self, data):
        self.send({'type': 'cmd', 'data': data})

    def reset_cmd(self):
        self.send({'type': 'reset_cmd'})

    # close connection
    def close(self):
        for process in self._to_kill:
            try:
                os.kill(process, 9)
            except:
                pass
        self._manager.shutdown()
        self._serial.close()

def cut_string(string, size = 32):
    for i in range(0, len(string), size):
        yield string[i:i + size]

