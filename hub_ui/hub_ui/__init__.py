# import modules
import os
import hub
import sys
import uasyncio as asyncio
import builtins

from .lib import EndOfLoopError, Print_hub_matrix, Picture, show_error, sync_programs
from .io import main as io
from .sensor_data import main as sensor_data
from .program_runner import main as program_runner
from .settings import main as settings

async def main(events):
    # get available user programs
    sys.path.append('/programs')
    listdir = os.listdir('/programs')
    programs = []
    for item in listdir:
        programs.append({'name': item.split('.py')[0], 'nickname': item.split('.py')[0]})

    # get program info
    try:
        file = open('/.program_info')
    except:
        data = []
    else:
        data = file.read()
        file.close()
        del file
        try:
            data = eval(data)
        except:
            data = []

        else:
            data = []

    # calculate programs to data dicts
    for program in programs:
        for program_data in data:
            if program['name'] == program_data['name']:
                program['nickname'] = program_data['nickname']
                if 'picture' in list(program.keys()):
                    program['picture'] = program_data['picture']

    # add settings menu to data
    programs.insert(0, {'name': 'settings', 'picture': [[[0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [0, 1, 0, 1, 0]]]})

    # startup ui
    selection = 0
    selection_ch = False
    # set animation
    keys = list(programs[selection].keys())
    if 'picture' in keys:
        animation = Picture(programs[selection]['picture'])
    else:
        animation = Print_hub_matrix(programs[selection]['name'], loop = True)

    hub.button.center.was_pressed()

    while True:
        if events['program_runner']:
            await asyncio.sleep(1)
            continue
        # update animation
        animation.show_next()
        # center button
        if hub.button.center.was_pressed():
            if programs[selection]['name'] == 'settings':
                a = settings()
                try:
                    while True:
                        if events['stop_ui']:
                            events['stop_ui'] = False
                            break
                        t = a.__next__()
                        if type(t) == int:
                            await asyncio.sleep(t)
                        else:
                            await asyncio.sleep(0)

                except builtins.StopIteration:
                    hub.button.center.was_pressed()
                    continue
                except Exception as error:
                    print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error)})
                    show_error()
                    hub.button.center.was_pressed()
                    continue
            else:
                # execute file
                try:
                    exec('import ' + programs[selection]['name'])
                except Exception as error:
                    print({'type': 'error', 'name': 'SystemError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't import module '" + programs[selection]['name'] + "'."})
                    show_error()
                    continue

                try:
                    a = eval(programs[selection]['name'] + '.main()')
                    if a:
                        try:
                            while True:
                                if events['stop_ui']:
                                    events['stop_ui'] = False
                                    break
                                t = a.__next__()
                                if type(t) == int:
                                    await asyncio.sleep(t)
                                else:
                                    await asyncio.sleep(0)

                        except builtins.StopIteration:
                            hub.button.center.was_pressed()
                            continue

                        except Exception as error:
                            print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error)})
                            show_error()
                            hub.button.center.was_pressed()
                            continue

                except Exception as error:
                    print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error)})
                    show_error()

                try:
                    del a
                    exec('del ' + programs[selection]['name'])
                except:
                    pass

            hub.button.center.was_pressed()

        # left button
        if hub.button.left.was_pressed():
            # select previous item
            selection = selection - 1
            selection_ch = True
        # right button
        if hub.button.right.was_pressed():
            # select next item
            selection = selection + 1
            selection_ch = True
        if selection < 0:
            selection = len(programs) - 1
        if selection >= len(programs):
            selection = 0
        if selection_ch:
            keys = list(programs[selection].keys())
            if 'picture' in keys:
                animation = Picture(programs[selection]['picture'])
            else:
                animation = Print_hub_matrix(programs[selection]['name'], loop = True)
            selection_ch = False
        # wait
        await asyncio.sleep(0.1)

