#!usr/bin/python

import Tkinter as tk
import tkFont
from PIL import Image, ImageTk
import ctypes
import grid_gui
import CarrotDB
import vault_encrypt as vault

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

        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = tk.Label(self, text="Welcome To CarrotKey!", anchor="n"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(column=0, row=1, columnspan=2, sticky="EW", pady=10, 
                          padx=pad)
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

    def checkAuth(self):
        auth = vault.auth_user(self.username.get(), self.password.get())
        if not auth:
            self.onDeny()
        else:
            self.onAuth()

    def onDeny(self):
        denyfont = tkFont.Font(family="futura", size=11)
        self.incor = tk.Label(self, text="The Password or Username Entered Was Incorrect.", fg=
                              "red", pady=5, font=denyfont)
        self.incor.grid(column=0, row=6)

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
