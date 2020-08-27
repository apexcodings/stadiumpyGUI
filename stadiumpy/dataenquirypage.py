import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y

from PIL import ImageTk, Image
from stadiumpy.widgets import SFrame, Button

from stadiumpy.top_buttons import display_main_buttons

def dataenquiry(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp):
    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx


    display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, disabledBtn=1)
