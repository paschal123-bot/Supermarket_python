# import all the modules
from tkinter import *
import sqlite3

conn = sqlite3.conn("D:\Store Management Software\Database\store.db")
c = conn.cursor()

class Database:
    def __init__(self, *args,  **kwargs):
        
        self.master = "master"
        self.heading = Label("master", text='Add to the database', font=("arial 40 bold"), fg='steelblue')
        self.heading.place(x=250 , y=0)
    
        # labels and entries for the window
        
        
        
root = Tk()
b = Database(root)

root.geometry("1366*768+0+0")
root.geometry("Add to the database") 
root.mainloop()       
        
        