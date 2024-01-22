
import os
import csv
import numpy as np
from async_tkinter_loop import async_handler
from datetime import datetime

class NotifyListener:
    def __init__(self, client, update_callback,update_callback2):
        self.client = client
        self.update_callback = update_callback
        self.temp_file_name = None
        self.update_callback2 = update_callback2

    @async_handler
    async def start_listening(self, characteristic_uuid):
        self.temp_file_name = f"{characteristic_uuid}_temp.csv"
        if self.client and self.client.is_connected:
            await self.client.start_notify(characteristic_uuid, self.notification_handler)

    async def notification_handler(self, sender, data):
        ints = np.frombuffer(data, dtype=np.uint8)
        floats = ints.astype(np.float32)
        print(len(floats))
        print(floats[3])
        current_time = datetime.now().strftime("%D-%M-%Y_%H:%M:%S")
        current_time1 = datetime.now().strftime("%H:%M:%S")
        self.save_to_csv(self.temp_file_name, [[current_time, *floats]])
        if self.update_callback:
            self.update_callback(floats)
        if self.update_callback2:
            self.update_callback2(current_time1,floats[2])

    def save_to_csv(self, file_name, data):
        mode = 'a' if os.path.exists(file_name) else 'w'
        with open(file_name, mode, newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    @async_handler
    async def stop_listening(self, characteristic_uuid):
        if self.client and self.client.is_connected:
            await self.client.stop_notify(characteristic_uuid)
            final_file_name = f"{characteristic_uuid}.csv"
            # Read from temp file and write to the final file
            if os.path.exists(self.temp_file_name):
                with open(self.temp_file_name, 'r') as temp_file:
                    data = temp_file.readlines()
                self.save_to_csv(final_file_name, [row.strip().split(',') for row in data])
                # Clear temp file content
                open(self.temp_file_name, 'w').close()
                print(f"Saved data to {final_file_name}")

            self.temp_file_name = None
