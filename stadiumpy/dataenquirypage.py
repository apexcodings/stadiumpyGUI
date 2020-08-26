import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y

from PIL import ImageTk, Image


def dataenquiry(self, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp):
    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx


    ## Startpage page
    PageDataEnquiry_stpg_button = ttk.Button(self, text="Start Page",style = 'W.TButton',
                        command=lambda: controller.show_frame(StartPage))
    RELX1 = RELWIDTH+0.02
    PageDataEnquiry_stpg_button.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## Data enquiry page
    PageDataEnquiry_dten_button = ttk.Button(self, text="Data Enquiry",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageDataEnquiry), state="disabled")
    RELX1 = RELWIDTH+0.02
    PageDataEnquiry_dten_button.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## RF page
    PageDataEnquiry_prf_button = ttk.Button(self, text="P-RF Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PagePRF))
    RELX1 += RELWIDTH+0.01
    PageDataEnquiry_prf_button.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## SRF page
    PageDataEnquiry_srf_button = ttk.Button(self, text="S-RF Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageSRF))
    RELX1 += RELWIDTH+0.01
    PageDataEnquiry_srf_button.place(relx=RELXS[3], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## SKS page
    PageDataEnquiry_sks_button = ttk.Button(self, text="SKS Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageSKS))
    RELX1 += RELWIDTH+0.01
    PageDataEnquiry_sks_button.place(relx=RELXS[4], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)