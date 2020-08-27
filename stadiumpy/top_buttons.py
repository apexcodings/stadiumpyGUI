
from stadiumpy.widgets import SFrame, Button

def display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, disabledBtn=0):
    topbuttons_options = {"borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}

    ## Startpage page
    stpg_button = Button(self, text="Home",
                        command=lambda: controller.show_frame(StartPage))

    ## Data enquiry page
    dataenquiry_btn = Button(self, text="Data Enquiry",
                        command=lambda: controller.show_frame(PageDataEnquiry))

    ## RF page
    prf_button = Button(self, text="P-RF Parameters",
                        command=lambda: controller.show_frame(PagePRF))

    ## RF page
    srf_button = Button(self, text="S-RF Parameters",
                        command=lambda: controller.show_frame(PageSRF))

    ## SKS page
    sks_button = Button(self, text="SKS Parameters",
                        command=lambda: controller.show_frame(PageSKS))

    buttons = [stpg_button, dataenquiry_btn, prf_button, srf_button, sks_button]
    for i in range(5):
        if i==disabledBtn:
            buttons[i].configure(**topbuttons_options_selected)
        else:
            buttons[i].configure(**topbuttons_options)
        buttons[i].place(relx=RELXS[i], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
