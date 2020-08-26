import numpy as np
import tkinter as tk
from tkinter import ttk
# from tkinter import *
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL

from plot_geomap import plot_map
from PIL import ImageTk, Image
import os



def display_image(self,image_name, RELXS, RELY, RELHEIGHT, RELWIDTH): 
    print("Running display_image in plot_map_gui")           
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
    print("width-height:",width, height)
 
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

def plotMap(self, controller, StartPage, PageDataEnquiry, PagePRF, PageSRF, PageSKS, inp, image_name):
    print("Running plotMap function in plot_map_gui")

    # ## create main frame
    # main_frame = tk.Frame(self)
    # main_frame.pack(fill=BOTH, expand=1)

    ## create a canvas
    my_canvas = tk.Canvas(self)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    ## Scrollbar
    my_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    ## configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    ## Another frame inside canvas
    second_frame = tk.Frame(my_canvas)

    # add new frame to the window in the canvas
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")




    # minlat, maxlat, minlon, maxlon = [geoCoords[i] for i in range(4)]
    RELY = 0
    RELHEIGHT, RELWIDTH = 0.05, 0.2
    RELXS = np.linspace(0,1,6)
    drelx = 0.01
    RELXS[1:]= RELXS[1:]+drelx

    topcanvas = tk.Canvas(self)
    topcanvas.config(bg='#ecebec')
    topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=4.8*RELHEIGHT )

    ## Startpage page
    PageDataEnquiry_stpg_button = ttk.Button(self, text="Start Page",style = 'W.TButton',
                        command=lambda: controller.show_frame(StartPage))
    RELX1 = RELWIDTH+0.02
    PageDataEnquiry_stpg_button.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)


    ## Data enquiry page
    button4 = ttk.Button(self, text="Data Enquiry",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageDataEnquiry))
    RELX1 = RELWIDTH+0.02
    button4.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
    
    ## RF page
    button = ttk.Button(self, text="P-RF Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PagePRF))
    RELX1 += RELWIDTH+0.01
    button.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## RF page
    button = ttk.Button(self, text="S-RF Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageSRF))
    RELX1 += RELWIDTH+0.01
    button.place(relx=RELXS[3], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

    ## SKS page
    button2 = ttk.Button(self, text="SKS Parameters",style = 'W.TButton',
                        command=lambda: controller.show_frame(PageSKS))
    RELX1 += RELWIDTH+0.01
    button2.place(relx=RELXS[4], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)


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
    plotmapRELY = RELY

    ##
    RELY += RELHEIGHT+0.01
    geoMinLatEntry = ttk.Entry(self, width=10)
    geoMinLatEntry.insert(0,str(minlat))
    geoMinLatEntry.place(relx=RELXS[3]/2, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
    
    ##
    res='i'
    topo_data = '@earth_relief_01m'

    # canvasRELXS = RELXS
    # canvasRELY = RELY
    # canvasRELHEIGHT = RELHEIGHT
    # canvasRELWIDTH = RELWIDTH
    coordFile = "regioninfo.npy"
    geoCoords = np.load(coordFile)
    minlat, maxlat, minlon, maxlon = [geoCoords[i] for i in range(4)]
    if not os.path.exists(image_name):
        plot_map(minlon,maxlon,minlat, maxlat,topo_data,outputfile=image_name,res=res)


    def read_map(image_name):        
        print("Running display_image in plot_map_gui")   
        # bkimg_read = Image.open(background_image)
        geoMap_read = Image.open(image_name)
        maxheight = 450
        maxwidth = 720

        width, height = geoMap_read.size
        print("width-height from readmap",width, height)
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
        print("width-height:",width, height)
        return geoMap
 
    RELY += RELHEIGHT+0.01

    def image_on_canvas(image_name):
        geoMap = read_map(image_name)
        if geoMap.width()<1200:
            canvas = tk.Canvas(second_frame, width = geoMap.width(), height = geoMap.height())
            # canvas = tk.Canvas(self, width = geoMap.width(), height = geoMap.height(), relief=SUNKEN, bd=2)
            canvas.create_image(0, 0, anchor="nw", image=geoMap) 
            canvas.image = geoMap
            canvas.grid(row=3,column=0, pady=(200,10), padx=10, sticky="nsew")
            # canvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH )
        else:
            canvas=None
        return canvas
    canvas = image_on_canvas(image_name)

    def refreshMap(canvas):
        minlat = geoMinLatEntry.get()
        maxlat = geoMaxLatEntry.get()
        minlon = geoMinLonEntry.get()
        maxlon = geoMaxLonEntry.get()
        plot_map(minlon,maxlon,minlat, maxlat,topo_data,outputfile=image_name,res=res)
        canvas.delete("all")
        canvas = image_on_canvas(image_name)


    button_plotmap = ttk.Button(self, text="RefreshMap", command=lambda: refreshMap(canvas))
    button_plotmap.place(relx=RELXS[3], rely=plotmapRELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)
