/*
 * CommandCommunication 
 * Used to retrieve/send data over UART
 */

#define MAX_BUFF_LEN 15

#define START_BYTE 0xA5
#define END_BYTE   0x5A

char cmdRecvQueue[MAX_BUFF_LEN] = {0};
bool readingCmd = false;
bool availableCmd = false;
char readPointer = 0;

void CommandComm_Init()
{
  Serial.begin(115200);
}

CommandType CommandComm_FetchCmd(unsigned char* outBuff)
{
  CommandType decodedCommand = NO_COMMAND;
  
  while(Serial.available()>0)
  {
    unsigned char byteRecv = Serial.read();

    if(byteRecv == START_BYTE && readingCmd == false)
    {
      //start byte is received so next bytes are part of command
      readingCmd = true;
    }
    else if(byteRecv == END_BYTE && readingCmd == true)
    {
      //end byte received and we are reading command so a command is in the buffer
      readingCmd = false;
      availableCmd = true;
    }
    else if(readingCmd == true)
    {
      if(readPointer>MAX_BUFF_LEN)
      {
        //buffer overflow, throw this command away
        ErrorHandler_SetError(RECV_BUFF_OVERFLOW_ERR);
        readPointer = 0;
        readingCmd = false;
      }
      else
      {
        // add to receive buffer
        cmdRecvQueue[readPointer] = byteRecv;
        readPointer++;  
      }
    }    
  }

  //data in queue
  if(availableCmd)
  {
    decodedCommand = CommandDecoder(cmdRecvQueue, readPointer, MAX_BUFF_LEN, outBuff);

    if(decodedCommand == COMMAND_INVALID)
    {
      //command buffer is corrupt flush it and send NACK
      ErrorHandler_SetError(CMD_INVALID_ERR);    
    }

    readPointer = 0;
    readingCmd = false;  
    availableCmd = false;
  }
  
  return decodedCommand;
}

void CommandComm_SendCmd()
{
  
}

