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


def toggle_mode(button_mode):
    if button_mode['text'] == 'Automated':
        dictAdd = {'text':'Stepwise', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
        for key, value in dictAdd.items():
            button_mode[key]=value
    else:
        dictAdd = {'text':'Automated', 'bg':'#ADEFD1', 'fg': '#00203F'}
        for key, value in dictAdd.items():
            button_mode[key]=value


def toggle_button(button):
    if button['text'] == 'True':
        dictAdd = {'text':'False', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
        for key, value in dictAdd.items():
            button[key]=value
    else:
        dictAdd = {'text':'True', 'bg':'#ADEFD1', 'fg': '#00203F'}
        for key, value in dictAdd.items():
            button[key]=value