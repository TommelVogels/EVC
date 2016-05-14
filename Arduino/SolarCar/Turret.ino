/*
 * Turret
 */
#define TURRET_LASER_PIN 12
#define TURRET_HOR_SERVO_PIN 4
#define TURRET_VER_SERVO_PIN 9

#include <Servo.h> 

Servo horServo;
Servo verServo;

unsigned char turretLaserOn = 0;
unsigned char turretHorAngle = 0;
unsigned char turretVerAngle = 0;

void Turret_Init()
{
  pinMode(TURRET_LASER_PIN,OUTPUT);

  horServo.attach(TURRET_HOR_SERVO_PIN);
  verServo.attach(TURRET_VER_SERVO_PIN);
}

void Turret_Maintain()
{
  /* Laser */
  if(turretLaserOn)
  {
    digitalWrite(TURRET_LASER_PIN, HIGH);
  }
  else
  {
    digitalWrite(TURRET_LASER_PIN, LOW);
  }

  horServo.write(turretHorAngle);
  verServo.write(turretVerAngle);
}

void Turret_SetLaser(unsigned char inState)
{
  turretLaserOn = inState;
}

void Turret_SetHorAngle(unsigned char inAngle)
{
  turretHorAngle = inAngle;
}

void Turret_SetVerAngle(unsigned char inAngle)
{
  turretVerAngle = inAngle;
}

