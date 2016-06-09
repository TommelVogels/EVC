# Name
# Description

#include dependencies
import serial #https://pypi.python.org/pypi/pyserial
from Debugging.Debug  import logToAll
from Communication.CommunicationBuffer import USE_UART
from Communication.CommandEncoder import START_BYTE
from Communication.CommandEncoder import END_BYTE

import binascii

#defines
PORT = '/dev/ttyAMA0' # 'COM7' # 'COM3'
BAUDRATE = 115200
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.EIGHTBITS

#variables
UART_opened = 0
receivedData = bytearray()
receivingCommand = 0

if USE_UART:
  try:
    logToAll("Init ; Opening COM port ;", 1)
    serialPort = serial.Serial(port=PORT, baudrate=BAUDRATE, parity=PARITY, stopbits=STOPBITS,bytesize=BYTESIZE,timeout=0)
    UART_opened = 1
  except serial.SerialException:
    logToAll("Init ; COM port could not be opened, no UART communication available! ; ", 1)

#functions
def SendUART(inData):
  logToAll("SendUART ; inData ; "+binascii.hexlify(inData), 2)
  
  if UART_opened==1:
    serialPort.write(inData)

def ReceiveUART():
  global serialPort
  global receivingCommand
  global cmdAvailable
  global receivedData
  
  dataOut = {"cmdAvailable":0,"data":""}
  cmdAvailable = 0
  
  if UART_opened==1:
    #data available
    logToAll("ReceiveUART ; availableBytes ; "+str(serialPort.inWaiting()),3);
    while serialPort.inWaiting()>0:
      data = serialPort.read()
      logToAll("ReceiveUART ; data ; "+str(data)+" - "+str(serialPort.inWaiting()), 4)
      
      if data==START_BYTE and receivingCommand==0:
        logToAll("ReceiveUART ; data ; START_BYTE", 4)
        #start receiving of command
        receivingCommand = 1
      elif data==END_BYTE and receivingCommand==1:
        logToAll("ReceiveUART ; data ; END_BYTE", 4)
        #command has been received
        cmdAvailable = 1
        receivingCommand = 0
        break;
      elif receivingCommand==1:
        logToAll("ReceiveUART ; receivedData ; "+str(data), 4)
        receivedData+=data
        
  if cmdAvailable==1:
    dataOut["cmdAvailable"]=1
    dataOut["data"]=receivedData
    cmdAvailable=0
    receivedData=bytearray()
  
  logToAll("ReceiveUART ; dataOut ; "+str(dataOut), 2)
  
  return dataOut
  
#calls
    
  
