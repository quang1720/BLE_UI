import tkinter as tk
from tkinter import ttk
import asyncio
from src.util.scan import discover_devices
from src.util.connect_disconnect import connect_device, disconnect_device

async def get_services_and_characteristics(client):
    services = client.services
    services_data = {}
    for service in services:
        characteristics = [char.uuid for char in service.characteristics]
        services_data[service.uuid] = characteristics
    return services_data

class BluetoothScannerApp:
    def __init__(self, root):
        self.root = root
        root.title("Bluetooth Scanner")
        self.client = None  # Assuming you have a BLE client object

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

        # Services Combobox and Label
        self.services_label = ttk.Label(root, text="Services")
        self.services_label.grid(row=2, column=0, padx=5, pady=5)
        self.services_combobox = ttk.Combobox(root, state="readonly")
        self.services_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Get Services Button
        self.get_services_button = ttk.Button(root, text="Get Services", command=self.get_services)
        self.get_services_button.grid(row=2, column=2, padx=5, pady=5)

        # Characteristics Combobox and Label
        self.characteristics_label = ttk.Label(root, text="Characteristics")
        self.characteristics_label.grid(row=3, column=0, padx=5, pady=5)
        self.characteristics_combobox = ttk.Combobox(root, state="readonly")
        self.characteristics_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Get Characteristics Button
        self.get_characteristics_button = ttk.Button(root, text="Get Characteristics", command=self.get_characteristics)
        self.get_characteristics_button.grid(row=3, column=2, padx=5, pady=5)

        self.address_to_connect = None
        self.services_data = {}

    def scan_devices(self):
        devices = asyncio.run(discover_devices())
        self.devices_combobox['values'] = [f"{name} ({address})" for name, address in devices]

    def connect_device(self):
        selected = self.devices_combobox.get()
        asyncio.run(connect_device(selected, self.update_on_connect))

    def update_on_connect(self, address, client):
        self.address_to_connect = address
        self.client = client

    def disconnect_device(self):
        disconnect_device(self.address_to_connect, self.update_on_disconnect)

    def update_on_disconnect(self):
        self.address_to_connect = None
        self.client = None
        self.services_combobox['values'] = []
        self.characteristics_combobox['values'] = []

        # Optionally, you can also clear the current selection if needed
        self.services_combobox.set('')
        self.characteristics_combobox.set('')
        print("Disconnected successfully.")

    def get_services(self):
        if self.client is not None:
            asyncio.run(self.update_services_combobox(self.client))

    def get_characteristics(self):
        selected_service_uuid = self.services_combobox.get()
        if selected_service_uuid:
            characteristics = self.services_data.get(selected_service_uuid, [])
            self.characteristics_combobox['values'] = characteristics
            if characteristics:
                self.characteristics_combobox.current(0)

    async def update_services_combobox(self, client):
        self.services_data = await get_services_and_characteristics(client)
        self.services_combobox['values'] = list(self.services_data.keys())
        self.services_combobox.current(0)
        self.on_service_selected(None)

    def on_service_selected(self, event):
        selected_service_uuid = self.services_combobox.get()
        characteristics = self.services_data.get(selected_service_uuid, [])
        self.characteristics_combobox['values'] = characteristics
        if characteristics:
            self.characteristics_combobox.current(0)