from tkinter import Button, Frame, Label, Toplevel
from PIL import Image, ImageTk

import cv2

from models.grading_models import AreaEnum, RawGrading

backside = cv2.imread("assets/card_backside.png")
backside = cv2.cvtColor(backside, cv2.COLOR_BGR2RGB)
backside = cv2.resize(backside, (300, 400))

class Grading_Dialog:


    def __init__(self, root, _rawGrading: RawGrading, _cardImage: ImageTk.PhotoImage):
        self.rawGrading = _rawGrading
        
        self.backsideImage = ImageTk.PhotoImage(Image.fromarray(backside))
        self.cardImage = _cardImage

        self.new = Toplevel(root)
        self.new.grab_set()
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

        self.setupScoreFrame()

        self.setupCardClickBoxes()

    def setupScoreFrame(self):
        self.scoreFrame = Frame(self.new, width=570, height=100, highlightcolor="black", highlightbackground="black", highlightthickness=2)
        self.scoreFrame.place(x=320, y=10)

        self.scoreTotalFrame = Frame(self.scoreFrame, width=120, height=100, highlightcolor="black", highlightbackground="black", highlightthickness=2)
        self.scoreTotalFrame.place(x=-2, y=-2)

        # center text in total score frame
        self.scoreTotalLabel = Label(self.scoreTotalFrame, text=self.rawGrading.totalScore(), font=("Helvetica", 25))
        self.scoreTotalLabel.place(x=58, y=40, anchor="center", width=115)

        self.scoreTotalNameLabel = Label(self.scoreTotalFrame, text=self.rawGrading.totalScoreName(), font=("Helvetica", 10))
        self.scoreTotalNameLabel.place(x=58, y=70, anchor="center", width=115)

        self.scoreIndividualFrame = Frame(self.scoreFrame, width=450, height=100, highlightcolor="black", highlightbackground="black", highlightthickness=2)
        self.scoreIndividualFrame.place(x=117, y=-2)

        # display the 4 scores (corners, edges, centering, surface) in the scoreIndividualFrame as labels
        self.scoreIndividualCornersLabel = Label(self.scoreIndividualFrame, text=self.rawGrading.Corners.score(), font=("Helvetica", 15))
        self.scoreIndividualCornersLabel.place(x=0, y=40, width=110, height=25)
        Label(self.scoreIndividualFrame, text="Corners", font=("Helvetica", 10)).place(x=0, y=10, width=110, height=25)

        self.scoreIndividualEdgesLabel = Label(self.scoreIndividualFrame, text=self.rawGrading.Edges.score(), font=("Helvetica", 15))
        self.scoreIndividualEdgesLabel.place(x=110, y=40, width=110, height=25)
        Label(self.scoreIndividualFrame, text="Edges", font=("Helvetica", 10)).place(x=110, y=10, width=110, height=25)

        self.scoreIndividualCenteringLabel = Label(self.scoreIndividualFrame, text=self.rawGrading.Centering.score(), font=("Helvetica", 15))
        self.scoreIndividualCenteringLabel.place(x=220, y=40, width=110, height=25)
        Label(self.scoreIndividualFrame, text="Centering", font=("Helvetica", 10)).place(x=220, y=10, width=110, height=25)

        self.scoreIndividualSurfaceLabel = Label(self.scoreIndividualFrame, text=self.rawGrading.Surface.score(), font=("Helvetica", 15))
        self.scoreIndividualSurfaceLabel.place(x=330, y=40, width=110, height=25)
        Label(self.scoreIndividualFrame, text="Surface", font=("Helvetica", 10)).place(x=330, y=10, width=110, height=25)

    def setupCardClickBoxes(self):
        # Corners
        self.setupCorners()
        
        # Edges
        pass

    def setupCorners(self):
        color = "white"
        borderColor = "black"

        self.topLeftCorner = Frame(self.imageFrame, width=25, height=25, cursor="hand2", bg="")
        Frame(self.topLeftCorner, width=20, height=5, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1).place(x=0, y=0)
        Frame(self.topLeftCorner, width=5, height=20, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1).place(x=0, y=0)
        self.topLeftCorner.bind("<Button-1>", lambda event: self.selectedArea(1, AreaEnum.Corners))
        self.topLeftCorner.place(x=5, y=5)

        topRightCorner_p1 = Frame(self.imageFrame, width=20, height=5, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1)
        topRightCorner_p2 = Frame(self.imageFrame, width=5, height=20, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1)
        # topRightCorner_p1.bind("<Button-1>", lambda event: self.selectedArea(2, AreaEnum.Corners))
        # topRightCorner_p2.bind("<Button-1>", lambda event: self.selectedArea(2, AreaEnum.Corners))
        topRightCorner_p1.place(x=275, y=5)
        topRightCorner_p2.place(x=290, y=5)

        bottomLeftCorner_p1 = Frame(self.imageFrame, width=20, height=5, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1)
        bottomLeftCorner_p2 = Frame(self.imageFrame, width=5, height=20, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1)
        # bottomLeftCorner_p1.bind("<Button-1>", lambda event: self.selectedArea(3, AreaEnum.Corners))
        # bottomLeftCorner_p2.bind("<Button-1>", lambda event: self.selectedArea(3, AreaEnum.Corners))
        bottomLeftCorner_p1.place(x=5, y=390)
        bottomLeftCorner_p2.place(x=5, y=375)

        bottomRightCorner_p1 = Frame(self.imageFrame, width=20, height=5, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1)
        bottomRightCorner_p2 = Frame(self.imageFrame, width=5, height=20, bg=color, cursor="hand2", highlightbackground=borderColor, highlightthickness=1)
        # bottomRightCorner_p1.bind("<Button-1>", lambda event: self.selectedArea(4, AreaEnum.Corners))
        # bottomRightCorner_p2.bind("<Button-1>", lambda event: self.selectedArea(4, AreaEnum.Corners))
        bottomRightCorner_p1.place(x=275, y=390)
        bottomRightCorner_p2.place(x=290, y=375)

    def selectedArea(self, id: int, area: AreaEnum):
        if area == AreaEnum.Corners:
            if id == 1:
                self.rawGrading.Corners.topLeft.Value = 1
            elif id == 2:
                self.rawGrading.Corners.topRight.Value = 1
            elif id == 3:
                self.rawGrading.Corners.bottomLeft.Value = 1
            elif id == 4:
                self.rawGrading.Corners.bottomRight.Value = 1
        elif area == AreaEnum.Edges:
            pass
        elif area == AreaEnum.Centering:
            pass
        elif area == AreaEnum.Surface:
            pass

        print(area, id)



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
        