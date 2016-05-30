#include <PID_v1.h>

#include "defines.h"


/*
 * MotorControl
 */
#define PWM_L 11
#define PWM_R 5

#define EN_L_BWD 8
#define EN_L_FWD 4

#define EN_R_BWD 6
#define EN_R_FWD 7

//#define ENCODER_R 9
//#define ENCODER_L 10

//#define ENCODER_R_2 2
//#define ENCODER_L_2 3

#define COUNTS_PER_REVOLUTION 408 //12*34
#define DISTANCE_PER_REVOLUTION 20 // 20 cm ???? TBD

void setMotor(const unsigned char cucPWM, const unsigned char cucFWD , const unsigned char cucBWD, const int ciSpeed);

#define MOTOR_MIN_POWER -255
#define MOTOR_MAX_POWER  255

int leftMotorSpeed = 0;
int rightMotorSpeed = 0;

double countPulses = 0;
int previousState = 0;

double countPulses2 = 0;
int previousState2 = 0;

//Define Variables we'll be connecting to
double Setpoint = 100;
double Input = 0;
double Output = 0;
double Input2 = 0;
double Output2 = 0;

//Specify the links and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint,2,5,1, DIRECT);
PID myPID2(&Input2, &Output2, &Setpoint,20,50,10, DIRECT);


void setup() {
  // put your setup code here, to run once:

  MotorControl_Init();

  Serial.begin(115200);

  Serial.println("Test");

  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(100, 255);
  myPID2.SetMode(AUTOMATIC);
  myPID2.SetOutputLimits(100, 255);

  Setpoint = 1000;

}

void loop() {
  // put your main code here, to run repeatedly:
  
  MotorControl_SetMotorPower(Output2, LEFT_MOTOR);
  MotorControl_SetMotorPower(Output, RIGHT_MOTOR);

  unsigned long pulseLeft = pulseIn(3, HIGH, 5000);
  pulseLeft += pulseIn(3, HIGH, 5000);
  pulseLeft += pulseIn(3, HIGH, 5000);
  pulseLeft += pulseIn(3, HIGH, 5000);
  pulseLeft += pulseIn(3, HIGH, 5000);
  pulseLeft /=5;
 
  
  unsigned long pulseRight = pulseIn(9, HIGH, 5000);
  pulseRight += pulseIn(9, HIGH, 5000);
  pulseRight += pulseIn(9, HIGH, 5000);
  pulseRight += pulseIn(9, HIGH, 5000);
  pulseRight += pulseIn(9, HIGH, 5000);
  pulseRight /= 5;
 
  if(pulseRight!=0)
  {
    Input = 1000000L/pulseRight;
  }
  else
  {
    Input = 0;
  }

  if(pulseLeft!=0)
  {
    Input2 = 1000000L/pulseLeft;
  }
  else
  {
    Input2 = 0;
  }

    myPID.Compute();
    myPID2.Compute(); 

    Serial.println(pulseLeft,DEC);
    Serial.println(Input2,DEC);

   delay(10);
} 


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

