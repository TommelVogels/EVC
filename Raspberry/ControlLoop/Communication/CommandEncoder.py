# CommandEncoder
# Manages the encoding and decoding of commands

#defines
START_BYTE = bytearray([0xA5])
END_BYTE = bytearray([0x5A])

#include dependencies
import binascii

from Debugging.Debug  import logToAll
from Communication.Commands.Commands  import CommandType
from Communication.Commands.Commands  import CommandTypeToInt
from Communication.Commands.Commands  import IntToCommandType

#variables

#functions
def DecodeCmd(inData):
  logToAll("DecodeCmd ; inData ; "+binascii.hexlify(inData), 3)
  
  length = inData[0];
  
  checksum = int(length)
  
  if len(inData) != (length + 2):
    return {'cmdID':CommandType.NO_COMMAND,'data':bytearray([])}
  
  
  cmdID = inData[1]
  checksum = checksum ^ cmdID
  
  found = 1
  #for value in list(CommandType):
  #  if (CommandTypeToInt(value) == int(cmdID)):
  #    found = 1
  
  if found == 0:
    logToAll("DecodeCmd ; Command unknown ; "+ str(int(cmdID)), 2)
    return {'cmdID':CommandType.NO_COMMAND,'data':bytearray([])}
  
  data = bytearray([])
  
  for value in inData[2:-1]:
    data.append(value)
    checksum = checksum ^ value

  if checksum!=int(inData[-1]):
    logToAll("DecodeCmd ; Checksum mismatch ; "+ str(checksum) + " " + str((inData[-1])), 2)
    return {'cmdID':CommandType.NO_COMMAND,'data':bytearray([])}
  
  return {'cmdID':IntToCommandType(cmdID),'data':data}

def EncodeCmd(inCmd,inData):
  logToAll("EncodeCmd ; inData ;" + str(inCmd) +  " " + binascii.hexlify(inData), 3)

  checksum = 0
  length = (len(inData)+1)
  
  checksum = checksum ^ length
  checksum = checksum ^ int(CommandTypeToInt(inCmd))
  
  array = bytearray();
  array.append(START_BYTE[0])
  array.append(length)
  array.append(CommandTypeToInt(inCmd))
  
  for value in inData:
    checksum = checksum ^ value
    array.append(value)
    
  array.append(checksum)
  array.append(END_BYTE[0])
  
  return array
  
#calls
    
  
