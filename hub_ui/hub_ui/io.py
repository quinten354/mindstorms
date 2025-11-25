import select
import sys
import hub
import uasyncio as asyncio
import os

from .lib import sync_programs

async def main(events):
    spoll = select.poll()
    spoll.register(sys.stdin, select.POLLIN)
    print()
    data = ''
    while True:
        if not spoll.poll(0):
            await asyncio.sleep(0.5)
            continue

        data = data + sys.stdin.read(1)
        if data[-1] != '\\n':
            await asyncio.sleep(0)
            continue

        try:
            data = eval(data)
        except:
            print({'type': 'error', 'name': 'InputError', 'message': 'Invalid received data: ' + str(data)})
            data = ''
            continue

        if type(data) != dict:
            print({'type': 'error', 'name': 'InputError', 'message': 'Input must be a dict, not a ' + str(type(data)) + '.'})
            data = ''
            continue

        keys = list(data.keys())

        if 'type' in keys:
            if data['type'] == 'upload_file':
                if 'path' in keys and 'content' in keys:
                    try:
                        file = open(data['path'], mode = 'w')
                        file.write(data['content'])
                        file.close()
                        del file
                    except Exception as error:
                        print({'type': 'error', 'name': 'SystemError', 'errname': str(type(error)), 'errmessage': str(error), 'message': 'Error by uploading a file.'})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for upload a file must have 'path' and 'content'."})

            elif data['type'] == 'download_file':
                if 'path' in keys:
                    try:
                        file = open(data['path'])
                        content = file.read()
                        file.close()
                        del file
                    except Exception as error:
                        print({'type': 'error', 'name': 'SystemError', 'errname': str(type(error)), 'errmessage': str(error), 'message': 'Error by downloading a file.'})

                    print({'type': 'req_file', 'name': data['path'], 'content': str(content)})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for upload a file must have 'path'."})

            elif data['type'] == 'power_off':
                if 'fast' in keys:
                    hub.power_off(fast = data['fast'])
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for power off must have 'fast'."})

            elif data['type'] == 'restart':
                if 'fast' in keys:
                    hub.power_off(restart = True, fast = data['fast'])
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for restart must have 'fast'."})

            elif data['type'] == 'power_off_timeout':
                if 'timeout' in keys:
                    hub.power_off(timeout = keys['timeout'])
                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for power off timeout must have 'fast'."})

            elif data['type'] == 'upload_program':
                if 'name' in keys and 'data' in keys and 'nickname' in keys:
                    file = open('/programs/' + data['name'] + '.py', mode = 'w')
                    file.write(data['data'])
                    file.close()

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
                            print({'type': 'error', 'name': 'SystemError', 'errname': str(type(error)), 'errmessage': str(error), 'message': 'Error by processing data.'})
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

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for upload a program must have 'name', 'data', and optional 'animation'."})

            elif data['type'] == 'execute':
                if 'command' in keys:
                    _ = None
                    exec(data['command'])
                    output = _
                    print({'type': 'req_execute', 'command': data['command'], 'output': output})

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for execute a command must have 'command'."})

            elif data['type'] == 'run_tmp':
                if 'name' in keys and 'data' in keys:
                    file = open('/tmp/' + data['name'] + '.py', mode = 'w')
                    file.write(data['data'])
                    file.close()

                    events['program_runner'] = True
                    events['run'] = data['name']

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program in tmp must have 'name' and 'data'."})

            elif data['type'] == 'run':
                if 'name' in keys:
                    events['program_runner'] = True
                    events['run'] = data['name']

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request to run a program must have 'name'."})

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

            elif data['type'] == 'delete_program':
                if 'name' in keys:
                    try:
                        os.remove('/programs/' + data['name'] + '.py')
                    except Exception as error:
                        print({'type': 'error', 'name': 'SystemError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't delete program '" + data['name'] + "'."})
                    sync_programs()

                else:
                    print({'type': 'error', 'name': 'InputError', 'message': "A request for delete a program must have 'name'."})

            elif data['type'] == 'sync_programs':
                sync_programs()

            elif data['type'] == 'stop':
                events['program_runner'] = False
                events['stop'] = True

            elif data['type'] == 'start_send_sensor_data':
                events['sensor_data'] = True

            elif data['type'] == 'stop_send_sensor_data':
                events['sensor_data'] = False

            else:
                print({'type': 'error', 'name': 'InputError', 'message': 'Unknown type: ' + str(data['type'])})

        else:
            print({'type': 'error', 'name': 'InputError', 'message': "'type' must be in dict."})

        data = ''

        await asyncio.sleep(0)

