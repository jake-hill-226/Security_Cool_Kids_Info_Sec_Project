#!usr/bin/python

import Tkinter
import tkFont
from PIL import Image, ImageTk

class login_gui(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        pad = 15
        self.grid()
        ico = ImageTk.PhotoImage(Image.open("../assets/corpCarrot.gif").resize((250,250)))
        self.icoLab = Tkinter.Label(image=ico)
        self.icoLab.image = ico
        
        self.icoLab.grid(column=0, row = 0, sticky="N")

        self.welcomestr = Tkinter.StringVar()
        self.welcomestr.set("Welcome To CarrotKey!")
        self.userstr= Tkinter.StringVar()
        self.userstr.set("Username")
        self.passwordstr = Tkinter.StringVar()
        self.passwordstr.set("Password")

        # change me to lato at some point
        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = Tkinter.Label(self, textvariable=self.welcomestr, anchor="n"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(column=0, row=1, columnspan=2, sticky="EW", pady=10, 
                          padx=pad)
        userlabel = Tkinter.Label(self, textvariable=self.userstr, anchor="n", 
                                  fg="white", bg="orange")
        userlabel.grid(column=0, row=2, columnspan=2, sticky="EW", pady=pad)
        passwordlabel = Tkinter.Label(self, textvariable=self.passwordstr, anchor="n", 
                                  fg="white", bg="orange")
        passwordlabel.grid(column=0, row=4, columnspan=2, sticky="EW", pady=pad)

        #username entry field
        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=0, row=3, sticky="N")
        #password entry field
        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=0, row=5, sticky='N')

        button = Tkinter.Button(self, text=u"Login", command="self.onPress", bg="orange"
                                , fg="white")
        button.grid(column=0, row=7, pady=(0, pad))
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

        rememberMe = Tkinter.Checkbutton(self, text="Remember Me")
        rememberMe.grid(column=0, row=6)


    def onPress(self):
        print("The button was pressed.")

if __name__ == "__main__":
    # the class has no parent becaue it is the root
    app = login_gui(None)
    app.title('CarrotKey')
    # program will loop to wait for events. 
    app.mainloop()
