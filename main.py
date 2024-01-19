import tkinter as tk
from src.ui.form.main_form import BluetoothScannerApp
import asyncio
from async_tkinter_loop import async_mainloop

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothScannerApp(root)
    async_mainloop(root)