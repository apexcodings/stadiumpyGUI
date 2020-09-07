"""
Wrapper for the stadiumpy GUI
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import yaml, os
from tkinter import Tk, RIGHT, BOTH, RAISED, X, LEFT, W, E, NW, N, S, SUNKEN, Y, VERTICAL, RIDGE, GROOVE
from tkinter.ttk import Frame, Style
import numpy as np

from stadiumpy.page_control import PageControl
# from stadiumpy.plot_map_gui import plotMap
from stadiumpy.font_properties import *
import stadiumpy as stdpy
from stadiumpy.widgets import SFrame, Button
from stadiumpy.top_buttons import display_main_buttons
from stadiumpy.styles import *

from stadiumpy.plot_geomap import plot_map
from PIL import ImageTk, Image
from tkinter import messagebox
import Pmw
import ast
from stadiumpy.backend import stadiumpyBackend


cachedirec=".cache"
if not os.path.exists(cachedirec):
    os.makedirs(cachedirec, exist_ok=True)

image_name = os.path.join('.cache', 'region-plot.png')

# read inputYAML
inp_file_yaml = os.path.join(stdpy.__path__[0], 'backend', 'input_file.yaml')
adv_prf_yaml = os.path.join(stdpy.__path__[0], 'backend', 'advRFparam.yaml')
descrip_yaml = os.path.join(stdpy.__path__[0], 'backend', 'description.yaml')
direc_yaml = os.path.join(stdpy.__path__[0], 'backend', 'directories_names.yaml')
stepwise_yaml = os.path.join(stdpy.__path__[0], 'backend', 'stepwise.yaml')

## User defined
USER_adv_prf_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_advRFparam.yaml')
USER_inp_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_input_file.yaml')
USER_direc_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_directories_names.yaml')
USER_stepwise_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_stepwise.yaml')


with open(inp_file_yaml) as f:
    inp = yaml.load(f, Loader=yaml.FullLoader)

with open(adv_prf_yaml) as f:
    adv_prf = yaml.load(f, Loader=yaml.FullLoader)

with open(descrip_yaml) as f:
    stdpydesc = yaml.load(f, Loader=yaml.FullLoader)

with open(USER_inp_yaml) as f:
    user_inp = yaml.load(f, Loader=yaml.FullLoader)

with open(direc_yaml) as f:
    direcDict = yaml.load(f, Loader=yaml.FullLoader)

with open(stepwise_yaml) as f:
    stepwiseDict = yaml.load(f, Loader=yaml.FullLoader)


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

        style.configure('W.TButton', **system_styles)
        
        ## TOP frame
        container = tk.Frame(self, relief=RAISED, borderwidth=1)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # ## Menu items
        # stadiumpyMenu = tk.Menu(self)
        # self.config(menu=stadiumpyMenu)

        # #create File menu
        # def reload_command():
        #     pass

        # fileMenu = tk.Menu(stadiumpyMenu)
        # stadiumpyMenu.add_cascade(label="File", menu=fileMenu)
        # fileMenu.add_command(label="Reload Defaults", command=reload_command)
        # fileMenu.add_command(label="Exit", command=self._quit)


        self.frames = {}
        
        ## all the pages in the app
        stadium_pages = (StartPage, PageDataEnquiry, PageRF, PageSKS, ProjectDir, PageGeoRegion,
         PageSRF, PRF_filenames, PRF_hkappa, PRF_profileconfig, PRF_eventsSearch,
         PRF_filter, PRF_display, PRFdirectoryStructure, SRFdirectoryStructure, 
         ProjectTreeStructure, StepWise, DataSettings)

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

            ## write homepage inputs from GUI
            inpFile_dict = self.frames[StartPage].getOutput()            
            
            inpYML = open(USER_inp_yaml, "w")
            yaml.dump(inpFile_dict,inpYML)
            inpYML.close()

            ## write stepwise and data setting inputs from GUI
            stepwise_dict = {}
            stepwise_dict1 = self.frames[StepWise].getOutput1()            
            stepwise_dict2 = self.frames[StepWise].getOutput2()            
            stepwise_dict3 = self.frames[StepWise].getOutput3()            
            stepwise_dict['plot_settings'] = stepwise_dict1    
            stepwise_dict['rf_stepwise'] = stepwise_dict2   
            stepwise_dict['srf_stepwise'] = stepwise_dict3    

            datasettings_dict = self.frames[DataSettings].getOutput()   
            stepwise_dict['data_settings'] = datasettings_dict    
            
            stepwiseYML = open(USER_stepwise_yaml, "w")
            yaml.dump(stepwise_dict,stepwiseYML)
            stepwiseYML.close()

            ## write directories from GUI
            direc_user_prf_dict = self.frames[PRFdirectoryStructure].getOutput()
            direc_user_srf_dict = self.frames[SRFdirectoryStructure].getOutput()

            with open(USER_direc_yaml, "w") as direcYML:
                yaml.dump(direc_user_prf_dict,direcYML)
                yaml.dump(direc_user_srf_dict,direcYML)


            ## write advanced PRF inputs from GUI
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
         PRF_filter, PRF_display, PRFdirectoryStructure, SRFdirectoryStructure,
         ProjectTreeStructure, StepWise, DataSettings)
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
        for ii,pg in enumerate(pageArgs):
            print(ii,pg)

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
        ## Mode

        lbl1 = ttk.Label(self, text="Mode:")
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        stepwiseBtnState = "normal"
        def gotostepwisepage():
                controller.show_frame(pageArgs[16])
        button_stepwise = ttk.Button(self, text="StepwiseSettings", command=gotostepwisepage, state=stepwiseBtnState)

        if inp['mode']=="Automated":
            stad_mode = "Automated"
            button_options = button_options_green_mode
            # stepwiseBtnState = "disabled"
            button_stepwise['state'] = "disabled"
        else:
            stad_mode = "Stepwise"
            button_options = button_options_red_mode
            # stepwiseBtnState = "normal"
            button_stepwise['state'] = "normal"

        def toggle_mode(button_mode):
            if button_mode['text'] == 'Automated':
                dictAdd = {'text':'Stepwise', 'bg':'#4287f5', 'fg': '#5F4B8B'}
                for key, value in dictAdd.items():
                    button_mode[key]=value
                button_stepwise['state'] = "normal"
            else:
                dictAdd = {'text':'Automated', 'bg':'#00FF00', 'fg': '#00203F'}
                for key, value in dictAdd.items():
                    button_mode[key]=value
                button_stepwise['state'] = "disabled"

        button_mode = Button(self, text=stad_mode, command=lambda: toggle_mode(button_mode), **button_options)

        button_mode.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        self.outputDict['mode'] = get_toggle_output_mode(button_mode)
        
        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['mode']) #binding it and assigning a text to it

        ## Data Settings button
        def gotodatasettingspage():
                controller.show_frame(pageArgs[17])
        button_filename = ttk.Button(self, text="DataSettings", command=gotodatasettingspage)

        button_filename.place(relx=RELXS[2], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        button_filename_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filename_tooltip.bind(button_filename,stdpydesc['inputfile']['datasettings']) #binding it and assigning a text to it
        
        ## Stepwise button

        button_stepwise.place(relx=RELXS[3], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        ## hover description
        button_stepwise_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_stepwise_tooltip.bind(button_stepwise,stdpydesc['inputfile']['stepwise']) #binding it and assigning a text to it
        
                
        ## fresh start
        RELY0 = RELY
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="FreshStart:")
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

        if not inp['fresh_start']:
            frsttext = "No"
            button_options = button_options_red
        else:
            frsttext = "Yes"
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

        ## Project Dir
        def browse_button(folder_path):
            # Allow user to select a directory and store it in global var
            # called folder_path
            # global folder_path
            filename = filedialog.askdirectory()
            folder_path.set(filename)
            print(filename)
            # buttonBrowse['text'] = filename
            # buttonBrowse['font'] = ('calibri', 8)
            # self.outputDict['project_dir_loc'] = filename
            entry1_projloc.delete(0,tk.END)
            entry1_projloc.insert(0,filename)
            
            

        RELY += 2*(RELHEIGHT+0.01)
        lbl1 = ttk.Label(self, text="ProjectLocation:")
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        # print(RELY)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['inputfile']['project_dir_loc']) #binding it and assigning a text to it


        folder_path = tk.StringVar()
        # buttonBrowse = tk.Button(text="Browse", command=lambda: browse_button(folder_path))
        # buttonBrowse.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)
        buttonBrowse = Button(self, 
                text="Browse",
                command=lambda: browse_button(folder_path),
                **button_options_browse
                )

        buttonBrowse.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)


        RELYbrowse = RELY0+7*RELHEIGHT+0.01
        entry1_projloc = ttk.Entry(self)
        entry1_projloc.place(relx=RELXS[0]+drelx, rely=RELYbrowse, relheight=RELHEIGHT, relwidth=2*RELWIDTH-drelx)
        entry1_projloc.insert(0,inp['project_dir_loc'])
        self.outputDict['project_dir_loc'] = entry1_projloc




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
            makeRFtext = "No"
            button_options = button_options_red
        else:
            makeRFtext = "Yes"
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
            makeSRFtext = "No"
            button_options = button_options_red
        else:
            makeSRFtext = "Yes"
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
            makeSKStext = "No"
            button_options = button_options_red
        else:
            makeSKStext = "Yes"
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

        lbl1 = ttk.Label(self, text="", relief=RIDGE)
        lbl1.configure(anchor="center")
        RELY += RELHEIGHT+0.01
        lbl1.place(relx=RELXS[3], rely=RELY-drelx, relheight=4*RELHEIGHT-1*drelx, relwidth=2*RELWIDTH)


        # RELY += RELHEIGHT+0.01
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
########################################P - Receiver Functions######################################################
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
##########################################S-RF####################################################
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
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=4)
        
        button_options = button_options_nav 
        fontDict = {"font":('calibri', 16, 'bold')}
        button_options = {**button_options, **fontDict}


        labHeadOptions = {"font":('calibri', 18, 'bold'), "anchor":"center"}

        ################TOP Button###########
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="Project Structure", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)


        ## PRF page
        RELY += RELHEIGHT+0.01 
        def gotofdirecStrPrf():
                controller.show_frame(pageArgs[13])

        button_filename = Button(self, text="P-S Receiver Functions", command=gotofdirecStrPrf, **button_options)

        button_filename.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH)

        ## hover description
        button_filename_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filename_tooltip.bind(button_filename,stdpydesc['dirnames']['PRF_direc_structure']) #binding it and assigning a text to it



        ## SRF page
        def gotodirecStrSrf():
                controller.show_frame(pageArgs[14])
        button_filename = Button(self, text="S-P Receiver Functions", command=gotodirecStrSrf, **button_options)

        button_filename.place(relx=RELXS[2]+halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=2.5*RELWIDTH-drelx)

        ## hover description
        button_filename_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filename_tooltip.bind(button_filename,stdpydesc['dirnames']['SRF_direc_structure']) #binding it and assigning a text to it
        
        ## Project Tree Structure
        RELY += RELHEIGHT+0.01 
        def gotoprojecttreeSrf():
                controller.show_frame(pageArgs[15])
        button_filename = Button(self, text="Visualize Project Structure", command=gotoprojecttreeSrf, **button_options)

        button_filename.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)

        ## hover description
        button_filename_tooltip = Pmw.Balloon(self) #Calling the tooltip
        button_filename_tooltip.bind(button_filename,stdpydesc['dirnames']['ProjectTreeStructure']) #binding it and assigning a text to it
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
class PRFdirectoryStructure(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=4)
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="P-RF  Directory Structure", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)


        def back_prf():
            controller.show_frame(pageArgs[4])


        button_mode = Button(self, text="<<", command=back_prf, **button_options_BACK)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        direc_vars = []
        direc_vals = []
        # direc_vars = list(direcDict.keys())
        # direc_vals = list(direcDict.values())
        for key,value in direcDict.items():
            if key[:2] == 'RF':
                direc_vars.append(key)
                direc_vals.append(value)
        kk=0
        self.outputDict = {}
        while kk<len(direc_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=direc_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['dirnames'][direc_vars[kk]]) #binding it and assigning a text to it
            


            entry1 = ttk.Entry(self)
            entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
            entry1.insert(0,direc_vals[kk])
            self.outputDict[direc_vars[kk]] = entry1

            ##
            if kk+1<len(direc_vars):
                kk+=1
                lbl1 = ttk.Label(self, text=direc_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['dirnames'][direc_vars[kk]]) #binding it and assigning a text to it
                

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,direc_vals[kk])
                self.outputDict[direc_vars[kk]] = entry1
            kk+=1
    
    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            outputResult[key] = value.get()
        return outputResult
##############################################################################################
class SRFdirectoryStructure(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=4)
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="S-RF Directory Structure", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)



        def back_prf():
            controller.show_frame(pageArgs[4])


        button_mode = Button(self, text="<<", command=back_prf, **button_options_BACK)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        direc_vars = []
        direc_vals = []

        for key,value in direcDict.items():
            if key[:2] == 'SF':
                direc_vars.append(key)
                direc_vals.append(value)
        kk=0
        self.outputDict = {}
        while kk<len(direc_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=direc_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['dirnames'][direc_vars[kk]]) #binding it and assigning a text to it
            


            entry1 = ttk.Entry(self)
            entry1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
            entry1.insert(0,direc_vals[kk])
            self.outputDict[direc_vars[kk]] = entry1

            ##
            if kk+1<len(direc_vars):
                kk+=1
                lbl1 = ttk.Label(self, text=direc_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXS[3]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH)

                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['dirnames'][direc_vars[kk]]) #binding it and assigning a text to it
                

                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXS[4]-halfCellX, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH+halfCellX)
                entry1.insert(0,direc_vals[kk])
                self.outputDict[direc_vars[kk]] = entry1
            kk+=1
    
    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            outputResult[key] = value.get()
        return outputResult
##############################################################################################
class ProjectTreeStructure(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=1)
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="Project Directory Visualization", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)


        def back_prf():
            controller.show_frame(pageArgs[4])


        button_mode = Button(self, text="<<", command=back_prf, **button_options_BACK)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        ###
        RELY += 2*RELHEIGHT+0.01 
        listNodes = tk.Listbox(self, width=20, height=20, font=("Helvetica", 16))
        listNodes.place(relx=RELXS[1]-halfCellX, rely=RELY, relheight=15*RELHEIGHT, relwidth=4*RELWIDTH)
        # listNodes.pack(side="left", fill="y")

        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=listNodes.yview)
        scrollbar.pack(side="right", fill="y")

        listNodes.config(yscrollcommand=scrollbar.set)
        if os.path.exists(USER_inp_yaml):
            dirPath = user_inp['project_dir_loc']
        else:
            dirPath = inp['project_dir_loc']

        outputDirStructureList = list_files("./")
        for x in outputDirStructureList:
            listNodes.insert(tk.END, x)   
##############################################################################################
class StepWise(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        # halfCellX = (RELXS[2]-RELXS[1])/2
        halfCellX = RELWIDTH/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=None)
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="StepWise Settings", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)



        def back_prf():
            controller.show_frame(pageArgs[0])


        button_mode = Button(self, text="<<", command=back_prf, **button_options_BACK)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)
        
        lbl1 = ttk.Label(self, text="Plot Settings:", **labHeadOptions, relief=RIDGE)
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)
        
        stepwisePlot_vars = list(stepwiseDict['plot_settings'].keys())
        stepwisePlot_vals = list(stepwiseDict['plot_settings'].values())


        RELWIDTHtemp1 = 0.2
        RELWIDTHtemp2 = 0.1
        RELWIDTHtemp3 = 0.03
        RELXStemp = np.linspace(0,1,4)
        kk=0
        self.outputDict = {}
        while kk<len(stepwisePlot_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=stepwisePlot_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[0]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePlot_vars[kk]]) #binding it and assigning a text to it
            


            frsttext, button_options = button_init(stepwisePlot_vals[kk])
            button_stepwisePlot_vals1 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwisePlot_vals1),
                    **button_options
                    )
            button_stepwisePlot_vals1.place(relx=RELXStemp[0]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict[stepwisePlot_vars[kk]] = get_toggle_output(button_stepwisePlot_vals1)
            # print(self.outputDict[stepwisePlot_vars[kk]])

            

            ##
            if kk+1<len(stepwisePlot_vars):
                kk+=1
                lbl1 = ttk.Label(self, text=stepwisePlot_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXStemp[1]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePlot_vars[kk]]) #binding it and assigning a text to it
  
                frsttext, button_options = button_init(stepwisePlot_vals[kk])
                button_stepwisePlot_vals2 = Button(self, 
                        text=frsttext,
                        command=lambda: toggle_button(button_stepwisePlot_vals2),
                        **button_options
                        )
                button_stepwisePlot_vals2.place(relx=RELXStemp[1]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
                self.outputDict[stepwisePlot_vars[kk]] = get_toggle_output(button_stepwisePlot_vals2)
                # print(self.outputDict[stepwisePlot_vars[kk]])
                

            if kk+1<len(stepwisePlot_vars):
                kk+=1
                lbl1 = ttk.Label(self, text=stepwisePlot_vars[kk]+":", **label_options)
                lbl1.place(relx=RELXStemp[2]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

                ## hover description
                lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
                lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePlot_vars[kk]]) #binding it and assigning a text to it

                frsttext, button_options = button_init(stepwisePlot_vals[kk])
                button_stepwisePlot_vals3 = Button(self, 
                        text=frsttext,
                        command=lambda: toggle_button(button_stepwisePlot_vals3),
                        **button_options
                        )
                button_stepwisePlot_vals3.place(relx=RELXStemp[2]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
                self.outputDict[stepwisePlot_vars[kk]] = get_toggle_output(button_stepwisePlot_vals3)
                # print(self.outputDict[stepwisePlot_vars[kk]])
            kk+=1
        
        #######
        lbl1 = ttk.Label(self, text="P-RF Stepwise:", **labHeadOptions, relief=RIDGE)
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)

        stepwisePRF_vars = list(stepwiseDict['rf_stepwise'].keys())
        stepwisePRF_vals = list(stepwiseDict['rf_stepwise'].values())
        RELWIDTHtemp1 = 0.2
        RELWIDTHtemp2 = 0.1
        RELWIDTHtemp3 = 0.03
        RELXStemp = np.linspace(0,1,4)
        kk=0
        self.outputDict2 = {}
        # while kk<len(stepwisePRF_vars):
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=stepwisePRF_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXStemp[0]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePRF_vars[kk]]) #binding it and assigning a text to it
        


        frsttext, button_options = button_init(stepwisePRF_vals[kk])
        button_stepwisePRF_vals1 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_stepwisePRF_vals1),
                **button_options
                )
        button_stepwisePRF_vals1.place(relx=RELXStemp[0]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
        self.outputDict2[stepwisePRF_vars[kk]] = get_toggle_output(button_stepwisePRF_vals1)
        # print(self.outputDict2[stepwisePRF_vars[kk]])
        

        ##
        if kk+1<len(stepwisePRF_vars):
            kk+=1
            lbl1 = ttk.Label(self, text=stepwisePRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[1]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePRF_vars[kk]]) #binding it and assigning a text to it

            frsttext, button_options = button_init(stepwisePRF_vals[kk])
            button_stepwisePRF_vals2 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwisePRF_vals2),
                    **button_options
                    )
            button_stepwisePRF_vals2.place(relx=RELXStemp[1]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict2[stepwisePRF_vars[kk]] = get_toggle_output(button_stepwisePRF_vals2)
            # print(self.outputDict2[stepwisePRF_vars[kk]])
            

        if kk+1<len(stepwisePRF_vars):
            kk+=1
            lbl1 = ttk.Label(self, text=stepwisePRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[2]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePRF_vars[kk]]) #binding it and assigning a text to it

            frsttext, button_options = button_init(stepwisePRF_vals[kk])
            button_stepwisePRF_vals3 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwisePRF_vals3),
                    **button_options
                    )
            button_stepwisePRF_vals3.place(relx=RELXStemp[2]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict2[stepwisePRF_vars[kk]] = get_toggle_output(button_stepwisePRF_vals3)
            # print(self.outputDict2[stepwisePRF_vars[kk]])

        if kk+1<len(stepwisePRF_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=stepwisePRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[0]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePRF_vars[kk]]) #binding it and assigning a text to it
            


            frsttext, button_options = button_init(stepwisePRF_vals[kk])
            button_stepwisePRF_vals4 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwisePRF_vals4),
                    **button_options
                    )
            button_stepwisePRF_vals4.place(relx=RELXStemp[0]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict2[stepwisePRF_vars[kk]] = get_toggle_output(button_stepwisePRF_vals4)
            # print(self.outputDict2[stepwisePRF_vars[kk]])
        if kk+1<len(stepwisePRF_vars):
            kk+=1
            lbl1 = ttk.Label(self, text=stepwisePRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[1]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwisePRF_vars[kk]]) #binding it and assigning a text to it

            frsttext, button_options = button_init(stepwisePRF_vals[kk])
            button_stepwisePRF_vals5 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwisePRF_vals5),
                    **button_options
                    )
            button_stepwisePRF_vals5.place(relx=RELXStemp[1]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict2[stepwisePRF_vars[kk]] = get_toggle_output(button_stepwisePRF_vals5)
            # print(self.outputDict2[stepwisePRF_vars[kk]])

            # kk+=1
        
        #######
        lbl1 = ttk.Label(self, text="S-RF Stepwise:", **labHeadOptions, relief=RIDGE)
        RELY += RELHEIGHT+0.01 
        lbl1.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=5*RELWIDTH)

        stepwiseSRF_vars = list(stepwiseDict['srf_stepwise'].keys())
        stepwiseSRF_vals = list(stepwiseDict['srf_stepwise'].values())
        kk=0
        RELWIDTHtemp1 = 0.2
        RELWIDTHtemp2 = 0.1
        RELWIDTHtemp3 = 0.03
        RELXStemp = np.linspace(0,1,4)
        self.outputDict3 = {}



        # while kk<len(stepwiseSRF_vars):
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text=stepwiseSRF_vars[kk]+":", **label_options)
        lbl1.place(relx=RELXStemp[0]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

        ## hover description
        lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
        lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwiseSRF_vars[kk]]) #binding it and assigning a text to it
        


        frsttext, button_options = button_init(stepwiseSRF_vals[kk])
        button_stepwiseSRF_vals1 = Button(self, 
                text=frsttext,
                command=lambda: toggle_button(button_stepwiseSRF_vals1),
                **button_options
                )
        button_stepwiseSRF_vals1.place(relx=RELXStemp[0]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
        self.outputDict3[stepwiseSRF_vars[kk]] = get_toggle_output(button_stepwiseSRF_vals1)

        

        ##
        if kk+1<len(stepwiseSRF_vars):
            kk+=1
            lbl1 = ttk.Label(self, text=stepwiseSRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[1]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwiseSRF_vars[kk]]) #binding it and assigning a text to it

            frsttext, button_options = button_init(stepwiseSRF_vals[kk])
            button_stepwiseSRF_vals2 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwiseSRF_vals2),
                    **button_options
                    )
            button_stepwiseSRF_vals2.place(relx=RELXStemp[1]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict3[stepwiseSRF_vars[kk]] = get_toggle_output(button_stepwiseSRF_vals2)

            

        if kk+1<len(stepwiseSRF_vars):
            kk+=1
            lbl1 = ttk.Label(self, text=stepwiseSRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[2]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwiseSRF_vars[kk]]) #binding it and assigning a text to it

            frsttext, button_options = button_init(stepwiseSRF_vals[kk])
            button_stepwiseSRF_vals3 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwiseSRF_vals3),
                    **button_options
                    )
            button_stepwiseSRF_vals3.place(relx=RELXStemp[2]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict3[stepwiseSRF_vars[kk]] = get_toggle_output(button_stepwiseSRF_vals3)

        if kk+1<len(stepwiseSRF_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=stepwiseSRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[0]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwiseSRF_vars[kk]]) #binding it and assigning a text to it
            


            frsttext, button_options = button_init(stepwiseSRF_vals[kk])
            button_stepwiseSRF_vals4 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwiseSRF_vals4),
                    **button_options
                    )
            button_stepwiseSRF_vals4.place(relx=RELXStemp[0]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict3[stepwiseSRF_vars[kk]] = get_toggle_output(button_stepwiseSRF_vals4)

        if kk+1<len(stepwiseSRF_vars):
            kk+=1
            lbl1 = ttk.Label(self, text=stepwiseSRF_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[1]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][stepwiseSRF_vars[kk]]) #binding it and assigning a text to it

            frsttext, button_options = button_init(stepwiseSRF_vals[kk])
            button_stepwiseSRF_vals5 = Button(self, 
                    text=frsttext,
                    command=lambda: toggle_button(button_stepwiseSRF_vals5),
                    **button_options
                    )
            button_stepwiseSRF_vals5.place(relx=RELXStemp[1]+RELWIDTHtemp1+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
            self.outputDict3[stepwiseSRF_vars[kk]] = get_toggle_output(button_stepwiseSRF_vals5)

            # kk+=1
    
    def getOutput1(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            outputResult[key] = value

        return outputResult

    def getOutput2(self):
        outputResult = {}
        for key, value in self.outputDict2.items():
            outputResult[key] = value
        return outputResult

    def getOutput3(self):
        outputResult = {}
        for key, value in self.outputDict3.items():
            outputResult[key] = value
        return outputResult
##############################################################################################
class DataSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pageArgs = pageArgsOut()
        RELY = 0
        RELHEIGHT, RELWIDTH = 0.05, 0.2
        RELXS = np.linspace(0,1,6)
        drelx = 0.01
        halfCellX = (RELXS[2]-RELXS[1])/2


        display_main_buttons(self,controller,RELXS, RELY, RELHEIGHT, RELWIDTH, *pageArgs, disabledBtn=None)
        RELY += RELHEIGHT+0.01 
        lbl1 = ttk.Label(self, text="Data Settings", **labHeadOptions)
        lbl1.configure(anchor="center")
        lbl1.place(relx=RELXS[1], rely=RELY, relheight=RELHEIGHT, relwidth=3*RELWIDTH)


        def back_prf():
            controller.show_frame(pageArgs[0])


        button_mode = Button(self, text="<<", command=back_prf, **button_options_BACK)

        button_mode.place(relx=RELXS[0], rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTH/2-drelx)

        
        dataSettings_vars = list(stepwiseDict['data_settings'].keys())
        dataSettings_vals = list(stepwiseDict['data_settings'].values())


        RELWIDTHtemp1 = 0.25
        RELWIDTHtemp2 = 0.2
        RELWIDTHtemp3 = 0.05
        RELXStemp = np.linspace(0,1,3)
        kk=0
        self.outputDict = {}
        
        def show_other_option(client, RELY_kk0):
            lbl1 = ttk.Label(self, text=client, **label_options)
            lbl1.configure(anchor="center")
            lbl1.place(relx=RELXStemp[1]+RELWIDTHtemp3, rely=RELY_kk0, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)
        
        while kk<len(dataSettings_vars):
            RELY += RELHEIGHT+0.01 
            lbl1 = ttk.Label(self, text=dataSettings_vars[kk]+":", **label_options)
            lbl1.place(relx=RELXStemp[0]+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp1)

            ## hover description
            lbl1_tooltip = Pmw.Balloon(self) #Calling the tooltip
            lbl1_tooltip.bind(lbl1,stdpydesc['stepwise'][dataSettings_vars[kk]]) #binding it and assigning a text to it
            

            if kk == 0:
                RELY_kk0 = RELY
                clientSel0 = tk.StringVar()
                clientOptions0 = ['All Available (*)','IRIS']
                clientSel0.set(clientOptions0[1])
                topo_drop = tk.OptionMenu(self,clientSel0, *clientOptions0)
                topo_drop.place(relx=RELXStemp[0]+RELWIDTHtemp2+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
   
                def change_dropdown0(*args):
                    print("Client is : ",clientSel0.get())
                    show_other_option(clientSel0.get(), RELY_kk0)
                show_other_option(clientSel0.get(), RELY_kk0)

                # link function to change dropdown
                clientSel0.trace('w', change_dropdown0)
                self.outputDict[dataSettings_vars[kk]] = clientSel0.get()
            elif kk == 1:
                RELY_kk1 = RELY
                clientSel1 = tk.StringVar()
                clientOptions = ['All Available (*)','TA']
                clientSel1.set(clientOptions[1])
                topo_drop = tk.OptionMenu(self,clientSel1, *clientOptions)
                topo_drop.place(relx=RELXStemp[0]+RELWIDTHtemp2+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
          
                show_other_option(clientSel1.get(),RELY_kk1)
   
                def change_dropdown1(*args):
                    print("Client is : ",clientSel1.get())
                    show_other_option(clientSel1.get(),RELY_kk1)

                # link function to change dropdown
                clientSel1.trace('w', change_dropdown1)
                self.outputDict[dataSettings_vars[kk]] = clientSel1.get()
            elif kk == 2:
                RELY_kk2 = RELY
                clientSel2 = tk.StringVar()
                clientOptions = ['All Available (*)','220A*']
                clientSel2.set(clientOptions[1])
                topo_drop = tk.OptionMenu(self,clientSel2, *clientOptions)
                topo_drop.place(relx=RELXStemp[0]+RELWIDTHtemp2+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
          
                show_other_option(clientSel2.get(),RELY_kk2)
   
                def change_dropdown1(*args):
                    print("Client is : ",clientSel2.get())
                    show_other_option(clientSel2.get(),RELY_kk2)

                # link function to change dropdown
                clientSel2.trace('w', change_dropdown1)
                self.outputDict[dataSettings_vars[kk]] = clientSel2.get()
            elif kk == 3:
                RELY_kk3 = RELY
                clientSel3 = tk.StringVar()
                clientOptions = ['BHZ,BHE,BHN']
                clientSel3.set(clientOptions[0])
                topo_drop = tk.OptionMenu(self,clientSel3, *clientOptions)
                topo_drop.place(relx=RELXStemp[0]+RELWIDTHtemp2+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
          
                show_other_option(clientSel3.get(),RELY_kk3)
   
                def change_dropdown1(*args):
                    print("Client is : ",clientSel3.get())
                    show_other_option(clientSel3.get(),RELY_kk3)

                # link function to change dropdown
                clientSel3.trace('w', change_dropdown1)
                self.outputDict[dataSettings_vars[kk]] = clientSel3.get()
            elif kk == 4:
                RELY_kk4 = RELY
                clientSel4 = tk.StringVar()
                clientOptions = ['""','00']
                clientSel4.set(clientOptions[1])
                topo_drop = tk.OptionMenu(self,clientSel4, *clientOptions)
                topo_drop.place(relx=RELXStemp[0]+RELWIDTHtemp2+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
          
                show_other_option(clientSel4.get(),RELY_kk4)
   
                def change_dropdown1(*args):
                    print("Client is : ",clientSel4.get())
                    show_other_option(clientSel4.get(),RELY_kk4)

                # link function to change dropdown
                clientSel4.trace('w', change_dropdown1)
                self.outputDict[dataSettings_vars[kk]] = clientSel4.get()
            else:
                entry1 = ttk.Entry(self)
                entry1.place(relx=RELXStemp[0]+RELWIDTHtemp2+RELWIDTHtemp3, rely=RELY, relheight=RELHEIGHT, relwidth=RELWIDTHtemp2)
                entry1.insert(0,dataSettings_vals[kk])
                self.outputDict[dataSettings_vars[kk]] = entry1

            kk+=1

    def getOutput(self):
        outputResult = {}
        for key, value in self.outputDict.items():
            outputResult[key] = value
        return outputResult
##############################################################################################


app = stadiumpyMain()
app.mainloop()