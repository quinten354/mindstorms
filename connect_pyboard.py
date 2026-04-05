# import modules
import os as _os
import inspect as _inspect
import time as _time

from rshell.pyboard import Pyboard

from .functions import find_device

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

        data = data.replace('\\', '\\\\').replace('\t', '\\t').replace('\r', '\\r')

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

