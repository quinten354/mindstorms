import uasyncio as asyncio
import sys
import builtins

sys.path.append('/tmp')

async def main(events):
    running = False
    while True:
        if not events['program_runner']:
            await asyncio.sleep(1)
            continue

        if events['stop']:
            events['run'] = None
            events['program_runner'] = False
            continue

        if not events['run']:
            events['program_runner'] = False
            continue

        if not running:
            try:
                exec('import ' + events['run'])
            except Exception as error:
                print({'type': 'error', 'name': 'SystemError', 'errname': str(type(error)), 'errmessage': str(error), 'message': "Can't import module '" + name + "'."})
                show_error()
                events['program_runner'] = False
                continue

            try:
                a = eval(data[selection]['name'] + '.main()')
            except:
                show_error()
                events['program_runner'] = False
                continue

            running = True

        if a:
            try:
                t = a.__next__()
                if type(t) == int:
                    await asyncio.sleep(t)
                else:
                    await asyncio.sleep(0)

            except builtins.StopIteration:
                running = False
                events['run'] = None
                events['program_runner'] = False
    
                try:
                    exec('del ' + events['run'])
                except:
                    pass
    
                events['program_runner'] = False
                continue

            except Exception as error:
                print({'type': 'error', 'name': 'ExecuteError', 'errname': str(type(error)), 'errmessage': str(error)})
                show_error()
    
                await asyncio.sleep(0.1)

        events['program_runner'] = False

