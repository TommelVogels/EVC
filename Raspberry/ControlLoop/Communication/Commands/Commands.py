# Commands.py
# This file contains all commands that are send over UART
#   and contains functions to convert commands to ints and vice versa

#defines
from enum import Enum
class CommandType(Enum):
  NO_COMMAND        = 0x00
  
  ERROR_STATUS      = 0x01
  COMMAND_QUEUE_LEN = 0x02
  SYSTEM_RESET      = 0x03
  TEST_SEQUENCE     = 0x04
  
  LEFT_MOTOR_SPEED  = 0x11
  RIGHT_MOTOR_SPEED = 0x12
  BOTH_MOTOR_SPEED  = 0x13

  BATTERY_CURRENT   = 0x21
  SYSTEM_CURRENT    = 0x22

  TURRET_HOR_ANGLE  = 0x31
  TURRET_VER_ANGLE  = 0x32
  TURRET_FIRE_1     = 0x33
  TURRET_FIRE_2     = 0x34
  TURRET_FIRE_ALL_1 = 0x35
  TURRET_FIRE_ALL_2 = 0x36
  TURRET_FIRE_ALL   = 0x37
  TURRET_LASER_SET  = 0x38
  TURRET_BOTH_ANGLE = 0x39

  COMMAND_INVALID   = 0xFF

#include dependencies
import sys
is_py2 = sys.version[0] == '2'

#variables

#functions
def CommandTypeToInt(inCmd):
  if is_py2:
    return inCmd
  else:
    return int(inCmd.value)
  
def IntToCommandType(inInt):
  if is_py2:
    return inInt
  else:
    return CommandType(inInt)
  
    
#calls
    
  
