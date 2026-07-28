# import modules
import select
import sys
import hub
import os

from hub_ui.sensor_data import send_sensor_data
from hub_ui.shell import main as user_shell

import device
import device.port
import device.battery
import device.path
import device.button
import device.motion
import device.display
import device.sound
import device.constants
import device.io
import device.remote
import device.system
from device import runtime_data
from device.system import print_error
from device.path import isdir

def main():
    # setup spoll
    spoll = select.poll()
    spoll.register(sys.stdin, select.POLLIN)
    print()
    data = ''
    cmd = {'print': device.io.print, 'input': device.io.input, 'getch': device.io.getch, 'getall': device.io.getall, 'input_avail': device.io.input_avail}
    while True:
        # when there is none input, wait
        if not spoll.poll(0):
            yield
            continue

        # when there is input, read 1 byte
        data = data + sys.stdin.read(1)
        if data[-1] == '\x01':
            user_shell()
            data = data[:-1]
            continue

        if data[-1] != '\n':
            yield
            continue

        if data == '\n':
            print()
            data = ''
            continue

        try:
            data = eval(data)
        except:
            print({'type': 'error', 'name': 'InputError', 'message': 'Invalid received data: ' + str(data)})
            data = ''
            continue

        # check data is a dict
        if type(data) != dict:
            print({'type': 'error', 'name': 'InputError', 'message': 'Input must be a dict, not a ' + str(type(data)) + '.'})
            data = ''
            continue

        # get keywords of dict
        keys = list(data.keys())

        # check type is in dict
        if 'type' in keys:
            # upload a file to the hub
            if data['type'] == 'upload_file':
                if 'path' in keys and 'content' in keys:
                    try:
                        file = open(data['path'], mode = 'w')
                        file.write(data['content'])
                        file.close()
                    except Exception as error:
                        print_error(error, 'Error by uploading a file to \'' + data['path'] + '\'.')

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for upload a file must have 'path' and 'size'."})

            # download a file to the computer
            elif data['type'] == 'download_file':
                if 'path' in keys:
                    try:
                        file = open(data['path'])
                        content = file.read()
                        file.close()
                        del file
                    except Exception as error:
                        print_error(error, 'Error by uploading a file.')
                        print_error(error, 'Error by downloading a file.')

                    print({'type': 'req_file', 'name': data['path'], 'content': str(content)})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for upload a file must have 'path'."})

            # power off the hub
            elif data['type'] == 'power_off':
                if 'fast' in keys:
                    hub.power_off(fast = data['fast'])
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for power off must have 'fast'."})

            # restart the hub
            elif data['type'] == 'restart':
                if 'fast' in keys:
                    hub.power_off(restart = True, fast = data['fast'])
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for restart must have 'fast'."})

            # execute a python command
            elif data['type'] == 'execute':
                if 'command' in keys:
                    try:
                        output = eval(data['command'])
                        print({'type': 'req_execute', 'command': data['command'], 'output': output})
                        del output
                    except Exception as error:
                        print_error(error, "Can't execute command.")
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't execute command."})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for execute a command must have 'command'."})

            elif data['type'] == 'cmd':
                if 'data' in keys:
                    try:
                        exec(data['data'], cmd)
                    except Exception as error:
                        print(type(error), error)
                        print_error(error)
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for execute a cmd must have 'data'."})

            elif data['type'] == 'reset_cmd':
                cmd = {'print': device.io.print, 'input': device.io.input, 'getch': device.io.getch, 'getall': device.io.getall, 'input_avail': device.io.input_avail}

            # run a program in /tmp
            elif data['type'] == 'run_tmp':
                if 'name' in keys and 'data' in keys:
                    file = open('/tmp/' + str(data['name']), mode = 'w')
                    file.write(str(data['data']))
                    file.close()

                    runtime_data['stop'] = False
                    runtime_data['run'] = '/tmp/' + str(data['name'])
                    runtime_data['ui'] = False

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program in tmp must have 'name' and 'data'."})

            # run a stored program
            elif data['type'] == 'run':
                if 'name' in keys:
                    runtime_data['stop'] = False
                    runtime_data['run'] = '/programs/' + str(data['name'])
                    runtime_data['ui'] = False

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program must have 'name'."})

            # run from a file
            elif data['type'] == 'run_file':
                if 'path' in keys:
                    runtime_data['stop'] = False
                    runtime_data['run'] = str(data['path'])
                    runtime_data['ui'] = False

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program must have 'path'."})

            # get all stored programs
            elif data['type'] == 'get_programs':
                listdir = os.listdir('/programs')
                print({'type': 'req_programs', 'programs': listdir})

            # delete a program
            elif data['type'] == 'delete_program':
                if 'name' in keys:
                    try:
                        os.remove('/programs/' + data['name'])
                    except Exception as error:
                        print_error(error, "Can't delete program '" + data['name'] + "'.")

                    runtime_data['refresh_ui'] = True

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for delete a program must have 'name'."})

            # stop running program
            elif data['type'] == 'stop':
                runtime_data['stop'] = True

            # start sending sensor data to computer
            elif data['type'] == 'start_send_sensor_data':
                runtime_data['sensor_data'] = True

            # stop sending sensor data to computer
            elif data['type'] == 'stop_send_sensor_data':
                runtime_data['sensor_data'] = False

            # controller command
            elif data['type'] == 'program_input':
                if 'value' in keys:
                    runtime_data['program_input'] = runtime_data['program_input'] + data['value']
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A program_input command must have 'value'."})

            # get all files and dirs in directory
            elif data['type'] == 'ls':
                if 'dir' in keys:
                    try:
                        listdir = os.listdir(data['dir'])
                    except Exception as error:
                        print_error(error,  "Can't get listdir of dir " + str(data['dir']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get listdir of dir " + str(data['dir']) + '.'})
                    
                    files = []
                    dirs = []

                    for item in listdir:
                        path = data['dir']
                        if path[-1] != '/':
                            path = path + '/'
                        path = path + item
                        
                        if isdir(path):
                            dirs.append(item)
                        else:
                            files.append(item)

                    print({'type': 'ls', 'dirs': str(dirs), 'files': str(files)})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A ls command must have 'dir'."})

            # create file
            elif data['type'] == 'touch':
                if 'path' in keys:
                    try:
                        open(data['path'], mode = 'x').close()
                    except Exception as error:
                        print_error("Can't create file " + str(data['path']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't create file " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A touch command must have 'path'."})

            # remove file
            elif data['type'] == 'remove':
                if 'path' in keys:
                    try:
                        os.remove(data['path'])
                    except Exception as error:
                        print_error(error, "Can't remove file " + str(data['path']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't remove file " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A remove command must have 'path'."})

            # create dir
            elif data['type'] == 'mkdir':
                if 'dir' in keys:
                    try:
                        os.mkdir(data['dir'])
                    except Exception as error:
                        print_error(error, "Can't create dir " + str(data['dir']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't create dir " + str(data['dir']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A mkdir command must have 'dir'."})

            # remove dir
            elif data['type'] == 'rmdir':
                if 'dir' in keys:
                    try:
                        os.rmdir(data['dir'])
                    except Exception as error:
                        print_error(error,  "Can't remove dir " + str(data['dir']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't remove dir " + str(data['dir']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A rmdir command must have 'dir'."})

            # reset ui
            elif data['type'] == 'reset_ui':
                runtime_data['refresh_ui'] = True

            # check given path is a directory
            elif data['type'] == 'isdir':
                if 'path' in keys:
                    try:
                        print({'type': 'isdir', 'value': isdir(data['path'])})
                    except Exception as error:
                        print_error(error, "Can't get isdir of path " + str(data['path']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get isdir of path " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A isdir command must have 'path'."})

            # get stat of path
            elif data['type'] == 'stat':
                if 'path' in keys:
                    try:
                        print({'type': 'stat', 'value': os.stat(data['path'])})
                    except Exception as error:
                        print_error(error,  "Can't get stat of path " + str(data['path']) + '.')
                        #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get stat of path " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A stat command must have 'path'."})

            # get file system stat
            elif data['type'] == 'fsstat':
                try:
                    print({'type': 'fsstat', 'value': os.statvfs('/')})
                except Exception as error:
                    print_error(error, "Can't get stat of filesystem.")
                    #print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get stat of filesystem."})

            # get runtime_data
            elif data['type'] == 'get_runtime_data':
                print({'type': 'runtime_data', 'value': runtime_data.copy()})

            # get sensor data
            elif data['type'] == 'get_sensor_data':
                send_sensor_data()

            else:
                print({'type': 'error', 'name': 'InputError', 'message': 'Unknown type: ' + str(data['type'])})

        else:
            print({'type': 'error', 'name': 'InputError', 'message': "'type' must be in dict."})

        data = ''

        yield

