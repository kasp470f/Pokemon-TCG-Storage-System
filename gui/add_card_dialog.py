from calendar import Calendar
from tkinter import Button, Checkbutton, Frame, Image, IntVar, Label, Radiobutton, Text, Toplevel
from tkcalendar import DateEntry
import tkinter
import cv2 as cv
from PIL import Image, ImageTk
from data.dataset import url_to_image
from spreadsheet import CardData


class AddCardDialog:

    storageLocations = ["Storage Box 1", "Storage Box 2", "Storage Box 3", "Storage Box 4", "Storage Box 5", "Storage Box 6", 
                        "Storage Box 7", "Storage Box 8", "Storage Box 9", "Trade Binder", "Union Binder", "Toploader Binder", "Playable Tin", "Other"]

    def __init__(self, root, googleSheets, card):
        self.googleSheets = googleSheets
        self.new = Toplevel(root)
        self.new.geometry('900x500')
        self.new.resizable(False, False)
        self.new.title('Add to Collection - ' + card['Name'])
        self.card = card
        self.setup(self.new, card)
        

    def setup(self, window, card):
        img = url_to_image(card['Images']['large'])
        img = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(cv.resize(img, (300, 450)), cv.COLOR_BGR2RGB)))
        imageFrame = Label(window, image=img)
        imageFrame.config(borderwidth=2, relief='solid')
        imageFrame.image = img
        imageFrame.place(x=10, y=20, bordermode='inside')

        Label(window, text='Name:', font="Helvetica 9 bold").place(x=350, y=20)
        Label(window, text=card['Name']).place(x=390, y=20)
        Label(window, text='Card Number:', font="Helvetica 9 bold").place(x=350, y=40)
        Label(window, text=f"Card Number: {str(card['Set']['Number'])} / {str(card['Set']['PrintedTotal'])} ({str(card['Set']['TotalCards'])})").place(x=430, y=40)
        Label(window, text='Set:', font="Helvetica 9 bold").place(x=350, y=60)
        Label(window, text=card['Set']['Name']).place(x=375, y=60)


        conditionFrame = Frame(window, width=255, height=220)
        conditionFrame.place(x=350, y=80)
        conditionFrame.config(highlightbackground="#d3d3d3", highlightthickness=1)
        Label(conditionFrame, text='Condition:', font="Helvetica 9 bold").place(x=5, y=0)
        self.condition = IntVar(value=1)
        condition1 = Radiobutton(conditionFrame, text='Mint', variable=self.condition, value=1, tristatevalue=0)
        condition1.place(x=5, y=20)
        condition2 = Radiobutton(conditionFrame, text='Near Mint', variable=self.condition, value=2, tristatevalue=0)
        condition2.place(x=5, y=40)
        condition3 = Radiobutton(conditionFrame, text='Light Played', variable=self.condition, value=3, tristatevalue=0)
        condition3.place(x=5, y=60)
        condition4 = Radiobutton(conditionFrame, text='Played', variable=self.condition, value=4, tristatevalue=0)
        condition4.place(x=5, y=80)
        condition5 = Radiobutton(conditionFrame, text='Damaged', variable=self.condition, value=5, tristatevalue=0)
        condition5.place(x=5, y=100)
        self.conditionNotesText = Text(conditionFrame, width=30, height=5)
        self.conditionNotesText.place(x=5, y=120)

        printingTypeFrame = Frame(window, width=230, height=220)
        printingTypeFrame.place(x=655, y=80)
        printingTypeFrame.config(highlightbackground="#d3d3d3", highlightthickness=1)
        Label(printingTypeFrame, text='Printing Type:', font="Helvetica 9 bold").place(x=5, y=0)
        self.printingType = tkinter.StringVar()
        self.printingType1 = Radiobutton(printingTypeFrame, text='Normal', variable=self.printingType, value="Normal", tristatevalue=0)
        self.printingType1.place(x=5, y=20)
        self.printingType2 = Radiobutton(printingTypeFrame, text='Holofoil', variable=self.printingType, value="Holofoil", tristatevalue=0)
        self.printingType2.place(x=5, y=40)
        self.printingType3 = Radiobutton(printingTypeFrame, text='Reverse Holofoil', variable=self.printingType, value="Reverse Holofoil", tristatevalue=0)
        self.printingType3.place(x=5, y=60)
        self.printingType4 = Radiobutton(printingTypeFrame, text='1st Edition', variable=self.printingType, value="1st Edition", tristatevalue=0) 
        self.printingType4.place(x=5, y=80)
        self.printingType5 = Radiobutton(printingTypeFrame, text='1st Edition Holofoil', variable=self.printingType, value="1st Edition Holofoil", tristatevalue=0)
        self.printingType5.place(x=5, y=100)
        self.printingType6 = Radiobutton(printingTypeFrame, text='Unlimited', variable=self.printingType, value="Unlimited", tristatevalue=0)
        self.printingType6.place(x=5, y=120)
        self.printingType7 = Radiobutton(printingTypeFrame, text='Unlimited Holofoil', variable=self.printingType, value="Unlimited Holofoil", tristatevalue=0)
        self.printingType7.place(x=5, y=140)
        self.setPrintingTypes(card)

        self.overridePrintingTypeValue = tkinter.IntVar()
        self.overridePrintingType = Checkbutton(printingTypeFrame, text='Override', variable=self.overridePrintingTypeValue, onvalue=1, offvalue=0, command=self.togglePrintingType)
        self.overridePrintingType.place(x=5, y=170)

        miscFrame = Frame(window, width=255, height=145)
        miscFrame.place(x=350, y=330)
        miscFrame.config(highlightbackground="#d3d3d3", highlightthickness=1)
        Label(miscFrame, text='Miscellaneous:', font="Helvetica 9 bold").place(x=5, y=0)

        Label(miscFrame, text='Location:').place(x=5, y=20)
        self.locationDropdown = tkinter.StringVar()
        self.locationDropdown.set(self.storageLocations[0])
        self.locationDropdownMenu = tkinter.OptionMenu(miscFrame, self.locationDropdown, *self.storageLocations)
        self.locationDropdownMenu.config(background='white', highlightbackground="#7a7a7a", highlightthickness=1, width=17, border=0)
        self.locationDropdownMenu.place(x=5, y=40)

        # add a calendar to select date obtained
        Label(miscFrame, text='Date Obtained:').place(x=5, y=70)
        self.dateObtainedCalender = DateEntry(miscFrame, width=20, date_pattern='dd/mm/yyyy')
        self.dateObtainedCalender.place(x=5, y=90)
        self.noDateValue = tkinter.IntVar()
        self.noDate = Checkbutton(miscFrame, text='Unknown date', variable=self.noDateValue, onvalue=1, offvalue=0, command=self.toggleDate)
        self.noDate.place(x=5, y=115)
        
        finalFrame = Frame(window, width=230, height=145)
        finalFrame.place(x=655, y=330)
        finalFrame.config(highlightbackground="#d3d3d3", highlightthickness=1)
        # add card to database
        self.addToDatabase = Button(finalFrame, text='Add to Database', command=self.addToDatabase)
        self.addToDatabase.place(x=5, y=90)
        

    def setPrintingTypes(self, card):
        if "normal" not in card["PrintingTypes"]:
            self.printingType1.config(state='disabled')
        if "holofoil" not in card["PrintingTypes"]:
            self.printingType2.config(state='disabled')
        if "reverseHolofoil" not in card["PrintingTypes"]:
            self.printingType3.config(state='disabled')
        if "1stEdition" not in card["PrintingTypes"]:
            self.printingType4.config(state='disabled')
        if "1stEditionHolofoil" not in card["PrintingTypes"]:
            self.printingType5.config(state='disabled')
        if "unlimited" not in card["PrintingTypes"]:
            self.printingType6.config(state='disabled')
        if "unlimitedHolofoil" not in card["PrintingTypes"]:
            self.printingType7.config(state='disabled')

        # set the default printing type to the first available printing type
        if self.printingType1['state'] == 'normal':
            self.printingType.set("Normal")
        elif self.printingType2['state'] == 'normal':
            self.printingType.set("Holofoil")
        elif self.printingType3['state'] == 'normal':
            self.printingType.set("Reverse Holofoil")
        elif self.printingType4['state'] == 'normal':
            self.printingType.set("1st Edition")
        elif self.printingType5['state'] == 'normal':
            self.printingType.set("1st Edition Holofoil")
        elif self.printingType6['state'] == 'normal':
            self.printingType.set("Unlimited")
        elif self.printingType7['state'] == 'normal':
            self.printingType.set("Unlimited Holofoil")
        

    def togglePrintingType(self):
        if self.overridePrintingTypeValue.get() == 1:
            self.printingType1.config(state='normal')
            self.printingType2.config(state='normal')
            self.printingType3.config(state='normal')
            self.printingType4.config(state='normal')
            self.printingType5.config(state='normal')
            self.printingType6.config(state='normal')
            self.printingType7.config(state='normal')
        else:
            self.setPrintingTypes(self.card)

    def toggleDate(self):
        if self.noDateValue.get() == 1:
            self.dateObtainedCalender.config(state='disable')
        else:
            self.dateObtainedCalender.config(state='normals')

    def addToDatabase(self):
        _newCard = CardData(self.card)
        _newCard.Condition = self.condition.get()
        _newCard.ConditionNotes = self.conditionNotesText.get("1.0", "end-1c")
        _newCard.PrintingType = self.printingType.get()
        _newCard.Location = self.locationDropdown.get()
        
        if self.noDateValue.get() != 1:
            _newCard.DateObtained = self.dateObtainedCalender.get_date()
        
        self.googleSheets.addCardExtended(_newCard)
        self.addToDatabase.config(state='disabled')
        self.new.after(2000, self.new.destroy())




        
        
