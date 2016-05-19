# Parameters.py
# Stores all parameters and allows them to be fetched and changed

#defines

#include dependencies

#variables
variablesState = {"leftMotorSpeed":0,"rightMotorSpeed":0,"angle":0}

def setVariableState(variable, value):
  variablesState[variable] = value;

def getVariableState(variable):
  return variablesState[variable];