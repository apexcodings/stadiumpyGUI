import numpy as np
import tkinter as tk
from tkinter import ttk
# from tkinter import *
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL, RIDGE, GROOVE

from stadiumpy.plot_geomap import plot_map
from PIL import ImageTk, Image
import os
from tkinter import messagebox
import stadiumpy as stpy
# from .tkmacosx import tkmacosx
from stadiumpy.widgets import SFrame, Button
# from tkmacosx import SFrame, Button

from stadiumpy.top_buttons import display_main_buttons

def display_image(self,image_name, RELXS, RELY, RELHEIGHT, RELWIDTH): 
    # print("Running display_image in plot_map_gui")           
    geoMap_read = Image.open(image_name)
    maxheight = 300

    width, height = geoMap_read.size
    hpercent = (maxheight/float(geoMap_read.size[1]))
    # wpercent = (maxwidth/float(geoMap_read.size[0]))
    wsize = int((float(geoMap_read.size[0])*float(hpercent)))
    # hsize = int((float(geoMap_read.size[1])*float(wpercent)))
    geoMap_read = geoMap_read.resize((wsize,maxheight), Image.ANTIALIAS)
    # geoMap_read = geoMap_read.resize((maxwidth,hsize), Image.ANTIALIAS)

    geoMap = ImageTk.PhotoImage(geoMap_read)
    # print("width-height:",width, height)
 
    RELY += RELHEIGHT+0.01
        
    canvas = tk.Canvas(self, width = geoMap.width(), height = geoMap.height(), relief=SUNKEN, bd=2)
    canvas.create_image(0, 0, anchor=N+W, image=geoMap) 
    canvas.image = geoMap
    canvas.pack(side="bottom", expand = True)
    # canvas.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT*20, relwidth=4*(RELWIDTH))
    return canvas

def startpagebtn(controller, StartPage):
    # canvas.delete("all")
    controller.show_frame(StartPage)

def plotMap(self, ttk, parent, controller, inp, image_name, *pageArgs):
    # print("Running plotMap function in plot_map_gui")

    main_frame = tk.Frame(self)
    main_frame.pack(fill=BOTH, expand=1)

    second_frame = SFrame(main_frame, scrollbarwidth=10,height=600, mousewheel=True)
    # second_frame = SFrame(main_frame, scrollbarwidth=10,height=600, mousewheel=True)
    second_frame.pack(pady=20,side=LEFT, fill=BOTH, expand=1, anchor="nw")


    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx

    topcanvas = tk.Canvas(self)
    topcanvas.config(bg='#ecebec')
    topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

    display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=None)



    #Geographic Region
    ## Plot map
    # image_name = "region-plot.png"
    minlon, maxlon = inp['mnlong'], inp['mxlong']
    minlat, maxlat = inp['mnlat'], inp['mxlat']

    # background_image="blackBackground.png"
    # bkimg_read = Image.open(background_image)

    lbl1 = ttk.Label(self, text="Region:")
    lbl1.configure(anchor="center")
    RELY += RELHEIGHT

    

    RELY += 0.01
    RELYmapwidth = RELY
    lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT*3, relwidth=RELWIDTH)

    geoMaxLatEntry = ttk.Entry(self, width=10)
    geoMaxLatEntry.insert(0,str(maxlat))
    geoMaxLatEntry.place(relx=RELXS[3]/2, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)


    RELY += RELHEIGHT+0.01
    geoMinLonEntry = ttk.Entry(self, width=10)
    geoMaxLonEntry = ttk.Entry(self, width=10)
    geoMinLonEntry.place(relx=RELXS[2]/2, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    geoMaxLonEntry.place(relx=RELXS[4]/2, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)



    geoMinLonEntry.insert(0,str(minlon))
    geoMaxLonEntry.insert(0,str(maxlon))
    

    ##
    RELY += RELHEIGHT+0.01
    geoMinLatEntry = ttk.Entry(self, width=10)
    geoMinLatEntry.insert(0,str(minlat))
    geoMinLatEntry.place(relx=RELXS[3]/2, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)

    ## dropdown menu for res
    resSel = tk.StringVar()
    resSel.set("intermediate")
    res_drop = tk.OptionMenu(self,resSel, "full", "high", "intermediate", "low", "crude")

    RELY += RELHEIGHT+0.01
    reslabel = ttk.Label(self, text="CoastRes:", relief=RIDGE)
    reslabel.configure(anchor="center")
    reslabel.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    res_drop.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    
    ##
    resDict = {"full":"f", "high":"h", "intermediate": "i", "low": "l", "crude": "c"}
    res=resDict[resSel.get()]

    ## dropdown menu for topography
    RELY += RELHEIGHT+0.01
    topoSel = tk.StringVar()
    topoOptions = ['01d', '30m', '20m', '15m', '10m', '06m', '05m', '04m', '03m', '02m', '01m', '30s', '15s']
    topoSel.set(topoOptions[10])
    topo_drop = tk.OptionMenu(self,topoSel, *topoOptions)

    topolabel = ttk.Label(self, text="ReliefRes:", relief=RIDGE)
    topolabel.configure(anchor="center")
    topolabel.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    topo_drop.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    
    ##
    topo_data="@earth_relief_" + topoSel.get()

    plotmapRELY = RELY


    mapwidthLabel = ttk.Label(self, text="MapWidth:", relief=RIDGE)
    mapwidthLabel.configure(anchor="center")
    mapwidthLabel.place(relx=RELXS[3], rely=RELYmapwidth, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    mapWidth = ttk.Entry(self, width=10)
    mapWidth.insert(0,"5c")
    mapWidth.place(relx=RELXS[3]+RELWIDTH/2, rely=RELYmapwidth, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    
    ##mapframe
    RELYmapframe = RELYmapwidth+RELHEIGHT+0.01
    mapframeLabel = ttk.Label(self, text="MapFrame:", relief=RIDGE)
    mapframeLabel.configure(anchor="center")
    mapframeLabel.place(relx=RELXS[3], rely=RELYmapframe, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    mapFrame = ttk.Entry(self, width=10)
    mapFrame.insert(0,"f")
    mapFrame.place(relx=RELXS[3]+RELWIDTH/2, rely=RELYmapframe, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    


    # coordFile = os.path.join(stpy.__path__[0], 'regioninfo.npy')
    # # coordFile = "regioninfo.npy"
    # geoCoords = np.load(coordFile)
    # minlat, maxlat, minlon, maxlon = [geoCoords[i] for i in range(4)]
    if not os.path.exists(image_name):
        plot_map(minlon,maxlon,minlat, maxlat,topo_data,outputfile=image_name,res=res)


    def read_map(image_name):        
        # print("Running display_image in plot_map_gui")   
        # bkimg_read = Image.open(background_image)
        geoMap_read = Image.open(image_name)
        # maxheight = 450
        maxwidth = 720

        width, height = geoMap_read.size
        # print("width-height from readmap",width, height)
        # if width>maxwidth:
        #     wpercent = (maxwidth/float(geoMap_read.size[0]))
        #     hsize = int((float(geoMap_read.size[1])*float(wpercent)))
        #     geoMap_read = geoMap_read.resize((maxwidth,hsize), Image.ANTIALIAS)
        # else:
        #     hpercent = (maxheight/float(geoMap_read.size[1]))
        #     wsize = int((float(geoMap_read.size[0])*float(hpercent)))
        #     geoMap_read = geoMap_read.resize((wsize,maxheight), Image.ANTIALIAS)
        # hpercent = (maxheight/float(geoMap_read.size[1]))
        # wsize = int((float(geoMap_read.size[0])*float(hpercent)))
        # geoMap_read = geoMap_read.resize((wsize,maxheight), Image.ANTIALIAS)
        wpercent = (maxwidth/float(geoMap_read.size[0]))
        hsize = int((float(geoMap_read.size[1])*float(wpercent)))
        geoMap_read = geoMap_read.resize((maxwidth,hsize), Image.ANTIALIAS)

        width, height = geoMap_read.size
        # bkimg_read = bkimg_read.resize((width, height), Image.ANTIALIAS)
        # bkimg = ImageTk.PhotoImage(bkimg_read)

        geoMap = ImageTk.PhotoImage(geoMap_read)
        # print("width-height:",width, height)
        return geoMap
 
    RELY += RELHEIGHT+0.01

    def image_on_canvas(image_name):
        geoMap = read_map(image_name)
        if geoMap.width()<1200:
            canvas = tk.Canvas(second_frame, width = geoMap.width(), height = geoMap.height())
            # canvas = tk.Canvas(self, width = geoMap.width(), height = geoMap.height(), relief=SUNKEN, bd=2)
            canvas.create_image(0, 0, anchor="nw", image=geoMap) 
            canvas.image = geoMap
            canvas.grid(row=3,column=0, pady=(260,10), padx=10, sticky="nsew")
            # canvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH )
        else:
            canvas=None
        return canvas
    canvas = image_on_canvas(image_name)

    def refreshMap(canvas):
        res=resDict[resSel.get()]
        topo_data="@earth_relief_" + topoSel.get()
        mapwidth = mapWidth.get()
        mapframe = mapFrame.get()
        minlat = geoMinLatEntry.get()
        maxlat = geoMaxLatEntry.get()
        minlon = geoMinLonEntry.get()
        maxlon = geoMaxLonEntry.get()
        try:
            plot_map(minlon,maxlon,minlat, maxlat,topo_data,outputfile=image_name,res=res, width=mapwidth, frame=mapframe)
            canvas.delete("all")
        except:
            messagebox.showwarning("Illegal Input","Please check the inputs")
        canvas = image_on_canvas(image_name)


    button_plotmap = ttk.Button(self, text="RefreshMap", command=lambda: refreshMap(canvas))
    button_plotmap.place(relx=RELXS[4], rely=plotmapRELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)