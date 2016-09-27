import sys
import os
import dbus

# project includes
import common

bus = dbus.SessionBus()
proxy = bus.get_object(common.ECHO_BUS_NAME, common.ECHO_OBJECT_PATH)
iface = dbus.Interface(proxy, common.ECHO_INTERFACE)

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

  
def PopCmd():
  cmd = iface.pop()
#  print(cmd)
  cmd_ba = bytearray(cmd)
#  print(cmd_ba)
  print(len(cmd_ba))
  
  if len(cmd_ba) != 0:
    cmd_ba = cmd_ba[1:-1]
    return DecodeCmd(cmd_ba)
  else: 
    print("else what, huh?")
      
def test():
  data = [0xa5, 0x01, 0x22, 0x23, 0x5a]
  ba = bytearray(data)
  iface.push(ba, 0)
  
def setMotorLeft(val):
  iface.SetMotor(True, False, val, 0)

def setMotorRight(val):
  iface.SetMotor(False, True, 0, val)

def setMotorBoth(val1, val2):
  iface.SetMotor(True, True, val1, val2)


