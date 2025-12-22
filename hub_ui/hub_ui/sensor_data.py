# import modules
import uasyncio as asyncio
import hub
from device.remote import get_pressed, is_connected
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

        if (time() - events['last_activity']) > (events['power_off_timeout'] / 1000):
            hub.power_off(fast = False)

        if hub.button.connect.was_pressed():
            events['remote_connect'] = 'connect'

        if hub.button.connect.is_pressed():
            bt_pressed = bt_pressed + 1
        else:
            bt_pressed = 0

        if bt_pressed > 3:
            events['remote_connect'] = 'disconnect'

        if hub.button.center.is_pressed():
            ct_pressed = ct_pressed + 1
        else:
            ct_pressed = 0

        if ct_pressed > 4:
            events['stop'] = True

        if not events['sensor_data']:
            await asyncio.sleep(0.1)
            continue

        data.append({'type': 'remote', 'name': 'remote', 'pressed': pressed})
        data.append({'type': 'events', 'name': 'events', 'events': events})
        print({'type': 'sensor_data', 'data': data})

        await asyncio.sleep(0.1)

