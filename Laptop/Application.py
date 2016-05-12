# LaptopApplication.py
# Main application to run from the laptop in order to monitor and control the solar car
# from the Laptop

#defines


#include dependencies
import time

from Debugging.Debug  import logToAll
from UI.UserInterface import buildUI
from Communication.CommandEncoder  import DecodeCmd
from Communication.CommandEncoder  import EncodeCmd
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd
from Communication.CommunicationBuffer  import SendCmds
from Communication.CommunicationBuffer  import ReceiveCmds

#variables


#functions

def main():
    logToAll("main ; Main application started ; ",1)

    #build and run the UI
    buildUI()
    
    while 1:
        #read to send/receive commands
        SendCmds()
        ReceiveCmds()
        
        cmd = PopCmd()

        #time.sleep(0.5)

    
#calls
main()
