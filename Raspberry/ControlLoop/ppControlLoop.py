# ControlLoop.py
# Main application and entry point

#defines


#include dependencies
import math
import time
import pp

from Debugging.Debug  import logToAll
from Parameters.Parameters import setVariableState
from Parameters.Parameters import getVariableState

from Communication.CommandEncoder  import DecodeCmd
from Communication.CommandEncoder  import EncodeCmd
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd
from Communication.CommunicationBuffer  import SendCmds
from Communication.CommunicationBuffer  import ReceiveCmds

from Communication.Commands.Commands  import CommandType

from ImageProcessing.PathRecognition.PathRecognition  import findPath
from ImageProcessing.SignDetection.SignDetection  import findSigns
from ImageProcessing.FrameFetch  import getFrame
from ImageProcessing.FrameFetch  import camera
from ImageProcessing.FrameFetch  import rawCapture
import cv2

## PP ##
from ImageProcessing.PathRecognition.PathRecognition  import hough
from ImageProcessing.PathRecognition.PathRecognition  import sortBy
from ImageProcessing.PathRecognition.PathRecognition import findClosestRightLineDistance
from ImageProcessing.PathRecognition.PathRecognition import findClosestLeftLineAngle
from ImageProcessing.PathRecognition.PathRecognition import findClosestRightLineAngle
from ImageProcessing.PathRecognition.PathRecognition import findClosestLeftLineDistance
from ImageProcessing.PathRecognition.PathRecognition import perp
from ImageProcessing.PathRecognition.PathRecognition import seg_intersect
from ImageProcessing.PathRecognition.PathRecognition import findHorizontalLine



#variables
desiredMotorSpeed = 255

ppservers = ()
job_server = pp.Server(2, ppservers=ppservers)

#functions
def main():
  logToAll("main ; Main application started ; ",1)

  #while 1:
  
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    t1 = time.time()
    image = (frame.array)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    top = image[120:360,0:640]
    bottom = image[250:480,0:640]
    rawCapture.truncate(0)
    t2 = time.time()
    logToAll("getFrame ; Get Frame ;  "+ str(float(t2-t1)) + " seconds",0)
    frameCut =  [top,bottom]
      
    cmd = PopCmd()
    
    #time.sleep(1)
    
    #if cmd["cmdID"] == CommandType.BOTH_MOTOR_SPEED:
    #  print("response for left motor")
    #frame = getFrame();
    
    ##PP here
    
    #job1 = job_server.submit(findPath, (frameCut[1],), (hough,sortBy,findClosestRightLineDistance,findClosestLeftLineAngle,findClosestRightLineAngle,findClosestLeftLineDistance,perp,seg_intersect,findHorizontalLine,), ("cv2","time","numpy", "math",)) 
    #pathData = job1()
    
    pathData = findPath(frameCut[1])
    signData = findSigns(frameCut[0])
    

    print(str(pathData))
    
    setVariableState("sign", signData)
    
    runStateActions(signData,pathData)    
	
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

def relativeSpeeds(direction, speed):
  motorFast="leftMotorSpeed"
  motorSlow="rightMotorSpeed"
  if direction=="left":
    motorFast = "rightMotorSpeed"
    motorSlow = "leftMotorSpeed"
  
  if speed==1:
    setVariableState(motorFast, 50)
    setVariableState(motorSlow, 0)
  elif speed==2:
    setVariableState(motorFast, 20)
    setVariableState(motorSlow, 0)  
  elif speed==3:
    setVariableState(motorFast, 50)
    setVariableState(motorSlow, 5) 
  elif speed==4:
    setVariableState(motorFast, 20)
    setVariableState(motorSlow, 5) 

signCounts = {"Stop":0,"Left":0,"Right":0,"Straight":0,"Uturn":0}

SIGN_DETECTED_INCREMENT = 1
SIGN_NOT_DETECTED_DECREMENT = 0.25
SIGN_DETECTED_CONFIDENCE = 3

def IncrementSignConfidence(signDetected):
  if signCounts["Stop"]>0:
    signCounts["Stop"] = signCounts["Stop"] + SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Left"]>0:
    signCounts["Left"] = signCounts["Left"] + SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Right"]>0:
    signCounts["Right"] = signCounts["Right"] + SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Straight"]>0:
    signCounts["Straight"] = signCounts["Straight"] + SIGN_NOT_DETECTED_DECREMENT
  if signCounts["Uturn"]>0:
    signCounts["Uturn"] = signCounts["Uturn"] + SIGN_DETECTED_INCREMENT
    
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
  if signCounts[sign]>SIGN_DETECTED_CONFIDENCE:
    return True
  else:
    return False
   
def runStateActions(signDetected, pathData):
  if getVariableState("control_state") == STATE_FOLLOW_PATH:
    followPath(pathData)
  elif getVariableState("control_state") == STATE_TURNING_LEFT:
    logToAll("runStateActions ; STATE_TURNING_LEFT ; ",4)
  elif getVariableState("control_state") == STATE_TURNING_RIGHT:
    logToAll("runStateActions ; STATE_TURNING_RIGHT ; ",4)
  elif getVariableState("control_state") == STATE_STOP:   
    stop()
  elif getVariableState("control_state") == STATE_GO_STRAIGHT:
    followPath(pathData)
  elif getVariableState("control_state") == STATE_UTURN:
    logToAll("runStateActions ; STATE_UTURN ; ",4)
  
  changeStateActions(signDetected)

def changeStateActions(signDetected): 
  if getVariableState("control_state") == STATE_FOLLOW_PATH:
    logToAll("changeStateActions ; STATE_FOLLOW_PATH ; ",4)
    
    IncrementSignConfidence(signDetected)
    
    if validSign("Stop"):
      setVariableState("control_state", STATE_STOP)
      
      global stop_time
      stop_time = time.time()
    
    #elif validSign("Left"):
      #setVariableState("control_state", STATE_TURNING_LEFT)
    #elif validSign("Right"):
      #setVariableState("control_state", STATE_TURNING_RIGHT)
    elif validSign("Straight"):
      setVariableState("control_state", STATE_GO_STRAIGHT)
    #elif validSign("Uturn"):
      #setVariableState("control_state", STATE_UTURN)
      
  elif getVariableState("control_state") == STATE_GO_STRAIGHT:
    logToAll("changeStateActions ; STATE_GO_STRAIGHT ; ",4)
    
    setVariableState("control_state", STATE_FOLLOW_PATH)
    
  elif getVariableState("control_state") == STATE_STOP:
    logToAll("changeStateActions ; STATE_STOP ; ",4)
    
    if (stop_time + STOP_WAIT_TIME) < time.time():
      setVariableState("control_state", STATE_FOLLOW_PATH)
   
def stop():
  logToAll("stop ; STATE_STOP ; ",4)
  setVariableState("leftMotorSpeed", 0)
  setVariableState("rightMotorSpeed", 0)
   
def followPath(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  distance = {"rightDis": pathData["RightLine"][4],"rightAngle": pathData["RightLine"][5],"leftDis":pathData["LeftLine"][4],"horDis":pathData["horizontalLine"][4]}
  
  followPathDistance(distance)
  
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

def followPathDistance(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  if pathData["horDis"]!=1000000 and pathData["horDis"]<160:
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
    
