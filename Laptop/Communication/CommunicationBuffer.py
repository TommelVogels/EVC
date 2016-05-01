#CommunicationBuffer.py
# Uses 2 FIFOs to handle the receiving and sending of commands
# Sends the commands queued by the Raspberry to the defined communication channels
# Receives commands and queus them from the defined communication channels

#defines
USE_UART = 1
USE_TCP  = 1


#include dependencies
import queue

#variables

# Queue to contain commands received over UART/TCP
receiveQueue = queue.Queue(maxsize=32)
#Queue to contain commands to send over UART/TCP
sendQueue = queue.Queue(maxsize=32)

def GetCmd():
    print("GetCmd")

    receive_Queue.put("test")

    queuedCmd = 

    

GetCmd()
