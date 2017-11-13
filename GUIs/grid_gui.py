#!usr/bin/python

import tkFont
import Tkinter as tk

class Account(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.grid()
        self.canvas = tk.Canvas(self, width=1000, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.grid(column=0, row=1, padx=15, pady=15)
        self.rows = 10
        self.columns = 10
        self.cellwidth = 100
        self.cellheight = 25

        self.headerfont = tkFont.Font(family="futura", size=32)

        welcomelabel = tk.Label(self, text="Dashboard", anchor="ne"
                                     , fg ="black", font=self.headerfont)
        welcomelabel.grid(pady=10, 
                          padx=15, column=0, row=0) 
        # code should look like for each $acc draw row 
        header = ["", "Account", "Username", "Password"]
        self.rect = {}
        for column in range(4):
            for row in range(1):
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


#@params account to add
def addAccount():
    pass
    
if __name__ == "__main__":
    acc = Account()
    acc.mainloop()
