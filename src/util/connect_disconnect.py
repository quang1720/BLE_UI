import asyncio
from bleak import BleakClient

async def connect(address):
    client = BleakClient(address)
    await client.connect()
    return client if client.is_connected else None

def disconnect(address):
    # Logic for disconnecting
    pass

async def connect_device(selected_device, connect_callback):
    if selected_device:
        address = selected_device.split(" (")[1].rstrip(")")
        client = await connect(address)
        if client:
            print(f"Connected to {address}")
            connect_callback(address, client)

def disconnect_device(address, disconnect_callback):
    if address:
        disconnect(address)
        print(f"Disconnected from {address}")
        disconnect_callback()
