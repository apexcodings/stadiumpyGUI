import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y

from PIL import ImageTk, Image
from stadiumpy.widgets import SFrame, Button

from stadiumpy.top_buttons import display_main_buttons
from stadiumpy.styles import button_options_red, button_options_green, toggle_mode, toggle_button, button_init

def prfview(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, adv_prf):
    

    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx

    # topcanvas = tk.Canvas(self)
    # topcanvas.config(bg='#ecebec')
    # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

    display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, disabledBtn=2)




    labHeadOptions = {"font":('calibri', 16, 'bold'), "anchor":"center"}
    label_options = {"font":('calibri', 12, 'normal')}
    ###########################################
    lbl1 = ttk.Label(self, text="Filenames:", **labHeadOptions)
    RELY += RELHEIGHT+0.01 
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)

    filename_vars = list(adv_prf['filenames'].keys())
    filename_vals = list(adv_prf['filenames'].values())
    kk=0

    halfCellX = (RELXS[2]-RELXS[1])/2
    while kk<len(filename_vars):
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=filename_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,filename_vals[kk])
        kk+=1

        ##
        lbl1 = ttk.Label(self, text=filename_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,filename_vals[kk])
        kk+=1

    ###########################################

    lbl1 = ttk.Label(self, text=r'Crustal Thickness (h) - Vp/Vs (kappa)', **labHeadOptions)
    RELY += RELHEIGHT+0.01 
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


    ##
    hkappa_vars = list(adv_prf['h_kappa_settings'].keys())
    hkappa_vals = list(adv_prf['h_kappa_settings'].values())

    RELY += RELHEIGHT+0.01 #new line
    kk = 0
    lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    entry1 = ttk.Entry(self)
    entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
    entry1.insert(0,hkappa_vals[kk])

    ##


    kk+=1
    lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
    lbl1.place(relx=RELXS[2]+halfCellX+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


    frsttext, button_options = button_init(hkappa_vals[kk])
    button_hkappa1 = Button(self, 
            text=frsttext,
            command=lambda: toggle_button(button_hkappa1),
            **button_options
            )
    button_hkappa1.place(relx=RELXS[3]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


    kk+=1
    lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
    lbl1.place(relx=RELXS[3]+halfCellX+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


    frsttext, button_options = button_init(hkappa_vals[kk])
    button_hkappa2 = Button(self, 
            text=frsttext,
            command=lambda: toggle_button(button_hkappa2),
            **button_options
            )
    button_hkappa2.place(relx=RELXS[4]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


    ###########################################

    lbl1 = ttk.Label(self, text=r'RF Profile Configure', **labHeadOptions)
    lbl1.configure(anchor="center")
    RELY += RELHEIGHT+0.01 
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


    ##
    hkappa_vars = list(adv_prf['rf_profile_settings'].keys())
    hkappa_vals = list(adv_prf['rf_profile_settings'].values())

    RELY += RELHEIGHT+0.01 #new line
    kk = 0
    lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    entry1 = ttk.Entry(self)
    entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    entry1.insert(0,hkappa_vals[kk])

    ##

    kk+=1
    lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
    lbl1.place(relx=RELXS[1]+halfCellX+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)


    entry1 = ttk.Entry(self)
    entry1.insert(0,hkappa_vals[kk])
    entry1.place(relx=RELXS[2]+drelx+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


    kk+=1
    lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
    lbl1.place(relx=RELXS[3]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)


    entry1 = ttk.Entry(self)
    entry1.insert(0,hkappa_vals[kk])
    entry1.place(relx=RELXS[4]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

    