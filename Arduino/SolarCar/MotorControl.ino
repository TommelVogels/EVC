/*
 * MotorControl
 */
#define PWM_L 10
#define PWM_R 11

#define EN_L_BWD 12
#define EN_L_FWD 13

#define EN_R_BWD 9
#define EN_R_FWD 8

#define ENCODER_R 7
#define ENCODER_L 6

#define ENCODER_R_2 5
#define ENCODER_L_2 4

#define COUNTS_PER_REVOLUTION 408 //12*34
#define DISTANCE_PER_REVOLUTION 20 // 20 cm ???? TBD

void setMotor(const unsigned char cucPWM, const unsigned char cucFWD , const unsigned char cucBWD, const int ciSpeed);

#define MOTOR_MIN_POWER -255
#define MOTOR_MAX_POWER  255

int leftMotorSpeed = 0;
int rightMotorSpeed = 0;


void MotorControl_Init()
{
  analogWrite(PWM_R, 0);  
  analogWrite(PWM_L, 0);
  digitalWrite(EN_L_FWD, LOW);
  digitalWrite(EN_L_BWD, LOW);
  digitalWrite(EN_R_FWD, LOW);
  digitalWrite(EN_R_BWD, LOW);

  pinMode(PWM_L, OUTPUT);
  pinMode(PWM_R, OUTPUT);
  pinMode(EN_L_FWD, OUTPUT);
  pinMode(EN_L_BWD, OUTPUT);
  pinMode(EN_R_FWD, OUTPUT);
  pinMode(EN_R_BWD, OUTPUT);
}

void MotorControl_DriveMotors()
{
  MotorControl_SetMotorPower(leftMotorSpeed, LEFT_MOTOR);
  MotorControl_SetMotorPower(rightMotorSpeed, RIGHT_MOTOR);
}

void MotorControl_SetMotorSpeed(int inSpeed, MotorType inMotor)
{
 switch(inMotor)
  {
    case LEFT_MOTOR:
      leftMotorSpeed = inSpeed;
    break;
    case RIGHT_MOTOR:
      rightMotorSpeed = inSpeed; 
    break;
  }
}


void MotorControl_SetMotorPower(int inSpeed, MotorType inMotor)
{
  if(inSpeed>MOTOR_MAX_POWER)
  {
    inSpeed = MOTOR_MAX_POWER;
  }
  if(inSpeed<MOTOR_MIN_POWER)
  {
    inSpeed = MOTOR_MIN_POWER;
  }
  
  switch(inMotor)
  {
    case LEFT_MOTOR:
    setMotor(PWM_L, EN_L_FWD, EN_L_BWD, inSpeed);
    break;
    case RIGHT_MOTOR:
    setMotor(PWM_R, EN_R_FWD, EN_R_BWD, inSpeed); 
    break;
  }
}

/* Provided function */
void setMotor(const unsigned char cucPWM, const unsigned char cucFWD , const unsigned char cucBWD, const int ciSpeed)
{ 
  if (ciSpeed < 0)
  {
    digitalWrite(cucFWD, LOW); 
    digitalWrite(cucBWD, LOW);  
    digitalWrite(cucFWD, LOW); 
    digitalWrite(cucBWD, HIGH);  
  }
  else
  {
    digitalWrite(cucFWD, LOW); 
    digitalWrite(cucBWD, LOW);  
    digitalWrite(cucFWD, HIGH); 
    digitalWrite(cucBWD, LOW);  
  }

  analogWrite(cucPWM, abs(ciSpeed));   
}

