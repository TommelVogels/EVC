/*
 * CommandDecoder
 * 
 */

CommandType CommandDecoder(char* inBuff, char inReadLen, char inTotalLen, unsigned char *outBuff)
{
  char checksum = 0;
  bool cmdRecognised = false;

  checksum ^= inBuff[0]; //length

  //length of data is too big
  if(inBuff[0]>inTotalLen)
  {
    return COMMAND_INVALID;
  }
  
  checksum ^= inBuff[1]; //cmd id

  switch(inBuff[1])
  {
    case LEFT_MOTOR_SPEED:
    case RIGHT_MOTOR_SPEED:
    {
      // len id direction speed checksum
      outBuff[0] = inBuff[2]; //direction
      checksum ^= inBuff[2];
      outBuff[1] = inBuff[3]; //motor speed
      checksum ^= inBuff[3];
      cmdRecognised = true;
    }
    break;
    case BOTH_MOTOR_SPEED:
    {
      // len id direction speed direction speed checksum
      outBuff[0] = inBuff[2]; //direction
      checksum ^= inBuff[2];
      outBuff[1] = inBuff[3]; //motor speed
      checksum ^= inBuff[3];
      outBuff[2] = inBuff[4]; //direction
      checksum ^= inBuff[4];
      outBuff[3] = inBuff[5]; //motor speed
      checksum ^= inBuff[5];
      cmdRecognised = true;
    }
    break;
    case TURRET_HOR_ANGLE:
    case TURRET_VER_ANGLE:
    {
      // len id angle_0-180 checksum 
      outBuff[0] = inBuff[2]; //angle 0-180
      checksum ^= inBuff[2];
      cmdRecognised = true;
    }
    break;
    case TURRET_LASER_SET:
    {
      // len id laser_on/off checksum 
      outBuff[0] = inBuff[2]; //laser on/off
      checksum ^= inBuff[2];
      cmdRecognised = true;
    }
    break;
  }

  char recvChecksum = inBuff[inBuff[0] + 1]; //length

  //Serial.print(recvChecksum);
  //Serial.print(checksum);
  if(!cmdRecognised || recvChecksum!=checksum )
  {
    return COMMAND_INVALID;
  }
  
  return (CommandType)(inBuff[1]);
}

