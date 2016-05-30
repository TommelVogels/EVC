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
from Communication.CommunicationBuffer  import SendCmds
from Communication.CommunicationBuffer  import ReceiveCmds

from ImageProcessing.PathRecognition.PathRecognition  import findPath
from ImageProcessing.SignDetection.SignDetection  import findSigns

#variables
desiredMotorSpeed = 100

#functions
def main():
  logToAll("main ; Main application started ; ",1)

  while 1:
    #read to send/receive commands
    #SendCmds()
    #ReceiveCmds()
              
    #cmd = PopCmd()
    
    pathData = findPath()
    signData = findSigns()
    
    setVariableState("leftDis", pathData["leftDis"])
    setVariableState("rightDis", pathData["rightDis"])
    
    setVariableState("sign", signData)
    
    runStateActions(signData,pathData)
    
    # pathData["angle"] = pathData["angle"] + 1
    #setVariableState("angle", pathData["angle"])
    
    #motorSpeeds = calculateMotorSpeeds()
    
    #setVariableState("leftMotorSpeed", motorSpeeds["left"])
    #setVariableState("rightMotorSpeed", motorSpeeds["right"])
    
    
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
MAX_MOTOR_SPEED = 100
MAX_LINE_OFFSET_POS   = 320
ONE_LINE_LOCATION_SETPOINT = 160 #if only one line is visible try to keep it at 160 1/4 of image
SEARCH_IN_DIRECTION_TIME = 0.25 #if no lines move in one direction for 5 seconds to try and find line
SEARCH_SPEED_FAST = 20
SEARCH_SPEED_SLOW = 10
lost_search_time = 0
lost_search_attempt = 0
    
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
    
    if signDetected == 100: #1
      setVariableState("control_state", STATE_STOP)
      
      global stop_time
      stop_time = time.time()
    
    #elif signDetected == 2:
      #setVariableState("control_state", STATE_TURNING_LEFT)
    #elif signDetected == 3:
      #setVariableState("control_state", STATE_TURNING_RIGHT)
    elif signDetected == 4:
      setVariableState("control_state", STATE_GO_STRAIGHT)
    #elif signDetected == 5:
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
  #setVariableState("leftMotorSpeed", 0)
  #setVariableState("rightMotorSpeed", 0)
   
def followPath(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  global lost_search_attempt
  global lost_search_time
  
  #if both lines are visible move to keep the offset of left and right the same
  if pathData["leftDis"]>=0 and pathData["rightDis"]>=0:
  
    lost_search_attempt = 0
    lost_search_time = 0
    
    difference = abs(pathData["leftDis"]-pathData["rightDis"])/2
    
    if pathData["leftDis"]>pathData["rightDis"]:
      #should correct to left
      if difference>MAX_MOTOR_SPEED/2:
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
        setVariableState("rightMotorSpeed", 0)
      else:
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2+difference)
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2-difference)
    elif pathData["rightDis"]>pathData["leftDis"]:
      #should correct to right
      if difference>MAX_MOTOR_SPEED/2:
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
        setVariableState("leftMotorSpeed", 0)
      else:
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2+difference)
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2-difference)
    else:
      #no correction needed
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2)
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2)
  
  #if only one line is visible try to keep line at an offset (quarter of image to right or left)
  elif pathData["leftDis"]>=0 and pathData["rightDis"]<0:
    #only left line visible
    
    lost_search_attempt = 0
    lost_search_time = 0
    
    difference = abs(pathData["leftDis"]-ONE_LINE_LOCATION_SETPOINT)/2
    
    if pathData["leftDis"]<ONE_LINE_LOCATION_SETPOINT:
      #should correct to right
      if difference>MAX_MOTOR_SPEED/2:
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
        setVariableState("rightMotorSpeed", 0)
      else:
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2+difference)
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2-difference)
    elif pathData["leftDis"]>ONE_LINE_LOCATION_SETPOINT:
      #should correct to left
      if difference>MAX_MOTOR_SPEED/2:
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
        setVariableState("leftMotorSpeed", 0)
      else:
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2+difference)
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2-difference)
    else:
      #no correction needed
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2)
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2)
      
  elif pathData["rightDis"]>=0 and pathData["leftDis"]<0:
    #only right line visible
    
    lost_search_attempt = 0
    lost_search_time = 0
    
    difference = abs(pathData["rightDis"]-ONE_LINE_LOCATION_SETPOINT)/2
    
    if pathData["rightDis"]>ONE_LINE_LOCATION_SETPOINT:
      #should correct to right
      if difference>MAX_MOTOR_SPEED/2:
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
        setVariableState("rightMotorSpeed", 0)
      else:
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2+difference)
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2-difference)
    elif pathData["rightDis"]<ONE_LINE_LOCATION_SETPOINT:
      #should correct to left
      if difference>MAX_MOTOR_SPEED/2:
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
        setVariableState("leftMotorSpeed", 0)
      else:
        setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2+difference)
        setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2-difference)
    else:
      #no correction needed
      setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED/2)
      setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED/2)
  
  #oh crap no lines are visible move left/right slowly until line is detected
  elif pathData["leftDis"]<0 and pathData["rightDis"]<0:
  
    #slowly increase the search duration 
    if (lost_search_time + SEARCH_IN_DIRECTION_TIME*lost_search_attempt) < time.time():
      lost_search_attempt = lost_search_attempt + 1
      lost_search_time = time.time()

    if (lost_search_attempt%2==0):
      #if even go in one direction
      setVariableState("rightMotorSpeed", SEARCH_SPEED_FAST)
      setVariableState("leftMotorSpeed", SEARCH_SPEED_SLOW)
    else:
      #if odd go the other direction
      setVariableState("rightMotorSpeed", SEARCH_SPEED_SLOW)
      setVariableState("leftMotorSpeed", SEARCH_SPEED_FAST)
    
  
   
def calculateMotorSpeeds():
  global pathData
  
  turnLeft = 0
  motorSpeeds = {"left":0,"right":0}
  
  angle = pathData["angle"]
  
  # if angle is negative turn left else turn right
  if(angle<0):
    turnLeft = 1
    #turn to positive number
    angle = angle*-1
  else:
    turnLeft = 0
    
  angle = angle/2 + 45
  
  speed1 = int(math.cos(math.radians(angle))*desiredMotorSpeed)
  speed2 = int(math.sin(math.radians(angle))*desiredMotorSpeed)
  
  if (turnLeft==1):
    motorSpeeds["left"] = speed1
    motorSpeeds["right"] = speed2
  else:
    motorSpeeds["left"] = speed2
    motorSpeeds["right"] = speed1
  
  return motorSpeeds
    
#calls
#main()
    
