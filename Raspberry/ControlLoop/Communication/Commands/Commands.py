# Name
# Description

#defines
from enum import Enum
class CommandType(Enum):
  NO_COMMAND        = 0x00,
  
  ERROR_STATUS      = 0x01,
  COMMAND_QUEUE_LEN = 0x02,
  SYSTEM_RESET      = 0x03,
  TEST_SEQUENCE     = 0x04,
  
  LEFT_MOTOR_SPEED  = 0x11,
  RIGHT_MOTOR_SPEED = 0x12,
  BOTH_MOTOR_SPEED  = 0x13,

  BATTERY_CURRENT   = 0x21,
  SYSTEM_CURRENT    = 0x22,

  TURRET_HOR_ANGLE  = 0x31,
  TURRET_VER_ANGLE  = 0x32,
  TURRET_FIRE_1     = 0x33,
  TURRET_FIRE_2     = 0x34,
  TURRET_FIRE_ALL_1 = 0x35,
  TURRET_FIRE_ALL_2 = 0x36,
  TURRET_FIRE_ALL   = 0x37,
  TURRET_LASER_SET  = 0x38,

  COMMAND_INVALID   = 0xFF

#include dependencies

#variables

#functions
    
#calls
    
  
