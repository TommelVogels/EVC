/*
 * CommandCommunication 
 * Used to retrieve/send data over UART
 */

#define MAX_QUEUE_LEN 15

char cmdRecvQueue[MAX_QUEUE_LEN] = {0};
char readPointer = 0;

void CommandComm_Init()
{
  Serial.begin(115200);
}

CommandType CommandComm_FetchCmd()
{
  CommandType decodedCommand = NO_COMMAND;
  
  while(Serial.available()>0)
  {
    if(readPointer>MAX_QUEUE_LEN)
    {
      ErrorHandler_SetError(RECV_BUFF_OVERFLOW);
      break;
    }
    
    cmdRecvQueue[readPointer] = Serial.read();
    readPointer++;
  }

  //data in queue
  if(readPointer>0)
  {
    char bytesRead = 0;
    
    decodedCommand = CommandDecoder(cmdRecvQueue, readPointer, MAX_QUEUE_LEN, 0, &bytesRead);

    if(decodedCommand == COMMAND_INVALID)
    {
      //command buffer is corrupt flush it and send NACK
      readPointer = 0;
      
    }
    else if(decodedCommand != NO_COMMAND)
    {
      //command was read clear the queue
      readPointer = 0;
    }
    //else waiting for more data
    
  }
  
  return decodedCommand;
}

void CommandComm_SendCmd()
{
  
}

