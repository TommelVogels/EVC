# Debug.py
# Used to log to console and file for debugging purposes

#defines
DEBUG_LEVEL = 1

#include dependencies
from datetime import datetime

#variables
fileName =  __file__.replace("Debug.py","")+"LOGS/"
fileName += datetime.now().strftime('%Y%m%d%H%M%S')+".txt"

def logToConsole(msg, level):
    if DEBUG_LEVEL>=level:
      print("["+str(datetime.now())+"]; "+msg)

def logToFile(msg, level):
    if DEBUG_LEVEL>=level:
      logFile = open(fileName,"a")
      logFile.write("["+str(datetime.now())+"]; "+msg+"\n")
      logFile.close()
    
def logToAll(msg, level):
    logToConsole(msg, level)
    logToFile(msg, level)
