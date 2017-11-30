#!usr/bin/python

# Written by Phaedra Paul and Jake Hill
# Displays a dymanic grid with the user's passwords, usernames, and sites used.

import tkFont
import Tkinter as tk
import ctypes
from PIL import Image, ImageTk
import controller


class Account(tk.Tk):
    def __init__(self, username, password, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #initialize canvas for drawing
        self.grid()
        self.canvas = tk.Canvas(self, width=1000, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.grid(column=0, row=1, padx=15, pady=15)
        self.rows = 10
        self.columns = 10
        self.cellwidth = 150
        self.cellheight = 25

        self.auth_username = username
        self.auth_pwd = password

        #Header, showing that this is the Dashboard
        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = tk.Label(self, text="Dashboard", anchor="ne"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(pady=10, 
                          padx=15, column=0, row=0) 

        #Builds a table from input username, password
        buildTable(self,username, password)

        
        #icons that link to functions, Logout, settings and add. Was unable to link these functions to 
        #actual db due to time constraints.
        self.logoutimg = ImageTk.PhotoImage(Image.open("../assets/logout.gif").resize((100,50)))
        self.logout = tk.Label(image=self.logoutimg)
        self.logout.image = self.logoutimg

        self.settingsimg =  ImageTk.PhotoImage(Image.open("../assets/settings.gif").resize((25,25)))
        self.settings = tk.Label(image= self.settingsimg)
        self.settings.image = self.settingsimg

        self.plus = ImageTk.PhotoImage(Image.open("../assets/add.gif").resize((25,25))) 
        self.plusi = tk.Label(image= self.plus)
        self.plusi.image = self.plus

        self.plusi.grid(column=1, row=2, padx=25, pady=25)
        self.settings.grid(column=1, row=0, sticky="ne", padx=(0, 25), pady=(25,0))
        self.settings.bind("<Button-1>", open_settings)
        self.plusi.bind("<Button-1>", add_password)


# o
def buildTable(self, username, password):
    entries = controller.search_vault(username)

    #header row shows
    header = ["", "Account", "Username", "Password","Paste"]
    self.rect = {}
    self.but = {}
    self.pwd = []

    for column in range(5):
        for row in range(len(entries) + 1):

            #calculates coordinates for x and y for each cell for drawing rectangles
            x1 = column * self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight

            #coordinates of center of rectangle for centering text
            xC = (x1+x2)/2
            yC = (y1+y2)/2
            # dont draw box at 0,0, this is the corner box.
            if column == 0 and row == 0:
                pass

            #numbered boxes far left
            elif column == 0 and row != 0:
               self.rect[row,column] = self.canvas.create_rectangle(
                   x1,y1,x2,y2, fill="lightgrey", tags="rect", outline="grey"
               )
               self.canvas.create_text((xC,yC), text=row)

            # styling of header row
            elif row == 0 and column != 0:
                self.rect[row,column] = self.canvas.create_rectangle(
                    x1,y1,x2,y2, fill="orange", tags="rect",outline="dimgrey"
                )
                self.canvas.create_text((xC, yC), text=header[column])

            #draw and style other boxes in grid.
            else: 
                self.rect[row,column] = self.canvas.create_rectangle(
                    x1,y1,x2,y2, fill="navajowhite", tags="rect", outline="grey"
                )
                content = ""
                tag = ""
                if column == 1:
                    content = entries[row - 1].url
                    tag = str(row) + '-url'
                elif column == 2:
                    content = entries[row - 1].username
                    tag = str(row) + '-usrname'
                elif column == 3:
                    content = controller.retrieve_pass(entries[row-1].username, entries[row-1].url, password)
                    self.pwd.append(content)
                    tag = str(row) + '-pwd'
                con = trim_text(content)
                self.canvas.create_text((xC, yC), text=con, tags=tag)

            # draws an oval used as a button inside of last column for copy paste
            if column == 4 and row != 0:
                self.rect[row,column] = self.canvas.create_rectangle(
                    x1,y1,x2,y2, fill="navajowhite", tags="rect", outline="grey"
                )
                self.but[row,column] = self.canvas.create_oval(x1+33,y1+2,x2-33,y2-2, fill="darkolivegreen", outline="darkgrey", tags=str(row)+"-bt")

                def __bt_handeler(event,self=self,row=row-1):
                    return on_copy_click(self,event,row)

                self.canvas.tag_bind(str(row) + "-bt", '<ButtonPress-1>', __bt_handeler)

#function called when button is clicked on the end of the row. securely simulates an alt tab and types password in 
#requested field. Written by Jake
def on_copy_click(self, event, row):
    password = self.pwd[row]

    controller.sim_Alt_Tab()
    controller.sim_typing(password)

#unlinked function to configure settings. this would have been an alternate GUI that could change a persistent user settings
#file for each such as preferred encryption, change password, purge db. 
def open_settings(event):
    print "settings open"

#unlinked function to add password to db
def add_password(event):
    print "add new password"

#used to trim longer passwords so they don't overflow the table.
def trim_text(text):
    if len(text) > 15:
        text = text[:12] + '...'
    return text
