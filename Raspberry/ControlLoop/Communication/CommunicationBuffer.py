#CommunicationBuffer.py
# Uses 2 FIFOs to handle the receiving and sending of commands
# Sends the commands queued by the Raspberry to the defined communication channels
# Receives commands and queus them from the defined communication channels

#defines (only use 1 communication channel)
USE_UART = 0
USE_DBUS = 1

from Communication.Commands.Commands  import CommandType
from Communication.CommandEncoder import EncodeCmd
from Communication.CommandEncoder import DecodeCmd
from Communication.Commands.Commands  import CommandTypeToInt

if USE_DBUS==1:
  import dbus
  import Communication.CommChannels.DBUS.common as common
  
  bus = dbus.SessionBus()
  proxy = bus.get_object(common.ECHO_BUS_NAME, common.ECHO_OBJECT_PATH)
  iface = dbus.Interface(proxy, common.ECHO_INTERFACE)
  
  def PopCmd():
    cmd = iface.pop()
    cmd_ba = bytearray(cmd)
    if len(cmd_ba) != 0:
      cmd_ba = cmd_ba[1:-1]
      return DecodeCmd(cmd_ba)
    else: 
      return {'cmdID':CommandType.NO_COMMAND,'data':bytearray([])}
  
  def PushCmd(inID,inData):
    id = CommandTypeToInt(inID)
    data = bytearray(inData)
    iface.push(data, id)
    
  
  
else:
  #include dependencies
  import serial #https://pypi.python.org/pypi/pyserial
  import sys
  is_py2 = sys.version[0] == '2'
  if is_py2:
      import Queue as queue
  else:
      import queue as queue
      
  import binascii

  from Debugging.Debug  import logToAll
  from Communication.CommChannels.UART.UART  import ReceiveUART
  from Communication.CommChannels.UART.UART  import SendUART

  #variables

  # Queue to contain commands received over UART
  receiveQueue = queue.Queue(maxsize=16)
  #Queue to contain commands to send over UART
  sendQueue = queue.Queue(maxsize=16)
  
  def SendCmds():
    try:
      command = sendQueue.get(False)
      logToAll("SendCmds ; command ; " + binascii.hexlify(command), 1)
          
      #send via channels
      if USE_UART==1:
        SendUART(command)
        
    except queue.Empty:
      # Handle empty queue here        
      logToAll("SendCmd ; command ;  QueueEmpty", 2)
    
  def ReceiveCmds():
    #receive via channels
    if USE_UART==1:
      dataIn = ReceiveUART()
      if dataIn['cmdAvailable']==1:
        decoded = DecodeCmd(dataIn['data'])
        logToAll("ReceiveCmds ; dataIn ; cmdAvailable "+binascii.hexlify(dataIn['data']),1)
        receiveQueue.put(decoded)

  def PushCmd(inID,inData):
    logToAll("PushCmd ; inData ; " + str(inID) + " " + binascii.hexlify(inData),1)
    encoded = EncodeCmd(inID,inData)
    try:
      sendQueue.put(encoded, False)
    except queue.Full:
      #handle full queue here
      logToAll("PushCmd ; command ; QueueFull", 2)
      
    SendCmds()
    
  def PopCmd():
    ReceiveCmds()
    SendCmds()
    
    command = {'cmdID':CommandType.NO_COMMAND,'data':bytearray([])}
    
    try:
      command = receiveQueue.get(False)
      logToAll("PopCmd ; command ; " + str(command),1)
    except queue.Empty:
      # Handle empty queue here        
      logToAll("PopCmd ; command ; QueueEmpty", 2)
    return command