import sys

from .errors import EndOfProgramError

import device
from device import runtime_data
from device.system import print_error, show_error

class User_program():
    def __init__(self, path):
        self.path = path

        try:
            file = open(self.path)
        except Exception as error:
            show_error()
            print_error(error, message = 'Cannot open file \'' + self.path + '\'.')
            self.main = None
            return

        data = file.read()
        file.close()
        del file

        def exit():
            raise EndOfProgramError

        self.ns = {'__name__': '__main__', '__file__': self.path, 'exit': exit, 'print': device.io.print, 'input': device.io.input, 'getch': device.io.getch, 'getall': device.io.getall}

        try:
            exec(data, self.ns)
        except Exception as error:
            show_error()
            print_error(error)
            self.main = None
            runtime_data['run'] = None
            runtime_data['ui'] = True
            runtime_data['stop'] = False
            device.system.reset()
            return

        del data

        if 'main' in list(self.ns.keys()):
            self.main_func = self.ns['main']
        else:
            show_error()
            print({'type': 'error', 'name': 'CustomedError', 'message': 'No \'main()\' function found in file \'' + self.path + '\'.'})
            self.main = None
            runtime_data['run'] = None
            runtime_data['ui'] = True
            runtime_data['stop'] = False
            device.system.reset()
            return

        try:
            self.main = self.main_func()
        except (StopIteration, SystemExit, EndOfProgramError):
            runtime_data['run'] = None
            runtime_data['ui'] = True
            runtime_data['stop'] = False
            self.main = None
            device.system.reset()
        except Exception as error:
            self.main = None
            print_error(error)
            show_error()
            runtime_data['run'] = None
            runtime_data['ui'] = True
            runtime_data['stop'] = False
            device.system.reset()

    def restart(self):
        try:
            self.main = self.main_func()
        except Exception as error:
            self.main = None
            print_error(error)

    def run(self):
        if str(type(self.main)) == "<class 'generator'>":
            try:
                next(self.main)
            except (StopIteration, SystemExit):
                self.main = None
                raise EndOfProgramError
            except Exception as error:
                show_error()
                print_error(error)
                runtime_data['run'] = None
                runtime_data['ui'] = True
                runtime_data['stop'] = False
                self.main = None
                device.system.reset()
        else:
            runtime_data['run'] = None
            runtime_data['ui'] = True
            runtime_data['stop'] = False
            self.main = None
            device.system.reset()

