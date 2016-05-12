#CommunicationBuffer.py
# Uses 2 FIFOs to handle the receiving and sending of commands
# Sends the commands queued by the Raspberry to the defined communication channels
# Receives commands and queus them from the defined communication channels

#defines
USE_UART = 1
USE_TCP  = 1


#include dependencies
import serial #https://pypi.python.org/pypi/pyserial
import queue

from Debugging.Debug  import logToAll
from Communication.CommChannels.UART.UART  import ReceiveUART
from Communication.CommChannels.UART.UART  import SendUART

#variables

# Queue to contain commands received over UART/TCP
receiveQueue = queue.Queue(maxsize=16)
#Queue to contain commands to send over UART/TCP
sendQueue = queue.Queue(maxsize=16)

def SendCmds():
  try:
    command = sendQueue.get(False)
    logToAll("SendCmds ; command ; " + str(command), 1)
        
    #send via channels
    if USE_UART==1:
      SendUART(command)
      
  except queue.Empty:
    # Handle empty queue here        
    logToAll("PushCmd ; command ;  QueueEmpty", 2)
  
def ReceiveCmds():
  #receive via channels
  if USE_UART==1:
    dataIn = ReceiveUART()
    if dataIn['cmdAvailable']==1:
      logToAll("PushCmd ; dataIn ; cmdAvailable",1)
      receiveQueue.put(dataIn['data'])

def PushCmd(inData):
  logToAll("PushCmd ; inData ; " + str(inData),1)
  sendQueue.put(inData)
  
def PopCmd():
  try:
    command = receiveQueue.get(False)
    logToAll("PopCmd ; command ; " + str(command),1)
  except queue.Empty:
    # Handle empty queue here        
    logToAll("PopCmd ; command ; QueueEmpty", 2)
  return "test"