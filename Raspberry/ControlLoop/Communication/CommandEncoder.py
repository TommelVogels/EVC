# CommandEncoder
# Manages the encoding and decoding of commands

#defines
START_BYTE = bytes([0xA5])
END_BYTE = bytes([0x5A])

#include dependencies
from Debugging.Debug  import logToAll
from Communication.Commands.Commands  import CommandType

#variables

#functions
def DecodeCmd(inData):
  logToAll("GetCmd ; inData ; "+str(inData), 1)
  return {'cmdID':0x01,'data':'1','valid':1}

def EncodeCmd(inData):
  logToAll("SetCmd ; inData ; "+str(inData), 1)
  return CommandType.ERROR_STATUS
  
#calls
    
  
