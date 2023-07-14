import sys
sys.dont_write_bytecode = True
import threading
import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import Button, Frame, Label, Tk, ttk
from PIL import Image, ImageTk
from data.dataset import findMatch, toHash, url_to_image
from detector import detectCard, transformCard
from gui.gui import Gui
from data.spreadsheet import GoogleSheets

root = Tk()
googleSheets = GoogleSheets()
gui = Gui(root, googleSheets)

cap = cv.VideoCapture(2)

foundCard = None

def videoLoop():
    global root, cap, detectCounter, foundCard

    while True:
        ret, frame = cap.read()
        # remove black bars from the frame
        frame = frame[60:frame.shape[0]-60, 0:frame.shape[1]]
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


videoThread = threading.Thread(target=videoLoop, args=())
videoThread.start()
root.mainloop()

# When everything done, release the capture and stop the thread
cap.release()
videoThread.join()
cv.destroyAllWindows()