from async_tkinter_loop import async_handler
import asyncio

class Reader_Char:
    def __init__(self, client):
        self.client = client

    @async_handler
    async def read_gatt_char(self, char_uuid):
        if self.client and self.client.is_connected:
            return await self.client.read_gatt_char(char_uuid)
        return None
