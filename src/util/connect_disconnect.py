import asyncio
from bleak import BleakClient

async def connect(address):
    client = BleakClient(address)
    await client.connect()
    return client if client.is_connected else None

def disconnect(address):
    # Logic for disconnecting
    pass

async def connect_device(address):
    client = BleakClient(address)
    try:
        await client.connect()
        if client.is_connected:
            print(f"Connected to {address}")
            return client
        else:
            return None
    except Exception as e:
        print(f"Failed to connect to {address}: {e}")
        return None

async def disconnect_device(client):
    try:
        await client.disconnect()
        print("Disconnected successfully.")
    except Exception as e:
        print(f"Failed to disconnect: {e}")
