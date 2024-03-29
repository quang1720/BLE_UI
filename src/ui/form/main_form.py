import tkinter as tk
from tkinter import ttk
import asyncio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Toplevel
from src.util.scan import discover_devices
from src.util.connect_disconnect import connect_device, disconnect_device
from src.util.notify_listener import NotifyListener
from src.util.read_char import Reader_Char
from src.util.write_and_verify_char import Write_And_Verify_Char
from src.ui.widget.plot_widget import Plot_Window
import matplotlib.dates as mdates
from datetime import datetime
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
        self.scan_button.grid(row=0, column=0, padx=2, pady=1)

        # Devices Combobox
        self.devices_combobox = ttk.Combobox(root, state="readonly")
        self.devices_combobox.grid(row=0, column=1, padx=2, pady=5)

        # Connect Button
        self.connect_button = ttk.Button(
            root, text="Connect", command=self.connect_device
        )
        self.connect_button.grid(row=1, column=0, padx=2, pady=1)

        # Disconnect Button
        self.disconnect_button = ttk.Button(
            root, text="Disconnect", command=self.disconnect_device
        )
        # self.disconnect_button.grid(row=1, column=1, padx=2, pady=5)

        # Listen Notify Button0
        self.listen_notify_button = ttk.Button(
            root, text="Listen Notify", command = self.on_listen_notify
        )
        self.listen_notify_button.grid(row=2, column=1, columnspan=1, padx=2, pady=1)
        # Listen Notify Button1
        self.listen_notify_button1 = ttk.Button(
            root, text="Listen Notify1", command = self.on_listen_notify1
        )
        self.listen_notify_button1.grid(row=2, column=2, columnspan=1, padx=2, pady=1)
        # Listen Notify Button2
        self.listen_notify_button2 = ttk.Button(
            root, text="Listen Notify2", command = self.on_listen_notify2
        )
        self.listen_notify_button2.grid(row=2, column=3, columnspan=1, padx=2, pady=1)
        # Listen Notify Button3
        self.listen_notify_button3 = ttk.Button(
            root, text="Listen Notify3", command = self.on_listen_notify3
        )
        self.listen_notify_button3.grid(row=2, column=4, columnspan=1, padx=2, pady=1)
        # Log notifications to csv button0
        self.log_notify_button = ttk.Button(
            root, text="Export Notify1", command = self.on_log_notify
            )
        self.log_notify_button.grid(row=4, column=1, columnspan=1, padx=2, pady=1)
        self.log_notify_button1 = ttk.Button(
            root, text="Export Notify2", command = self.on_log_notify1
            )
        self.log_notify_button1.grid(row=4, column=2, columnspan=1, padx=2, pady=1)
        self.log_notify_button2 = ttk.Button(
            root, text="Export Notify3", command = self.on_log_notify2
            )
        self.log_notify_button2.grid(row=4, column=3, columnspan=1, padx=2, pady=1)
        self.log_notify_button3 = ttk.Button(
            root, text="Export Notify4", command = self.on_log_notify3
            )
        self.log_notify_button3.grid(row=4, column=4, columnspan=1, padx=2, pady=1)
        # Plot Data Button0
        self.plot_data_button = ttk.Button(root, text="Plot Data 1", command=self.plot_data)
        self.plot_data_button.grid(row=3, column=1, padx=2, pady=1)
        self.plot_data_button1 = ttk.Button(root, text="Plot Data 2", command=self.plot_data1)
        self.plot_data_button1.grid(row=3, column=2, padx=2, pady=1)
        self.plot_data_button2 = ttk.Button(root, text="Plot Data 3", command=self.plot_data2)
        self.plot_data_button2.grid(row=3, column=3, padx=2, pady=1)
        self.plot_data_button3 = ttk.Button(root, text="Plot Data 4", command=self.plot_data3)
        self.plot_data_button3.grid(row=3, column=4, padx=2, pady=1)
        # Plot Widget
        self.plotwidget = Plot_Window(self.root)
        self.plotwidget1 = Plot_Window(self.root)
        self.plotwidget2 = Plot_Window(self.root)
        self.plotwidget3 = Plot_Window(self.root)

        # Text Box for read characteristic
        self.read_characteristic_textbox = tk.Text(root, height=2, width=70)
        self.read_characteristic_textbox.grid(row=6, column=1, columnspan=2, padx=2, pady=1)
        # read characteristic Button
        self.read_characteristic_button = ttk.Button(
            root, text="Read_char", command = self.on_read_characteristic
        )
        self.read_characteristic_button.grid(row=6, column=0, columnspan=1, padx=2, pady=1)

        # Write Widget
        self.textbox1 = tk.Text(root, height=2, width=20)
        self.textbox1.grid(row=7, column=1, padx=0, pady=2)

        self.textbox2 = tk.Text(root, height=2, width=20)
        self.textbox2.grid(row=7, column=2, padx=0, pady=2)

        self.textbox3 = tk.Text(root, height=2, width=20)
        self.textbox3.grid(row=7, column=3, padx=30, pady=2)

        self.textbox4 = tk.Text(root, height=2, width=20)
        self.textbox4.grid(row=7, column=4, padx=30, pady=2)

        self.write_button = ttk.Button(root, text="Write to Char", command = self.on_write_to_char)
        self.write_button.grid(row=7, columnspan=1)



    @async_handler
    async def on_write_to_char(self):
        # await self.write_and_verify_characteristic()
        self.write_and_verify_char = Write_And_Verify_Char(self.client, [self.textbox1, self.textbox2, self.textbox3, self.textbox4])
        await self.write_and_verify_char.write_and_verify_characteristic("eca1a4d3-06d7-4696-aac7-6e9444c7a3be")

    @async_handler
    async def scan_devices(self):
        self.devices_combobox.set("Scaning")
        devices = await discover_devices()
        self.update_devices_combobox(devices)
        if not devices:
            self.devices_combobox.set("No devices found")
        else:
            self.devices_combobox.set("Select a device")

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
                if self.check_gatt_profile(self.client):
                    print(
                        f"Connected to {address} with required services and characteristics"
                    )
                    self.connect_button.grid_forget()
                    self.disconnect_button.grid(row=1, column=0, padx=2, pady=5)
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
            self.disconnect_button.grid_forget()
            self.connect_button.grid(row=1, column=0, padx=2, pady=5)
    
    @async_handler
    async def on_listen_notify(self):
        if self.client:
            self.notify_listener = NotifyListener(self.client,  self.update_plotdata)
            await self.notify_listener.start_listening("3e20933e-2607-4e75-94bf-6e507b58dc5d")
    @async_handler
    async def on_listen_notify1(self):
            self.notify_listener1 = NotifyListener(self.client, self.update_plotdata1)
            await self.notify_listener1.start_listening("f27769db-02bc-40a2-afb0-addfb72dd658")
    @async_handler
    async def on_listen_notify2(self):
            self.notify_listener2 = NotifyListener(self.client, self.update_plotdata2)
            await self.notify_listener2.start_listening("3918cbce-b2a3-433a-afc8-8490e3b689f4")
    @async_handler
    async def on_listen_notify3(self):
            self.notify_listener3 = NotifyListener(self.client, self.update_plotdata3)
            await self.notify_listener3.start_listening("b0084375-1400-4947-8f78-9b32a6373b32")   

    @async_handler
    async def on_log_notify(self):
        if self.client:
            self.notify_listener.stop_listening("3e20933e-2607-4e75-94bf-6e507b58dc5d")

    @async_handler
    async def on_log_notify1(self):
        if self.client:
            self.notify_listener1.stop_listening("f27769db-02bc-40a2-afb0-addfb72dd658")
    
    @async_handler
    async def on_log_notify2(self):
        if self.client:
            self.notify_listener2.stop_listening("3918cbce-b2a3-433a-afc8-8490e3b689f4")
    
    @async_handler
    async def on_log_notify3(self):
        if self.client:
            self.notify_listener3.stop_listening("b0084375-1400-4947-8f78-9b32a6373b32")
    
    @async_handler
    async def on_read_characteristic(self):
        char_uuid = "eca1a4d3-06d7-4696-aac7-6e9444c7a3be"
        reader = Reader_Char(self.client, self.update_read_characteristic_box)
        await reader.read_char(char_uuid)
    
    def update_read_characteristic_box(self, data):
        self.read_characteristic_textbox.delete("1.0", tk.END)
        self.read_characteristic_textbox.insert(tk.END, f"{data}\n")

    def update_plotdata(self, datax, datay, sender):
        self.plotwidget.get_data(datax, datay, sender)

    def update_plotdata1(self, datax, datay, sender):
        self.plotwidget1.get_data(datax, datay, sender)

    def update_plotdata2(self, datax, datay, sender):
        self.plotwidget2.get_data(datax, datay, sender)
        
    def update_plotdata3(self, datax, datay, sender):
        self.plotwidget3.get_data(datax, datay, sender)


    def plot_data(self):
        self.plotwidget.plotdata()  

    def plot_data1(self):
        self.plotwidget1.plotdata()

    def plot_data2(self):
        self.plotwidget2.plotdata()

    def plot_data3(self):
        self.plotwidget3.plotdata()
    