# import modules
import os
import hub
from time import sleep as wait, time_ns as time

from .program_runner import User_program
from .errors import EndOfProgramError

import device
from device.display import Print_hub_matrix, Image
from device import runtime_data


def main():
    while True:
        if not runtime_data['ui']:
            if runtime_data['run']:
                user_program = User_program(runtime_data['run'])
                runtime_data['run'] = None
            if runtime_data['stop']:
                del user_program
                runtime_data['ui'] = True
                runtime_data['stop'] = False
                device.system.reset()
                continue
            try:
                user_program.run()
            except EndOfProgramError:
                del user_program
                runtime_data['ui'] = True
                device.system.reset()
            yield
            continue

        else:
            if runtime_data['stop']:
                runtime_data['stop'] = False
                device.system.reset()
            listdir = os.listdir('/programs')
            programs = []
            for item in listdir:
                programs.append({'path': '/programs/' + item, 'name': item})

            # add home menu to data
            programs.insert(0, {'path': '/hub_ui/home.py', 'name': 'home', 'picture': [[1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]})

            # startup ui
            selection = 0
            selection_ch = False
            # set animation
            keys = list(programs[selection].keys())
            if 'picture' in keys:
                animation = Image(programs[selection]['picture'])
            else:
                animation = Print_hub_matrix(programs[selection]['nickname'], loop = True)

            # if the center button was pressed while starting up, ignore it
            hub.button.center.was_pressed()

            while True:
                if runtime_data['refresh_ui']:
                    runtime_data['refresh_ui'] = False
                    yield
                    break

                # update animation
                animation.show_next()
                # center button
                if hub.button.center.was_pressed():
                    runtime_data['run'] = programs[selection]['path']
                    runtime_data['ui'] = False
                    break

                if hub.button.left.was_pressed():
                    # select previous item
                    selection = selection - 1
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
                        animation = Image(programs[selection]['picture'])
                    else:
                        animation = Print_hub_matrix(programs[selection]['name'], loop = True)
                    selection_ch = False

                # wait
                # get time in sec (ms accuracy)
                btime = time()
                while time() - btime < 125000000:
                    yield

