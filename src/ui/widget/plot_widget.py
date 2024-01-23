import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Toplevel


class Plot_Window:
    def __init__(self, root):
        self.root = root
        self.x = []
        self.y = []
        self.animations = []
    
    def get_data(self,datax,datay):
        self.x.append(datax) 
        self.y.append(datay)
        self.x = self.x[-10:]
        self.y = self.y[-10:]


    # def create_window(self):
    #     self.window = Toplevel(self.root)
    #     self.window.title("Plot")
    #     self.window.geometry("800x600")
    #     self.window.resizable(False, False)
    #     # self.window.protocol("WM_DELETE_WINDOW", self.close_window)
    #     self.plotdata()

    def plotdata(self):
        new_window = Toplevel()
        new_window.title("Plot Window")
        new_window.geometry("800x600")
        new_window.resizable(False, False)

        fig, ax = plt.subplots()

        def animate(i):
            ax.clear()
            ax.plot(self.x, self.y)
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Character Value')
            # plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Live Graph with Timestamp and Sliding Window')

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        ani = animation.FuncAnimation(fig, animate, interval=1000)
        self.animations.append(ani)