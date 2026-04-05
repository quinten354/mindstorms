# import modules
from serial.tools.list_ports import comports

# find device of the hub
def find_device():
    for port in comports():
        if port.vid == 00 and port.pid == 00:
            return port.device
    else:
        raise RuntimeError('Device not found.')

