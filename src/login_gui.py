#!usr/bin/python

# Created by Phaedra Paul 
# This code creates a login window with the CarrotKey logo.
# External Libararies used: Tkinter for GUI, PIL for image support, Tkfont for font support.

import Tkinter as tk
import tkFont
from PIL import Image, ImageTk
import ctypes
import grid_gui
import CarrotDB
import vault_encrypt as vault
import factor_auth_gui

class login_gui(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.grid()
        self.initialize()

        self.auth_count = 0
    
    def initialize(self):
        pad = 15

        #corporal carrot image logo
        ico = ImageTk.PhotoImage(Image.open("../assets/corpCarrot.gif").resize((250,250)))
        self.icoLab = tk.Label(image=ico)
        self.icoLab.image = ico

        self.icoLab.grid(column=0, row = 0, sticky="N")

        #header
        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = tk.Label(self, text="Welcome To CarrotKey!", anchor="n"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(column=0, row=1, columnspan=2, sticky="EW", pady=10, 
                          padx=pad)

        #usenname and password labels
        userlabel = tk.Label(self, text="Username", anchor="n", 
                                  fg="white", bg="orange")
        userlabel.grid(column=0, row=2, columnspan=2, sticky="EW", pady=pad)
        passwordlabel = tk.Label(self, text="Password", anchor="n", 
                                  fg="white", bg="orange")
        passwordlabel.grid(column=0, row=4, columnspan=2, sticky="EW", pady=pad)

        #username entry field
        self.username = tk.Entry(self)
        self.username.grid(column=0, row=3, sticky="N")
        #password entry field
        self.password = tk.Entry(self, show=u"*")
        self.password.grid(column=0, row=5, sticky='N')

        self.button = tk.Button(self)
        self.button["text"] ="Login"
        self.button["command"] = self.checkAuth
        self.button["pady"] = 15

        self.button.grid(column=0, row=7, pady=(0, pad))
        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)

    #checks if input matches. on 3 failed attempts, calls 2 factor auth code
    def checkAuth(self):
        self.un = self.username.get()
        self.pw = self.password.get()
        auth = vault.auth_user(self.un, self.pw)
        if not auth:
            self.onDeny()
            self.auth_count += 1
            if self.auth_count == 3:
                self.onValidate()
        else:
            self.onAuth()

    #displays incorrect entry to user
    def onDeny(self):
        denyfont = tkFont.Font(family="futura", size=11)
        self.incor = tk.Label(self, text="The Password or Username Entered Was Incorrect.", fg=
                              "red", pady=5, font=denyfont)
        self.incor.grid(column=0, row=6)

    # if properly authenticated, destroys window and opens the gui.
    def onAuth(self):
        self.destroy()
        grid_gui.Account(self.un, self.pw)

    #if 3 failed attempts, destroys current window and opens 2 fator auth gui
    def onValidate(self):
        self.destroy()
        factor_auth_gui.Auth()

#main application loop
if __name__ == "__main__":
    # the class has no parent becaue it is the root
    app = login_gui(None)
    app.geometry("400x600")
    app.title('CarrotKey')

    def destroy(self):
        app.destroy()
    # program will loop to wait for events. 

    app.mainloop()
