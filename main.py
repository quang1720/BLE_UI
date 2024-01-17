import tkinter as tk
from src.ui.form.main_form import BluetoothScannerApp

if __name__ == "__main__":
    root = tk.Tk()
    
    app = BluetoothScannerApp(root)
    root.mainloop()