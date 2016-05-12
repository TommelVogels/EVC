#CommunicationBuffer.py
# Uses 2 FIFOs to handle the receiving and sending of commands
# Sends the commands queued by the Raspberry to the defined communication channels
# Receives commands and queus them from the defined communication channels

#defines
USE_UART = 1
USE_TCP  = 1


#include dependencies
import queue
from Debugging.Debug  import logToAll


#variables

# Queue to contain commands received over UART/TCP
receiveQueue = queue.Queue(maxsize=16)
#Queue to contain commands to send over UART/TCP
sendQueue = queue.Queue(maxsize=16)

if USE_UART:
  InitUART()

  #def PushCmd(inID,inData):
def PushCmd(inData):
    logToAll("PushCmd ; " + str(inData))

    sendQueue.put(inData)
    
    #send via channels

#{cmID:NONE,data:{0}}def PopCmd():
def PopCmd():

    #receive via channels

    try:
        command = receiveQueue.get(False)
        logToAll("PopCmd ; " + str(command))
    except queue.Empty:
        # Handle empty queue here        
        logToAll("PopCmd ; QueueEmpty")
    return "test"
