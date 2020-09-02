"""
tweak the filenames for the P-receiver functions
"""
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL, RIDGE, GROOVE

from PIL import ImageTk, Image
from stadiumpy.widgets import SFrame, Button

from stadiumpy.top_buttons import display_main_buttons
from stadiumpy.styles import button_options_red, button_options_green, toggle_mode, toggle_button, button_init, toggle_PRF, button_options_nav, button_options_back


def prf_filter_settings(self, ttk, controller, adv_prf, *pageArgs):
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2

        # topcanvas = tk.Canvas(self)
        # topcanvas.config(bg='#ecebec')
        # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
                
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
                controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ##########################################

        lbl1 = ttk.Label(self, text=r'Filter Settings', **labHeadOptions, relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ##
        evsearch_vars = list(adv_prf['rf_filter_settings'].keys())
        evsearch_vals = list(adv_prf['rf_filter_settings'].values())

        kk=0
        while kk<len(evsearch_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                kk+=1

                ##
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                kk+=1
        