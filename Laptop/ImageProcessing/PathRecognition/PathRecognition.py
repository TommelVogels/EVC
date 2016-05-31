# Name
# Description

#defines
INJECT = 1

#include dependencies
from Debugging.Debug  import logToAll
import random

#variables
destination = 0
current = 0

#functions

def findPath():
  global current
  global destination
  
  if destination==current:
    destination = random.randint(0,320)
  
  if current>destination:
    current = current-1
  else:
    current = current + 1
  
  return {"leftDis":current,"rightDis":320-current}

#calls
    
  
