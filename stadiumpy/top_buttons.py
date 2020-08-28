
from stadiumpy.widgets import SFrame, Button

def display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=0):
    topbuttons_options = {"borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}
    ## Startpage page
    stpg_button = Button(self, text="Home",
                        command=lambda: controller.show_frame(pageArgs[0]))

    ## Data enquiry page
    dataenquiry_btn = Button(self, text="Data Enquiry",
                        command=lambda: controller.show_frame(pageArgs[1]))

    ## RF page
    prf_button = Button(self, text="RF Parameters",
                        command=lambda: controller.show_frame(pageArgs[2]))

    ## SKS page
    sks_button = Button(self, text="SKS Parameters",
                        command=lambda: controller.show_frame(pageArgs[3]))

    ## 
    ressum_button = Button(self, text="Results Summary",
                        command=lambda: controller.show_frame(pageArgs[4]))

    buttons = [stpg_button, dataenquiry_btn, prf_button, sks_button, ressum_button]
    for i in range(len(buttons)):
        if i==disabledBtn:
            buttons[i].configure(**topbuttons_options_selected)
        else:
            buttons[i].configure(**topbuttons_options)
        buttons[i].place(relx=RELXS[i], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
