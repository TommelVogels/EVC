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
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd
from Communication.Commands.Commands  import CommandType
from Communication.Commands.Commands  import CommandTypeToInt
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
        cmd = PopCmd()
        

        #time.sleep(0.5)
    
    
#calls
LaptopApplication()
