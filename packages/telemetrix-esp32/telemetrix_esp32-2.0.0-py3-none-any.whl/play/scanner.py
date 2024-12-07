import asyncio
from bleak import BleakScanner


async def run():
    devices = await BleakScanner.discover()
    # device = await BleakScanner.find_device_by_name('Telemetrix4ESP32BLE')

    for d in devices:
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

