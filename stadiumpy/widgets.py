import stadiumpy.basewidget as tkb

class SFrame(tkb.SFrameBase):
    """### Scrollable Frame ButtonBase.    
    (Only supports vertical scrolling)

    Sames as tkinter Frame. These are some extra resources.
    - `scrollbarwidth`: Set the width of scrollbar.
    - `mousewheel`: Set mousewheel scrolling.
    - `avoidmousewheel`: Give widgets that also have mousewheel scrolling and is a child of SFrame \
        this will configure widgets to support their mousewheel scrolling as well. \
        For eg:- Text widget inside SFrame can have mousewheel scrolling as well as SFrame.

    Scrollbar of SFrame can be configured by calling `scrollbar_configure(**options)`. 
    To access methods of the scrollbar it can be called through the scrollbar instance `self['scrollbar']`.

    ### How to use?
    Use it like a normal frame.

    ### Example:

        root = Tk()
        frame = SFrame(root, bg='pink')
        frame.pack()

        for i in range(100):
            Button(frame, text='Button %s'%i).pack()

        root.mainloop()
    """
    def __init__(self, master=None, cnf={}, **kw):
        tkb.SFrameBase.__init__(self, master=master, cnf=cnf, **kw)
        # Extra functions
        self.scrollbar_configure = self['scrollbar'].configure

class Button(tkb.ButtonBase):
    """ Button for macos, supports almost all the features of tkinter button,
    - Looks very similar to ttk Button.
    - There are few extra features as compared to default Tkinter Button:
    - To check the list of all the resources. To get an overview about
        the allowed keyword arguments call the method `keys`. 
            print(Button().keys())

    ### Examples:
        import tkinter as tk
        import tkmacosx as tkm
        import tkinter.ttk as ttk

        root = tk.Tk()
        root.geometry('200x200')
        tkm.Button(root, text='Mac OSX', bg='lightblue', fg='yellow').pack()
        tk.Button(root, text='Mac OSX', bg='lightblue', fg='yellow').pack()
        ttk.Button(root, text='Mac OSX').pack()
        root.mainloop()

    ### Get a cool gradient effect in activebackground color.
        import tkinter as tk
        import tkmacosx as tkm
        
        root = tk.Tk()
        root.geometry('200x200')
        tkm.Button(root, text='Press Me!!', activebackground=('pink','blue') ).pack()
        tkm.Button(root, text='Press Me!!', activebackground=('yellow','green') ).pack()
        tkm.Button(root, text='Press Me!!', activebackground=('red','blue') ).pack()
        root.mainloop()"""

    # all the instance of class Button will be stored in _button list.

    def __init__(self, master=None, cnf={}, **kw):
        tkb.ButtonBase.__init__(self, master=master, cnf=cnf, **kw)

    def invoke(self):
        """Invoke the command associated with the button.

        The return value is the return value from the command,
        or an empty string if there is no command associated with
        the button. This command is ignored if the button's state
        is disabled.
        """
        if self['state'] not in ('disable', 'disabled'):
            return self.cnf['command']() if self.cnf.get('command') else None
