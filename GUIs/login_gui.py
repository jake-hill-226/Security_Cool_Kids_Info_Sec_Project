#!usr/bin/python

import Tkinter

class login_gui(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        
        self.userstr= Tkinter.StringVar()
        self.userstr.set("Username")
        self.passwordstr = Tkinter.StringVar()
        self.passwordstr.set("Password")

        userlabel = Tkinter.Label(self, textvariable=self.userstr, anchor="n", 
                                  fg="white", bg="orange")
        userlabel.grid(column=0, row=0, columnspan=2, sticky="EW")
        passwordlabel = Tkinter.Label(self, textvariable=self.passwordstr, anchor="n", 
                                  fg="white", bg="orange")
        passwordlabel.grid(column=0, row=2, columnspan=2, sticky="EW")

        #username entry field
        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=0, row=1, sticky="N")
        #password entry field
        self.entry = Tkinter.Entry(self)
        self.entry.grid(column=0, row=3, sticky='N')

        button = Tkinter.Button(self, text=u"Login", command="self.onPress")
        button.grid(column=0, row=4)
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

    def onPress(self):
        print "The button was pressed."

if __name__ == "__main__":
    # the class has no parent becaue it is the root
    app = login_gui(None)
    app.title('CarrotKey')
    # program will loop to wait for events. 
    app.mainloop()
