# LaptopApplication.py
# Main application to run from the laptop in order to monitor and control the solar car
# from the Laptop

#defines


#include dependencies
from Debugging.Debug  import logToAll
from UI.UserInterface import buildUI

import time


#variables


#functions

def main():
    logToAll("Main application started")

    #build and run the UI
    buildUI()

    while 1:
        #loop to read from UART
        print("test")
        time.sleep(1)
        #loop to read from TCP


    
#calls
main()
