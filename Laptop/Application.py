# LaptopApplication.py
# Main application to run from the laptop in order to monitor and control the solar car
# from the Laptop

#defines
EMULATE_CONTROL_LOOP = 1

#include dependencies
import time

from Debugging.Debug  import logToAll
from UI.UserInterface import buildUI

from ControlLoop import main
from Communication.CommandEncoder  import DecodeCmd
from Communication.CommandEncoder  import EncodeCmd
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd
from Communication.CommunicationBuffer  import SendCmds
from Communication.CommunicationBuffer  import ReceiveCmds

#variables


#functions

def LaptopApplication():
    logToAll("LaptopApplication ; Main LaptopApplication started ; ",1)

    #build and run the UI
    buildUI()
    
    #call the control loop
    if EMULATE_CONTROL_LOOP==1:
      main()
    else:
    
      while 1:
        #read to send/receive commands
        SendCmds()
        ReceiveCmds()
        
        cmd = PopCmd()

        #time.sleep(0.5)
    
    
#calls
LaptopApplication()
