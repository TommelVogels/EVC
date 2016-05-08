# Name
# Description

#include dependencies
import serial #https://pypi.python.org/pypi/pyserial
from Debugging.Debug  import logToAll
from Communication.CommunicationBuffer import USE_UART

#defines
PORT = 'COM7'
BAUDRATE = 115200
PARITY = serial.PARITY_NONE
STOPBITS = serial.STOPBITS_ONE
BYTESIZE = serial.EIGHTBITS

#variables
UART_opened = 0

if USE_UART:
  try:
    logToAll("Opening COM port")
    serialPort = serial.Serial(port=PORT, baudrate=BAUDRATE, parity=PARITY, stopbits=STOPBITS,bytesize=BYTESIZE,timeout=0)
    UART_opened = 1
  except serial.SerialException:
    logToAll("COM port could not be opened, no UART communication available!")

#functions
def SendUART(inData):
  logToAll("SendUART ; "+str(inData))

def ReceiveUART():
  global serialPort
  
  logToAll("ReceiveUART ; ")
  bytesToRead = serialPort.inWaiting()
  stri =   serialPort.read(bytesToRead)
  print(str(stri)+str(bytesToRead))
  
#calls
    
  
