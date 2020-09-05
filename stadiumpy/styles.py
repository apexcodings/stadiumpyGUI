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

button_options = button_options_back 
fontDict = {"font":('calibri', 12, 'bold')}
button_options_BACK = {**button_options, **fontDict}

labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
label_options = {"font":('calibri', 12, 'normal')}

os_platform_styles = platform.system()

if os_platform_styles == "Darwin":
    topbuttons_options = {"borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}
    system_styles = {"font" : fontOSX,  "borderwidth" : '2', "background":"#c8ccc9"}

elif os_platform_styles == "Linux":
    topbuttons_options = {"borderwidth":1, "font":('calibri', 10, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 10, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}
    system_styles = {"font" : fontLinuX,  "borderwidth" : '2', "background":"#c8ccc9"}
else:
    topbuttons_options = {"borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised"}
    topbuttons_options_selected = { "borderwidth":1, "font":('calibri', 16, 'bold'), "relief":"raised", "bg":"#a1a3a6", "fg":"white"}
    system_styles = {"font" : fontOSX,  "borderwidth" : '2', "background":"#c8ccc9"}


def toggle_mode(button_mode):
    if button_mode['text'] == 'Automated':
        dictAdd = {'text':'Stepwise', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
        for key, value in dictAdd.items():
            button_mode[key]=value
        stepwiseBtnState = "disabled"
    else:
        dictAdd = {'text':'Automated', 'bg':'#ADEFD1', 'fg': '#00203F'}
        for key, value in dictAdd.items():
            button_mode[key]=value
        stepwiseBtnState = "normal"

def toggle_PRF(button_mode, controller, pageArgs):
    controller.show_frame(pageArgs[6])


def toggle_SRF(button_mode, controller, pageArgs):
    controller.show_frame(pageArgs[2])


def toggle_button(button):
    if button['text'] == 'Yes':
        dictAdd = {'text':'No', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
        for key, value in dictAdd.items():
            button[key]=value
        output = 1 
    else:
        dictAdd = {'text':'Yes', 'bg':'#ADEFD1', 'fg': '#00203F'}
        for key, value in dictAdd.items():
            button[key]=value
        output = 0
    return output

def get_toggle_output(button):
    if button['text'] == 'Yes':
        output = 1 
    else:
        output = 0
    return output

def get_toggle_output_mode(button):
    if button['text'] == 'Automated':
        output = 1 
    else:
        output = 0
    return output

import ast
def convert_input(value):
    try:
        if isinstance(value, str):
            try:
                output = ast.literal_eval(value)
            except:
                output = value

        else:
            output = ast.literal_eval(value)
    except:
        output = value
    return output


def button_init(hkappa_val):
    if not hkappa_val:
        frsttext = "No"
        button_options = button_options_red
    else:
        frsttext = "Yes"
        button_options = button_options_green
    return frsttext, button_options


import os

def list_files(startpath):
    outputLists = []
    for root, dirs, files in os.walk(startpath):
        rootCheck = root.replace(startpath, '')
        if not rootCheck.startswith('.') and not rootCheck.startswith('__'):
            # print('{}{}/'.format(indent, os.path.basename(root)))
            if not os.path.basename(root).startswith('__'):
                level = root.replace(startpath, '').count(os.sep)
                indent = '-> ' * 8 * (level)
                outputLists.append('{}{}/'.format(indent, os.path.basename(root)))
                subindent = '-  ' * 8 * (level + 1)
                for f in files:
                    if not f.startswith('.'):
                        outputLists.append('{}{}'.format(subindent, f))
    return outputLists