from tkinter import Frame, Image, Text, Tk, Label, Button, Toplevel
from PIL import Image, ImageTk
from gui.add_card_dialog import AddCardDialog
import cv2 as cv
import numpy as np

from data.dataset import url_to_image

class Gui:
    cvSearchImage = None
    searchImg = None
    searched = False
    foundCard = None

    def __init__(self, root, googleSheets):
        self.root = root
        self.googleSheets = googleSheets
        root.title("Pokémon Card Scanner")
        root.geometry('1600x800')
        root.resizable(False, False)
        self.setupGui(root)

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

        self.setupInfoFrame()

    def setImageNone(self, feed):
        blank = np.zeros((400, 300, 3), np.uint8)
        blank.fill(255)
        blank = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(blank, cv.COLOR_BGR2RGB)))
        feed.configure(image=blank)
        feed.image = blank
        
    def updateCameraFeed(self, img):
        cameraFeedImg = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(cv.resize(img, (325, 500)), cv.COLOR_BGR2RGB)))
        self.cameraFeed.configure(image=cameraFeedImg)
        self.cameraFeed.image = cameraFeedImg

    def updateTransformFeed(self, img):
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
        self.infoFrame = Frame(self.root, width=304, height=130)
        self.infoFrame.config(highlightbackground="black", highlightthickness=2)
        self.infoFrame.place(x=1080, y=450)
        self.nameLabel = Label(self.infoFrame, text='Name:').place(x=10, y=10)
        self.cardNumberLabel = Label(self.infoFrame, text='Card Number:').place(x=10, y=40)
        self.setLabel = Label(self.infoFrame, text='Set:').place(x=10, y=70)
        self.cardRarityLabel = Label(self.infoFrame, text='Rarity:').place(x=10, y=100)

        # create a button but disable it until a card is found
        self.addToCollectionBulkButton = Button(self.root, text='Add to Collection (Bulk)', command=self.addToCollection, state='disabled')
        self.addToCollectionBulkButton.place(x=1160, y=590)
        self.addToCollectionExtendedButton = Button(self.root, text='Add to Collection (Extended)', command=self.addToCollectionExtended, state='disabled')
        self.addToCollectionExtendedButton.place(x=1150, y=620)

    def updateInfoFrame(self, card):
        self.infoFrame.destroy()
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
        self.addToCollectionExtendedButton.config(state='normal')
        self.addToCollectionBulkButton.config(state='normal')
        self.foundCard = card

    def addToCollection(self):
        print(self.foundCard)

    def addToCollectionExtended(self):
        AddCardDialog(self.root, self.googleSheets, self.foundCard)

        
        
