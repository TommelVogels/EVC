/*
 * CommandDecoder
 * 
 */

CommandType CommandDecoder(char* inBuff, char inReadLen, char inTotalLen, char *outBuff, char* outRead)
{
  char checksum = 0;

  checksum |= inBuff[0];
  *outRead++;

  switch(inBuff[0])
  {
    //todo
  }
}

