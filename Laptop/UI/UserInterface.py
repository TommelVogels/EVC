# UserInterface.py
# Shows and manages the user interface 

#defines
MOTORSPEED_MIN = -100
MOTORSPEED_MAX = 100
MOTORSPEED_RESOLUTION = 1

VER_TUR_ANGLE_MAX = 90
VER_TUR_ANGLE_MIN = 0
VER_TUR_RESOLUTION = 1

HOR_TUR_ANGLE_MAX = 90
HOR_TUR_ANGLE_MIN = -90
HOR_TUR_RESOLUTION = 1

#include dependencies
from tkinter import *
import threading

from Debugging.Debug import logToAll
from Communication.CommunicationBuffer  import PushCmd

#variables

class UI:
  def __init__(self, root):
    self.frame = Frame(root)
    self.frame.pack(expand=YES, fill=BOTH)
    
    root.title("SolarCar Remote Control")
    root.minsize(1200, 900)
    
    Label(root, text="Motor Speeds:").place(x=10,y=5)
    
    #slider for left speed
    self.LeftSpeed = IntVar()
    #self.LeftSpeed.trace("w", self.LeftMotorChange)
    self.scaleLeft = Scale( root, length=200, from_= MOTORSPEED_MAX, to=MOTORSPEED_MIN, resolution=MOTORSPEED_RESOLUTION, variable = self.LeftSpeed, command=self.LeftMotorChange).place(x=10,y=40)
    
    #slider for right speed
    self.RightSpeed = IntVar()
    self.scaleRight = Scale( root, length=200, from_= MOTORSPEED_MAX, to=MOTORSPEED_MIN, resolution=MOTORSPEED_RESOLUTION, variable = self.RightSpeed, command = self.RightMotorChange ).place(x=120,y=40)
   
    #slider for both speed
    self.BothSpeed = IntVar()
    self.scaleBoth = Scale( root, length=200, from_= MOTORSPEED_MAX, to=MOTORSPEED_MIN, resolution=MOTORSPEED_RESOLUTION, variable = self.BothSpeed, command = self.BothMotorChange ).place(x=230,y=40)

    
    Label(root, text="Turret positioning:").place(x=10, y=260)
    
    #slider for Vertical Turrent
    self.VerTurret = IntVar()
    self.scaleVerTurret = Scale( root, length=200, from_= VER_TUR_ANGLE_MAX, to=VER_TUR_ANGLE_MIN, resolution=VER_TUR_RESOLUTION, variable = self.VerTurret, command = self.VerTurretChange).place(x=135, y=300)
    
    #slider for horizontal Turret
    self.HorTurret = IntVar()
    self.scaleHorTurret = Scale( root, length=300, from_= HOR_TUR_ANGLE_MIN, to=HOR_TUR_ANGLE_MAX, resolution=HOR_TUR_RESOLUTION, variable = self.HorTurret, orient=HORIZONTAL, command = self.HorTurretChange ).place(x=10, y=500)
   
    Label(root, text="Firing:").place(x=10, y=580)
    
    #buttons for firing:
    Button(root,text = "Laser ON", command = self.LaserOn).place(x=10, y=620)
    Button(root,text = "Laser OFF", command = self.LaserOff).place(x=100, y=620)
    Button(root,text = "T1 FIRE ONE").place(x=10, y=670)
    Button(root,text = "T1 FIRE ALL").place(x=100, y=670)
    Button(root,text = "T2 FIRE ONE").place(x=10, y=720)
    Button(root,text = "T2 FIRE ALL").place(x=100, y=720)
    Button(root,text = "T1 & T2 FIRE ALL").place(x=10, y=770)
    
    self.tcpVar = IntVar()
    #self.tcpUI = Checkbutton(root, text ="Show title", variable = self.tcpVar, command = self.click)
    #self.tcpUI.place(x=50,y=50)
    
  def LaserOn(arg):
    logToAll("LaserOn ; buttonClicked; ", 3)
    PushCmd(bytearray([0xA5,0x02,0x38,0x01,0x3B,0x5A]))
  def LaserOff(arg):
    logToAll("LaserOff ; buttonClicked; ", 3)
    PushCmd(bytearray([0xA5,0x02,0x38,0x00,0x3A,0x5A]))
  def LeftMotorChange(obj, value):
    logToAll("LeftMotorChange ; Slider changed; "+str(value), 3)
    obj.BothSpeed.set(value);
    if int(value)>0:
      PushCmd(bytearray([0xA5,0x03,0x11,0x01,int(value),0x13^int(value),0x5A]))
    else:
      PushCmd(bytearray([0xA5,0x03,0x11,0x00,(int(value)*-1),0x12^(int(value)*-1),0x5A]))
  def RightMotorChange(obj, value):
    logToAll("RightMotorChange ; Slider changed; "+str(value), 3)
    obj.BothSpeed.set(value);
    if int(value)>0:
      PushCmd(bytearray([0xA5,0x03,0x12,0x01,int(value),0x10^int(value),0x5A]))
    else:
      PushCmd(bytearray([0xA5,0x03,0x12,0x00,(int(value)*-1),0x11^(int(value)*-1),0x5A]))
  def BothMotorChange(obj, value):
    logToAll("BothMotorChange ; Slider changed; "+str(value), 3)
    obj.RightSpeed.set(value);
    obj.LeftSpeed.set(value);
    if int(value)>0:
      PushCmd(bytearray([0xA5,0x05,0x13,0x01,int(value),0x01,int(value),0x16^int(value)^int(value),0x5A]))
    else:
      PushCmd(bytearray([0xA5,0x05,0x13,0x00,(int(value)*-1),0x00,(int(value)*-1),0x16^(int(value)*-1)^(int(value)*-1),0x5A]))
  def HorTurretChange(obj, value):
    logToAll("HorTurretChange ; Slider changed; "+str(value), 3)
    PushCmd(bytearray([0xA5,0x02,0x31,int(value)+90,0x33^(int(value)+90),0x5A])) 
  def VerTurretChange(obj, value):
    logToAll("VerTurretChange ; Slider changed; "+str(value), 3)
    PushCmd(bytearray([0xA5,0x02,0x32,int(value),0x30^(int(value)),0x5A]))     


def buildUI():
    logToAll("buildUI ; ; ",1)
    
    #start the UI thread
    t = threading.Thread(target=runUI)
    t.start()

    logToAll("buildUI ; UI thread started ; "+str(t), 2)
    
def runUI():
    root = Tk()
    
    uiHandle = UI(root)
    
    root.mainloop()
    
  
