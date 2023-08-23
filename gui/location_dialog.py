from msilib import Table
from tkinter import Button, Text, Toplevel
from tkinter.ttk import Treeview

from services.database import Database


class Location_Dialog:

    def __init__(self, root, database: Database):
        self.new = Toplevel(root)
        self.new.grab_set()
        self.new.geometry('900x500')
        self.new.resizable(False, False)
        self.new.title("Location Management")
        self.new.wm_iconbitmap('assets/icon.ico')
        self.db = database

        self.setupGui()

    def setupGui(self):
        self.table = Treeview(self.new, columns=('Id', 'Location Name', 'Date Created'), show='headings', height=23)
        self.table.heading('Id', text='Id')
        self.table.heading('Location Name', text='Location Name')
        self.table.heading('Date Created', text='Date Created')
        self.table.column('Id', width=50)
        self.table.column('Location Name', width=300)
        self.table.column('Date Created', width=300)
        self.table.place(x=20, y=0)

        self.addText = Text(self.new, height=2, width=20)
        self.addText.place(x=700, y=100)
        add = Button(self.new, text='Add location', command=self.addLocation)
        add.place(x=750, y=140)

        # TODO: Add buttons to edit

        delete = Button(self.new, text='Delete location', command=self.deleteLocation)
        delete.place(x=750, y=450)
        

        self.refreshTable()

    def refreshTable(self):
        self.table.delete(*self.table.get_children())
        locations = self.db.get_locations()
        for location in locations:
            self.table.insert('', 'end', values=(location.id, location.name, location.date_created))

    def addLocation(self):
        name = self.addText.get("1.0", 'end-1c')
        for location in self.db.get_locations(): 
            if location.name == name:
                print("Location already exists")
                return
            
        self.db.insert_location(name)
        self.refreshTable()
        self.addText.delete("1.0", 'end-1c')

    def deleteLocation(self):
        selected = self.table.focus()
        if selected:
            id = self.table.item(selected)['values'][0]
            self.db.delete_location(id)
            self.table.delete(selected)


        