# import modules
import uasyncio as asyncio
import sys
import builtins

from .settings import main as settings
from device.system import show_error, print_error, reset

# if the user runs a program in tmp (for example for a test)
sys.path.append('/tmp')

async def main(events):
    running = False
    while True:
        # check if the program runner is on
        if not events['program_runner']:
            # do nothing
            await asyncio.sleep(1)
            continue

        # when stop is True, the program runner must exit
        if events['stop_program_runner']:
            events['run'] = None
            events['program_runner'] = False
            events['stop_program_runner'] = False
            continue

        # if the program runner is on, run must have a name of what the program runner must run
        if not events['run']:
            events['program_runner'] = False
            continue

        # if running is False (the program runner has not setted up), set up
        if not running:
            if events['run'] == 'settings':
                a = settings()
            else:
                # import program
                try:
                    exec('import ' + events['run'])
                except Exception as error:
                    print_error(error)
                    show_error()
                    running = False
                    events['program_runner'] = False
                    events['run'] = None
                    reset()
                    continue

                # execute MODULE.main to setup program
                try:
                    a = eval(events['run'] + '.main()')
                except Exception as error:
                    print_error(error)
                    show_error()
                    running = False
                    events['program_runner'] = False
                    events['run'] = None
                    reset()
                    continue

            # set running to True, the program has setted up
            running = True

        # when a has a value
        if a:
            # continue program and continue event loop
            try:
                while True:
                    t = a.__next__()
                    if type(t) == int:
                        await asyncio.sleep(t)
                    else:
                        await asyncio.sleep(0)

            except builtins.StopIteration:
                try:
                    exec('del ' + events['run'])
                except:
                    pass
    
                running = False
                events['program_runner'] = False
                events['run'] = None
                reset()
                continue

            except Exception as error:
                print_error(error)
                show_error()
                reset()
    
                await asyncio.sleep(0.1)

        # turn off program runner
        else:
            running = False
            events['program_runner'] = False
            events['run'] = None
            reset()

