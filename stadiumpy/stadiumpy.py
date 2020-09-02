"""
Wrapper for the stadiumpy GUI
"""
import tkinter as tk
from tkinter import ttk
# from tkinter import filedialog, Text
import yaml, os
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL, RIDGE, GROOVE
from tkinter.ttk import Frame, Style
import numpy as np

from stadiumpy.page_control import PageControl
# from stadiumpy.plot_map_gui import plotMap
from stadiumpy.font_properties import *
import platform
import stadiumpy as stdpy
from stadiumpy.widgets import SFrame, Button
from stadiumpy.top_buttons import display_main_buttons
from stadiumpy.styles import button_options_red, button_options_green, toggle_mode, toggle_button, button_init, toggle_PRF, button_options_nav, button_options_back

from stadiumpy.plot_geomap import plot_map
from PIL import ImageTk, Image
from tkinter import messagebox
print("Hello from", __name__)

cachedirec=".cache"
if not os.path.exists(cachedirec):
    os.makedirs(cachedirec, exist_ok=True)

image_name = os.path.join('.cache', 'region-plot.png')

# read inputYAML
inp_file_yaml = os.path.join(stdpy.__path__[0], 'settings', 'input_file.yaml')
adv_prf_yaml = os.path.join(stdpy.__path__[0], 'settings', 'advancedRF.yaml')
# inp_file_yaml = 'settings/input_file.yaml'

with open(inp_file_yaml) as f:
    inp = yaml.load(f, Loader=yaml.FullLoader)


with open(adv_prf_yaml) as f:
    adv_prf = yaml.load(f, Loader=yaml.FullLoader)




class stadiumpyMain(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "STADIUMpy")
        tk.Tk.wm_geometry(self, "800x700+300+300")
        # tk.Tk.wm_resizable(self, 0, 0) #fixed window size
        tk.Tk.wm_minsize(self, 800, 700) 
        style = Style()
        style.theme_use("default")

        os_platform = platform.system()
        if os_platform is "Darwin":
            style.configure('W.TButton', font = fontOSX,  borderwidth = '2', background="#c8ccc9")
        elif os_platform is "Linux":
            style.configure('W.TButton', font = fontLinuX,  borderwidth = '2', background="#c8ccc9")
        else:
            style.configure('W.TButton', font = fontOSX,  borderwidth = '2', background="#c8ccc9")



        ## style for all buttons
        # style.configure('TButton', font = ('calibri', 16, 'bold'),  borderwidth = '2') 
        
        ## TOP frame
        container = tk.Frame(self, relief=RAISED, borderwidth=1)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        
        stadium_pages = (StartPage, PageDataEnquiry, PageRF, PageSKS, ResultsSummary, PageGeoRegion,
         PageSRF, PRF_filenames, PRF_hkappa, PRF_eventsSearch, PRF_profileconfig,
         PRF_filter, PRF_display)
        # stadium_pages = (StartPage, PageRF, PageSRF, PageDataEnquiry, PageSKS, PageControl, PageGeoRegion,
        #     ResultsSummary, PRF_filenames, PRF_hkappa, PRF_eventsSearch, PRF_profileconfig,
        #     PRF_filter, PRF_display)
        for F in stadium_pages:

            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        ## Bottom frame
        container2 = tk.Frame(self, relief=RAISED, borderwidth=2)
        container2.pack(side="bottom",fill="both", expand=True)

        closeButton = ttk.Button(container2, text="Close", command=self._quit,style = 'W.TButton')
        closeButton.pack(side="right", padx=5, pady=5)

        def runStadiumpy():
            print("Run Stadiumpy")
            print(self.frames[PRF_filenames].getOutput())
            # print(self.frames[PRF_filenames].outputDict)

            # out = PRF_filenames.get_output()
            # out = prf_filename(self, ttk, parent, controller, adv_prf, *pageArgsOut())
            # print(out)

        runButton = ttk.Button(container2,style = 'W.TButton', text="Run", command=runStadiumpy)
        runButton.pack(side="left", padx=5, pady=5)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def _quit(self):
        root = tk.Tk()
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent


##############################################################################################
def pageArgsOut():
    # pageArgs = (StartPage, PageControl)
    pageArgs = (StartPage, PageDataEnquiry, PageRF, PageSKS, ResultsSummary, PageGeoRegion,
         PageSRF, PRF_filenames, PRF_hkappa, PRF_eventsSearch, PRF_profileconfig,
         PRF_filter, PRF_display)
    return pageArgs


##############################################################################################
class StartPage(tk.Frame):
    """
    This script for the startpage (homepage) of the stadiumpy. This can be used to set the main parameters of
    the software run. It can also be use to access other pages including results and computations.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        pageArgs = pageArgsOut()

        main_frame = tk.Frame(self)
        main_frame.pack(fill=BOTH, expand=1)

        second_frame = SFrame(main_frame, scrollbarwidth=10,height=600, mousewheel=True)
        second_frame.pack(pady=20,side=LEFT, fill=BOTH, expand=1, anchor="nw")


        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx

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

##############################################################################################

## P - Receiver Functions
class PageRF(tk.Frame):
    """
    This page is to set the parameters for the P-receiver functions of the stadiumpy
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()

        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "Go to S-RF"
        button_options = button_options_nav 
        fontDict = {"font":('calibri', 16, 'bold')}
        button_options = {**button_options, **fontDict}

        fontDictSecondary = {"font":('calibri', 12, 'bold')}
        button_optionsSecondary = {**button_options_back, **fontDictSecondary}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}

        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        button_mode = Button(self, text=stad_mode, command=lambda: toggle_PRF(button_mode, controller, pageArgs), **button_optionsSecondary)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ## filenames button
        RELY += RELHEIGHT+0.01 
        def gotofilenameprf():
                controller.show_frame(pageArgs[7])
        button_filename = Button(self, text="Set File Names", command=gotofilenameprf, **button_options)

        button_filename.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## set h kappa
        def gotohkappaprf():
                controller.show_frame(pageArgs[8])
        button_filename = Button(self, text="Set H-Kappa", command=gotohkappaprf, **button_options)

        button_filename.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)

        ## RF profile config
        RELY += RELHEIGHT+0.01 

        def gotoprofileconfig():
                controller.show_frame(pageArgs[10])
        button_profile = Button(self, text="Configure Profile", command=gotoprofileconfig, **button_options)

        button_profile.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## RF events search
        def gotoeventssearch():
                controller.show_frame(pageArgs[9])
        button_evsearch = Button(self, text="Configure Events Search", command=gotoeventssearch, **button_options)

        button_evsearch.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)
        
        ## RF filter
        RELY += RELHEIGHT+0.01 
        def gotofiltersettings():
                controller.show_frame(pageArgs[11])
        button_filter = Button(self, text="Set Filter", command=gotofiltersettings, **button_options)

        button_filter.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)
        
        ## RF filter
        def gotofplotsettings():
                controller.show_frame(pageArgs[12])
        button_filter = Button(self, text="Configure RF plot", command=gotofplotsettings, **button_options)

        button_filter.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)


##############################################################################################


# S-RF
class PageSRF(tk.Frame):
    """
    This page is to set the parameters for the S-receiver functions of the stadiumpy
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "Go to P-RF"
        button_options = button_options_nav 
        fontDict = {"font":('calibri', 16, 'bold')}
        button_options = {**button_options, **fontDict}

        fontDictSecondary = {"font":('calibri', 12, 'bold')}
        button_optionsSecondary = {**button_options_back, **fontDictSecondary}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        # label_options = {"font":('calibri', 12, 'normal')}
            
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="S-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        button_mode = Button(self, text=stad_mode, command=lambda: toggle_SRF(button_mode, controller, pageArgs), **button_optionsSecondary)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)
##############################################################################################


class PageDataEnquiry(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=1)
        
##############################################################################################

class PageSKS(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=3)

##############################################################################################


class PageGeoRegion(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        main_frame = tk.Frame(self)
        main_frame.pack(fill=BOTH, expand=1)

        second_frame = SFrame(main_frame, scrollbarwidth=10,height=600, mousewheel=True)
        # second_frame = SFrame(main_frame, scrollbarwidth=10,height=600, mousewheel=True)
        second_frame.pack(pady=20,side=LEFT, fill=BOTH, expand=1, anchor="nw")


        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx

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
        

        if not os.path.exists(image_name):
            plot_map(minlon,maxlon,minlat, maxlat,topo_data,outputfile=image_name,res=res)


        def read_map(image_name):        
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
        
##############################################################################################
class ResultsSummary(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=4)


##############################################################################################

class PRF_filenames(tk.Frame):
    """
    tweak the filenames for the P-receiver functions
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2

        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
            
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
            controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ###########################################
        lbl1 = ttk.Label(self, text="Filenames:", **labHeadOptions, relief=RIDGE)
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)

        filename_vars = list(adv_prf['filenames'].keys())
        filename_vals = list(adv_prf['filenames'].values())
        kk=0
        self.outputDict = {}
        while kk<len(filename_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=filename_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

            entry1 = ttk.Entry(self)
            entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
            entry1.insert(0,filename_vals[kk])
            self.outputDict[filename_vars[kk]] = entry1
            kk+=1

            ##
            lbl1 = ttk.Label(self, text=filename_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

            entry1 = ttk.Entry(self)
            entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
            entry1.insert(0,filename_vals[kk])
            self.outputDict[filename_vars[kk]] = entry1
            kk+=1

    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            outputResult[key] = value.get()
        return outputResult
            

        # print(self.outputDict)


##############################################################################################
class PRF_hkappa(tk.Frame):
    """
    tweak the h-kappa settings for the P-receiver functions
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
            
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
            controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ###########################################

        lbl1 = ttk.Label(self, text=r'Crustal Thickness (h) - Vp/Vs (kappa)', **labHeadOptions, relief=RIDGE)
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ##
        hkappa_vars = list(adv_prf['h_kappa_settings'].keys())
        hkappa_vals = list(adv_prf['h_kappa_settings'].values())

        RELY += RELHEIGHT+0.01 #new line
        kk = 0
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,hkappa_vals[kk])

        ##


        kk+=1
        RELY += RELHEIGHT+0.01 #new line
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)


        frsttext, button_options = button_init(hkappa_vals[kk])
        button_hkappa1 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_hkappa1),
                **button_options
                )
        button_hkappa1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)


        kk+=1
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)


        frsttext, button_options = button_init(hkappa_vals[kk])
        button_hkappa2 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_hkappa2),
                **button_options
                )
        button_hkappa2.place(relx=RELXS[3]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)


##############################################################################################
class PRF_profileconfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2

        # topcanvas = tk.Canvas(self)
        # topcanvas.config(bg='#ecebec')
        # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
                
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
                controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ##########################################

        lbl1 = ttk.Label(self, text=r'RF Profile Configure', **labHeadOptions, relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ##
        hkappa_vars = list(adv_prf['rf_profile_settings'].keys())
        hkappa_vals = list(adv_prf['rf_profile_settings'].values())

        RELY += RELHEIGHT+0.01 #new line
        kk = 0
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
        entry1.insert(0,hkappa_vals[kk])

        ##

        kk+=1
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[1]+halfCellX+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)


        entry1 = ttk.Entry(self)
        entry1.insert(0,hkappa_vals[kk])
        entry1.place(relx=RELXS[2]+drelx+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


        kk+=1
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)


        entry1 = ttk.Entry(self)
        entry1.insert(0,hkappa_vals[kk])
        entry1.place(relx=RELXS[4]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)


##############################################################################################
class PRF_eventsSearch(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2

        # topcanvas = tk.Canvas(self)
        # topcanvas.config(bg='#ecebec')
        # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
                
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
                controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ##########################################

        lbl1 = ttk.Label(self, text=r'Events Search', **labHeadOptions, relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ##
        evsearch_vars = list(adv_prf['rf_event_search_settings'].keys())
        evsearch_vals = list(adv_prf['rf_event_search_settings'].values())

        kk=0
        while kk<len(evsearch_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                kk+=1

                ##
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                kk+=1
        

##############################################################################################
class PRF_filter(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2

        # topcanvas = tk.Canvas(self)
        # topcanvas.config(bg='#ecebec')
        # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
                
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
                controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ##########################################

        lbl1 = ttk.Label(self, text=r'Filter Settings', **labHeadOptions, relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ##
        evsearch_vars = list(adv_prf['rf_filter_settings'].keys())
        evsearch_vals = list(adv_prf['rf_filter_settings'].values())

        kk=0
        while kk<len(evsearch_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                kk+=1

                ##
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                kk+=1
        

##############################################################################################
class PRF_display(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # RELXS[1:]= RELXS[1:]+drelx
        halfCellX = (RELXS[2]-RELXS[1])/2

        # topcanvas = tk.Canvas(self)
        # topcanvas.config(bg='#ecebec')
        # topcanvas.place(relx=RELXS[0], rely=RELY, relwidth = 5*RELWIDTH, relheight=8*RELHEIGHT )

        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=2)
        stad_mode = "<<"
        button_options = button_options_back 
        fontDict = {"font":('calibri', 12, 'bold')}
        button_options = {**button_options, **fontDict}



        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}
        label_options = {"font":('calibri', 12, 'normal')}
                
        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        def back_prf():
                controller.show_frame(pageArgs[2])


        button_mode = Button(self, text=stad_mode, command=back_prf, **button_options)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ##########################################

        lbl1 = ttk.Label(self, text=r'Plot Settings', **labHeadOptions, relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ##
        display_vars = list(adv_prf['rf_display_settings'].keys())
        display_vals = list(adv_prf['rf_display_settings'].values())

        kk=0
        while kk<len(display_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=display_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,display_vals[kk])
                kk+=1

                ##
                lbl1 = ttk.Label(self, text=display_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,display_vals[kk])
                kk+=1
        
        
        
        ##
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=r'Plot Filters', **labHeadOptions, relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        plotting_vars = list(adv_prf['rf_plotting_settings'].keys())
        plotting_vals = list(adv_prf['rf_plotting_settings'].values())

        kk=0
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,plotting_vals[kk])
        kk+=1

        ##
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,plotting_vals[kk])
        kk+=1

        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        frsttext, button_options = button_init(plotting_vals[kk])
        button_good_bad = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_good_bad),
                **button_options
                )
        button_good_bad.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)

        # entry1 = ttk.Entry(self)
        # entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        # entry1.insert(0,plotting_vals[kk])
        kk+=1

        ##
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        frsttext, button_options = button_init(plotting_vals[kk])
        button_good_bad2 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_good_bad2),
                **button_options
                )
        button_good_bad2.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)

        

##############################################################################################
        

app = stadiumpyMain()
app.mainloop()