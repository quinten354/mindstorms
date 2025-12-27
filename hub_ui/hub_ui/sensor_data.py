# import modules
import uasyncio as asyncio
import hub
from device.remote import get_pressed, is_connected
import device.port
import device.motion
import device.battery
from time import time

async def main(events):
    bt_pressed = 0
    ct_pressed = 0
    while True:
        data = []
        if hub.button.center.is_pressed() or hub.button.connect.is_pressed() or hub.button.left.is_pressed() or hub.button.right.is_pressed():
            events['last_activity'] = time()

        if is_connected(events):
            pressed = get_pressed(events)
        else:
            pressed = None

        if type(pressed) == tuple:
            if len(pressed) > 0:
                events['last_activity'] = time()

        if (time() - events['last_activity']) > (events['power_off_timeout'] / 1000) and events['power_off_timeout'] != 0:
            hub.power_off(fast = False)

        if hub.button.connect.was_pressed():
            events['remote_connect'] = 'connect'

        if hub.button.connect.is_pressed():
            if bt_pressed == 0:
                bt_pressed = time()
        else:
            bt_pressed = 0

        if (time() - bt_pressed) > 0.35 and bt_pressed != 0:
            events['remote_connect'] = 'disconnect'

        if hub.button.center.is_pressed():
            if ct_pressed == 0:
                ct_pressed = time()
        else:
            ct_pressed = 0

        if (time() - ct_pressed) > 0.6 and ct_pressed != 0:
            events['stop_ui'] = True
            events['stop_program_runner'] = True

        if not events['sensor_data']:
            await asyncio.sleep(0.1)
            continue

        data.append({'type': 'remote', 'pressed': pressed})
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
                rgb = device.port.devices.color_distance_sensor.get_rgb(port)
                counted = device.port.devices.color_distance_sensor.get_counted(port)
                cm = device.port.devices.color_distance_sensor.get_cm(port)
                inches = device.port.devices.color_distance_sensor.get_inches(port)
                device.port.set_mode(port, mode)
                data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'color-distance sensor', 'color': color, 'reflection': reflection, 'rgb': rgb, 'counted': counted, 'cm': cm, 'inches': inches})
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
                data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'color sensor', 'color': color, 'reflection': reflection, 'rgb': rgb})
            # distance sensor
            elif dev_type == 62:
                mode = device.port.get_mode(port)
                cm = device.port.devices.distance_sensor.get_cm(port)
                inches = device.port.devices.distance_sensor.get_inch(port)
                light = device.port.devices.distance_sensor.get_light(port)
                device.port.set_mode(port, mode)
                data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'distance sensor', 'cm': cm, 'inches': inches, 'light': light})
            # 3x3 light matrix
            elif dev_type == 64:
                data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': '3x3 light matrix'})
            else:
                data.append({'type': 'port', 'port': port, 'device_type': dev_type, 'name': 'unknown'})
        print({'type': 'sensor_data', 'data': data})

        await asyncio.sleep(0.1)

