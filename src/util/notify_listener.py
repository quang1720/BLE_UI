import os
import csv
import numpy as np
from async_tkinter_loop import async_handler
from datetime import datetime

class NotifyListener:
    def __init__(self, client, update_callback):
        self.client = client
        self.update_callback = update_callback
        self.received_data = []

    @async_handler
    async def start_listening(self, characteristic_uuid):
        if self.client and self.client.is_connected:
            await self.client.start_notify(characteristic_uuid, self.notification_handler)

    async def notification_handler(self, sender, data):
        ints = np.frombuffer(data, dtype=np.uint32)
        floats = ints.astype(np.float32)
        print(floats)
        current_time = datetime.now()#.strftime("%H:%M:%S")
        self.received_data.append([current_time, floats])
        if self.update_callback:
            self.update_callback(floats)

    def save_to_csv(self,file_name, data):
        mode = 'a' if os.path.exists(file_name) else 'w'
        with open(file_name, mode, newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    @async_handler
    async def stop_listening(self, characteristic_uuid):
        await self.client.stop_notify(characteristic_uuid)
        file_name = f"{characteristic_uuid}.csv"
        self.save_to_csv(file_name, self.received_data)
        print(f"Saved data to {file_name}")
