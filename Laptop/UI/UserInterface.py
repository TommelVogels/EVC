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

PLOT_UPDATE_MS = 250
PLOT_POINTS    = 20

#include dependencies
from tkinter import *
import threading

from Debugging.Debug import logToAll
from Parameters.Parameters import setVariableState
from Parameters.Parameters import getVariableState
from Communication.CommunicationBuffer  import PushCmd

#variables
leftMotorSpeedHistory  = []
leftMotorSpeedHisLen   = 0
rightMotorSpeedHistory = []
rightMotorSpeedHisLen   = 0
angleHistory = []
angleHisLen   = 0
aimActive = 0

class UI:
  def __init__(self, root):
    self.frame = Frame(root)
    self.frame.pack(expand=YES, fill=BOTH)
    self.root = root
    
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
    #self.scaleVerTurret = Scale( root, length=200, from_= VER_TUR_ANGLE_MAX, to=VER_TUR_ANGLE_MIN, resolution=VER_TUR_RESOLUTION, variable = self.VerTurret, command = self.VerTurretChange).place(x=135, y=300)
    
    #slider for horizontal Turret
    self.HorTurret = IntVar()
    #self.scaleHorTurret = Scale( root, length=300, from_= HOR_TUR_ANGLE_MIN, to=HOR_TUR_ANGLE_MAX, resolution=HOR_TUR_RESOLUTION, variable = self.HorTurret, orient=HORIZONTAL, command = self.HorTurretChange ).place(x=10, y=500)
    
    Label(root, text="Firing:").place(x=10, y=480)
    
    #buttons for firing:
    Button(root,text = "Laser ON", command = self.LaserOn).place(x=10, y=510)
    Button(root,text = "Laser OFF", command = self.LaserOff).place(x=100, y=510)
    Button(root,text = "T1 FIRE ONE").place(x=10, y=560)
    Button(root,text = "T1 FIRE ALL").place(x=110, y=560)
    Button(root,text = "T2 FIRE ONE").place(x=10, y=610)
    Button(root,text = "T2 FIRE ALL").place(x=110, y=610)
    Button(root,text = "T1 & T2 FIRE ALL").place(x=10, y=660)
    
    #canvas to plot motor speeds
    self.plot = Canvas(root, width=840, height=400)
    self.plot.place(x=370,y=10)
    self.plot.configure(background='white')
    self.plot.create_line(0, 150, 840, 150)
    self.update_plot()
    
    #canvas for aiming
    self.aim = Canvas(root, width=360, height=180)
    self.aim.place(x=0,y=290)
    self.aim.configure(background='grey')
    self.aim.bind('<Motion>',self.mouseMove)
    self.aim.bind("<Button-1>", self.activateAim)
    

  def update_plot(obj):
    
    global rightMotorSpeedHistory
    global leftMotorSpeedHistory
    global rightMotorSpeedHisLen
    global leftMotorSpeedHisLen
    global angleHistory
    global angleHisLen
    
    rightMotorSpeedHistory.append(getVariableState("rightMotorSpeed"))
    obj.RightSpeed.set(getVariableState("rightMotorSpeed"));
    if rightMotorSpeedHisLen>=PLOT_POINTS:
      rightMotorSpeedHistory.pop(0)
    else:
      rightMotorSpeedHisLen   = rightMotorSpeedHisLen + 1
      
    leftMotorSpeedHistory.append(getVariableState("leftMotorSpeed")) 
    obj.LeftSpeed.set(getVariableState("leftMotorSpeed"));
    if leftMotorSpeedHisLen>=PLOT_POINTS:
      leftMotorSpeedHistory.pop(0)
    else:
      leftMotorSpeedHisLen   = leftMotorSpeedHisLen + 1
      
    angleHistory.append(getVariableState("angle")) 
    if angleHisLen>=PLOT_POINTS:
      angleHistory.pop(0)
    else:
      angleHisLen   = angleHisLen + 1
      
    obj.plot.delete("all")
    
    obj.plot.create_text(60, 10, text='Left Min -100%') 
    obj.plot.create_text(60, 190, text='Left Max 100%') 
    obj.plot.create_text(60, 210, text='Right Max 100%') 
    obj.plot.create_text(60, 390, text='Right Min -100%') 
    obj.plot.create_line(0, 100, 840,  100, fill="black")
    obj.plot.create_line(0, 200, 840,  200, fill="black")
    obj.plot.create_line(0, 300, 840,  300, fill="black")
    
    
    for i in range(1, leftMotorSpeedHisLen):
      obj.plot.create_line(int(840/PLOT_POINTS*(i-1)), (int(leftMotorSpeedHistory[i-1])+MOTORSPEED_MIN*-1), int(840/PLOT_POINTS*i), (int(leftMotorSpeedHistory[i])+MOTORSPEED_MIN*-1) , fill="red")
      obj.plot.create_line(int(840/PLOT_POINTS*(i-1)), MOTORSPEED_MAX*3-int(rightMotorSpeedHistory[i-1]), int(840/PLOT_POINTS*i), MOTORSPEED_MAX*3-int(rightMotorSpeedHistory[i]), fill="green")
      obj.plot.create_line(int(840/PLOT_POINTS*(i-1)), int(angleHistory[i-1])+200, int(840/PLOT_POINTS*i), int(angleHistory[i])+200, fill="blue")
    
    obj.root.after(PLOT_UPDATE_MS, obj.update_plot)
    
  def LaserOn(arg):
    logToAll("LaserOn ; buttonClicked; ", 3)
    PushCmd(bytearray([0xA5,0x02,0x38,0x01,0x3B,0x5A]))
  def LaserOff(arg):
    logToAll("LaserOff ; buttonClicked; ", 3)
    PushCmd(bytearray([0xA5,0x02,0x38,0x00,0x3A,0x5A]))
  def LeftMotorChange(obj, value):
    logToAll("LeftMotorChange ; Slider changed; "+str(value), 3)
    obj.BothSpeed.set(value);
    setVariableState("leftMotorSpeed", value)
    
    if int(value)>0:
      PushCmd(bytearray([0xA5,0x03,0x11,0x01,int(value),0x13^int(value),0x5A]))
    else:
      PushCmd(bytearray([0xA5,0x03,0x11,0x00,(int(value)*-1),0x12^(int(value)*-1),0x5A]))
  def RightMotorChange(obj, value):
    logToAll("RightMotorChange ; Slider changed; "+str(value), 3)
    obj.BothSpeed.set(value);
    setVariableState("rightMotorSpeed", value)
    
    if int(value)>0:
      PushCmd(bytearray([0xA5,0x03,0x12,0x01,int(value),0x10^int(value),0x5A]))
    else:
      PushCmd(bytearray([0xA5,0x03,0x12,0x00,(int(value)*-1),0x11^(int(value)*-1),0x5A]))
  def BothMotorChange(obj, value):
    logToAll("BothMotorChange ; Slider changed; "+str(value), 3)
    obj.RightSpeed.set(value);
    obj.LeftSpeed.set(value);
    setVariableState("leftMotorSpeed", value)
    setVariableState("rightMotorSpeed", value)
    
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

  def mouseMove(obj, event): 
    global aimActive
    logToAll("mouseMove ; Aim mouse move; "+str(event.x/2)+","+str(event.y/2), 3)
    if aimActive == 1:
      PushCmd(bytearray([0xA5,0x02,0x31,int(int(event.x)/2),0x33^(int(int(event.x)/2)),0x5A]))
      PushCmd(bytearray([0xA5,0x02,0x32,int(int(event.y)/2),0x30^(int(int(event.y)/2)),0x5A]))
  
  def activateAim(obj, event):
    global aimActive
    logToAll("activateAim ; Aim activation; "+str(aimActive), 3)
    if aimActive == 0:
      aimActive = 1
    else:
      aimActive = 0


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
    
  
