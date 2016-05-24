/*
 * Turret
 */
#define TURRET_LASER_PIN A2

#define TURRET_HOR_SERVO_PIN 2
#define TURRET_VER_SERVO_PIN 3

#define FIRE1_PIN A3
#define FIRE2_PIN A4


#define BULLET_DURATION 90
#define BULLET_ALL_DURATION 600

#define TURRET_QUEUE_SIZE 12 //can queue up to 12 commands

#include <Servo.h> 

Servo horServo;
Servo verServo;

unsigned char turretLaserOn = 0;
unsigned char turretHorAngle = 0;
unsigned char turretVerAngle = 0;

typedef struct{
  char turret;
  unsigned long  duration;
} turretAction;

turretAction turretQueue[TURRET_QUEUE_SIZE] = {0};
char turretQueueLength = 0;

unsigned long currentCount = 0;

void Turret_Init()
{
  pinMode(TURRET_LASER_PIN,OUTPUT);

  pinMode(FIRE1_PIN,OUTPUT);
  pinMode(FIRE2_PIN,OUTPUT);

  digitalWrite(FIRE1_PIN, LOW);
  digitalWrite(FIRE2_PIN, LOW);

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

  /* Aiming */
  horServo.write(turretHorAngle);
  verServo.write(turretVerAngle);

  /* Firing */
  if(turretQueueLength>0)
  {
    currentCount = millis()+turretQueue[0].duration;

    if(turretQueue[0].turret == 1)
    {
      digitalWrite(FIRE1_PIN, HIGH);
    }
    else if(turretQueue[0].turret == 2)
    {
      digitalWrite(FIRE2_PIN, HIGH);
    }
    else if(turretQueue[0].turret == 3)
    {
      digitalWrite(FIRE1_PIN, HIGH);
      digitalWrite(FIRE2_PIN, HIGH);
    }

    turretQueueLength--;

    /* Move everything up in queue */
    for(int i=0;i<turretQueueLength;i++)
    {
      turretQueue[i].duration = turretQueue[i+1].duration;
      turretQueue[i].turret = turretQueue[i+1].turret;
    }
  }
  
  if(currentCount<=millis())
  {
    digitalWrite(FIRE1_PIN, LOW);
    digitalWrite(FIRE2_PIN, LOW);
  }
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

//inTurret 
void Turret_SetFire(unsigned char inTurret, boolean inAll)
{
  turretQueue[turretQueueLength].turret = inTurret;
  turretQueue[turretQueueLength].duration = (inAll)?BULLET_ALL_DURATION:BULLET_DURATION;
  turretQueueLength++;
}

