/*
 * Main Application File
 * 
 */

#include "Commands.h"
#include "Errors.h"
#include "TypesDefines.h"

#define MAX_CMD_DATA_LEN 10

#define MOTOR_CONTROL_TASK_INTERVAL 1
#define CURRENT_SENSE_TASK_INTERVAL 20000
#define TURRET_CONTROL_TASK_INTERVAL 1

unsigned int motorControlCount = 0;
unsigned int currentSenseCount = 0;
unsigned int turretControlCount = 0;

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
  if(motorControlCount >= MOTOR_CONTROL_TASK_INTERVAL)
  {
    MotorControl_DriveMotors();
    motorControlCount = 0;
  }
  if(currentSenseCount >= CURRENT_SENSE_TASK_INTERVAL)
  {
    CurrentSensing_UpdateCurrents();
    currentSenseCount = 0;
  }
  if(turretControlCount >= TURRET_CONTROL_TASK_INTERVAL)
  {
    Turret_Maintain();
    turretControlCount = 0;
  }

  motorControlCount++;
  currentSenseCount++;
  turretControlCount++;
  
  //delayMicroseconds(10);
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
       MotorControl_SetMotorSpeed((inBuff[1])*-1, LEFT_MOTOR);
      }

      CommandComm_SendAckCmd(LEFT_MOTOR_SPEED);
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

      CommandComm_SendAckCmd(RIGHT_MOTOR_SPEED);
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

      CommandComm_SendAckCmd(BOTH_MOTOR_SPEED);
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

      CommandComm_SendAckCmd(TURRET_LASER_SET);
    break;
    case TURRET_HOR_ANGLE:
        Turret_SetHorAngle(inBuff[0]);
        CommandComm_SendAckCmd(TURRET_HOR_ANGLE);
    break;
    case TURRET_VER_ANGLE:
        Turret_SetVerAngle(inBuff[0]);
        CommandComm_SendAckCmd(TURRET_VER_ANGLE);
    break;
    case TURRET_BOTH_ANGLE:
        Turret_SetHorAngle(inBuff[0]);
        Turret_SetVerAngle(inBuff[1]);
        CommandComm_SendAckCmd(TURRET_BOTH_ANGLE);
    case TURRET_FIRE_1:
        Turret_SetFire(1, false);
        CommandComm_SendAckCmd(TURRET_FIRE_1);
    break;
    case TURRET_FIRE_2:
        Turret_SetFire(2, false);
        CommandComm_SendAckCmd(TURRET_FIRE_2);
    break;
    case TURRET_FIRE_ALL_1:
        Turret_SetFire(1, true);
        CommandComm_SendAckCmd(TURRET_FIRE_ALL_1);
    break;
    case TURRET_FIRE_ALL_2:
        Turret_SetFire(2, true);
        CommandComm_SendAckCmd(TURRET_FIRE_ALL_2);
    break;
    case TURRET_FIRE_ALL:
        Turret_SetFire(3, true);
        CommandComm_SendAckCmd(TURRET_FIRE_ALL);
    break;

    /* current commands */
    case BATTERY_CURRENT:
    {
        unsigned char buff[3] = {0};
        CurrentSensing_FetchCurrent(1, buff);
        CommandComm_SendCmd(BATTERY_CURRENT, buff, 3);
    }
    break;
    case SYSTEM_CURRENT:
    {
        unsigned char buff[3] = {0};
        CurrentSensing_FetchCurrent(0, buff);
        CommandComm_SendCmd(SYSTEM_CURRENT, buff, 3);
    }
    break;
  }
}

