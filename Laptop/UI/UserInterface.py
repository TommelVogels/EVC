# UserInterface.py
# Shows and manages the user interface 

#defines
MOTORSPEED_MIN = -10
MOTORSPEED_MAX = 10
MOTORSPEED_RESOLUTION = 0.1


#include dependencies
from Debugging.Debug import logToAll

from tkinter import *
import threading

#variables


def buildUI():
    logToAll("buildUI")
    
    #start the UI thread
    t = threading.Thread(target=runUI)
    t.start()

    logToAll("done")
    
def runUI():
    root = Tk()
    w = Label(root, text="Hello, world!")
    w.pack()
    
    #slider for left speed
    LeftSpeed = DoubleVar()
    scaleLeft = Scale( root, length=200, from_= MOTORSPEED_MAX, to=MOTORSPEED_MIN, resolution=MOTORSPEED_RESOLUTION, variable = LeftSpeed )
    scaleLeft.pack(anchor=CENTER)
    
    #slider for right speed
    RightSpeed = DoubleVar()
    scaleRight = Scale( root, length=200, from_= MOTORSPEED_MAX, to=MOTORSPEED_MIN, resolution=MOTORSPEED_RESOLUTION, variable = RightSpeed )
    scaleRight.pack(anchor=CENTER)
    
    root.mainloop()
    
  
