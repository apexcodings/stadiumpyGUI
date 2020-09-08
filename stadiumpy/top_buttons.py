"""
Setting the primary top button of the GUI
"""
import numpy as np

from stadiumpy.widgets import SFrame, Button
from stadiumpy.styles import topbuttons_options, topbuttons_options_selected

def display_main_buttons(self,controller, *pageArgs, disabledBtn=0):
    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    
    ## Startpage page
    stpg_button = Button(self, text="Home",
                        command=lambda: controller.show_frame(pageArgs[0]))

    ## Data enquiry page
    dataenquiry_btn = Button(self, text="Data Enquiry",
                        command=lambda: controller.show_frame(pageArgs[1]),
                        state="disabled")

    ## RF page
    prf_button = Button(self, text="Receiver Functions",
                        command=lambda: controller.show_frame(pageArgs[2]))

    ## SKS page
    sks_button = Button(self, text="Shear-wave Splitting",
                        command=lambda: controller.show_frame(pageArgs[3]),
                        state="disabled")

    ## 
    projdir_button = Button(self, text="Project Directory",
                        command=lambda: controller.show_frame(pageArgs[4]))

    buttons = [stpg_button, dataenquiry_btn, prf_button, sks_button, projdir_button]
    for i in range(len(buttons)):
        if i==disabledBtn:
            buttons[i].configure(**topbuttons_options_selected)
        else:
            buttons[i].configure(**topbuttons_options)
        buttons[i].place(relx=RELXS[i], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        
    return RELXS, RELY, RELHEIGHT, RELWIDTH, drelx
