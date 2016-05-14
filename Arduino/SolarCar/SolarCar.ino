/*
 * Main Application File
 * 
 */

#include "Commands.h"
#include "Errors.h"
#include "TypesDefines.h"

#define MAX_CMD_DATA_LEN 10

void Command_DoCommand(CommandType inCmd, unsigned char *inBuff);

 
void setup() {
  // put your setup code here, to run once:

  MotorControl_Init();
  Turret_Init();
  CurrentSensing_Init();
  
  CommandComm_Init();
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned char recvBuff[MAX_CMD_DATA_LEN] = {0};
  
  CommandType currentCommand = CommandComm_FetchCmd(recvBuff);

 // Serial.print(currentCommand,DEC);
  /* respond to possible commands */
  Command_DoCommand(currentCommand, recvBuff);

  /* tick everything */
  MotorControl_DriveMotors();
  CurrentSensing_UpdateCurrents();
  Turret_Maintain();

  //At end of loop send possible command to Pi
  CommandComm_SendCmd();

  delay(1);
}

void Command_DoCommand(CommandType inCmd, unsigned char *inBuff)
{
  switch(inCmd)
  {
    case NO_COMMAND:
    break;

    /* motor commands */
    case LEFT_MOTOR_SPEED:
      if(inBuff[0]==1)
      {
        MotorControl_SetMotorSpeed(inBuff[1], LEFT_MOTOR);
      }
      else
      {
        MotorControl_SetMotorSpeed(inBuff[1]*-1, LEFT_MOTOR);
      }
    break;
    case RIGHT_MOTOR_SPEED:
      if(inBuff[0]==1)
      {
        MotorControl_SetMotorSpeed(inBuff[1], RIGHT_MOTOR);
      }
      else
      {
        MotorControl_SetMotorSpeed(inBuff[1]*-1, RIGHT_MOTOR);
      }
    break;
    case BOTH_MOTOR_SPEED:
      if(inBuff[0]==1)
      {
        MotorControl_SetMotorSpeed(inBuff[1], LEFT_MOTOR);
      }
      else
      {
        MotorControl_SetMotorSpeed(inBuff[1]*-1, LEFT_MOTOR);
      }
   
      if(inBuff[2]==1)
      {
        MotorControl_SetMotorSpeed(inBuff[3], RIGHT_MOTOR);
      }
      else
      {
        MotorControl_SetMotorSpeed(inBuff[3]*-1, RIGHT_MOTOR);
      }
    break;
    

    /* turret commands */
    case TURRET_LASER_SET:
      if(inBuff[0]!=0)
      {
        Turret_SetLaser(1);
      }
      else
      {
        Turret_SetLaser(0);
      }
    break;
    case TURRET_HOR_ANGLE:
        Turret_SetHorAngle(inBuff[0]);
    break;
    case TURRET_VER_ANGLE:
        Turret_SetVerAngle(inBuff[0]);
    break;
  }
}

