import numpy as np
from async_tkinter_loop import async_handler

class NotifyListener:
    def __init__(self, client, update_callback):
        self.client = client
        self.update_callback = update_callback

    @async_handler
    async def start_listening(self, characteristic_uuid):
        if self.client and self.client.is_connected:
            await self.client.start_notify(characteristic_uuid, self.notification_handler)

    async def notification_handler(self, sender, data):
        ints = np.frombuffer(data, dtype=np.uint32)
        floats = ints.astype(np.float32)
        print(floats)
        if self.update_callback:
            self.update_callback(floats)

    @async_handler
    async def stop_listening(self, characteristic_uuid):
        if self.client and self.client.is_connected:
            await self.client.stop_notify(characteristic_uuid)
