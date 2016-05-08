# Debug.py
# Used to log to console and file for debugging purposes

#defines


#include dependencies
from datetime import datetime

#variables
fileName =  __file__.replace("Debug.py","")+"LOGS/"
fileName += datetime.now().strftime('%Y%m%d%H%M%S')+".txt"

def logToConsole(msg):
    print("["+str(datetime.now())+"]; "+msg)

def logToFile(msg):
    logFile = open(fileName,"a")
    logFile.write("["+str(datetime.now())+"]; "+msg+"\n")
    logFile.close()
    
def logToAll(msg):
    logToConsole(msg)
    logToFile(msg)

