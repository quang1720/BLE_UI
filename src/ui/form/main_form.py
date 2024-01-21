import tkinter as tk
from tkinter import ttk
import asyncio
import threading
from src.util.scan import discover_devices
from src.util.connect_disconnect import connect_device, disconnect_device
from src.util.notify_listener import NotifyListener
from src.util.read_char import Reader_Char
from src.util.write_and_verify_char import Write_And_Verify_Char
from async_tkinter_loop import async_handler
import numpy as np

SERVICES_UUIDS = [
    "23aab796-82b3-444e-9d72-01889d69512a",
    "17148dc5-3e60-4b28-939a-21102ca1de71",
]
CHARACTERISTICS_UUIDS = [
    "eca1a4d3-06d7-4696-aac7-6e9444c7a3be",
    "3e20933e-2607-4e75-94bf-6e507b58dc5d",
    "f27769db-02bc-40a2-afb0-addfb72dd658",
    "3918cbce-b2a3-433a-afc8-8490e3b689f4",
    "b0084375-1400-4947-8f78-9b32a6373b32",
]


class BluetoothScannerApp:
    def __init__(self, root):
        self.root = root
        root.title("Bluetooth Scanner")
        self.client = None

        # Scan Button
        self.scan_button = ttk.Button(root, text="Scan", command=self.scan_devices)
        self.scan_button.grid(row=0, column=0, padx=2, pady=5)

        # Devices Combobox
        self.devices_combobox = ttk.Combobox(root, state="readonly")
        self.devices_combobox.grid(row=0, column=1, padx=2, pady=5)

        # Connect Button
        self.connect_button = ttk.Button(
            root, text="Connect", command=self.connect_device
        )
        self.connect_button.grid(row=1, column=0, padx=2, pady=5)

        # Disconnect Button
        self.disconnect_button = ttk.Button(
            root, text="Disconnect", command=self.disconnect_device
        )
        self.disconnect_button.grid(row=1, column=1, padx=2, pady=5)

        # Text Box0 for Notifications
        self.notifications_textbox = tk.Text(root, height=2, width=70)
        self.notifications_textbox.grid(row=2, column=1, columnspan=2, padx=2, pady=5)
        # Listen Notify Button0
        self.listen_notify_button = ttk.Button(
            root, text="Listen Notify0", command = self.on_listen_notify
        )
        self.listen_notify_button.grid(row=2, column=0, columnspan=1, padx=2, pady=5)

        # Text Box1 for Notifications
        self.notifications_textbox1 = tk.Text(root, height=2, width=70)
        self.notifications_textbox1.grid(row=3, column=1, columnspan=2, padx=2, pady=5)
        # Listen Notify Button1
        self.listen_notify_button1 = ttk.Button(
            root, text="Listen Notify1", command = self.on_listen_notify1
        )
        self.listen_notify_button1.grid(row=3, column=0, columnspan=1, padx=2, pady=5)

        # Text Box2 for Notifications
        self.notifications_textbox2 = tk.Text(root, height=2, width=70)
        self.notifications_textbox2.grid(row=4, column=1, columnspan=2, padx=2, pady=5)
        # Listen Notify Button2
        self.listen_notify_button2 = ttk.Button(
            root, text="Listen Notify2", command = self.on_listen_notify2
        )
        self.listen_notify_button2.grid(row=4, column=0, columnspan=1, padx=2, pady=5)

        # Text Box3 for Notifications
        self.notifications_textbox3 = tk.Text(root, height=2, width=70)
        self.notifications_textbox3.grid(row=5, column=1, columnspan=2, padx=2, pady=5)
        # Listen Notify Button3
        self.listen_notify_button3 = ttk.Button(
            root, text="Listen Notify3", command = self.on_listen_notify3
        )
        self.listen_notify_button3.grid(row=5, column=0, columnspan=1, padx=2, pady=5)

        # Text Box for read characteristic
        self.read_characteristic_textbox = tk.Text(root, height=2, width=70)
        self.read_characteristic_textbox.grid(row=6, column=1, columnspan=2, padx=2, pady=5)
        # read characteristic Button
        self.read_characteristic_button = ttk.Button(
            root, text="Read_char", command = self.on_read_characteristic
        )
        self.read_characteristic_button.grid(row=6, column=0, columnspan=1, padx=2, pady=5)

        # Write Widget
        self.textbox1 = tk.Text(root, height=2, width=20)
        self.textbox1.grid(row=7, column=1, padx=0, pady=10)

        self.textbox2 = tk.Text(root, height=2, width=20)
        self.textbox2.grid(row=7, column=2, padx=0, pady=10)

        self.textbox3 = tk.Text(root, height=2, width=20)
        self.textbox3.grid(row=7, column=3, padx=30, pady=10)

        self.textbox4 = tk.Text(root, height=2, width=20)
        self.textbox4.grid(row=7, column=4, padx=30, pady=10)

        self.write_button = ttk.Button(root, text="Write to Char", command = self.on_write_to_char)
        self.write_button.grid(row=7, columnspan=1)

    @async_handler
    async def on_write_to_char(self):
        # await self.write_and_verify_characteristic()
        self.write_and_verify_char = Write_And_Verify_Char(self.client, [self.textbox1, self.textbox2, self.textbox3, self.textbox4])
        await self.write_and_verify_char.write_and_verify_characteristic("eca1a4d3-06d7-4696-aac7-6e9444c7a3be")

    # @async_handler
    # async def write_and_verify_characteristic(self):
    #     CHARACTERISTIC_UUID = "eca1a4d3-06d7-4696-aac7-6e9444c7a3be"
    #     if not self.client:
    #         print("No device connected")
    #         return

    #     data_to_write = self.get_data()

    #     # Write data to characteristic
    #     await self.client.write_gatt_char(CHARACTERISTIC_UUID, data_to_write, response=True)

    #     # Wait for 1ms (1000 microseconds)
    #     await asyncio.sleep(0.1)

    #     # Read data back from characteristic
    #     read_data = await self.client.read_gatt_char(CHARACTERISTIC_UUID)

    #     # Verify if the written data matches the read data
    #     if data_to_write == read_data:
    #         print("Write success")
    #     else:
    #         print("Data mismatch")

    
    # def get_data(self):
    #     data_array = []

    #     for textbox in [self.textbox1, self.textbox2, self.textbox3, self.textbox4]:
    #         text = textbox.get("1.0", "end-1c").strip()
    #         print(text)
    #         if text:
    #             try:
    #                 # Assuming the input should be converted to integer
    #                 data_array.append(int(text))
    #             except ValueError:
    #                 print(f"Invalid input in a textbox: {text}")
    #         else:
    #             data_array.append(0)
    #     print(data_array)
    #     print(bytearray(data_array))
    #     return bytearray(data_array)

    @async_handler
    async def scan_devices(self):
        devices = await discover_devices()
        self.update_devices_combobox(devices)

    def update_devices_combobox(self, devices):
        self.devices_combobox["values"] = [
            f"{name} ({address})" for name, address in devices
        ]

    @async_handler
    async def connect_device(self):
        selected = self.devices_combobox.get()
        if selected:
            address = selected.split(" (")[1].rstrip(")")
            self.client = await connect_device(address)
            if self.client:
                if self.check_gatt_profile(self.client):  # Remove 'await' here
                    print(
                        f"Connected to {address} with required services and characteristics"
                    )
                else:
                    print(
                        "Required services or characteristics not found. Disconnecting."
                    )
                    await disconnect_device(self.client)
                    self.client = None

    def check_gatt_profile(self, client):
        found_services = {uuid: False for uuid in SERVICES_UUIDS}
        found_characteristics = {uuid: False for uuid in CHARACTERISTICS_UUIDS}

        for service in client.services:
            if service.uuid in SERVICES_UUIDS:
                found_services[service.uuid] = True
                for char in service.characteristics:
                    if char.uuid in CHARACTERISTICS_UUIDS:
                        found_characteristics[char.uuid] = True

        return all(found_services.values()) and all(found_characteristics.values())

    def disconnect_device(self):
        if self.client:
            asyncio.create_task(disconnect_device(self.client))
            self.client = None
    
    @async_handler
    async def on_listen_notify(self):
        if self.client:
            self.notify_listener = NotifyListener(self.client, self.update_notification_box)
            await self.notify_listener.start_listening("3e20933e-2607-4e75-94bf-6e507b58dc5d")
    @async_handler
    async def on_listen_notify1(self):
        if self.client:
            self.notify_listener = NotifyListener(self.client, self.update_notification_box1)
            await self.notify_listener.start_listening("f27769db-02bc-40a2-afb0-addfb72dd658")
    
    @async_handler
    async def on_listen_notify2(self):
        if self.client:
            self.notify_listener = NotifyListener(self.client, self.update_notification_box2)
            await self.notify_listener.start_listening("3918cbce-b2a3-433a-afc8-8490e3b689f4")
    
    @async_handler
    async def on_listen_notify3(self):
        if self.client:
            self.notify_listener = NotifyListener(self.client, self.update_notification_box3)
            await self.notify_listener.start_listening("b0084375-1400-4947-8f78-9b32a6373b32")

    def update_notification_box(self, notification):
        self.notifications_textbox.delete("1.0", tk.END)
        self.notifications_textbox.insert(tk.END, f"{notification}\n")
    
    def update_notification_box1(self, notification):
        self.notifications_textbox1.delete("1.0", tk.END)
        self.notifications_textbox1.insert(tk.END, f"{notification}\n")

    def update_notification_box2(self, notification):
        self.notifications_textbox2.delete("1.0", tk.END)
        self.notifications_textbox2.insert(tk.END, f"{notification}\n")
    
    def update_notification_box3(self, notification):
        self.notifications_textbox3.delete("1.0", tk.END)
        self.notifications_textbox3.insert(tk.END, f"{notification}\n")
    
    @async_handler
    async def on_read_characteristic(self):
        char_uuid = "eca1a4d3-06d7-4696-aac7-6e9444c7a3be"
        reader = Reader_Char(self.client, self.update_read_characteristic_box)
        await reader.read_char(char_uuid)
        # if self.client:
        #     value = await self.client.read_gatt_char(char_uuid)
        #     print(value)
    
    def update_read_characteristic_box(self, data):
        self.read_characteristic_textbox.delete("1.0", tk.END)
        self.read_characteristic_textbox.insert(tk.END, f"{data}\n")


