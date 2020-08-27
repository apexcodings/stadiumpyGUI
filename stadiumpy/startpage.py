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

def startview(self, ttk, parent, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, PageGeoRegion, inp, image_name):
    
    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx

    topcanvas = tk.Canvas(self)
    topcanvas.config(bg='#ecebec')
    topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=9*RELHEIGHT )

    ## Startpage page
    stpg_button = ttk.Button(self, text="Start Page",
                        command=lambda: controller.show_frame(StartPage), style = 'W.TButton',state="disabled")
    stpg_button.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)


    ## Data enquiry page
    button4 = ttk.Button(self, text="Data Enquiry",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageDataEnquiry))
    button4.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    
    ## RF page
    button = ttk.Button(self, text="P-RF Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PagePRF))
    button.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## RF page
    button = ttk.Button(self, text="S-RF Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageSRF))
    button.place(relx=RELXS[3], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## SKS page
    button2 = ttk.Button(self, text="SKS Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageSKS))
    button2.place(relx=RELXS[4], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

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

    RELY0 = RELY
    ## Mode
    def toggle_mode():
        if button_mode['text'] == 'Automated':
            dictAdd = {'text':'Stepwise', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
            for key, value in dictAdd.items():
                button_mode[key]=value
        else:
            dictAdd = {'text':'Automated', 'bg':'#ADEFD1', 'fg': '#00203F'}
            for key, value in dictAdd.items():
                button_mode[key]=value

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

    button_mode = Button(self, text=stad_mode, command=toggle_mode, **button_options)

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

    def toggle_button(button_freshstart):
        if button_freshstart['text'] == 'True':
            dictAdd = {'text':'False', 'bg':'#E69A8D', 'fg': '#5F4B8B'}
            for key, value in dictAdd.items():
                button_freshstart[key]=value
        else:
            dictAdd = {'text':'True', 'bg':'#ADEFD1', 'fg': '#00203F'}
            for key, value in dictAdd.items():
                button_freshstart[key]=value


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


    
    

    # minlat = geoMinLatEntry.get()
    # maxlat = geoMaxLatEntry.get()
    # minlon = geoMinLonEntry.get()
    # maxlon = geoMaxLonEntry.get()
    # geoCoords = np.array([minlat, maxlat, minlon, maxlon])
    # coordFile = "regioninfo.npy"
    # np.save(coordFile,geoCoords)

    if os.path.exists(image_name):
        os.remove(image_name)



    def showMap():
        # minlat = geoMinLatEntry.get()
        # maxlat = geoMaxLatEntry.get()
        # minlon = geoMinLonEntry.get()
        # maxlon = geoMaxLonEntry.get()
        # res='i'
        # topo_data = '@earth_relief_01m'
        # geoCoords = np.array([minlat, maxlat, minlon, maxlon])
        # coordFile = "regioninfo.npy"
        # np.save(coordFile,geoCoords)
        # print("geoCoords",geoCoords)
        # plot_map(minlon,maxlon,minlat, maxlat,topo_data,res=res)
        # pagegeo = PageGeoRegion(parent,controller)
        # plotMap(pagegeo, ttk, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS)
        controller.show_frame(PageGeoRegion)

    RELY += RELHEIGHT+0.01
    button_plotmap = ttk.Button(self, text="ExploreMap", command=showMap)
    button_plotmap.place(relx=RELXS[4], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)