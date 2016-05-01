/*
 * Main Application File
 * 
 */

#include "Commands.h"
#include "Errors.h"
 
void setup() {
  // put your setup code here, to run once:

  MotorControl_Init();
  Turret_Init();
  CurrentSensing_Init();
  
  CommandComm_Init();

  /* temp */
  pinMode(11,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  CommandType currentCommand = CommandComm_FetchCmd();

  switch(currentCommand)
  {
    case NO_COMMAND:
    break;
    
  }
 
  MotorControl_DriveMotors();
  CurrentSensing_UpdateCurrents();
  Turret_Maintain();

  //At end of loop send command from queue to Pi
  CommandComm_SendCmd();
}
