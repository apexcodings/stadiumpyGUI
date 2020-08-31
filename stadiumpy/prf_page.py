"""
This page is to set the parameters for the P-receiver functions of the stadiumpy
"""
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL, RIDGE, GROOVE

from PIL import ImageTk, Image
from stadiumpy.widgets import SFrame, Button

from stadiumpy.top_buttons import display_main_buttons
from stadiumpy.styles import button_options_red, button_options_green, toggle_mode, toggle_button, button_init, toggle_PRF, button_options_nav, button_options_back

def prfview(self, ttk, parent, controller, adv_prf, *pageArgs):

        #     print("response from prf page")

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
        stad_mode = "Go to S-RF"
        button_options = button_options_nav 
        fontDict = {"font":('calibri', 16, 'bold')}
        button_options = {**button_options, **fontDict}

        fontDictSecondary = {"font":('calibri', 12, 'bold')}
        button_optionsSecondary = {**button_options_back, **fontDictSecondary}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}

        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        button_mode = Button(self, text=stad_mode, command=lambda: toggle_PRF(button_mode, controller, pageArgs), **button_optionsSecondary)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ## filenames button
        RELY += RELHEIGHT+0.01 
        def gotofilenameprf():
                controller.show_frame(pageArgs[7])
        button_filename = Button(self, text="Set File Names", command=gotofilenameprf, **button_options)

        button_filename.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## set h kappa
        def gotohkappaprf():
                controller.show_frame(pageArgs[8])
        button_filename = Button(self, text="Set H-Kappa", command=gotohkappaprf, **button_options)

        button_filename.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)

        ## RF profile config
        RELY += RELHEIGHT+0.01 

        def gotoprofileconfig():
                controller.show_frame(pageArgs[10])
        button_profile = Button(self, text="Configure Profile", command=gotoprofileconfig, **button_options)

        button_profile.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## RF events search
        def gotoeventssearch():
                controller.show_frame(pageArgs[9])
        button_evsearch = Button(self, text="Configure Events Search", command=gotoeventssearch, **button_options)

        button_evsearch.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)
        
        ## RF filter
        RELY += RELHEIGHT+0.01 
        def gotofiltersettings():
                controller.show_frame(pageArgs[11])
        button_filter = Button(self, text="Set Filter", command=gotofiltersettings, **button_options)

        button_filter.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)
        
        ## RF filter
        def gotofplotsettings():
                controller.show_frame(pageArgs[12])
        button_filter = Button(self, text="Configure RF plot", command=gotofplotsettings, **button_options)

        button_filter.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)
        

        