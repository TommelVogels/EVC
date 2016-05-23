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
    case BATTERY_CURRENT:
    case SYSTEM_CURRENT:
    case TURRET_FIRE_1:
    case TURRET_FIRE_2:
    case TURRET_FIRE_ALL_1:
    case TURRET_FIRE_ALL_2:
    case TURRET_FIRE_ALL:
    {
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

int CommandEncoder(CommandType inCmd, unsigned char* inData, char inDataLen, unsigned char *outBuff)
{
  char checksum = 0;
  int len = 0;

  //0xA5,0x02,0x38,0x01,0x3B,0x5A

  outBuff[len] = START_BYTE;
  len++;

  //length
  outBuff[len] = (unsigned char)(inDataLen+1);
  len++;
  checksum ^= (unsigned char)(inDataLen+1);

  //cmd id
  outBuff[len] = (unsigned char)(inCmd);
  len++;
  checksum ^= (unsigned char)(inCmd);

  //data
  for(int i=0;i<inDataLen;i++)
  {
    outBuff[len] = inData[i];
    len++;
    checksum ^= inData[i];
  }

  //checksum
  outBuff[len] = checksum;
  len++;

  outBuff[len] = END_BYTE;
  len++;

  return len;
}


