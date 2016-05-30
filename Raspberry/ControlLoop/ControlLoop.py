# ControlLoop.py
# Main application and entry point

#defines


#include dependencies
import math
import time

from Debugging.Debug  import logToAll
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
    
    #pathData = findPath()
    signData = findSigns()
    
    pathData["angle"] = pathData["angle"] + 1
    
    motorSpeeds = calculateMotorSpeeds()

    SendCmds()
    ReceiveCmds()
        
    
    time.sleep(1)
    
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
  
  print(str(pathData["angle"])+" "+str(angle)+ " Left:" + str(motorSpeeds["left"])+ " Right:" + str(motorSpeeds["right"]));
    
#calls
main()
    
