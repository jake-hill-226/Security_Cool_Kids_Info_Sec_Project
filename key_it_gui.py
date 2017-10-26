#!usr/bin/python

from tkinter import *

class Key_It:
    def __init__(self, master):
        self.master = master
        master.title("Key.It!")

        self.label = Label(master, text="Welcome to Key.It!")
        self.label.pack()

        self.greet_button = Button(master, text="Start", command=self.start)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        #Layout
    def start(self):
        # If it's first launch Create Master Password for application
        #                       Call Setup  2FA for Master Pwd?
        #             Call "Main" Page should have button where you can "Add 'Database' I.E. 'School Passwords'
        #                       Create folder on disk
        #                       then a form should pop up where username and pwd is filled out but also  has an
        #                        Auto Generate Button -> Then a Save button which initiates an encryption and writes
        #                       to appropriate folder/to/file on disk
        #             Bring back to Main Page
        #Else Ask for Master password
        #     if correct:
        #         2FA
        #         if 2FA_Passed:
        #         Go to Main Page
        #         Should have "open database" and "add database"
        #         When Double_click = True
        #             Initiate decryption and retrieval
        #             Open up account info

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
