import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y

from PIL import ImageTk, Image
from stadiumpy.widgets import SFrame, Button

from stadiumpy.top_buttons import display_main_buttons

def prfview(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, adv_prf):
    
    


    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx

    # topcanvas = tk.Canvas(self)
    # topcanvas.config(bg='#ecebec')
    # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

    display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, disabledBtn=1)




    ###########################################
    lbl1 = ttk.Label(self, text="Filenames:")
    lbl1.configure(anchor="center")
    RELY += RELHEIGHT+0.01 
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)

    filename_vars = list(adv_prf['filenames'].keys())
    filename_vals = list(adv_prf['filenames'].values())
    kk=0

    label_options = {"font":('calibri', 12, 'normal')}
    drelx = (RELXS[2]-RELXS[1])/2
    while kk<len(filename_vars):
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=filename_vars[kk], **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+drelx)
        entry1.insert(0,filename_vals[kk])
        kk+=1

        ##
        lbl1 = ttk.Label(self, text=filename_vars[kk], **label_options)
        lbl1.place(relx=RELXS[3]-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[4]-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+drelx)
        entry1.insert(0,filename_vals[kk])
        kk+=1

    ###########################################
    