import sys
sys.dont_write_bytecode = True
import threading
import cv2 as cv
from tkinter import Tk
from data.dataset import findMatch
from services.detector import detectCard, transformCard
from gui.gui import Gui
from services.spreadsheet import GoogleSheets

root = Tk()
googleSheets = GoogleSheets()
gui = Gui(root, googleSheets)

cap = cv.VideoCapture(2)

# foundCard = None

def videoLoop():
    global root, cap, detectCounter, foundCard

    while True:
        ret, frame = cap.read()

        if ret:
            detectedImg, approx_corners = detectCard(frame.copy())
            gui.updateCameraFeed(detectedImg)

            if approx_corners is not None:
                    transformImg = transformCard(frame.copy(), approx_corners)
                    gui.updateTransformFeed(transformImg)
            else:
                gui.updateTransformFeed(frame)

            if gui.searchImg is not None and gui.searched == False:
                gui.searched = True
                foundCard = findMatch(gui.cvSearchImage)
                if foundCard is not None:
                    gui.updateSearchFeed(foundCard)


videoThread = threading.Thread(target=videoLoop, args=(), name="Video/Cam Thread", daemon=True)
videoThread.start()
root.protocol("WM_DELETE_WINDOW", gui.onClose)
root.mainloop()