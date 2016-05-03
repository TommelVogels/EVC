# CommandEncoder
# Manages the encoding and decoding of commands

#defines


#include dependencies
from Debugging.Debug  import logToAll
from Communication.Commands.Commands  import CommandType

#variables

#functions
def GetCmd(inData):
  logToAll("GetCmd ; "+str(inData))
  return {'cmdID':0x01,'data':'1','valid':1}

def SetCmd(inData):
  logToAll("SetCmd ; "+str(inData))
  return CommandType.ERROR_STATUS
  
#calls
    
  
