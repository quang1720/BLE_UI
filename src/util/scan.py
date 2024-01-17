import asyncio
from bleak import BleakScanner

async def discover_devices():
    devices = await BleakScanner.discover()
    return [(device.name, device.address) for device in devices]
