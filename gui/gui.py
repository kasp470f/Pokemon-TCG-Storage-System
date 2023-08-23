from tkinter import Checkbutton, Frame, Image, IntVar, Menu, OptionMenu, Radiobutton, Label, Button, Tk
from tkcalendar import DateEntry
import tkinter
from PIL import Image, ImageTk
from gui.grading_dialog import Grading_Dialog
from gui.location_dialog import Location_Dialog
from models.card_dto import CardDto
import cv2 as cv
import numpy as np

from data.dataset import url_to_image
from models.grading_models import RawGrading
from services.database import Database

class Gui:
    cvSearchImage = None
    searchImg = None
    searched = False
    foundCard = None
    
    obtainedHow =  [ "Opened", "Bought", "Traded", "Other" ]

    def __init__(self, root: Tk, database: Database):
        self.root = root
        self.menu = Menu(root)

        self.root.config(menu=self.menu)
        self.database = database
        self.storageLocations = self.database.get_locations()
        # self.rawGrading = RawGrading()
        root.title("Pokémon Card Scanner")
        root.geometry('1600x800')
        root.resizable(False, False)
        root.wm_iconbitmap('assets/icon.ico')  

        self.setupMenu()
        self.setupGui(root)
        self.closed = False

    def setupMenu(self):
        fileMenu = Menu(self.menu, tearoff=0)
        fileMenu.add_command(label='Locations', command=self.openLocationWindow)
        fileMenu.add_command(label='Exit', command=self.onClose)
        self.menu.add_cascade(label='File', menu=fileMenu)

    def setupGui(self, root):
        # Camera frame which contains the detected image
        self.cameraFrame = Frame(root, width=350, height=600)
        self.cameraFrame.place(x=10, y=10)
        Label(self.cameraFrame, text='Camera Feed').place(x=120, y=10)
        ## Camera feed
        self.cameraFeed = Label(self.cameraFrame,  width=325, height=500, borderwidth=2, relief='solid')
        self.cameraFeed.place(x=0, y=40, bordermode='inside')
        self.setImageNone(self.cameraFeed)

        # Transform frame which contains the transformed image
        self.transformFrame = Frame(root, width=350, height=600)
        self.transformFrame.place(x=365, y=10)
        Label(self.transformFrame, text='Flattened Feed').place(x=115, y=10)
        Button(self.transformFrame, text='Capture', command=self.captureCurrentTransform).place(x=120, y=450)
        ## Transform feed
        self.transformFeed = Label(self.transformFrame,  width=300, height=400, borderwidth=2, relief='solid')
        self.transformFeed.place(x=0, y=40, bordermode='inside')
        self.setImageNone(self.transformFeed)

        # Card frame with a button to capture the image
        self.screenshotFrame = Frame(root, width=350, height=600)
        self.screenshotFrame.place(x=675, y=10)
        Label(self.screenshotFrame, text='Saved Screenshot').place(x=115, y=10)
        ## Card feed
        self.cardFeed = Label(self.screenshotFrame,  width=300, height=400, borderwidth=2, relief='solid')
        self.cardFeed.place(x=0, y=40, bordermode='inside')
        self.setImageNone(self.cardFeed)

        # line to separate the search frame from the camera frame
        Frame(root, width=2, height=500, bg='#e6e3e3').place(x=1030, y=50)

        # Search frame with a button to search the card
        self.searchFrame = Frame(root, width=350, height=600)
        self.searchFrame.place(x=1080, y=10)
        self.searchFeed = Label(self.searchFrame,  width=300, height=400, borderwidth=2, relief='solid')
        self.searchFeed.place(x=0, y=40, bordermode='inside')
        self.setImageNone(self.searchFeed)

        # Misc frame
        self.miscFrame = Frame(self.root, width=220, height=197)
        self.miscFrame.place(x=1384, y=403)
        self.miscFrame.config(highlightbackground="#d3d3d3", highlightthickness=1)
        Label(self.miscFrame, text='Miscellaneous:', font="Helvetica 9 bold").place(x=5, y=0)

        Label(self.miscFrame, text='Location:').place(x=5, y=20)
        self.locationDropdown = tkinter.Variable()
        self.refreshLocationDropdown();
        
        # add a calendar to select date obtained
        Label(self.miscFrame, text='Date Obtained:').place(x=5, y=70)
        self.dateObtainedCalender = DateEntry(self.miscFrame, width=20, date_pattern='dd/mm/yyyy')
        self.dateObtainedCalender.place(x=5, y=90)
        self.noDateValue = tkinter.IntVar()
        self.noDate = Checkbutton(self.miscFrame, text='Unknown date', variable=self.noDateValue, onvalue=1, offvalue=0, command=self.toggleDate)
        self.noDate.place(x=5, y=115)

        Label(self.miscFrame, text='Obtained How:').place(x=5, y=140)
        self.obtainedHowDropdown = tkinter.StringVar()
        self.obtainedHowDropdown.set(self.obtainedHow[0])
        self.obtainedHowDropdownMenu = tkinter.OptionMenu(self.miscFrame, self.obtainedHowDropdown, *self.obtainedHow)
        self.obtainedHowDropdownMenu.config(background='white', highlightbackground="#7a7a7a", highlightthickness=1, width=17, border=0)
        self.obtainedHowDropdownMenu.place(x=5, y=160)

        self.setupInfoFrame()

    def setImageNone(self, feed):
        blank = np.zeros((400, 300, 3), np.uint8)
        blank.fill(255)
        blank = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(blank, cv.COLOR_BGR2RGB)))
        feed.configure(image=blank)
        feed.image = blank
        
    def updateCameraFeed(self, img):
        if self.closed == False:
            cameraFeedImg = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(cv.resize(img, (325, 500)), cv.COLOR_BGR2RGB)))
            self.cameraFeed.configure(image=cameraFeedImg)
            self.cameraFeed.image = cameraFeedImg

    def updateTransformFeed(self, img):
        if self.closed == False:
            self.cvSearchImage = img
            transformFeedImg = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(cv.resize(img, (300, 400)), cv.COLOR_BGR2RGB)))
            self.transformFeed.configure(image=transformFeedImg)
            self.transformFeed.image = transformFeedImg
        
    def captureCurrentTransform(self):
        self.updateCardFeed(self.cvSearchImage.copy())

    def updateCardFeed(self, img):
        self.searchImg = img
        cardFeedImg = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(cv.resize(self.searchImg, (300, 400)), cv.COLOR_BGR2RGB)))
        self.cardFeed.configure(image=cardFeedImg)
        self.cardFeed.image = cardFeedImg
        self.searched = False

    def updateSearchFeed(self, card):
        img = url_to_image(card['Images']['large'])
        searchFeedImg = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(cv.resize(img, (300, 400)), cv.COLOR_BGR2RGB)))
        self.searchFeed.configure(image=searchFeedImg)
        self.searchFeed.image = searchFeedImg
        self.updateInfoFrame(card)


    def setupInfoFrame(self):
        # Information frame with below search feed
        self.infoFrame = Frame(self.root, width=304, height=150)
        self.infoFrame.config(highlightbackground="black", highlightthickness=2)
        self.infoFrame.place(x=1080, y=450)
        self.nameLabel = Label(self.infoFrame, text='Name:').place(x=10, y=10)
        self.cardNumberLabel = Label(self.infoFrame, text='Card Number:').place(x=10, y=40)
        self.setLabel = Label(self.infoFrame, text='Set:').place(x=10, y=70)
        self.cardRarityLabel = Label(self.infoFrame, text='Rarity:').place(x=10, y=100)

        self.cardDetailsSetup()

        # create a button but disable it until a card is found
        self.addToCollectionButton = Button(self.root, text='Add to Collection', command=self.addToCollection, state='disabled')
        self.addToCollectionButton.place(x=1160, y=610)

    def cardDetailsSetup(self):
        conditionFrame = Frame(self.root, width=220, height=150)
        conditionFrame.place(x=1384, y=50)
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
        
        # grading button
        # self.gradingButton = Button(conditionFrame, text='Grading', command=self.openGradingWindow, state='disabled')
        # self.gradingButton.place(x=157, y=5)

        # Printing Type frame
        printingTypeFrame = Frame(self.root, width=220, height=220)
        printingTypeFrame.place(x=1384, y=185)
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
        self.setPrintingTypes()

        self.overridePrintingTypeValue = tkinter.IntVar()
        self.overridePrintingType = Checkbutton(printingTypeFrame, text='Override', variable=self.overridePrintingTypeValue, onvalue=1, offvalue=0, command=self.togglePrintingType)
        self.overridePrintingType.place(x=5, y=170)

    def setPrintingTypes(self):
        if self.foundCard is not None:
            if self.foundCard["PrintingTypes"] is not None:
                if "normal" not in self.foundCard["PrintingTypes"]:
                    self.printingType1.config(state='disabled')
                if "holofoil" not in self.foundCard["PrintingTypes"]:
                    self.printingType2.config(state='disabled')
                if "reverseHolofoil" not in self.foundCard["PrintingTypes"]:
                    self.printingType3.config(state='disabled')
                if "1stEdition" not in self.foundCard["PrintingTypes"]:
                    self.printingType4.config(state='disabled')
                if "1stEditionHolofoil" not in self.foundCard["PrintingTypes"]:
                    self.printingType5.config(state='disabled')
                if "unlimited" not in self.foundCard["PrintingTypes"]:
                    self.printingType6.config(state='disabled')
                if "unlimitedHolofoil" not in self.foundCard["PrintingTypes"]:
                    self.printingType7.config(state='disabled')
            else: 
                self.printingType1.config(state='normal')
                self.printingType2.config(state='normal')
                self.printingType3.config(state='normal')
                self.printingType4.config(state='normal')
                self.printingType5.config(state='normal')
                self.printingType6.config(state='normal')
                self.printingType7.config(state='normal')

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
            self.setPrintingTypes()

    def toggleDate(self):
        if self.noDateValue.get() == 1:
            self.dateObtainedCalender.config(state='disable')
        else:
            self.dateObtainedCalender.config(state='normals')

    def updateInfoFrame(self, card):
        self.infoFrame.destroy()
        self.foundCard = card
        self.setupInfoFrame()
        self.nameLabel = Label(self.infoFrame, text=f"Name: {card['Name']}").place(x=10, y=10)

        global cardNumberLabeltext
        if str(card['Set']['Number']).isnumeric():
            cardNumberLabeltext = f"{str(card['Set']['Number'])} / {str(card['Set']['PrintedTotal'])} ({str(card['Set']['TotalCards'])})"
        else:
            # get the characters in the string before the first number and put them in a new string 
            cardSubset = ''.join([i for i in card['Set']['Number'] if not i.isdigit()])
            cardNumberLabeltext = f"{str(card['Set']['Number'])} / {cardSubset}{str(card['Set']['TotalCards'])}"

        self.cardNumberLabel = Label(self.infoFrame, text=f"Card Number: {cardNumberLabeltext}").place(x=10, y=40)
        self.setLabel = Label(self.infoFrame, text=f"Set: {card['Set']['Name']}").place(x=10, y=70)
        self.cardRarityLabel = Label(self.infoFrame, text=f"Rarity: {card['Rarity']}").place(x=10, y=100)
        self.addToCollectionButton.config(state='normal')
        # self.gradingButton.config(state='normal')

    def openGradingWindow(self):
        dialog = Grading_Dialog(self.root, self.rawGrading, self.searchFeed.image)

        # wait til the window is closed before continuing the program
        self.root.wait_window(dialog.new)
        self.rawGrading = dialog.rawGrading

    def openLocationWindow(self):
        dialog = Location_Dialog(self.root, self.database)

        # wait til the window is closed before continuing the program
        self.root.wait_window(dialog.new)
        self.refreshLocationDropdown()
        
    def refreshLocationDropdown(self):
        self.storageLocations = self.database.get_locations()
        if len(self.storageLocations) > 0:
            self.locationDropdownMenu = OptionMenu(self.miscFrame, self.locationDropdown, *[location.name for location in self.storageLocations])
        else:
            self.locationDropdownMenu = OptionMenu(self.miscFrame, self.locationDropdown, "None")
        self.locationDropdownMenu.config(background='white', highlightbackground="#7a7a7a", highlightthickness=1, width=17, border=0)
        self.locationDropdownMenu.place(x=5, y=40)
        
        

    def addToCollection(self):
        _newCard = CardDto(self.foundCard)
        _newCard.Condition = self.condition.get()
        _newCard.PrintingType = self.printingType.get()

        # find the location object from the name of the location
        for location in self.storageLocations:
            if location.name == self.locationDropdown.get():
                _newCard.Location = location
                break
        
        _newCard.ObtainedHow = self.obtainedHowDropdown.get()

        if self.noDateValue.get() != 1:
            _newCard.DateObtained = self.dateObtainedCalender.get_date()

        self.database.insert_card(_newCard)



    def onClose(self):
        self.closed = True
        self.root.destroy()


        
        
