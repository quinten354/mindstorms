import uasyncio as asyncio

async def main(events):
    while True:
        if not events['sensor_data']:
            await asyncio.sleep(1)
            continue

        await asyncio.sleep(0.5)

