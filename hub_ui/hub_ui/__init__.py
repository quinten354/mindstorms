import sys
import hub

from .ui import main as ui_func
from .io import main as io_func
from .sensor_data import main as event_loop_func, send_loop as sensor_data_func
from device.system import print_error

list_cel = {'ui': ui_func(), 'io': io_func(), 'event_loop': event_loop_func(), 'sensor_data': sensor_data_func()}

def cel():
    try:
        next(list_cel['io'])
    except Exception as error:
        print_error(error)
        list_cel['io'] = io_func()

    try:
        next(list_cel['event_loop'])
    except Exception as error:
        print_error(error)
        list_cel['sensor_data'] = sensor_data_func()

    try:
        next(list_cel['sensor_data'])
    except Exception as error:
        print_error(error)
        list_cel['event_loop'] = event_loop_func()

hub.config['cel'] = cel

def main():
    while True:
        try:
            next(list_cel['ui'])
        except Exception as error:
            print_error(error)
            list_cel['ui'] = ui_func()

        try:
            next(list_cel['io'])
        except Exception as error:
            print_error(error)
            list_cel['io'] = io_func()

        try:
            next(list_cel['event_loop'])
        except Exception as error:
            print_error(error)
            list_cel['sensor_data'] = sensor_data_func()

        try:
            next(list_cel['sensor_data'])
        except Exception as error:
            print_error(error)
            list_cel['event_loop'] = event_loop_func()

