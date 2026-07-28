# import modules
import hub as _hub

runtime_data = {'ui': True, 'run': None, 'stop': False, 'refresh_ui': False, 'sensor_data': False, 'program_input': ''}

def get_data_dir():
    if runtime_data['run']:
        program = runtime_data['run'].split('/')[-1]
        return '/var/' + program

def get_led():
    return _hub.led()

def set_led(*args):
    _hub.led(*args)

def get_temp():
    return _hub.temperature()

