/*
 * ErrorHandler
 */

ErrorType currentError = NO_ERROR;

void ErrorHandler_SetError(ErrorType inErr)
{
  currentError = inErr;
}

