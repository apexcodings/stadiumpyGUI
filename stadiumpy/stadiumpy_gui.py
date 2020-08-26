import tkinter as tk
from tkinter import ttk
# from tkinter import filedialog, Text
import yaml, os
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y
from tkinter.ttk import Frame, Button, Style
import numpy as np
from stadiumpy.startpage import startview
from stadiumpy.prf_page import prfview
from stadiumpy.srf_page import srfview
from stadiumpy.dataenquirypage import dataenquiry
from stadiumpy.sks_page import sksview
from stadiumpy.page_control import PageControl
from stadiumpy.plot_map_gui import plotMap
import stadiumpy as stpy

cachedirec=".cache"
if not os.path.exists(cachedirec):
    os.makedirs(cachedirec, exist_ok=True)
    
image_name = os.path.join('.cache', 'region-plot.png')
# image_name = ".stadiumpyCache/region-plot.png"
# image_name = "region-plot.png"

# read inputYAML

inp_file_yaml = os.path.join(stpy.__path__[0], 'settings', 'input_file.yaml')
# inp_file_yaml = 'settings/input_file.yaml'
with open(inp_file_yaml) as f:
    inp = yaml.load(f, Loader=yaml.FullLoader)

print(inp)

class stadiumpy(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "STADIUMpy")
        tk.Tk.wm_geometry(self, "800x700+300+300")
        # tk.Tk.wm_resizable(self, 0, 0) #fixed window size
        tk.Tk.wm_minsize(self, 800, 700) 
        style = Style()
        style.theme_use("default")
        style.configure('W.TButton', font = ('calibri', 16, 'bold'),  borderwidth = '2', background="#c8ccc9")

        ## style for all buttons
        # style.configure('TButton', font = ('calibri', 16, 'bold'),  borderwidth = '2') 
        
        ## TOP frame
        container = tk.Frame(self, relief=RAISED, borderwidth=1)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)



        ## Bottom frame
        container2 = tk.Frame(self, relief=RAISED, borderwidth=2)
        container2.pack(side="bottom",fill="both", expand=True)

        closeButton = Button(container2, text="Close", command=self._quit,style = 'W.TButton')
        closeButton.pack(side="right", padx=5, pady=5)


        runButton = Button(container2,style = 'W.TButton', text="Run")
        runButton.pack(side="left", padx=5, pady=5)


        self.frames = {}

        for F in (StartPage, PagePRF, PageSRF, PageDataEnquiry, PageSKS, PageControl, PageGeoRegion):

            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def _quit(self):
        root = tk.Tk()
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent


        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        startview(self, ttk, parent, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, PageGeoRegion, inp, image_name)
        



## P - Receiver Functions
class PagePRF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        prfview(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp)




# S-RF
class PageSRF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        srfview(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp)
        


class PageDataEnquiry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        dataenquiry(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp)
        

    

class PageSKS(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        sksview(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp)


class PageGeoRegion(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # image_name = "region-plot.png"
        # Tk.update(self)
        # sksview(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp)
        plotMap(self, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp, image_name)
        



app = stadiumpy()
app.mainloop()