import tkinter as tk
from tkinter import ttk
from async_tkinter_loop import async_handler
import asyncio


class WriteWidget:
    def __init__(self, root, client):
        self.client = client  # Assign the client to an instance variable
        self.textbox1 = tk.Text(root, height=2, width=20)
        self.textbox1.grid(row=4, column=1, padx=0, pady=10)

        self.textbox2 = tk.Text(root, height=2, width=20)
        self.textbox2.grid(row=4, column=2, padx=0, pady=10)

        self.textbox3 = tk.Text(root, height=2, width=20)
        self.textbox3.grid(row=4, column=3, padx=30, pady=10)

        self.textbox4 = tk.Text(root, height=2, width=20)
        self.textbox4.grid(row=4, column=4, padx=30, pady=10)

        self.write_button = ttk.Button(root, text="Write to Char", command=self.write_to_char)
        self.write_button.grid(row=4, columnspan=1)


    def get_data(self):
        data = bytearray()
        text_boxes = [self.textbox1, self.textbox2, self.textbox3, self.textbox4]

        for box in text_boxes:
            content = box.get("1.0", tk.END).strip()
            if content:
                try:
                    # Assuming the input is a string of hex numbers
                    byte_content = bytes.fromhex(content)
                except ValueError:
                    # Handle invalid hex input, for example, by skipping or logging
                    continue
            else:
                byte_content = b'\x00'

            data.extend(byte_content)

        return data
    
    @async_handler
    async def write_and_verify(self, data):
        char_uuid = "eca1a4d3-06d7-4696-aac7-6e9444c7a3be"
        await self.client.write_gatt_char(char_uuid, data)
        await asyncio.sleep(0.001)  # Wait for 1ms
        read_data = await self.client.read_gatt_char(char_uuid)

        if read_data == data:
            print("Write success")
        else:
            print("Write failed")

    def write_to_char(self):
        data = self.get_data()
        asyncio.create_task(self.write_and_verify(data))