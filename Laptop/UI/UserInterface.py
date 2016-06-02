# UserInterface.py
# Shows and manages the user interface 

#defines
MOTORSPEED_MIN = -255
MOTORSPEED_MAX = 255
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

import time

from Debugging.Debug import logToAll
from Parameters.Parameters import setVariableState
from Parameters.Parameters import getVariableState
from Communication.CommunicationBuffer  import PushCmd

from Communication.Commands.Commands  import CommandType

#variables
leftMotorSpeedHistory  = []
leftMotorSpeedHisLen   = 0
rightMotorSpeedHistory = []
rightMotorSpeedHisLen   = 0
angleHistory = []
angleHisLen   = 0
aimActive = 0
leftDisHistory = []
leftDisHisLen   = 0
rightDisHistory = []
rightDisHisLen   = 0

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
    Button(root,text = "T1 FIRE ONE", command = self.Fire1).place(x=10, y=560)
    Button(root,text = "T1 FIRE ALL", command = self.Fire1All).place(x=110, y=560)
    Button(root,text = "T2 FIRE ONE", command = self.Fire2).place(x=10, y=610)
    Button(root,text = "T2 FIRE ALL", command = self.Fire2All).place(x=110, y=610)
    Button(root,text = "T1 & T2 FIRE ALL", command = self.FireAll).place(x=10, y=660)
    
    self.signDetectText = StringVar()
    self.signDetected = Label(root, textvariable=self.signDetectText).place(x=370, y=420)
    
    self.pathText = StringVar()
    self.path = Label(root, textvariable=self.pathText).place(x=570, y=420)
    
    self.controlStateText = StringVar()
    self.controlState = Label(root, textvariable=self.controlStateText).place(x=870, y=420)
    
    
    #canvas to plot motor speeds
    self.plot = Canvas(root, width=840, height=400)
    self.plot.place(x=370,y=10)
    self.plot.configure(background='white')
    self.plot.create_line(0, 150, 840, 150)
    
    self.plotInput = Canvas(root, width=840, height=320)
    self.plotInput.place(x=370,y=450)
    self.plotInput.configure(background='white')
    self.plotInput.create_line(0, 150, 840, 150)
    
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
    global leftDisHistory
    global leftDisHisLen
    global rightDisHistory
    global rightDisHisLen
    
    obj.signDetectText.set("Detected Sign: "+str(getVariableState("sign")))
    obj.pathText.set("Left offset: "+str(getVariableState("leftDis"))+ " Right offset: "+str(getVariableState("rightDis")))
    
    if getVariableState("control_state")==0:
      obj.controlStateText.set("State: STATE_FOLLOW_PATH")
    elif getVariableState("control_state")==1:
      obj.controlStateText.set("State: STATE_TURNING_LEFT")
    elif getVariableState("control_state")==2:
      obj.controlStateText.set("State: STATE_TURNING_RIGHT")
    elif getVariableState("control_state")==3:
      obj.controlStateText.set("State: STATE_STOP")
    elif getVariableState("control_state")==4:
      obj.controlStateText.set("State: STATE_GO_STRAIGHT")
    elif getVariableState("control_state")==5:
      obj.controlStateText.set("State: STATE_UTURN")
    
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
      
    rightDisHistory.append(getVariableState("rightDis"))
    if rightDisHisLen>=PLOT_POINTS:
      rightDisHistory.pop(0)
    else:
      rightDisHisLen   = rightDisHisLen + 1
      
    leftDisHistory.append(getVariableState("leftDis"))
    if leftDisHisLen>=PLOT_POINTS:
      leftDisHistory.pop(0)
    else:
      leftDisHisLen   = leftDisHisLen + 1
      
    obj.plot.delete("all")
    obj.plotInput.delete("all")
    
    obj.plot.create_text(60, 10, text='Left Min -100%') 
    obj.plot.create_text(60, 190, text='Left Max 100%') 
    obj.plot.create_text(60, 210, text='Right Max 100%') 
    obj.plot.create_text(60, 390, text='Right Min -100%') 
    obj.plot.create_line(0, 100, 840,  100, fill="black")
    obj.plot.create_line(0, 200, 840,  200, fill="black")
    obj.plot.create_line(0, 300, 840,  300, fill="black")
    
    obj.plotInput.delete("all")
    obj.plotInput.create_line(0, 160, 840,  160, fill="black")    
    
    for i in range(1, leftMotorSpeedHisLen):
      obj.plot.create_line(int(840/PLOT_POINTS*(i-1)), (int(leftMotorSpeedHistory[i-1])+MOTORSPEED_MIN*-1), int(840/PLOT_POINTS*i), (int(leftMotorSpeedHistory[i])+MOTORSPEED_MIN*-1) , fill="red")
      obj.plot.create_line(int(840/PLOT_POINTS*(i-1)), MOTORSPEED_MAX-int(rightMotorSpeedHistory[i-1]), int(840/PLOT_POINTS*i), MOTORSPEED_MAX-int(rightMotorSpeedHistory[i]), fill="green")
      obj.plot.create_line(int(840/PLOT_POINTS*(i-1)), int(angleHistory[i-1])+200, int(840/PLOT_POINTS*i), int(angleHistory[i])+200, fill="blue")
      obj.plotInput.create_line(int(840/PLOT_POINTS*(i-1)), int(int(rightDisHistory[i-1])/2)+160, int(840/PLOT_POINTS*i), int(int(rightDisHistory[i])/2)+160, fill="orange")
      obj.plotInput.create_line(int(840/PLOT_POINTS*(i-1)), 160-int(int(leftDisHistory[i-1])/2), int(840/PLOT_POINTS*i), 160-int(int(leftDisHistory[i])/2), fill="orange")
    
    obj.root.after(PLOT_UPDATE_MS, obj.update_plot)
    
  def LaserOn(arg):
    logToAll("LaserOn ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_LASER_SET, bytearray([0x01]))
  def LaserOff(arg):
    logToAll("LaserOff ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_LASER_SET, bytearray([0x00]))
  def LeftMotorChange(obj, value):
    logToAll("LeftMotorChange ; Slider changed; "+str(value), 3)
    obj.BothSpeed.set(value);
    setVariableState("leftMotorSpeed", value)
    
    if int(value)>0:
      PushCmd(CommandType.LEFT_MOTOR_SPEED,bytearray([0x01,int(value)]))
    else:
      PushCmd(CommandType.LEFT_MOTOR_SPEED,bytearray([0x00,int(int(value)*-1)]))
  def RightMotorChange(obj, value):
    logToAll("RightMotorChange ; Slider changed; "+str(value), 3)
    obj.BothSpeed.set(value);
    setVariableState("rightMotorSpeed", value)
    
    if int(value)>0:
      PushCmd(CommandType.RIGHT_MOTOR_SPEED,bytearray([0x01,int(value)]))
    else:
      PushCmd(CommandType.RIGHT_MOTOR_SPEED,bytearray([0x00,int(int(value)*-1)]))
  def BothMotorChange(obj, value):
    logToAll("BothMotorChange ; Slider changed; "+str(value), 3)
    obj.RightSpeed.set(value);
    obj.LeftSpeed.set(value);
    setVariableState("leftMotorSpeed", value)
    setVariableState("rightMotorSpeed", value)
    
    if int(value)>0:
      PushCmd(CommandType.BOTH_MOTOR_SPEED,bytearray([0x01,int(value),0x01,int(value)]))
    else:
      PushCmd(CommandType.BOTH_MOTOR_SPEED,bytearray([0x00,int(int(value)*-1),0x00,int(int(value)*-1)]))
  def HorTurretChange(obj, value):
    logToAll("HorTurretChange ; Slider changed; "+str(value), 3)
    PushCmd(CommandType.TURRET_HOR_ANGLE, bytearray([int(value)+90])) 
  def VerTurretChange(obj, value):
    logToAll("VerTurretChange ; Slider changed; "+str(value), 3)
    PushCmd(CommandType.TURRET_VER_ANGLE,bytearray([int(value)]))

  def Fire1(arg):
    logToAll("Fire1 ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_FIRE_1,bytearray([]))
  def Fire2(arg):
    logToAll("Fire2 ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_FIRE_2,bytearray([]))
  def Fire1All(arg):
    logToAll("Fire1All ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_FIRE_ALL_1,bytearray([]))
  def Fire2All(arg):
    logToAll("Fire2All ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_FIRE_ALL_2,bytearray([]))
  def FireAll(arg):
    logToAll("FireAll ; buttonClicked; ", 3)
    PushCmd(CommandType.TURRET_FIRE_ALL,bytearray([]))   

  def mouseMove(obj, event): 
    global aimActive
    logToAll("mouseMove ; Aim mouse move; "+str(event.x/2)+","+str(event.y/2), 3)
    if aimActive == 1:
        PushCmd(CommandType.TURRET_BOTH_ANGLE,bytearray([int(int(event.x)/2),int(90-int(int(event.y)/2))]))
  
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
    
  
