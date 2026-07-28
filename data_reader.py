import multiprocessing
import os
import serial

from .sensor_data import update as update_sensor_data

def chsize(bytes):
    pow = 0
    while bytes >= 1024:
        bytes = bytes / 1024
        pow = pow + 1

    bytes = str(bytes)
    bytes = bytes[:4]
    if bytes[-1] == '.':
        bytes = bytes[:-1]
    size = bytes + ['', 'K', 'M', 'G', 'T'][pow]
    return size

# set function to get data on requests from the hub
def get_data_from_hub(hub):
    def add_output(dict_):
        dict_ = hub._manager.dict(dict_)
        hub._cmd_output.append(dict_)
        hub._cmd_event.set()

    def add_error(string):
        hub._cmd_errors.append(string)
        hub._cmd_event.set()

    def main():
        hub._to_kill.append(os.getpid())
        # read lines of serial connection
        while True:
            try:
                for line in hub._serial:
                    data = line.strip().decode()
                    # create dict from data
                    try:
                        data = eval(data)
                    except:
                        print('ERROR: Invalid type of received data: ' + str(data))
                        add_error('ERROR: Invalid type of received data: ' + str(data))
                        continue

                    # check received data is a dict
                    if type(data) != dict:
                        print('ERROR: Not a dict: ' + str(data))
                        add_error('ERROR: Not a dict: ' + str(data))
                        continue

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
                                        add_output(data)
                                elif data['name'] == 'ExecuteError':
                                    if 'errmessage' in keys and 'message' in keys:
                                        print('Received ExecuteError: errmessage: ' + str(data['errmessage']) + ': ' + str(data['message']))
                                        add_output(data)
                                else:
                                    print('ERROR: Unknown received type of error: ' + data['name'] + '.')
                                    add_error('ERROR: Unknown received type of error: ' + data['name'] + '.')

                            else:
                                print('ERROR: Received data misses keyword \'name\'.')
                                add_error('ERROR: Received data misses keyword \'name\'.')

                        elif data['type'] == 'req_file':
                            if 'name' in keys and 'content' in keys:
                                try:
                                    path = hub._data[str(data['name'])]
                                except:
                                    print('ERROR: Unexpected file: ' + data['name'] + '.')
                                    add_error('ERROR: Unexpected file: ' + data['name'] + '.')
                                    continue
                                try:
                                    file = open(path, mode = 'w')
                                    file.write(data['content'])
                                    file.close()
                                except Exception as error:
                                    print('ERROR: ' + str(type(error)) + ': ' + str(error) + ': Cannot write to file: ' + path + '.')
                                    add_error('ERROR: ' + str(type(error)) + ': ' + str(error) + ': Cannot write to file: ' + path + '.')
                                try:
                                    del hub._data[str(data['name'])]
                                except:
                                    pass

                            else:
                                print('ERROR: Received data misses keywords \'name\' and \'content\'.')
                                add_error('ERROR: Received data misses keywords \'name\' and \'content\'.')

                        elif data['type'] == 'req_execute':
                            if 'command' in keys and 'output' in keys:
                                print('OUTPUT: Output execute: Command: ' + str(data['command']) + ', Output: ' + str(data['output']))
                                add_output(data)

                            else:
                                print('ERROR: Received data misses keywords \'command\' and \'output\'.')
                                add_error('ERROR: Received data misses keywords \'command\' and \'output\'.')

                        elif data['type'] == 'req_programs':
                            if 'programs' in keys:
                                print('OUTPUT: Availeble programs: ' + str(data['programs'])[1:][:-1])
                                add_output(data)

                            else:
                                print('ERROR: Received data misses keyword \'programs\'.')
                                add_error('ERROR: Received data misses keyword \'programs\'.')
                        
                        elif data['type'] == 'sensor_data':
                            if 'data' in keys:
                                hub._io['sensor_data'] = str(data['data'])
                                hub._sdevent.set()
                                #print('OUTPUT: ' + str(data['data']))

                            else:
                                print('ERROR: Received data misses keyword \'data\'.')
                                add_error('ERROR: Received data misses keyword \'data\'.')

                        elif data['type'] == 'output':
                            if 'value' in keys:
                                hub._io['output'] = hub._io['output'] + str(data['value'])
                                print('OUTPUT: ' + str(data['value']))

                            else:
                                print('ERROR: Received data misses keyword \'value\'.')
                                add_error('ERROR: Received data misses keyword \'value\'.')
                
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

                                add_output(data)

                            else:
                                print('ERROR: Received data misses keywords \'dirs\' and \'files\'.')
                                add_error('ERROR: Received data misses keywords \'dirs\' and \'files\'.')

                        elif data['type'] == 'isdir':
                            if 'value' in keys:
                                if data['value']:
                                    print('OUTPUT: Isdir: Directory.')
                                else:
                                    print('OUTPUT: Isdir: File.')
                                add_output(data)

                            else:
                                print('ERROR: Received data misses keyword \'value\'.')
                                add_error('ERROR: Received data misses keyword \'value\'.')

                        elif data['type'] == 'stat':
                            if 'value' in keys:
                                print('OUTPUT: Stat: Type: ' + str(data['value'][0]) + ', Size: ' + str(data['value'][6]))
                                add_output(data)

                            else:
                                print('ERROR: Received data misses keyword \'value\'.')
                                add_error('ERROR: Received data misses keyword \'value\'.')

                        elif data['type'] == 'fsstat':
                            if 'value' in keys:
                                print('OUTPUT: Fsstat: Total size: ' + chsize(data['value'][2] * data['value'][1]) + ', Used size: ' + chsize((data['value'][2] - data['value'][3]) * data['value'][1]) + ', Free size: ' + chsize(data['value'][3] * data['value'][1]) + ', Usage: ' + str(round(((data['value'][2] - data['value'][3]) / data['value'][3]) * 100, 2)) + '%.')
                                add_output(data)

                            else:
                                print('ERROR: Received data misses keyword \'value\'.')
                                add_error('ERROR: Received data misses keyword \'value\'.')

                        elif data['type'] == 'runtime_data':
                            if 'value' in keys:
                                print('OUTPUT: Runtime_data: ' + str(data['value']))
                                add_output(data)

                            else:
                                print('ERROR: Received data misses keyword \'value\'.')
                                add_error('ERROR: Received data misses keyword \'value\'.')

                        else:
                            print('ERROR: Unknown received type of data: ' + data['type'] + '.')
                            add_error('ERROR: Unknown received type of data: ' + data['type'] + '.')

            except KeyboardInterrupt:
                continue

            except serial.serialutil.SerialException:
                print('Connection closed.')
                for process in hub._to_kill:
                    if process != os.getpid():
                        try:
                            os.kill(process, 9)
                        except: 
                            pass
                hub._manager.shutdown()
                hub._serial.close()
                exit()

            except Exception as error:
                print('Error: ' + str(type(error)) + ': ' + str(error))
                add_error('Error: ' + str(type(error)) + ': ' + str(error))
                continue

    hub._get_data_from_hub = multiprocessing.Process(target = main, daemon = True)
    hub._get_data_from_hub.start()

