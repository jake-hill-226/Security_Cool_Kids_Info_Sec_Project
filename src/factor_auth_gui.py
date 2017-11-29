#!usr/bin/python

# Written by Phaedra Paul
# Rudimentary GUI with buttons for 2 Factor authentication.
import tkFont
import Tkinter as tk
import ctypes
from PIL import Image, ImageTk
import controller


class Auth(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.grid()
        self.initialize()
        
    def initialize(self):
        self.headerfont = tkFont.Font(family="futura", size=12)

        #shows reason for popup
        label = tk.Label(
            self, text="You've entered your password incorrectly 3 times. Please verify your identity.",
            anchor="ne", fg ="black", font=self.headerfont
        )
        label.grid(pady=10, padx=15, column=0, row=0) 

        #contains buttons for validation, email, text, and entry field
        #for verification code
        self.emailbtn = tk.Button(self)
        self.textbtn = tk.Button(self)
        self.validate = tk.Button(self)
        self.validateentry = tk.Entry(self)

        #place entites
        self.emailbtn.grid(column=0, row=1, pady=5)
        self.textbtn.grid(column=0, row=2,  pady=5)
        self.validateentry.grid(column=0, row=3,  pady=(10, 5))
        self.validate.grid(column=0, row=4, pady=5)

        #bind buttons to function calls
        self.emailbtn.bind("<Button-1>", send_email)
        self.textbtn.bind("<Button-1>", text_msg)
        self.validate.bind("<Button-1>", validate_code)

        #set button text
        self.emailbtn["text"] = "Confirm via Email"
        self.textbtn["text"] = "Receive text message"
        self.validate["text"] = "Validate"

#sends email to user for auth
def send_email(event):
    print "Send Email to User"

#send text to user for auth
def text_msg(event):
    print "Will send Text Message to User"

#checks validation code
def validate_code(event):
    print "Validation Code"

