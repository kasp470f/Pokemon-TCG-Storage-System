from tkinter import Button, Frame, Label, Toplevel
from PIL import Image, ImageTk

import cv2

from models.grading_models import PersonalGrading

backside = cv2.imread("assets/card_backside.png")
backside = cv2.cvtColor(backside, cv2.COLOR_BGR2RGB)
backside = cv2.resize(backside, (300, 400))

class Grading_Dialog:


    def __init__(self, root, _personalGrading: PersonalGrading, _cardImage: ImageTk.PhotoImage):
        self.personalGrading = _personalGrading
        
        self.backsideImage = ImageTk.PhotoImage(Image.fromarray(backside))
        self.cardImage = _cardImage

        self.new = Toplevel(root)
        self.new.geometry('900x500')
        self.new.resizable(False, False)
        self.new.title("Personal Grading")
        
        self.setup()    
    
    def setup(self):
        self.side = 0

        self.imageFrame = Frame(self.new, width=300, height=400)
        self.imageFrame.place(x=10, y=10)

        self.imageLabel = Label(self.imageFrame)
        self.imageLabel.place(x=0, y=0)

        self.sideSelect(side=0)

        self.frontButton = Button(self.new, text="Front Side", command=self.flip)
        self.frontButton.place(x=80, y=420)
        self.frontButton.configure(state="disabled")
        self.backButton = Button(self.new, text="Back Side", command=self.flip)
        self.backButton.place(x=180, y=420)
        self.backButton.configure(state="normal")

        self.setupCardClickBoxes()


    def setupCardClickBoxes(self):
        pass


    def flip(self):
        if self.side == 0:
            self.sideSelect(side=1)
            self.backButton.configure(state="disabled")
            self.frontButton.configure(state="normal")
        else:
            self.sideSelect(side=0)
            self.backButton.configure(state="normal")
            self.frontButton.configure(state="disabled")
        

    def sideSelect(self, side: int):
        self.side = side

        global frontButton, backButton

        if side == 0: # frontside
            self.imageLabel.configure(image=self.cardImage)
            self.imageLabel.image = self.cardImage
        else: # backside
            self.imageLabel.configure(image=self.backsideImage)
            self.imageLabel.image = self.backsideImage
        
        self.imageFrame.update()
        