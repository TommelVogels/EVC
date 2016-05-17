# ControlLoop.py
# Main application and entry point

#defines


#include dependencies
from Debugging.Debug  import logToAll
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

  while 1:
    #read to send/receive commands
    SendCmds()
    ReceiveCmds()
              
    cmd = PopCmd()
    
#calls
main()
    
