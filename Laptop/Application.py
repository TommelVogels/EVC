# LaptopApplication.py
# Main application to run from the laptop in order to monitor and control the solar car
# from the Laptop

#defines


#include dependencies
from Debugging.Debug  import logToAll
from UI.UserInterface import buildUI
from Communication.CommandEncoder  import GetCmd
from Communication.CommandEncoder  import SetCmd
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd

import time


#variables


#functions

def main():
    logToAll("Main application started")

    #build and run the UI
    buildUI()

    while 1:
        #read to see if there are commands
        cmd = PopCmd()
        
        print("test")
        time.sleep(1)
        #loop to read from TCP


    
#calls
main()
