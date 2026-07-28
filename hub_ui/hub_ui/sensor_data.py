# import modules
import uasyncio as asyncio
import hub
import device.port
import device.motion
import device.battery
from time import time_ns as time
from device import runtime_data

def main():
    #bt_pressed = 0
    ct_pressed = 0
    while True:
        #if hub.button.center.is_pressed() or hub.button.connect.is_pressed() or hub.button.left.is_pressed() or hub.button.right.is_pressed():
            #runtime_data['last_activity'] = time()

        #if is_connected(runtime_data):
            #pressed = get_pressed(runtime_data)
        #else:
            #pressed = None

        #if type(pressed) == tuple:
            #if len(pressed) > 0:
                #runtime_data['last_activity'] = time()

        #if (time() - runtime_data['last_activity']) > (runtime_data['power_off_timeout'] / 1000) and runtime_data['power_off_timeout'] != 0:
            #hub.power_off(fast = False)

        #if hub.button.connect.was_pressed():
            #runtime_data['remote_connect'] = 'connect'

        #if hub.button.connect.is_pressed():
            #if bt_pressed == 0:
                #bt_pressed = time()
        #else:
            #bt_pressed = 0

        #if (time() - bt_pressed) > 0.35 and bt_pressed != 0:
            #runtime_data['remote_connect'] = 'disconnect'

        if hub.button.center.is_pressed():
            if ct_pressed == 0:
                ct_pressed = time()
        else:
            ct_pressed = 0

        if (time() - ct_pressed) > 600000000 and ct_pressed != 0:
            runtime_data['stop'] = True

        yield

def send_loop():
    while True:
        prev_time = time()
        if runtime_data['sensor_data']:
            send_sensor_data()
        while (time() - prev_time) < 2000000000:
            yield

def send_sensor_data():
    data = []
    acceleration = device.motion.get_acceleration()
    data.append({'type': 'acceleration', 'x': acceleration[0], 'y': acceleration[1], 'z': acceleration[2]})
    gyroscope = device.motion.get_gyroscope()
    data.append({'type': 'gyroscope', 'x': gyroscope[0], 'y': gyroscope[1], 'z': gyroscope[2]})
    data.append({'type': 'yaw', 'value': device.motion.get_yaw()})
    data.append({'type': 'pitch', 'value': device.motion.get_pitch()})
    data.append({'type': 'roll', 'value': device.motion.get_roll()})
    data.append({'type': 'battery', 'capacity': device.battery.get_current()})
    data.append({'type': 'temperature', 'value': device.get_temp()})
    for port in 'A', 'B', 'C', 'D', 'E', 'F':
        dev_type = device.port.get_type(port)
        if not dev_type:
            data.append({'type': 'port', 'port': port, 'device_type': None})
        # color-distance sensor
        elif dev_type == 37:
            mode = device.port.get_mode(port)
            color = device.port.devices.color_distance_sensor.get_color(port)
            reflection = device.port.devices.color_distance_sensor.get_reflection(port)
            counted = device.port.devices.color_distance_sensor.get_counted(port)
            cm = device.port.devices.color_distance_sensor.get_cm(port)
            inches = device.port.devices.color_distance_sensor.get_inches(port)
            device.port.set_mode(port, mode)
            data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'color-distance', 'color': color, 'reflection': reflection, 'counted': counted, 'cm': cm, 'inches': inches})
        # motor
        elif dev_type == 47 or dev_type == 75:
            mode = device.port.get_mode(port)
            busy = device.port.motor.get_busy(port)
            speed = device.port.motor.get_speed(port)
            rel_pos = device.port.motor.get_rel_pos(port)
            abs_pos = device.port.motor.get_abs_pos(port)
            device.port.set_mode(port, mode)
            data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'motor', 'busy': busy, 'speed': speed, 'rel_pos': rel_pos, 'abs_pos': abs_pos})
        # color sensor
        elif dev_type == 61:
            mode = device.port.get_mode(port)
            color = device.port.devices.color_sensor.get_color(port)
            reflection = device.port.devices.color_sensor.get_reflection(port)
            rgb = device.port.devices.color_sensor.get_rgb(port)
            device.port.set_mode(port, mode)
            data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'color', 'color': color, 'reflection': reflection, 'rgb': rgb})
        # distance sensor
        elif dev_type == 62:
            mode = device.port.get_mode(port)
            cm = device.port.devices.distance_sensor.get_cm(port)
            inches = device.port.devices.distance_sensor.get_inch(port)
            light = device.port.devices.distance_sensor.get_light(port)
            device.port.set_mode(port, mode)
            data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'distance', 'cm': cm, 'inches': inches, 'light': light})
        # 3x3 light matrix
        elif dev_type == 64:
            data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': '3x3 matrix'})
        else:
            data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'unknown'})
    print({'type': 'sensor_data', 'data': data})

