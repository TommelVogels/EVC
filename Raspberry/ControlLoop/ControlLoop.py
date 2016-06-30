#!/home/pi/.virtualenvs/cv/bin/python
# ControlLoop.py
# Main application and entry point

#defines


#include dependencies
import math
import time

from Debugging.Debug  import logToAll
from Parameters.Parameters import setVariableState
from Parameters.Parameters import getVariableState

from Communication.CommandEncoder  import DecodeCmd
from Communication.CommandEncoder  import EncodeCmd
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd
#from Communication.CommunicationBuffer  import SendCmds
#from Communication.CommunicationBuffer  import ReceiveCmds

from Communication.Commands.Commands  import CommandType

from ImageProcessing.PathRecognition.PathRecognition  import findPath
from ImageProcessing.SignDetection.SignDetection  import findSigns
from ImageProcessing.FrameFetch  import getFrame
from ImageProcessing.FrameFetch  import camera
from ImageProcessing.FrameFetch  import rawCapture
import cv2

#variables
desiredMotorSpeed = 255

current_time = 0
SENSOR_TIME = 1

#functions
def main():
  logToAll("main ; Main application started ; ",1)

  #while 1:
  
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    t1 = time.time()
    image = (frame.array)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    top = image[0:240,0:640]
    bottom = image[250:480,0:640]
    rawCapture.truncate(0)
    t2 = time.time()
    logToAll("getFrame ; Get Frame ;  "+ str(float(t2-t1)) + " seconds",0)
    frameCut =  [top,bottom]
      
    cmd = PopCmd()
    
    if (current_time + SENSOR_TIME) < time.time():
      PushCmd(CommandType.BATTERY_CURRENT,bytearray(0))
      PushCmd(CommandType.SYSTEM_CURRENT,bytearray(0))
      
    
    #time.sleep(1)
    
    if cmd["cmdID"] == CommandType.BATTERY_CURRENT:
      print("response for left motor")
    #frame = getFrame();
    
    pathData = findPath(frameCut[1])
    signData,coords = findSigns(frameCut[0])
    
    aim(signData,coords)
    
    setVariableState("sign", signData)
    
    print(pathData)
    
    runStateActions(signData,coords,pathData)    
	
    # send motor speeds
	
    speedData = bytearray(4);
    
    if getVariableState("leftMotorSpeed")>0:
      speedData[0]=0x01
      speedData[1]=int(getVariableState("leftMotorSpeed"))
    else:
      speedData[0]=0x00
      speedData[1]=int(int(getVariableState("leftMotorSpeed"))*-1)
    
    if getVariableState("rightMotorSpeed")>0:
      speedData[2]=0x01
      speedData[3]=int(getVariableState("rightMotorSpeed"))
    else:
      speedData[2]=0x00
      speedData[3]=int(int(getVariableState("rightMotorSpeed"))*-1)
	
    PushCmd(CommandType.BOTH_MOTOR_SPEED,speedData)
    
    time.sleep(0)

STATE_FOLLOW_PATH   = 0 #define 0: no signs detected just follow path
STATE_TURNING_LEFT  = 1 #define 1: turning left
STATE_TURNING_RIGHT = 2 #define 2: turning right
STATE_STOP          = 3 #define 3: stop
STATE_GO_STRAIGHT   = 4 #define 4: straight
STATE_UTURN         = 5 #define 5: uturn

#stop defines
stop_time = 0
STOP_WAIT_TIME = 10   

#uturn defines
uturn_time = 0
UTURN_WAIT_TIME = 6

#go straight / follow defines
MIN_MOTOR_SPEED = 0
MAX_MOTOR_SPEED = 50
MAX_LINE_OFFSET_POS   = 320
ONE_LINE_LOCATION_SETPOINT = 300 #if only one line is visible try to keep it at 160 1/4 of image
SEARCH_IN_DIRECTION_TIME = 2 #if no lines move in one direction for 5 seconds to try and find line
SEARCH_SPEED_FAST = 10
SEARCH_SPEED_SLOW = 0
lost_search_time = 0
lost_search_attempt = 0

def aim(signData,coords):
  if signData!=0:
    x = int(91-(91-46)/640.0*coords[0])
    y = int(95-(95-30)/240.0*coords[1])
    speedData = bytearray([x,y])
    PushCmd(CommandType.TURRET_BOTH_ANGLE,speedData)
    PushCmd(CommandType.TURRET_LASER_SET,bytearray([1]))
  else:
    PushCmd(CommandType.TURRET_LASER_SET,bytearray([0]))

firedMissiles = 0    
def fire(signData,coords):
  global firedMissiles
  print(coords[2])
  if signData!=0 and coords[2]>80:
    x = int(91-(91-46)/640.0*coords[0])
    y = int(100-(80-30)/240.0*coords[1])
    speedData = bytearray([x,y])
    PushCmd(CommandType.TURRET_BOTH_ANGLE,speedData)
    PushCmd(CommandType.TURRET_LASER_SET,bytearray([1]))
    print("firing turret")
    if firedMissiles%2==0:
     PushCmd(CommandType.TURRET_FIRE_1,bytearray(0))
    else:
      PushCmd(CommandType.TURRET_FIRE_2,bytearray(0))
    firedMissiles = firedMissiles+1
  else:
    PushCmd(CommandType.TURRET_LASER_SET,bytearray([0]))
    print("not firing turret")
 

def relativeSpeeds(direction, speed):
  motorFast="leftMotorSpeed"
  motorSlow="rightMotorSpeed"
  if direction=="left":
    motorFast = "rightMotorSpeed"
    motorSlow = "leftMotorSpeed"
  
  # if speed==1:
    # setVariableState(motorFast, 100)
    # setVariableState(motorSlow, 5)
  # elif speed==2:
    # setVariableState(motorFast, 70)
    # setVariableState(motorSlow, 5)  
  # elif speed==3:
    # setVariableState(motorFast, 50)
    # setVariableState(motorSlow, 5) 
  # elif speed==4:
    # setVariableState(motorFast, 20)
    # setVariableState(motorSlow, 5) 
  
  if speed==1:
    setVariableState(motorFast, 5)
    setVariableState(motorSlow, 0)
  elif speed==2:
    setVariableState(motorFast, 100)
    setVariableState(motorSlow, 5)  
  elif speed==3:
    setVariableState(motorFast, 50)
    setVariableState(motorSlow, 5) 
  elif speed==4:
    setVariableState(motorFast, 50)
    setVariableState(motorSlow, 10) 

signCounts = {"Stop":0,"Left":0,"Right":0,"Straight":0,"Uturn":0}

SIGN_DETECTED_INCREMENT = 1
SIGN_NOT_DETECTED_DECREMENT = 0.1
SIGN_DETECTED_CONFIDENCE = 2

def IncrementSignConfidence(signDetected):
  if signCounts["Stop"]>0:
    signCounts["Stop"] = signCounts["Stop"] - SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Left"]>0:
    signCounts["Left"] = signCounts["Left"] - SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Right"]>0:
    signCounts["Right"] = signCounts["Right"] - SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Straight"]>0:
    signCounts["Straight"] = signCounts["Straight"] - SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Uturn"]>0:
    signCounts["Uturn"] = signCounts["Uturn"] - SIGN_NOT_DETECTED_DECREMENT
    
  if signDetected==1:
   signCounts["Stop"] = signCounts["Stop"] + SIGN_DETECTED_INCREMENT
  elif signDetected==2:
   signCounts["Left"] = signCounts["Left"] + SIGN_DETECTED_INCREMENT
  elif signDetected==3:
   signCounts["Right"] = signCounts["Right"] + SIGN_DETECTED_INCREMENT
  elif signDetected==4:
   signCounts["Straight"] = signCounts["Straight"] + SIGN_DETECTED_INCREMENT
  elif signDetected==5:
   signCounts["Uturn"] = signCounts["Uturn"] + SIGN_DETECTED_INCREMENT

def validSign(sign):
  global signCounts
  if signCounts[sign]>SIGN_DETECTED_CONFIDENCE:
    signCounts = {"Stop":0,"Left":0,"Right":0,"Straight":0,"Uturn":0}
    return True
  else:
    return False

SIGN_DISCARD_SIZE = 110
NUMBER_OF_MISSED_SIGNS = 5
NUMBER_OF_MISSED_SIGNS_UTURN = 2
numSigns = NUMBER_OF_MISSED_SIGNS

def runStateActions(signDetected, coords, pathData):
  global numSigns
  global uturn_time
  global stop_time
  global turn_time
    
  if getVariableState("control_state") == STATE_FOLLOW_PATH:
    followPath(pathData)
  elif getVariableState("control_state") == STATE_TURNING_LEFT:
  
    if pathData["horizontalLine"][4]==1000000 or pathData["horizontalLine"][4]>100:
      followPath(pathData)
    else:
      turnLeft()    
      
  elif getVariableState("control_state") == STATE_TURNING_RIGHT:
    
    if pathData["horizontalLine"][4]==1000000 or pathData["horizontalLine"][4]>100:
      followPath(pathData)
    else:
      turnRight()    
      
  elif getVariableState("control_state") == STATE_STOP:
  
    if (signDetected!=1 and numSigns!=0)  or (signDetected==1 and coords[2]>SIGN_DISCARD_SIZE and numSigns!=0):
     numSigns=numSigns-1
     
     if numSigns==0:
      global stop_time
      stop_time = time.time()
     
    elif numSigns!=0 and numSigns<NUMBER_OF_MISSED_SIGNS:
      numSigns=numSigns+1
     
    if numSigns!=0:
      followPath(pathData)  
    else:
      stop()
    
  elif getVariableState("control_state") == STATE_GO_STRAIGHT:
    followPath(pathData)
  elif getVariableState("control_state") == STATE_UTURN:
    
    if (signDetected!=5 and numSigns!=0) or (signDetected==5 and coords[2]>SIGN_DISCARD_SIZE and numSigns!=0):
     numSigns=numSigns-1
     
     if numSigns==0:
      uturn_time = time.time()
     
    elif numSigns!=0 and numSigns<NUMBER_OF_MISSED_SIGNS_UTURN:
      numSigns=numSigns+1
     
    if numSigns!=0:
      followPath(pathData)  
    else:
      uturn()
  
  changeStateActions(signDetected,coords)

def changeStateActions(signDetected,coords): 
  global signCounts
  global numSigns
  global stop_time
  global uturn_time
  global turn_time
    
  IncrementSignConfidence(signDetected)
  print(signCounts)
  

  if getVariableState("control_state") == STATE_FOLLOW_PATH:
    logToAll("changeStateActions ; STATE_FOLLOW_PATH ; "+str(signDetected),0)
    
    if validSign("Stop"):
      numSigns = NUMBER_OF_MISSED_SIGNS
      fire(signDetected,coords)
      setVariableState("control_state", STATE_STOP)    
    elif validSign("Left"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_TURNING_LEFT)
    elif validSign("Right"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_TURNING_RIGHT)
    elif validSign("Straight"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_GO_STRAIGHT)
    elif validSign("Uturn"):
      numSigns = NUMBER_OF_MISSED_SIGNS_UTURN
      fire(signDetected,coords)
      setVariableState("control_state", STATE_UTURN)
      
  elif getVariableState("control_state") == STATE_GO_STRAIGHT:
    logToAll("changeStateActions ; STATE_GO_STRAIGHT ; ",0)
    
    setVariableState("control_state", STATE_FOLLOW_PATH)
    
  elif getVariableState("control_state") == STATE_TURNING_RIGHT:
    logToAll("turnRight ; STATE_TURN_RIGHT ; ",0)
    
    if validSign("Stop"):
      numSigns = NUMBER_OF_MISSED_SIGNS
      fire(signDetected,coords)
      setVariableState("control_state", STATE_STOP)    
    elif validSign("Left"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_TURNING_LEFT)
    elif validSign("Right"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_TURNING_RIGHT)
    elif validSign("Straight"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_GO_STRAIGHT)
    elif validSign("Uturn"):
      numSigns = NUMBER_OF_MISSED_SIGNS_UTURN
      fire(signDetected,coords)
      setVariableState("control_state", STATE_UTURN)

  elif getVariableState("control_state") == STATE_TURNING_LEFT:
    logToAll("turnLeft ; STATE_TURNING_LEFT ; ",0)
    
    if validSign("Stop"):
      numSigns = NUMBER_OF_MISSED_SIGNS
      fire(signDetected,coords)
      setVariableState("control_state", STATE_STOP)    
    elif validSign("Left"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_TURNING_LEFT)
    elif validSign("Right"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_TURNING_RIGHT)
    elif validSign("Straight"):
      fire(signDetected,coords)
      setVariableState("control_state", STATE_GO_STRAIGHT)
    elif validSign("Uturn"):
      numSigns = NUMBER_OF_MISSED_SIGNS_UTURN
      fire(signDetected,coords)
      setVariableState("control_state", STATE_UTURN)
      
  elif getVariableState("control_state") == STATE_UTURN:
    logToAll("changeStateActions ; STATE_UTURN ; ",0)
    
    if numSigns==0:
      if (uturn_time + UTURN_WAIT_TIME) < time.time():
        signCounts = {"Stop":0,"Left":0,"Right":0,"Straight":0,"Uturn":0}
        setVariableState("control_state", STATE_FOLLOW_PATH)
    
  elif getVariableState("control_state") == STATE_STOP:
    logToAll("changeStateActions ; STATE_STOP ; ",0)
    if numSigns==0:
      global stop_time
      if (stop_time + STOP_WAIT_TIME) < time.time():
        signCounts = {"Stop":0,"Left":0,"Right":0,"Straight":0,"Uturn":0}
        setVariableState("control_state", STATE_FOLLOW_PATH)

def stop():
  logToAll("stop ; STATE_STOP ; ",0)
  setVariableState("leftMotorSpeed", 0)
  setVariableState("rightMotorSpeed", 0)
  
def turnRight():
  setVariableState("leftMotorSpeed", 5)
  setVariableState("rightMotorSpeed", -5)

def turnLeft():
  setVariableState("leftMotorSpeed", -5)
  setVariableState("rightMotorSpeed", 5)
  
def followPath(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  distance = {"rightDis": pathData["RightLine"][4],"rightAngle": pathData["RightLine"][5],"leftDis":pathData["LeftLine"][4],"horDis":pathData["horizontalLine"][4]}
  
  followPathDistance(distance)

def uturn():
  logToAll("stop ; STATE_UTURN ; ",0)
  setVariableState("leftMotorSpeed", 5)
  setVariableState("rightMotorSpeed", -5)
  
def pxToSpeedBoth(pixels):
  if pixels>180:
   return 4
  if pixels>160:
   return 3
  if pixels>140:
   return 2
  else:
   return 1

def pxToSpeed1(pixels):
  if pixels<320:
   return 4
  if pixels<340:
   return 3
  if pixels<360:
   return 2
  else:
   return 1

def turnRightDistance(pathData2):
  pathData={"rightDis":pathData2["RightLine"][4]};

  if pathData["rightDis"]!=1000000:
    print("right line")
    
    if pathData["rightDis"]>400:
      print("large distance - Move right")
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MIN_MOTOR_SPEED)
      return;
    
    if pathData["rightDis"]>300:
      print("moving to right")
      #should correct to right
      relativeSpeeds("right", pxToSpeed1(pathData["rightDis"]))
    elif pathData["rightDis"]<200 and pathData["rightDis"]>=-320:
      #should correct to left
      print("moving to left")
      relativeSpeeds("left", pxToSpeedBoth(pathData["rightDis"]))
    else:
      #should move straight
      print("moving straight")
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
    return False;
  else:
    print("no left going right")
    relativeSpeeds("right", pxToSpeed1(380))
    return True
        

def followPathDistance(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  if 0==1 and pathData["horDis"]!=1000000 and pathData["horDis"]<160:
    print("horizontal line straight ahead!")
    setVariableState("leftMotorSpeed", 0)
    setVariableState("rightMotorSpeed", 0)
    return;
  
  if pathData["rightDis"]!=1000000 and pathData["leftDis"]!=1000000:
    print("both lines")
    if pathData["leftDis"]<200:
      print("going right")
      #should correct to right
      relativeSpeeds("right", pxToSpeedBoth(pathData["leftDis"]))
    elif pathData["rightDis"]<200:
      #should correct to left
      print("moving to left")
      relativeSpeeds("left", pxToSpeedBoth(pathData["rightDis"]))
    else:
      #should move straight
      print("moving straight")
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
    return;  
  
  if pathData["rightDis"]!=1000000 and pathData["leftDis"]==1000000:
    print("right line")
  
    if pathData["rightDis"]>400:
      print("large distance - Move left")
      setVariableState("leftMotorSpeed", MIN_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
      return;
    
    if pathData["rightDis"]>300:
      print("moving to right")
      #should correct to right
      relativeSpeeds("right", pxToSpeed1(pathData["rightDis"]))
    elif pathData["rightDis"]<200 and pathData["rightDis"]>=-320:
      #should correct to left
      print("moving to left")
      relativeSpeeds("left", pxToSpeedBoth(pathData["rightDis"]))
    else:
      #should move straight
      print("moving straight")
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
    return;
      
  if pathData["leftDis"]!=1000000 and pathData["rightDis"]==1000000:
    print("left line")
    
    if pathData["leftDis"]>400:
      print("large distance - Move right")
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MIN_MOTOR_SPEED)
      return;
    
    if pathData["leftDis"]>300:
      print("moving to left")
      #should correct to left
      relativeSpeeds("left", pxToSpeed1(pathData["leftDis"]))
    elif pathData["leftDis"]<200 and pathData["leftDis"]>=-320:
      #should correct to right
      print("moving to right")
      relativeSpeeds("right", pxToSpeedBoth(pathData["leftDis"]))
    else:
      #should move straight
      print("moving straight")
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
    return;
  
  if pathData["leftDis"]==1000000 and pathData["rightDis"]==1000000:
    print("no lines") 
    print("moving straight") 
    setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
    setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)    
  
#calls
main()
    
