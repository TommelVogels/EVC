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

from Communication.Commands.Commands  import CommandType

from ImageProcessing.PathRecognition.PathRecognition  import findPath
from ImageProcessing.SignDetection.SignDetection  import findSigns

#variables
desiredMotorSpeed = 255

#functions
def main():
  logToAll("main ; Main application started ; ",1)

  while 1:
      
    cmd = PopCmd()
    
    if cmd["cmdID"] == CommandType.BOTH_MOTOR_SPEED:
      print("response for left motor")
    
    pathData = findPath()
    signData = findSigns()
    

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
MAX_MOTOR_SPEED = 100
MAX_LINE_OFFSET_POS   = 320
ONE_LINE_LOCATION_SETPOINT = 300 #if only one line is visible try to keep it at 160 1/4 of image
SEARCH_IN_DIRECTION_TIME = 2 #if no lines move in one direction for 5 seconds to try and find line
SEARCH_SPEED_FAST = 10
SEARCH_SPEED_SLOW = 0
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
    
    if signDetected == 1:
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
  setVariableState("leftMotorSpeed", 0)
  setVariableState("rightMotorSpeed", 0)
   
def followPath(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  #motorSpeeds=calculateMotorSpeeds(pathData)
  
  distance = {"rightDis": pathData["RightLine"][4],"rightAngle": pathData["RightLine"][5],"leftDis":-1}
  
  followPathDistance(distance)
  
  #setVariableState("leftMotorSpeed", motorSpeeds["left"])
  #setVariableState("rightMotorSpeed", motorSpeeds["right"])

   
def calculateMotorSpeeds(pathData):
  
  turnLeft = 0
  motorSpeeds = {"left":0,"right":0}
  
  angle = pathData[0][4]
  
  # if angle is negative turn left else turn right
  if(angle<45):
    turnLeft = 1
    #turn to positive number
    angle = angle*-1
  else:
    turnLeft = 0
    
  angle = angle/2
  
  speed1 = int(math.cos(math.radians(angle))*desiredMotorSpeed)
  speed2 = int(math.sin(math.radians(angle))*desiredMotorSpeed)
  
  if (turnLeft==1):
    motorSpeeds["left"] = speed1
    motorSpeeds["right"] = speed2
  else:
    motorSpeeds["left"] = speed2
    motorSpeeds["right"] = speed1
  
  return motorSpeeds

def followPathDistance(pathData):
  logToAll("followPath ; STATE_FOLLOW_PATH | STATE_GO_STRAIGHT ; ",4)
  
  #if pathData["rightAngle"]<20 or pathData["rightAngle"]>160:
  #  return;
  if pathData["rightDis"]>600:
    setVariableState("leftMotorSpeed", 1)
    setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
    return;
  
  if pathData["rightDis"]>300 and pathData["rightDis"]>=0:
    #should correct to right
    setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
    setVariableState("rightMotorSpeed", 1)
  elif pathData["rightDis"]<200 and pathData["rightDis"]>=0:
    #should correct to right
    setVariableState("leftMotorSpeed", 1)
    setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
  else:
    #should correct to right
    setVariableState("leftMotorSpeed", MAX_MOTOR_SPEED)
    setVariableState("rightMotorSpeed", MAX_MOTOR_SPEED)
       
  
#calls
main()
    
