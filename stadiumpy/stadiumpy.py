"""
Wrapper for the stadiumpy GUI
"""
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
from stadiumpy.results_summary_page import res_sum
from stadiumpy.page_control import PageControl
from stadiumpy.plot_map_gui import plotMap
import stadiumpy

cachedirec=".cache"
if not os.path.exists(cachedirec):
    os.makedirs(cachedirec, exist_ok=True)

image_name = os.path.join('.cache', 'region-plot.png')

# read inputYAML

inp_file_yaml = os.path.join(stadiumpy.__path__[0], 'settings', 'input_file.yaml')
adv_prf_yaml = os.path.join(stadiumpy.__path__[0], 'settings', 'advancedRF.yaml')
# inp_file_yaml = 'settings/input_file.yaml'

with open(inp_file_yaml) as f:
    inp = yaml.load(f, Loader=yaml.FullLoader)

with open(adv_prf_yaml) as f:
    adv_prf = yaml.load(f, Loader=yaml.FullLoader)


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

        for F in (StartPage, PageRF, PageSRF, PageDataEnquiry, PageSKS, PageControl, PageGeoRegion, ResultsSummary):

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

def pageArgsOut():
    pageArgs = (StartPage, PageDataEnquiry, PageRF, PageSKS, ResultsSummary, PageGeoRegion, PageSRF)
    return pageArgs

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        startview(self, ttk, parent, controller, inp, image_name, *pageArgsOut())

        

## P - Receiver Functions
class PageRF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        prfview(self, ttk, parent, controller, adv_prf, *pageArgsOut())



# S-RF
class PageSRF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        srfview(self, ttk, parent, controller, inp, *pageArgsOut())
        


class PageDataEnquiry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        dataenquiry(self, ttk, parent, controller, inp, *pageArgsOut())
        

    

class PageSKS(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        sksview(self, ttk, parent, controller, inp, *pageArgsOut())


class PageGeoRegion(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        plotMap(self, ttk, parent, controller, inp, image_name, *pageArgsOut())
        
class ResultsSummary(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        res_sum(self, ttk, parent, controller, inp, *pageArgsOut())

        



app = stadiumpy()
app.mainloop()