"""
Everything related to page styling.
"""
from stadiumpy.font_properties import *
import platform

button_options_red = {'bg':'#E69A8D', 
                "fg":'#5F4B8B', 
                "borderless":1,
                'activebackground':('#AE0E36', '#D32E5E')
                }
button_options_green = {
            "bg":'#ADEFD1', 
            "fg":'#00203F', 
            "borderless":1,
            'activebackground':('#AE0E36', '#D32E5E')
            }
# button_options_nav = {
#             "bg":'#e67e22', 
#             "fg":'#00203F', 
#             "borderless":1,
#             'activebackground':('#AE0E36', '#D32E5E')
#             }
button_options_back = {
            "bg":'#3598dc', 
            "fg":'#00203F', 
            "borderless":1,
            'activebackground':('#AE0E36', '#D32E5E')
            }
button_options_nav = { "borderwidth":1, "font":('calibri', 16, 'bold'), "fg":"black"}


os_platform = platform.system()

if os_platform is "Darwin":
    topbuttons_options = {"borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}
elif os_platform is "Linux":
    topbuttons_options = {"borderwidth":1, "font":('calibri', 10, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 10, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}
else:
    topbuttons_options = {"borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}


def toggle_mode(button_mode):
    if button_mode['text'] == 'Automated':
        dictAdd = {'text':'Stepwise', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
        for key, value in dictAdd.items():
            button_mode[key]=value
    else:
        dictAdd = {'text':'Automated', 'bg':'#ADEFD1', 'fg': '#00203F'}
        for key, value in dictAdd.items():
            button_mode[key]=value

def toggle_PRF(button_mode, controller, pageArgs):
    controller.show_frame(pageArgs[6])


def toggle_SRF(button_mode, controller, pageArgs):
    controller.show_frame(pageArgs[2])


def toggle_button(button):
    if button['text'] == 'True':
        dictAdd = {'text':'False', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
        for key, value in dictAdd.items():
            button[key]=value
    else:
        dictAdd = {'text':'True', 'bg':'#ADEFD1', 'fg': '#00203F'}
        for key, value in dictAdd.items():
            button[key]=value


def button_init(hkappa_val):
    if not hkappa_val:
        frsttext = "False"
        button_options = button_options_red
    else:
        frsttext = "True"
        button_options = button_options_green
    return frsttext, button_options