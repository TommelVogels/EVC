/*
 * MotorControl
 */

#define PWM_L 11
#define PWM_R 5

#define EN_L_BWD 8
#define EN_L_FWD 4

#define EN_R_BWD 6
#define EN_R_FWD 7

#define ENCODER_L_1 2
#define ENCODER_L_2 3

#define ENCODER_R_1 9
#define ENCODER_R_2 10

#define COUNTS_PER_REVOLUTION 408 //12*34
#define DISTANCE_PER_REVOLUTION 25.3 // 25.3 cm diameter

#define PULSE_RESOLUTION 6 //for each increase in motor speed we expect 6 pulses 1500/255 = 6

void setMotor(const unsigned char cucPWM, const unsigned char cucFWD , const unsigned char cucBWD, const int ciSpeed);

#define MOTOR_MIN_POWER -255
#define MOTOR_MAX_POWER  255

int leftMotorSpeed = 0;
int rightMotorSpeed = 0;

int leftMotorPower = 0;
int rightMotorPower = 0;


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
  /* LEFT MOTOR */
  unsigned long pulseL = pulseIn(ENCODER_L_1, HIGH, 5000);
  unsigned int InputLeft = (pulseL)?(1000000L/pulseL):(0);

 if(InputLeft<abs(leftMotorSpeed*PULSE_RESOLUTION))
 {
  leftMotorPower+=1;
  if(leftMotorPower>255){leftMotorPower=255;}
 }
 else if(InputLeft>abs(leftMotorSpeed*PULSE_RESOLUTION))
 {
  leftMotorPower-=1;
  if(leftMotorPower<0){leftMotorPower=0;}
 }
 else if(leftMotorSpeed==0)
 {
  leftMotorPower = 0;
 }

 if(leftMotorSpeed<0)
 {
 // leftMotorPower*=-1;
 }
  
  MotorControl_SetMotorPower((int)((leftMotorSpeed<0)?leftMotorPower*-1:leftMotorPower), LEFT_MOTOR);

  /* RIGHT MOTOR */
  unsigned long pulseR = pulseIn(ENCODER_R_1, HIGH, 5000);
  unsigned int InputRight = (pulseR)?(1000000L/pulseR):(0);

 if(InputRight<abs(rightMotorSpeed*PULSE_RESOLUTION))
 {
  rightMotorPower+=1;
  if(rightMotorPower>255){rightMotorPower=255;}
 }
 else if(InputRight>abs(rightMotorSpeed*PULSE_RESOLUTION))
 {
  rightMotorPower-=1;
  if(rightMotorPower<0){rightMotorPower=0;}
 }
 else if(rightMotorSpeed==0)
 {
  rightMotorPower = 0;
 }

  MotorControl_SetMotorPower((int)((rightMotorSpeed<0)?rightMotorPower*-1:rightMotorPower), RIGHT_MOTOR);
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

