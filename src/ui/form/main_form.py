import tkinter as tk
from tkinter import ttk
import asyncio
from src.util.scan import discover_devices
from src.util.connect_disconnect import connect_device, disconnect_device

# Constants for service and characteristic UUIDs
SERVICES_UUIDS = ["23aab796-82b3-444e-9d72-01889d69512a", "17148dc5-3e60-4b28-939a-21102ca1de71"]
CHARACTERISTICS_UUIDS = ["eca1a4d3-06d7-4696-aac7-6e9444c7a3be", "3e20933e-2607-4e75-94bf-6e507b58dc5d", "f27769db-02bc-40a2-afb0-addfb72dd658", "3918cbce-b2a3-433a-afc8-8490e3b689f4", "b0084375-1400-4947-8f78-9b32a6373b32"]

class BluetoothScannerApp:
    def __init__(self, root):
        self.root = root
        root.title("Bluetooth Scanner")

        # Scan Button
        self.scan_button = ttk.Button(root, text="Scan", command=self.scan_devices)
        self.scan_button.grid(row=0, column=0, padx=5, pady=5)

        # Devices Combobox
        self.devices_combobox = ttk.Combobox(root, state="readonly")
        self.devices_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Connect Button
        self.connect_button = ttk.Button(root, text="Connect", command=self.connect_device)
        self.connect_button.grid(row=1, column=0, padx=5, pady=5)

        # Disconnect Button
        self.disconnect_button = ttk.Button(root, text="Disconnect", command=self.disconnect_device)
        self.disconnect_button.grid(row=1, column=1, padx=5, pady=5)

        # Text Box for Notifications
        self.notifications_textbox = tk.Text(root, height=10, width=50)
        self.notifications_textbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Listen Notify Button
        self.listen_notify_button = ttk.Button(root, text="Listen Notify", command=self.on_listen_notify)
        self.listen_notify_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.client = None

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Schedule the first call to run the asyncio tasks
        self.root.after(100, self.run_pending_asyncio_tasks)

    def run_pending_asyncio_tasks(self):
        # Run all pending asyncio tasks
        self.loop.run_until_complete(asyncio.sleep(0))

        # Schedule the next run
        self.root.after(100, self.run_pending_asyncio_tasks)

    def on_listen_notify(self):
        # Schedule an asyncio task
        asyncio.run_coroutine_threadsafe(self.listen_notify(), self.loop)
        
    def scan_devices(self):
        devices = asyncio.run(discover_devices())
        self.devices_combobox['values'] = [f"{name} ({address})" for name, address in devices]

    def connect_device(self):
        selected = self.devices_combobox.get()
        asyncio.run(self.connect_and_check(selected))

    async def connect_and_check(self, selected_device):
        if selected_device:
            address = selected_device.split(" (")[1].rstrip(")")
            self.client = await connect_device(address)
            if self.client:
                if self.check_gatt_profile(self.client):
                    print(f"Connected to {address} with required services and characteristics")
                else:
                    print("Required services or characteristics not found. Disconnecting.")
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
            asyncio.run(disconnect_device(self.client))
            self.client = None
            print("Disconnected successfully.")

    async def listen_notify(self):
        if self.client:
            characteristic = self.find_characteristic(CHARACTERISTICS_UUIDS[1]) # UUID you specified
            if characteristic:
                await self.client.start_notify(characteristic, self.notification_handler)

    async def notification_handler(self, sender, data):
        formatted_data = f"Received data: {data}\n"
        self.notifications_textbox.insert(tk.END, formatted_data)
    
    def find_characteristic(self, uuid):
        for service in self.client.services:
            for char in service.characteristics:
                if char.uuid == uuid:
                    return char
        return None