# import modules
from rshell.pyboard import Pyboard
from serial.tools.list_ports import comports
from time import sleep as wait
import serial as _serial
import os as _os
import inspect as _inspect
import time as _time
import multiprocessing as _multiprocessing

# find device of the hub
def find_device():
    for port in comports():
        if port.vid == 00 and port.pid == 00:
            return port.device
    else:
        raise RuntimeError('Device not found.')

def install(device = None):
    if not device:
        device = find_device()
    hub = Hub_connect_pyboard(device)
    hub.exec('hub.power_off(timeout = 0)')
    hub.exec('hub.led((0, 255, 50))')
    hub.exec('hub.display.pixel(0, 0, 0)')
    hub.exec('hub.display.pixel(1, 0, 0)')
    hub.exec('hub.display.pixel(2, 0, 100)')
    hub.exec('hub.display.pixel(3, 0, 0)')
    hub.exec('hub.display.pixel(4, 0, 0)')
    hub.exec('hub.display.pixel(0, 1, 0)')
    hub.exec('hub.display.pixel(1, 1, 0)')
    hub.exec('hub.display.pixel(2, 1, 100)')
    hub.exec('hub.display.pixel(3, 1, 0)')
    hub.exec('hub.display.pixel(4, 1, 0)')
    hub.exec('hub.display.pixel(0, 2, 100)')
    hub.exec('hub.display.pixel(1, 2, 0)')
    hub.exec('hub.display.pixel(2, 2, 100)')
    hub.exec('hub.display.pixel(3, 2, 0)')
    hub.exec('hub.display.pixel(4, 2, 100)')
    hub.exec('hub.display.pixel(0, 3, 0)')
    hub.exec('hub.display.pixel(1, 3, 100)')
    hub.exec('hub.display.pixel(2, 3, 100)')
    hub.exec('hub.display.pixel(3, 3, 100)')
    hub.exec('hub.display.pixel(4, 3, 0)')
    hub.exec('hub.display.pixel(0, 4, 0)')
    hub.exec('hub.display.pixel(1, 4, 0)')
    hub.exec('hub.display.pixel(2, 4, 100)')
    hub.exec('hub.display.pixel(3, 4, 0)')
    hub.exec('hub.display.pixel(4, 4, 0)')
    hub.install(restart = False)
    hub.restart()
    hub.close()

# connect with the hub using pyboard
class Hub_connect_pyboard:
    '''
    Connect with the hub using rshell.pyboard.Pyboard(device).
    This interrupt the event-loop on the hub, programs running on the hub will be killed.

    Connect with hub
    hub = Hub_connect_pyboard(device)

    Close connection
    hub.close()

    Execute micropython string on hub
    hub.exec(string)

    Upload file to hub
    hub.upload_file(file_on_computer, file_on_hub)

    Download file to computer
    hub.download_file(file_on_hub, file_on_computer)

    Restart, power off or set power off timeout
    hub.restart(fast = False)
    hub.power_off(fast = False)
    hub.set_power_off_timeout(miliseconds)

    Install
    hub.install(restart = True)
        If restart is True, the hub will restart and connect again.
    '''

    # setup connection
    def __init__(self, device = None):
        # find device
        if not device:
            device = find_device()

        self.device = device

        # connect
        self._pb = Pyboard(device)
        try:
            self._pb.enter_raw_repl()
        except:
            self.close()

        # import some modules
        self.exec('import hub')
        self.exec('import os')
        self.exec('import sys')

    # close connection
    def close(self):
        self._pb.close()

    # execute string on micropython shell on hub, get output in raw bytes
    def _exec(self, string):
        return self._pb.exec(string)

    # execute string on micropython shell on hub, get output in text
    def exec(self, string):
        return self._exec(string).decode()

    # upload a file to the hub
    def upload_file(self, path_computer, path_hub):
        # read file
        file = open(path_computer, mode = 'r')
        data = file.read()
        file.close()

        # write file to hub
        self.exec('file = open(\'' + str(path_hub) + '\', mode = \'w\')')
        self.exec('file.write(\'\'\'' + data + '\'\'\')')
        self.exec('file.close()')
        self.exec('del file')

    # download a file from the hub
    def download_file(self, path_hub, path_computer):
        # read file from hub
        data = self.exec('file = open(\'' + path_hub + '\', mode = \'r\'); print(file.read()); file.close(); del file')

        # write file
        file = open(path_computer, mode = 'w')
        file.write(data)
        file.close()

    # power off
    def power_off(self, fast = False):
        self.exec('hub.power_off(fast = ' + str(fast) + ', restart = False)')

    # restart the hub
    def restart(self, fast = False):
        self.exec('hub.power_off(fast = ' + str(fast) + ', restart = True)')

    # set power off timeout
    def set_power_off_timeout(self, timeout):
        self.exec('hub.power_off(timeout = ' + str(timeout) + ')')

    # install
    def install(self, restart = True):
        # get program directory
        program_dir = _os.path.dirname(_os.path.abspath(_inspect.getfile(_inspect.currentframe())))
        install_dir = program_dir + '/hub_ui'
        # upload main.py
        self.upload_file(install_dir + '/main.py', '/main.py')
        # get listdir on hub /
        listdir_hub = eval(self.exec('import os; print(os.listdir(\'/\'))'))
        # create hub_ui directory on hub
        if 'hub_ui' not in listdir_hub:
            self.exec('os.mkdir(\'/hub_ui\')')
        # remove all existing files in hub_ui
        for file in eval(self.exec('print(os.listdir(\'/hub_ui\'))')):
            self.exec('os.remove(\'/hub_ui/' + file + '\')')
        # upload all files in hub_ui
        for file in _os.listdir(install_dir + '/hub_ui'):
            self.upload_file(install_dir + '/hub_ui/' + file, '/hub_ui/' + file)
        # create device directory on hub
        if 'device' not in listdir_hub:
            self.exec('os.mkdir(\'/device\')')
        # remove all existing files in device
        for file in eval(self.exec('print(os.listdir(\'/device\'))')):
            self.exec('os.remove(\'/device/' + file + '\')')
        # upload all files in device
        for file in _os.listdir(install_dir + '/device'):
            self.upload_file(install_dir + '/device/' + file, '/device/' + file)
        # show installed text
        print()
        print('The ui is installed on the hub!')
        if restart:
            print('Rebooting the hub...')
            # reboot hub
            self.restart(fast = True)
            self.close()
            # give time to restart hub
            _time.sleep(5)
            # connect with hub
            print('Connecting with the hub...')
            self = self.__init__(self.device)
            print('Connected with the hub.')

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
        self._serial = _serial.Serial(device)
        self._serial.write(b'\n')

        # set function to get data on requests from the hub
        def get_data_from_hub():
            # read lines of serial connection
            while True:
                try:
                    for line in self._serial:
                        data = line.strip().decode()
                        # create dict from data
                        try:
                            data = eval(data)
                        except:
                            print('ERROR: Invalid type of received data: ' + str(data))
                            continue

                        # check received data is a dict
                        if type(data) != dict:
                            print('ERROR: Not a dict: ' + str(data))
                            continue

                        #print('Received data: ' + str(data))
    
                        keys = []
                        items = list(data.items())
                        for item in items:
                            keys.append(item[0])

                        if 'type' in keys:
                            if data['type'] == 'error':
                                if 'name' in keys:
                                    if data['name'] == 'InputError':
                                        if 'message' in keys:
                                            print('Received error: ' + str(data['message']))
                                    elif data['name'] == 'ExecuteError':
                                        if 'errname' in keys and 'errmessage' in keys and 'message' in keys:
                                            print('Received ExecuteError: errname: ' + str(data['errname']) + ', errmessage: ' + str(data['errmessage']) + ': ' + str(data['message']))
                                    else:
                                        print('ERROR: Unknown received type of error: ' + data['name'] + '.')

                                else:
                                    print('ERROR: Received data misses keyword \'name\'.')

                            elif data['type'] == 'req_file':
                                if 'name' in keys and 'content' in keys:
                                    try:
                                        path = self._data[str(data['name'])]
                                    except:
                                        print('ERROR: Unexpected file: ' + data['name'] + '.')
                                        continue
                                    try:
                                        file = open(path, mode = 'w')
                                        file.write(data['content'])
                                        file.close()
                                    except Exception as error:
                                        print('ERROR: ' + str(type(error)) + ': ' + str(error) + ': Cannot write to file: ' + path + '.')
                                    try:
                                        del self._data[str(data['name'])]
                                    except:
                                        pass

                                else:
                                    print('ERROR: Received data misses keywords \'name\' and \'content\'.')

                            elif data['type'] == 'req_execute':
                                if 'command' in keys and 'output' in keys:
                                    print('OUTPUT: Output execute: Command: ' + str(data['command']) + ', Output: ' + str(data['output']))

                                else:
                                    print('ERROR: Received data misses keywords \'command\' and \'output\'.')

                            elif data['type'] == 'req_programs':
                                if 'programs' in keys:
                                    print('OUTPUT: Availeble programs: ' + str(data['programs'])[1:][:-1])

                                else:
                                    print('ERROR: Received data misses keyword \'programs\'.')
                            
                            elif data['type'] == 'sensor_data':
                                if 'data' in keys:
                                    self._io['sensor_data'] = str(data['data'])

                                else:
                                    print('ERROR: Received data misses keyword \'data\'.')

                            elif data['type'] == 'output':
                                if 'value' in keys:
                                    self._io['output'] = self._io['output'] + str(data['value'])

                                else:
                                    print('ERROR: Received data misses keyword \'value\'.')
                    
                            elif data['type'] == 'ls':
                                if 'dirs' in keys and 'files' in keys:
                                    if len(str(data['dirs'])) > 2 and len(str(data['files'])) > 2:
                                        print('OUTPUT: Ls: Dirs: ' + str(data['dirs'])[1:][:-1] + ', Files: ' + str(data['files'])[1:][:-1])
                                    elif len(str(data['dirs'])) > 2:
                                        print('OUTPUT: Ls: Dirs: ' + str(data['dirs'])[1:][:-1])
                                    elif len(str(data['files'])) > 2:
                                        print('OUTPUT: Ls: Files: ' + str(data['files'])[1:][:-1])
                                    else:
                                        print('OUTPUT: Ls: Directory empty.')

                                else:
                                    print('ERROR: Received data misses keywords \'dirs\' and \'files\'.')

                            elif data['type'] == 'isdir':
                                if 'value' in keys:
                                    if data['value']:
                                        print('OUTPUT: Isdir: Directory.')
                                    else:
                                        print('OUTPUT: Isdir: File.')

                            elif data['type'] == 'stat':
                                if 'value' in keys:
                                    print('OUTPUT: Stat: Type: ' + str(data['value'][0]) + ', Size: ' + str(data['value'][6]))

                            elif data['type'] == 'fsstat':
                                if 'value' in keys:
                                    print('OUTPUT: Fsstat: Total blocks: ' + str(data['value'][2]) + ', Used blocks: ' + str(data['value'][2] - data['value'][3]) + ', Free blocks: ' + str(data['value'][3]) + ', Usage: ' + str(round(((data['value'][2] - data['value'][3]) / data['value'][3]) * 100, 2)) + '%.')

                            elif data['type'] == 'events':
                                if 'value' in keys:
                                    print('OUTPUT: Events: ' + str(data['value']))

                            else:
                                print('ERROR: Unknown received type of data: ' + data['type'] + '.')

                except KeyboardInterrupt:
                    continue

                except _serial.serialutil.SerialException:
                    print('Connection closed.')
                    self._manager._process.kill()
                    self._serial.close()
                    exit()

                except Exception as error:
                    print('Error: ' + str(type(error)) + ': ' + str(error))
                    continue

        # setup manager
        self._manager = _multiprocessing.Manager()
        self._data = self._manager.dict()
        self._io = self._manager.dict()

        # set waitings dict, here come all requests to the hub while we wait for answer
        self._io['output'] = ''
        self._io['sensor_data'] = ''

        # start function as a new process
        self._get_data_from_hub = _multiprocessing.Process(target = get_data_from_hub, daemon = True)
        self._get_data_from_hub.start()

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

    def upload_program(self, path_computer, name = None, nickname = None, animation = None):
        # get name
        if not name:
            if _os.name == 'nt':
                name = path_computer.split('\\')[-1].split('.py')[0]
            else:
                name = path_computer.split('/')[-1].split('.py')[0]

        # delete invalid characters
        for char in ['/', '\\', '\'', '`', '"', '~', '.', ',', ' ', '-', '=', '+']:
            name.replace(char, '')

        # delete first character if it is a number
        if name[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            name = name[1:]

        if name in ['main', '__main__', '_onewire', '_uasyncio', 'buildins', 'cmath', 'firmware', 'gc', 'hub', 'math', 'micropython', 'uarray', 'array', 'uasyncio', 'asyncio', 'ubinascii', 'ubluetooth', 'bluetooth', 'ucollections', 'collections', 'uctypes', 'ctypes', 'uerrno', 'errno', 'uhashlib', 'hashlib', 'uheapq', 'heapq', 'uio', 'io', 'ujson', 'json', 'umachine', 'machine', 'uos', 'os', 'urandom', 'random', 'ure', 're', 'uselect', 'select', 'ustruct', 'struct', 'usys', 'sys', 'utime', 'time', 'utimeq', 'timeq', 'uzlib', 'zlib']:
            print('Warning: invalid name; change name to \'' + name + '_' + '\'.')
            name = name + '_'

        if not nickname:
            nickname = name

        if animation:
            self.send({'type': 'upload_program', 'name': name, 'nickname': nickname, 'animation': animation})
        else:
            self.send({'type': 'upload_program', 'name': name, 'nickname': nickname})

        self.upload_file(path_computer, '/programs/' + name + '.py')

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

    def get_programs(self):
        self.send({'type': 'get_programs'})

    def delete_program(self, name):
        self.send({'type': 'delete_program', 'name': name})

    def sync_programs(self):
        self.send({'type': 'sync_programs'})

    def stop_all(self):
        self.send({'type': 'stop_all'})

    def stop_ui(self):
        self.send({'type': 'stop_ui'})

    def stop_program_runner(self):
        self.send({'type': 'stop_program_runner'})

    def start_send_sensor_data(self):
        self.send({'type': 'start_send_sensor_data'})

    def stop_send_sensor_data(self):
        self.send({'type': 'stop_send_sensor_data'})

    def send(self, dict_):
        data = cut_string(str(dict_) + '\n')
        for string in data:
            string = str(string).encode()
            self._serial.write(string)
            self._serial.flush()
            wait(0.6)

    def exec(self, command):
        self.send({'type': 'execute', 'command': str(command)})

    def send_program_input(self, value):
        self.send({'type': 'program_input', 'value': str(value)})

    def power_off(self, fast = False):
        self.send({'type': 'power_off', 'fast': fast})
        self.close()

    def set_power_off_timeout_tmp(self, timeout):
        '''
        Set power off timeout in seconds. This will be resetted after a restart.
        '''

        self.send({'type': 'power_off_timeout_tmp', 'timeout': timeout})

    def set_power_off_timeout(self, timeout):
        '''
        Set power off timeout in seconds.
        '''

        self.send({'type': 'power_off_timeout', 'timeout': timeout})

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

    def get_sensor_data(self):
        return self._io['sensor_data']

    def stat(self, path):
        self.send({'type': 'stat', 'path': path})

    def fsstat(self):
        self.send({'type': 'fsstat'})

    def isdir(self, path):
        self.send({'type': 'isdir', 'path': path})

    def get_events(self):
        self.send({'type': 'get_events'})

    # close connection
    def close(self):
        self._get_data_from_hub.kill()
        self._manager._process.kill()
        self._serial.close()

def cut_string(string, size = 512):
    data = []
    count = size
    for char in string:
        if count >= size:
            count = 0
            data.append(char)
        else:
            data[-1] = data[-1] + char
        count = count + 1

    return data

