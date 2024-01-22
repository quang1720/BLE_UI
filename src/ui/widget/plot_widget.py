import tkinter as tk
from tkinter import Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plot_Window:
    def __init__(self, root):
        self.root = root
        self.x = []
        self.y = []
    
    def get_data(self, x, y):
        self.x = x
        self.y = y

    def create_window(self):
        self.window = Toplevel(self.root)
        self.window.title("Plot")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        # self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.plotdata()

    def plotdata(self):
        x_data = self.x[-10:]
        y_data = self.y[-10:]
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data)
        canvas = FigureCanvasTkAgg(fig, root=self.new_window) 
        canvas.draw()
        canvas.get_tk_widget().pack()