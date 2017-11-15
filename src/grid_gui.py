#!usr/bin/python

import tkFont
import Tkinter as tk
import ctypes
from PIL import Image, ImageTk
import controller


class Account(tk.Tk):
    def __init__(self, username, password, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.grid()
        self.canvas = tk.Canvas(self, width=1000, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.grid(column=0, row=1, padx=15, pady=15)
        self.rows = 10
        self.columns = 10
        self.cellwidth = 100
        self.cellheight = 25

        self.auth_username = username
        self.auth_pwd = password

        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = tk.Label(self, text="Dashboard", anchor="ne"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(pady=10, 
                          padx=15, column=0, row=0) 
        buildTable(self,username, password)
        self.logoutimg = ImageTk.PhotoImage(Image.open("../assets/logout.gif").resize((100,50)))
        self.settingsimg =  ImageTk.PhotoImage(Image.open("../assets/settings.gif").resize((50,50)))
        self.settings = tk.Label(image= self.settingsimg)
        self.settings.image = self.settingsimg

        self.settings.grid(column=0, row=1, sticky="ne")
 
def buildTable(self, username, password):
    entries = controller.search_vault(username)

    header = ["", "Account", "Username", "Password"]
    self.rect = {}
    for column in range(4):
        for row in range(len(entries) + 1):
            x1 = column * self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            xC = (x1+x2)/2
            yC = (y1+y2)/2
            # dont draw box at 0,0
            if column == 0 and row == 0:
                pass
            #numbered boxes far left are slightly smaller than their larger counterparts
            elif column == 0 and row != 0:
               self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="lightgrey", tags="rect")
               self.canvas.create_text((xC,yC), text=row)
            elif row == 0 and column != 0:
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="orange", tags="rect")
                self.canvas.create_text((xC, yC), text=header[column])
            else: 
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")


                content = None
                if column == 1:
                    content = entries[row - 1].url
                elif column == 2:
                    content = entries[row - 1].username
                elif column == 3:
                    content = controller.retrieve_pass(entries[row-1].username, entries[row-1].url, password)

                self.canvas.create_text((xC, yC), text=content)
if __name__ == "__main__":
    acc = Account("jake", "temp")
    acc.title('CarrotKey')
    acc.mainloop()
