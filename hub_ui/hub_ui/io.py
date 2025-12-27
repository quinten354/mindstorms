# import modules
import select
import sys
import hub
import uasyncio as asyncio
import os

from device.system import sync_programs, print_error
from device.path import isdir

async def main(events):
    # setup spoll
    spoll = select.poll()
    spoll.register(sys.stdin, select.POLLIN)
    print()
    data = ''
    while True:
        # when there is none input, wait
        if not spoll.poll(0):
            await asyncio.sleep(0.5)
            continue

        # whan there is input, read 1 byte
        data = data + sys.stdin.read(1)
        # when the last character is a newline, execute command
        if data[-1] != '\\n':
            # else, wait
            await asyncio.sleep(0)
            continue

        if data == '\\n':
            print()
            data = ''
            continue

        # convert string to dict
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
                        print_error(error, 'Error by uploading a file.')

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

            # set temporarily power off timeout
            elif data['type'] == 'power_off_timeout_tmp':
                if 'timeout' in keys:
                    hub.power_off(timeout = data['timeout'] * 1000)
                    hub.config['powerdown_timeout'] = data['timeout'] * 1000
                    events['power_off_timeout'] = data['timeout'] * 1000
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for power off timeout must have 'timeout'."})

            elif data['type'] == 'power_off_timeout':
                if 'timeout' in keys:
                    hub.power_off(timeout = data['timeout'] * 1000)
                    hub.config['powerdown_timeout'] = data['timeout'] * 1000
                    events['power_off_timeout'] = data['timeout'] * 1000
                    file = open('/etc/config')
                    config = file.read()
                    file.close()
                    try:
                        config = eval(config)
                    except:
                        config = {}
                    config['power_off_timeout'] = data['timeout'] * 1000
                    file = open('/etc/config', mode = 'w')
                    file.write(str(config))
                    file.close()
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for power off timeout must have 'timeout'."})

            # upload a program
            elif data['type'] == 'upload_program':
                if 'name' in keys and 'nickname' in keys:
                    try:
                        file = open('/.program_info')
                        program_info = file.read()
                        file.close()
                    except:
                        open('/.program_info', mode = 'x').close()
                        program_info = ''

                    if program_info != '':
                        try:
                            list_info = eval(program_info)
                        except Exception as error:
                            print_error(error, 'Error by processing data.')
                            data = ''
                            continue
                    else:
                        list_info = []

                    for info in list_info:
                        if info['name'] == data['name']:
                            list_info.remove(info)

                    if 'animation' in keys:
                        list_info.append({'name': data['name'], 'nickname': data['nickname'], 'picture': data['animation']})
                    else:
                        list_info.append({'name': data['name'], 'nickname': data['nickname']})

                    file = open('/.program_info', mode = 'w')
                    file.write(str(list_info))
                    file.close()

                    events['refresh_ui'] = True

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for upload a program must have 'name', 'data', and optional 'animation'."})

            # execute a python command
            elif data['type'] == 'execute':
                if 'command' in keys:
                    try:
                        output = eval(data['command'])
                        print({'type': 'req_execute', 'command': data['command'], 'output': output})
                        del output
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't execute command."})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for execute a command must have 'command'."})

            # run a program in /tmp
            elif data['type'] == 'run_tmp':
                if 'name' in keys and 'data' in keys:
                    file = open('/tmp/' + str(data['name']) + '.py', mode = 'w')
                    file.write(str(data['data']))
                    file.close()

                    events['program_runner'] = True
                    events['run'] = str(data['name'])

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program in tmp must have 'name' and 'data'."})

            # run a stored program
            elif data['type'] == 'run':
                if 'name' in keys:
                    events['program_runner'] = True
                    events['run'] = str(data['name'])

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program must have 'name'."})

            # get all stored programs
            elif data['type'] == 'get_programs':
                listdir = os.listdir('/programs')
                avail_programs = []
                for item in listdir:
                    avail_programs.append({'name': item.split('.py')[0], 'nickname': item.split('.py')[0]})

                file = open('/.program_info')
                try:
                    program_info = eval(file.read())
                except:
                    program_info = []

                for av_program in avail_programs:
                    for prog_info in program_info:
                        if av_program['name'] == prog_info['name']:
                            av_program['nickname'] = prog_info['nickname']
                            if 'picture' in list(prog_info.keys()):
                                av_program['picture'] = prog_info['picture']

                print({'type': 'req_programs', 'programs': avail_programs})

            # delete a program
            elif data['type'] == 'delete_program':
                if 'name' in keys:
                    try:
                        os.remove('/programs/' + data['name'] + '.py')
                    except Exception as error:
                        print_error(error, "Can't delete program '" + data['name'] + "'.")

                    sync_programs()

                    events['refresh_ui'] = True

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for delete a program must have 'name'."})

            # sync all programs (update /.program_info)
            elif data['type'] == 'sync_programs':
                sync_programs()
                events['refresh_ui'] = True

            # stop all programs and continue ui
            elif data['type'] == 'stop_all':
                events['stop_program_runner'] = True
                events['stop_ui'] = True

            elif data['type'] == 'stop_ui':
                events['stop_ui'] = True

            elif data['type'] == 'stop_program_runner':
                events['stop_program_runner'] = True

            # start sending sensor data to computer
            elif data['type'] == 'start_send_sensor_data':
                events['sensor_data'] = True

            # stop sending sensor data to computer
            elif data['type'] == 'stop_send_sensor_data':
                events['sensor_data'] = False

            # controller command
            elif data['type'] == 'program_input':
                if 'value' in keys:
                    events['program_input'] = events['program_input'] + data['value']
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A program_input command must have 'value'."})

            elif data['type'] == 'ls':
                if 'dir' in keys:
                    try:
                        listdir = os.listdir(data['dir'])
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get listdir of dir " + str(data['dir']) + '.'})
                    
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

            elif data['type'] == 'touch':
                if 'path' in keys:
                    try:
                        open(data['path'], mode = 'x').close()
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't create file " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A touch command must have 'path'."})

            elif data['type'] == 'remove':
                if 'path' in keys:
                    try:
                        os.remove(data['path'])
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't remove file " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A remove command must have 'path'."})

            elif data['type'] == 'mkdir':
                if 'dir' in keys:
                    try:
                        os.mkdir(data['dir'])
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't create dir " + str(data['dir']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A mkdir command must have 'dir'."})

            elif data['type'] == 'rmdir':
                if 'dir' in keys:
                    try:
                        os.rmdir(data['dir'])
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't remove dir " + str(data['dir']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A rmdir command must have 'dir'."})

            elif data['type'] == 'reset_ui':
                events['refresh_ui'] = True

            elif data['type'] == 'isdir':
                if 'path' in keys:
                    try:
                        print({'type': 'isdir', 'value': isdir(path)})
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get isdir of path " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A isdir command must have 'path'."})

            elif data['type'] == 'stat':
                if 'path' in keys:
                    try:
                        print({'type': 'stat', 'value': os.stat(data['path'])})
                    except Exception as error:
                        print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get stat of path " + str(data['path']) + '.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A stat command must have 'path'."})

            elif data['type'] == 'fsstat':
                try:
                    print({'type': 'fsstat', 'value': os.statvfs('/')})
                except Exception as error:
                    print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't get stat of filesystem."})

            elif data['type'] == 'get_events':
                ev = events.copy()
                del ev['remote']
                print({'type': 'events', 'value': ev})

            else:
                print({'type': 'error', 'name': 'InputError', 'message': 'Unknown type: ' + str(data['type'])})

        else:
            print({'type': 'error', 'name': 'InputError', 'message': "'type' must be in dict."})

        data = ''

        await asyncio.sleep(0)

