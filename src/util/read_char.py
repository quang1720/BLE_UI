from async_tkinter_loop import async_handler
import asyncio
import numpy as np

class Reader_Char:
    def __init__(self, client, update_callback):
        self.client = client
        self.update_callback = update_callback

    @async_handler
    async def read_char(self, char_uuid):
        if self.client:
             data = await self.client.read_gatt_char(char_uuid)
             await self.data_handler(data)
            # return data
    
    async def data_handler(self, data):
        ints = np.frombuffer(data, dtype=np.uint8)
        floats = ints.astype(np.float32)
        print(floats)
        if self.update_callback:
            self.update_callback(floats)