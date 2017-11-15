#!usr/bin/python

import Tkinter as tk
import tkFont
from PIL import Image, ImageTk
import ctypes
import grid_gui

class login_gui(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.grid()
        self.initialize()
    
    def initialize(self):
        pad = 15
        ico = ImageTk.PhotoImage(Image.open("../assets/corpCarrot.gif").resize((250,250)))
        self.icoLab = tk.Label(image=ico)
        self.icoLab.image = ico
        
        self.icoLab.grid(column=0, row = 0, sticky="N")

        self.welcomestr = tk.StringVar()
        self.welcomestr.set("Welcome To CarrotKey!")
        self.userstr= tk.StringVar()
        self.userstr.set("Username")
        self.passwordstr = tk.StringVar()
        self.passwordstr.set("Password")

        # change me to lato at some point
        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = tk.Label(self, textvariable=self.welcomestr, anchor="n"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(column=0, row=1, columnspan=2, sticky="EW", pady=10, 
                          padx=pad)
        userlabel = tk.Label(self, textvariable=self.userstr, anchor="n", 
                                  fg="white", bg="orange")
        userlabel.grid(column=0, row=2, columnspan=2, sticky="EW", pady=pad)
        passwordlabel = tk.Label(self, textvariable=self.passwordstr, anchor="n", 
                                  fg="white", bg="orange")
        passwordlabel.grid(column=0, row=4, columnspan=2, sticky="EW", pady=pad)

        #username entry field
        self.entry = tk.Entry(self)
        self.entry.grid(column=0, row=3, sticky="N")
        #password entry field
        self.entry = tk.Entry(self, show=u"*")
        self.entry.grid(column=0, row=5, sticky='N')

        self.button = tk.Button(self)
        self.button["text"] ="Login"
        self.button["command"] = self.checkAuth

        self.button.grid(column=0, row=7, pady=(0, pad))
        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)

        rememberMe = tk.Checkbutton(self, text="Remember Me")
        rememberMe.grid(column=0, row=6)

    def checkAuth(self):
        auth = False
        if not auth:
            self.onDeny()

    def onDeny(self):
        self.exitico = ImageTk.PhotoImage(Image.open("../assets/logout.png").resize((100,50)))
        self.denyEntry = tk.Label(self, text="The Password or Username Entered Was Incorrect.")

    def onAuth(self):
        self.destroy()
        grid_gui.Account()

if __name__ == "__main__":
    # the class has no parent becaue it is the root
    app = login_gui(None)
    app.geometry("400x600")
    app.title('CarrotKey')

    def destroy(self):
        app.destroy()
    # program will loop to wait for events. 
    app.mainloop()
