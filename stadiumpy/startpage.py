import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL, RIDGE, GROOVE

from stadiumpy.plot_geomap import plot_map
from PIL import ImageTk, Image
# from stadiumpy_gui import PageGeoRegion
from stadiumpy.plot_map_gui import plotMap
import os
# from stadiumpy_gui import mapImage
import stadiumpy as stpy

from stadiumpy.widgets import SFrame, Button
from stadiumpy.top_buttons import display_main_buttons
from stadiumpy.styles import button_options_red, button_options_green, toggle_mode, toggle_button
# from stadiumpy.stadiumpy import pageArgs


def startview(self, ttk, parent, controller, inp, image_name, *pageArgs):
    
    main_frame = tk.Frame(self)
    main_frame.pack(fill=BOTH, expand=1)

    second_frame = SFrame(main_frame, scrollbarwidth=10,height=600, mousewheel=True)
    second_frame.pack(pady=20,side=LEFT, fill=BOTH, expand=1, anchor="nw")


    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx

    topcanvas = tk.Canvas(self)
    topcanvas.config(bg='#ecebec')
    topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )


    display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=0)


    RELY0 = RELY
    ## Mode

    lbl1 = ttk.Label(self, text="Mode:")
    lbl1.configure(anchor="center")
    RELY += RELHEIGHT+0.01 
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    if inp['mode']=="Automated":
        stad_mode = "Automated"
        button_options = button_options_green
    else:
        stad_mode = "Stepwise"
        button_options = button_options_red

    button_mode = Button(self, text=stad_mode, command=lambda: toggle_mode(button_mode), **button_options)

    button_mode.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)



    ## fresh start
    RELY += RELHEIGHT+0.01 
    lbl1 = ttk.Label(self, text="FreshStart:")
    lbl1.configure(anchor="center")
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    if not inp['fresh_start']:
        frsttext = "False"
        button_options = button_options_red
    else:
        frsttext = "True"
        button_options = button_options_green
    


    button_freshstart = Button(self, 
            text=frsttext,
            command=lambda: toggle_button(button_freshstart),
            **button_options
            )
    # button_freshstart = ttk.Button(self, text=frsttext,command=lambda: toggle_button(button_freshstart))

    button_freshstart.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)



    ## Project name
    lbl1 = ttk.Label(self, text="ProjectName:")
    lbl1.configure(anchor="center")
    RELY += RELHEIGHT+0.01 
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    entry1 = ttk.Entry(self)
    entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    entry1.insert(0,inp['project_name'])


    ## Summary file name
    RELY += RELHEIGHT+0.01
    lbl1 = ttk.Label(self, text="SummaryFile:")
    lbl1.configure(anchor="center")
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    entry1 = ttk.Entry(self)
    entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    entry1.insert(0,inp['summary_file'])




    RELY = RELY0
    RELY += RELHEIGHT+0.01
    lbl1 = ttk.Label(self, text="Selected Methods", relief=RIDGE)
    lbl1.configure(anchor="center")
    lbl1.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    RELY += RELHEIGHT+0.01

    # makeRF-P
    makeRF_lab = ttk.Label(self, text="P-RF:")
    makeRF_lab.configure(anchor="center")
    makeRF_lab.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)

    
    if not inp['makeRF']:
        makeRFtext = "False"
        button_options = button_options_red
    else:
        makeRFtext = "True"
        button_options = button_options_green

    button_makerf = Button(self, 
        text=makeRFtext, 
        command=lambda: toggle_button(button_makerf),
        **button_options
        )
    button_makerf.place(relx=RELXS[2]+(RELXS[2]-RELXS[1])/2+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

    # makeRF-S
    RELY += RELHEIGHT+0.01
    makeSRF_lab = ttk.Label(self, text="S-RF:")
    makeSRF_lab.configure(anchor="center")
    makeSRF_lab.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)

    if not inp['makeSRF']:
        makeSRFtext = "False"
        button_options = button_options_red
    else:
        makeSRFtext = "True"
        button_options = button_options_green
    
    button_makesrf = Button(self, 
        text=makeSRFtext, 
        command=lambda: toggle_button(button_makesrf),
        **button_options
        )
    # button_makesrf = ttk.Button(self, text=makeSRFtext, command=lambda: toggle_button(button_makesrf))
    button_makesrf.place(relx=RELXS[2]+(RELXS[3]-RELXS[2])/2+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


    # makeSKS
    RELY += RELHEIGHT+0.01
    makeSKS_lab = ttk.Label(self, text="SKS:")
    makeSKS_lab.configure(anchor="center")
    makeSKS_lab.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)

    if not inp['makeSKS']:
        makeSKStext = "False"
        button_options = button_options_red
    else:
        makeSKStext = "True"
        button_options = button_options_green


    button_makesks = Button(self, 
        text=makeSKStext, 
        command=lambda: toggle_button(button_makesks),
        **button_options
        )
    button_makesks.place(relx=RELXS[2]+(RELXS[3]-RELXS[2])/2+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

    #Geographic Region
    RELY=RELY0
    ## Plot map
    # image_name = "region-plot.png"
    minlon, maxlon = inp['mnlong'], inp['mxlong']
    minlat, maxlat = inp['mnlat'], inp['mxlat']


    lbl1 = ttk.Label(self, text="Geographic Region", relief=RIDGE)
    lbl1.configure(anchor="center")
    RELY += RELHEIGHT+0.01
    lbl1.place(relx=RELXS[3], rely=RELY, relheight=RELHEIGHT, relwidth=2*RELWIDTH)


    RELY += RELHEIGHT+0.01
    geoMaxLatEntry = ttk.Entry(self, width=10)
    geoMaxLatEntry.insert(0,str(maxlat))
    geoMaxLatEntry.place(relx=RELXS[3]+1.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)


    RELY += RELHEIGHT+0.01
    geoMinLonEntry = ttk.Entry(self, width=10)
    geoMaxLonEntry = ttk.Entry(self, width=10)
    geoMinLonEntry.place(relx=RELXS[3]+0.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    geoMaxLonEntry.place(relx=RELXS[4]+0.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)



    geoMinLonEntry.insert(0,str(minlon))
    geoMaxLonEntry.insert(0,str(maxlon))
    # plotmapRELY = RELY

    # ##
    RELY += RELHEIGHT+0.01
    geoMinLatEntry = ttk.Entry(self, width=10)
    geoMinLatEntry.insert(0,str(minlat))
    geoMinLatEntry.place(relx=RELXS[3]+1.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)


    
    

    if os.path.exists(image_name):
        os.remove(image_name)



    def showMap():
        controller.show_frame(pageArgs[5])

    RELY += RELHEIGHT+0.01
    button_plotmap = ttk.Button(self, text="ExploreMap", command=showMap)
    button_plotmap.place(relx=RELXS[4], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)
    print(RELHEIGHT)

    RELY += RELHEIGHT+0.01
    listbox = tk.Listbox(self)
    listbox.place(relx=RELXS[0], rely=RELY, relheight=13*RELHEIGHT, relwidth=5*RELWIDTH)
    for jj in range(500):
        listbox.insert(0, f"test {jj}")
        # listbox.insert(tk.END, f"test {jj}")