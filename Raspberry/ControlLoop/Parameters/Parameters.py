# Parameters.py
# Stores all parameters and allows them to be fetched and changed

#defines

#include dependencies

#variables
variablesState = {"leftMotorSpeed":0,"rightMotorSpeed":0,"angle":0,"sign":0,"control_state":0,"leftDis":0,"rightDis":0}

def setVariableState(variable, value):
  variablesState[variable] = value;

def getVariableState(variable):
  return variablesState[variable];