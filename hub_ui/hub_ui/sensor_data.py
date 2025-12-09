# import modules
import uasyncio as asyncio
import hub
from device.remote import get_pressed

async def main(events):
    while True:
        data = []
        pressed = get_pressed(events)
        if type(pressed) == tuple:
            if len(pressed) > 0:
                hub.power_off(timeout = events['power_off_timeout'])
                hub.config['powerdown_timeout'] = events['power_off_timeout']
                print('timeout sensor data')

        if not events['sensor_data']:
            await asyncio.sleep(0.1)
            continue

        data.append({'type': 'remote', 'name': 'remote', 'pressed': pressed})
        data.append({'type': 'events', 'name': '-', 'events': events})
        print({'type': 'sensor_data', 'data': data})

        await asyncio.sleep(0.1)

