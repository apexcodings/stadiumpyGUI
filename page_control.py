import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y

from PIL import ImageTk, Image

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

LARGE_FONT= ("Helvetica", 20)

class PageControl(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Results", font=LARGE_FONT)
        label.grid(row=0, column=0, padx=10, pady=10, columnspan=10, sticky="nsew")

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0, padx=10, pady=10, columnspan=1)

        button2 = ttk.Button(self, text="RF Parameters",
                            command=lambda: controller.show_frame(PagePRF))
        button2.grid(row=1, column=1, padx=10, pady=10, columnspan=1, sticky="nsew")

        f = plt.Figure(figsize=(6,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=4, sticky="nsew")