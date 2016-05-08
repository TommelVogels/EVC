# ControlLoop.py
# Main application and entry point

#defines


#include dependencies
from Debugging.Debug  import logToAll
from Communication.CommandEncoder  import GetCmd
from Communication.CommandEncoder  import SetCmd
from Communication.CommunicationBuffer  import PopCmd
from Communication.CommunicationBuffer  import PushCmd

#variables

#functions
def main():
  logToAll("Main Started")
  
  PushCmd("a")
  PopCmd()
  
  print(str(SetCmd("a")))
    
#calls
main()
    