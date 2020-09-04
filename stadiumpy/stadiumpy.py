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
from stadiumpy.styles import *

from stadiumpy.plot_geomap import plot_map
from PIL import ImageTk, Image
from tkinter import messagebox
import Pmw
import ast

print("Hello from", __name__)

cachedirec=".cache"
if not os.path.exists(cachedirec):
    os.makedirs(cachedirec, exist_ok=True)

image_name = os.path.join('.cache', 'region-plot.png')

# read inputYAML
inp_file_yaml = os.path.join(stdpy.__path__[0], 'settings', 'input_file.yaml')
adv_prf_yaml = os.path.join(stdpy.__path__[0], 'settings', 'advRFparam.yaml')
descrip_yaml = os.path.join(stdpy.__path__[0], 'settings', 'description.yaml')

## User defined
USER_adv_prf_yaml = os.path.join(stdpy.__path__[0], 'settings', 'USER_advRFparam.yaml')
USER_inp_yaml = os.path.join(stdpy.__path__[0], 'settings', 'USER_input_file.yaml')

# adv_prf_yaml = os.path.join(stdpy.__path__[0], 'settings', 'advancedRF.yaml')
# inp_file_yaml = 'settings/input_file.yaml'

with open(inp_file_yaml) as f:
    inp = yaml.load(f, Loader=yaml.FullLoader)


with open(adv_prf_yaml) as f:
    adv_prf = yaml.load(f, Loader=yaml.FullLoader)

with open(descrip_yaml) as f:
    stdpydesc = yaml.load(f, Loader=yaml.FullLoader)


class stadiumpyMain(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        Pmw.initialise(self) #initializing it in the root window

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

        
        ## TOP frame
        container = tk.Frame(self, relief=RAISED, borderwidth=1)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        
        ## all the pages in the app
        stadium_pages = (StartPage, PageDataEnquiry, PageRF, PageSKS, ProjectDir, PageGeoRegion,
         PageSRF, PRF_filenames, PRF_hkappa, PRF_profileconfig, PRF_eventsSearch,
         PRF_filter, PRF_display, RFdirectoryStructure)

        for F in stadium_pages:

            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #displays the StartPage when the app opens
        self.show_frame(StartPage)

        ## Bottom frame
        container2 = tk.Frame(self, relief=RAISED, borderwidth=2)
        container2.pack(side="bottom",fill="both", expand=True)

        closeButton = ttk.Button(container2, text="Close", command=self._quit,style = 'W.TButton')
        closeButton.pack(side="right", padx=5, pady=5)
        ############### RUN function###################
        def runStadiumpy():
            print("Run Stadiumpy")

            inpFile_dict = self.frames[StartPage].getOutput()
            
            inpYML = open(USER_inp_yaml, "w")
            yaml.dump(inpFile_dict,inpYML)
            inpYML.close()


            advPRF_dict = {}
            prf_filenames_dict = self.frames[PRF_filenames].getOutput()
            advPRF_dict["filenames"] = prf_filenames_dict

            prf_hkappa_dict = self.frames[PRF_hkappa].getOutput()
            advPRF_dict["h_kappa_settings"] = prf_hkappa_dict

            prf_profile_dict = self.frames[PRF_profileconfig].getOutput()
            advPRF_dict["rf_profile_settings"] = prf_profile_dict

            prf_evsearch_dict = self.frames[PRF_eventsSearch].getOutput()
            advPRF_dict["rf_event_search_settings"] = prf_evsearch_dict

            prf_filter_dict = self.frames[PRF_filter].getOutput()
            advPRF_dict["rf_filter_settings"] = prf_filter_dict
            
            prf_display_dict = self.frames[PRF_display].getOutput1()
            advPRF_dict["rf_display_settings"] = prf_display_dict
            
            prf_plotting_dict = self.frames[PRF_display].getOutput2()
            advPRF_dict["rf_plotting_settings"] = prf_plotting_dict

            prfADVYML = open(USER_adv_prf_yaml, "w")
            yaml.dump(advPRF_dict,prfADVYML)
            prfADVYML.close()
            

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
    pageArgs = (StartPage, PageDataEnquiry, PageRF, PageSKS, ProjectDir, PageGeoRegion,
         PageSRF, PRF_filenames, PRF_hkappa, PRF_eventsSearch, PRF_profileconfig,
         PRF_filter, PRF_display, RFdirectoryStructure)
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

        self.outputDict = {}
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
        self.outputDict['mode'] = get_toggle_output(button_mode)
        
        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['mode']) #binding it and assigning a text to it

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
        self.outputDict['fresh_start'] = get_toggle_output(button_freshstart)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['fresh_start']) #binding it and assigning a text to it


        ## Project name
        lbl1 = ttk.Label(self, text="ProjectName:")
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['project_name']) #binding it and assigning a text to it



        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        entry1.insert(0,inp['project_name'])
        self.outputDict['project_name'] = entry1


        ## Summary file name
        RELY += RELHEIGHT+0.01
        lbl1 = ttk.Label(self, text="SummaryFile:")
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['summary_file']) #binding it and assigning a text to it


        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        entry1.insert(0,inp['summary_file'])
        self.outputDict['summary_file'] = entry1




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
        ## hover description
        makeRF_lab_tooltip = Pmw.Balloon(self) #Calling the tooltip
        makeRF_lab_tooltip.bind(makeRF_lab,stdpydesc['inputfile']['makeRF']) #binding it and assigning a text to it


        
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
        self.outputDict['makeRF'] = get_toggle_output(button_makerf)


        # makeRF-S
        RELY += RELHEIGHT+0.01
        makeSRF_lab = ttk.Label(self, text="S-RF:")
        makeSRF_lab.configure(anchor="center")
        makeSRF_lab.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)

        ## hover description
        makeSRF_lab_tooltip = Pmw.Balloon(self) #Calling the tooltip
        makeSRF_lab_tooltip.bind(makeSRF_lab,stdpydesc['inputfile']['makeSRF']) #binding it and assigning a text to it


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
        self.outputDict['makeSRF'] = get_toggle_output(button_makerf)

        # makeSKS
        RELY += RELHEIGHT+0.01
        makeSKS_lab = ttk.Label(self, text="SKS:")
        makeSKS_lab.configure(anchor="center")
        makeSKS_lab.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)

        ## hover description
        makeSKS_lab_tooltip = Pmw.Balloon(self) #Calling the tooltip
        makeSKS_lab_tooltip.bind(makeSKS_lab,stdpydesc['inputfile']['makeSKS']) #binding it and assigning a text to it


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
        self.outputDict['makeSKS'] = get_toggle_output(button_makesks)

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
        self.outputDict['mxlat'] = geoMaxLatEntry

        ## hover description
        geoMaxLatEntry_tooltip = Pmw.Balloon(self) #Calling the tooltip
        geoMaxLatEntry_tooltip.bind(geoMaxLatEntry,stdpydesc['inputfile']['mxlat']) #binding it and assigning a text to it



        RELY += RELHEIGHT+0.01
        geoMinLonEntry = ttk.Entry(self, width=10)
        geoMaxLonEntry = ttk.Entry(self, width=10)
        geoMinLonEntry.place(relx=RELXS[3]+0.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
        geoMaxLonEntry.place(relx=RELXS[4]+0.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
        self.outputDict['mnlong'] = geoMinLonEntry
        self.outputDict['mxlong'] = geoMaxLonEntry

        ## hover description
        geoMinLonEntry_tooltip = Pmw.Balloon(self) #Calling the tooltip
        geoMinLonEntry_tooltip.bind(geoMinLonEntry,stdpydesc['inputfile']['mnlong']) #binding it and assigning a text to it


        ## hover description
        geoMaxLonEntry_tooltip = Pmw.Balloon(self) #Calling the tooltip
        geoMaxLonEntry_tooltip.bind(geoMaxLonEntry,stdpydesc['inputfile']['mxlong']) #binding it and assigning a text to it


        geoMinLonEntry.insert(0,str(minlon))
        geoMaxLonEntry.insert(0,str(maxlon))
        # plotmapRELY = RELY

        # ##
        RELY += RELHEIGHT+0.01
        geoMinLatEntry = ttk.Entry(self, width=10)
        geoMinLatEntry.insert(0,str(minlat))
        geoMinLatEntry.place(relx=RELXS[3]+1.5*(RELXS[4]-RELXS[3])/2-drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
        self.outputDict['mnlat'] = geoMinLatEntry

        ## hover description
        geoMinLatEntry_tooltip = Pmw.Balloon(self) #Calling the tooltip
        geoMinLatEntry_tooltip.bind(geoMinLatEntry,stdpydesc['inputfile']['mnlat']) #binding it and assigning a text to it

        if os.path.exists(image_name):
            os.remove(image_name)


        def showMap():
            controller.show_frame(pageArgs[5])

        RELY += RELHEIGHT+0.01
        ## Project Dir
        lbl1 = ttk.Label(self, text="Project Location:")
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['summary_file']) #binding it and assigning a text to it


        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        entry1.insert(0,inp['summary_file'])
        self.outputDict['summary_file'] = entry1

        button_plotmap = ttk.Button(self, text="ExploreMap", command=showMap)
        button_plotmap.place(relx=RELXS[4], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)

        ## hover description
        button_plotmap_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_plotmap_tooltip.bind(button_plotmap,stdpydesc['inputfile']['exploreMap']) #binding it and assigning a text to it
    
    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            try:
                outputResult[key] = convert_input(value.get())
            except:
                outputResult[key] = value
        return outputResult


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

        ## hover description
        button_mode_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_mode_tooltip.bind(button_mode,stdpydesc['others']['goToSRF']) #binding it and assigning a text to it


        ## filenames button
        RELY += RELHEIGHT+0.01 
        def gotofilenameprf():
                controller.show_frame(pageArgs[7])
        button_filename = Button(self, text="Set File Names", command=gotofilenameprf, **button_options)

        button_filename.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## hover description
        button_filename_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filename_tooltip.bind(button_filename,stdpydesc['PRFpage']['btnFilenamePage']) #binding it and assigning a text to it



        ## set h kappa
        def gotohkappaprf():
                controller.show_frame(pageArgs[8])
        button_filename = Button(self, text="Set H-Kappa", command=gotohkappaprf, **button_options)

        button_filename.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)

        ## hover description
        button_filename_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filename_tooltip.bind(button_filename,stdpydesc['PRFpage']['btnHKappaPage']) #binding it and assigning a text to it


        ## RF profile config
        RELY += RELHEIGHT+0.01 

        def gotoprofileconfig():
                controller.show_frame(pageArgs[10])
        button_profile = Button(self, text="Configure Profile", command=gotoprofileconfig, **button_options)

        button_profile.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## hover description
        button_profile_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_profile_tooltip.bind(button_profile,stdpydesc['PRFpage']['btnConfigProfilePage']) #binding it and assigning a text to it


        ## RF events search
        def gotoeventssearch():
                controller.show_frame(pageArgs[9])
        button_evsearch = Button(self, text="Configure Events Search", command=gotoeventssearch, **button_options)

        button_evsearch.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)

        ## hover description
        button_evsearch_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_evsearch_tooltip.bind(button_evsearch,stdpydesc['PRFpage']['btnEvtSearchPage']) #binding it and assigning a text to it
        
        ## RF filter
        RELY += RELHEIGHT+0.01 
        def gotofiltersettings():
                controller.show_frame(pageArgs[11])
        button_filter = Button(self, text="Set Filter", command=gotofiltersettings, **button_options)

        button_filter.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## hover description
        button_filter_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filter_tooltip.bind(button_filter,stdpydesc['PRFpage']['btnSetFilterPage']) #binding it and assigning a text to it
        
        
        ## RF filter
        def gotofplotsettings():
                controller.show_frame(pageArgs[12])
        button_filter = Button(self, text="Configure RF plot", command=gotofplotsettings, **button_options)

        button_filter.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)

        ## hover description
        button_filter_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filter_tooltip.bind(button_filter,stdpydesc['PRFpage']['btnConfigRFPlotPage']) #binding it and assigning a text to it
        


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

        ## hover description
        button_mode_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_mode_tooltip.bind(button_mode,stdpydesc['others']['goToPRF']) #binding it and assigning a text to it

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
class ProjectDir(tk.Frame):

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


        ## hover description
        button_mode_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_mode_tooltip.bind(button_mode,stdpydesc['others']['backBtn']) #binding it and assigning a text to it
        

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

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][filename_vars[kk]]) #binding it and assigning a text to it
            


            entry1 = ttk.Entry(self)
            entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
            entry1.insert(0,filename_vals[kk])
            self.outputDict[filename_vars[kk]] = entry1
            kk+=1

            ##
            lbl1 = ttk.Label(self, text=filename_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][filename_vars[kk]]) #binding it and assigning a text to it
            

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

        self.outputDict = {}
        RELY += RELHEIGHT+0.01 #new line
        kk = 0
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][hkappa_vars[kk]]) #binding it and assigning a text to it
        

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,hkappa_vals[kk])
        self.outputDict[hkappa_vars[kk]] = entry1

        ##


        kk+=1
        RELY += RELHEIGHT+0.01 #new line
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][hkappa_vars[kk]]) #binding it and assigning a text to it
  


        frsttext, button_options = button_init(hkappa_vals[kk])
        button_hkappa1 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_hkappa1),
                **button_options
                )
        button_hkappa1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        self.outputDict[hkappa_vars[kk]] = get_toggle_output(button_hkappa1)
        # print(frsttext)

        kk+=1
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][hkappa_vars[kk]]) #binding it and assigning a text to it
  
        frsttext, button_options = button_init(hkappa_vals[kk])
        button_hkappa2 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_hkappa2),
                **button_options
                )
        button_hkappa2.place(relx=RELXS[3]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        self.outputDict[hkappa_vars[kk]] = get_toggle_output(button_hkappa2)

    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            try:
                outputResult[key] = value.get()
            except:
                outputResult[key] = value

        return outputResult

##############################################################################################
class PRF_profileconfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
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

        self.outputDict = {}
        RELY += RELHEIGHT+0.01 #new line
        kk = 0
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][hkappa_vars[kk]]) #binding it and assigning a text to it
 

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2)
        entry1.insert(0,hkappa_vals[kk])
        self.outputDict[hkappa_vars[kk]] = entry1

        ##

        kk+=1
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[1]+halfCellX+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][hkappa_vars[kk]]) #binding it and assigning a text to it
 

        entry1 = ttk.Entry(self)
        entry1.insert(0,hkappa_vals[kk])
        entry1.place(relx=RELXS[2]+drelx+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)
        self.outputDict[hkappa_vars[kk]] = entry1

        kk+=1
        lbl1 = ttk.Label(self, text=hkappa_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH-drelx)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][hkappa_vars[kk]]) #binding it and assigning a text to it
 

        entry1 = ttk.Entry(self)
        entry1.insert(0,hkappa_vals[kk])
        entry1.place(relx=RELXS[4]+drelx, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)
        self.outputDict[hkappa_vars[kk]] = entry1

    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            try:
                outputResult[key] = convert_input(value.get())
            except:
                outputResult[key] = value
        return outputResult

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
        self.outputDict = {}
        while kk<len(evsearch_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][evsearch_vars[kk]]) #binding it and assigning a text to it
        


                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                self.outputDict[evsearch_vars[kk]] = entry1

                kk+=1

                ##
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
                
                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][evsearch_vars[kk]]) #binding it and assigning a text to it
        

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                self.outputDict[evsearch_vars[kk]] = entry1
                kk+=1

    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            try:
                outputResult[key] = ast.literal_eval(value.get())
            except:
                outputResult[key] = value
        return outputResult

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
        self.outputDict = {}
        while kk<len(evsearch_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][evsearch_vars[kk]]) #binding it and assigning a text to it

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                self.outputDict[evsearch_vars[kk]] = entry1
                kk+=1

                ##
                lbl1 = ttk.Label(self, text=evsearch_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][evsearch_vars[kk]]) #binding it and assigning a text to it

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,evsearch_vals[kk])
                self.outputDict[evsearch_vars[kk]] = entry1
                kk+=1
    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            try:
                outputResult[key] = ast.literal_eval(value.get())
            except:
                outputResult[key] = value
        return outputResult

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
        self.outputDict1 = {}
        while kk<len(display_vars):
                RELY += RELHEIGHT+0.01 
                lbl1 = ttk.Label(self, text=display_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][display_vars[kk]]) #binding it and assigning a text to it


                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,display_vals[kk])
                self.outputDict1[display_vars[kk]] = entry1
                kk+=1

                ##
                lbl1 = ttk.Label(self, text=display_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][display_vars[kk]]) #binding it and assigning a text to it

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,display_vals[kk])
                self.outputDict1[display_vars[kk]] = entry1
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
        self.outputDict2 = {}
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][plotting_vars[kk]]) #binding it and assigning a text to it

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,plotting_vals[kk])
        self.outputDict2[plotting_vars[kk]] = entry1
        kk+=1

        ##
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][plotting_vars[kk]]) #binding it and assigning a text to it

        entry1 = ttk.Entry(self)
        entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        entry1.insert(0,plotting_vals[kk])
        self.outputDict2[plotting_vars[kk]] = entry1
        kk+=1

        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][plotting_vars[kk]]) #binding it and assigning a text to it

        frsttext, button_options = button_init(plotting_vals[kk])
        button_good_bad = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_good_bad),
                **button_options
                )
        button_good_bad.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        self.outputDict2[plotting_vars[kk]] = get_toggle_output(button_good_bad)


        kk+=1

        ##
        lbl1 = ttk.Label(self, text=plotting_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['rfparams'][plotting_vars[kk]]) #binding it and assigning a text to it

        frsttext, button_options = button_init(plotting_vals[kk])
        button_good_bad2 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_good_bad2),
                **button_options
                )
        button_good_bad2.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
        self.outputDict2[plotting_vars[kk]] = get_toggle_output(button_good_bad2)
    
    def getOutput1(self):
        outputResult = {}
        for key, value in self.outputDict1.items():
            try:
                outputResult[key] = convert_input(value.get())
            except:
                outputResult[key] = value.get()
        return outputResult
    def getOutput2(self):
        outputResult = {}
        for key, value in self.outputDict2.items():
            try:
                outputResult[key] = ast.literal_eval(value.get())
            except:
                outputResult[key] = value
        return outputResult
        

##############################################################################################
class RFdirectoryStructure(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=4)


##############################################################################################

app = stadiumpyMain()
app.mainloop()