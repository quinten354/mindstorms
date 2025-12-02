# import modules
import os
import hub
import sys
import uasyncio as asyncio
import builtins

from device.display import EndOfLoopError, Print_hub_matrix, Picture
from device.system import show_error, sync_programs, print_error
from .io import main as io
from .sensor_data import main as sensor_data
from .program_runner import main as program_runner
from .settings import main as settings
from .remote import Remote

async def main(events):
    # get available user programs
    sys.path.append('/programs')
    while True:
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

        # if the center button was pressed while starting up, ignore it
        hub.button.center.was_pressed()

        while True:
            rem_pressed = ()
            if events['remote']:
                pressed = events['remote'].pressed()
                if type(pressed) == tuple:
                    rem_pressed = pressed

            # if the program runner is active, pause the ui
            if events['program_runner']:
                await asyncio.sleep(1)
                continue

            if events['refresh_ui']:
                events['refresh_ui'] = False
                await asyncio.sleep(0.1)
                break

            # update animation
            animation.show_next()
            # center button
            if hub.button.center.was_pressed() or 'LEFT' in rem_pressed:
                if programs[selection]['name'] == 'settings':
                    # settings program
                    # setup
                    a = settings()
                    # run
                    try:
                        while True:
                            if events['stop']:
                                events['stop'] = False
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
                        print_error(error)
                        show_error()
                        continue

                else:
                    # other programs
                    # setup
                    try:
                        exec('import ' + programs[selection]['name'])
                    except Exception as error:
                        print_error(error)
                        show_error()
                        continue

                    # run
                    try:
                        mod = eval(programs[selection]['name'])
                        a = mod.main(events)
                        if a:
                            try:
                                while True:
                                    if events['stop']:
                                        events['stop'] = False
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
                                print_error(error)
                                show_error()
                                hub.button.center.was_pressed()
                                continue

                    except Exception as error:
                        print_error(error)
                        show_error()

                    try:
                        del a
                        exec('del ' + programs[selection]['name'])
                    except:
                        pass

                # if the center button was pressed when the program is running, ignore it
                hub.button.center.was_pressed()

            # left button
            if 'LEFT_MINUS' in rem_pressed:
                while 'LEFT_MINUS' in events['remote'].pressed():
                    await asyncio.sleep(0.1)
                # select previous item
                selection = selection - 1
                selection_ch = True

            if hub.button.left.was_pressed():
                # select previous item
                selection = selection - 1
                selection_ch = True

            # right button
            if 'LEFT_PLUS' in rem_pressed:
                while 'LEFT_PLUS' in events['remote'].pressed():
                    await asyncio.sleep(0.1)
                # select next item
                selection = selection + 1
                selection_ch = True

            if hub.button.right.was_pressed():
                # select next item
                selection = selection + 1
                selection_ch = True

            if selection < 0:
                selection = len(programs) - 1
            if selection >= len(programs):
                selection = 0

            # create a new animation when the selection changes
            if selection_ch:
                keys = list(programs[selection].keys())
                if 'picture' in keys:
                    animation = Picture(programs[selection]['picture'])
                else:
                    animation = Print_hub_matrix(programs[selection]['name'], loop = True)
                selection_ch = False

            # wait
            await asyncio.sleep(0.1)

