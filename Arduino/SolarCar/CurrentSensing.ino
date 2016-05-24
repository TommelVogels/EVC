/*
 * CurrentSensing
 */
#define BATTERY_CURRENT_PIN  A0
#define SYSTEM_CURRENT_PIN   A1

/*
 * Sensor is ACS712-05 with a range of +-5 A
 * Sensitivity: 185mV/A
 * 1.55V at -5A
 * 3.45V at 5A
*/
#define MV_PER_MA 0.185
#define MV_OFFSET 2500

#define ADC_0A  512

#define ADC_TO_MVOLTS(adc) ((adc/1024.0)*5000)

#define ADC_TO_MA(adc) ((ADC_TO_MVOLTS(adc)-MV_OFFSET)/MV_PER_MA)

/* mA */
int battCurrent = 0;
int systemCurrent = 0;

#define ROLLING_AVERAGE_SIZE 20
unsigned int battCurrentArray[ROLLING_AVERAGE_SIZE] = {0};
unsigned int systemCurrentArray[ROLLING_AVERAGE_SIZE] = {0};

void CurrentSensing_Init()
{
  for(int i=0;i<20;i++)
  {
    battCurrentArray[i] = analogRead(BATTERY_CURRENT_PIN);
    systemCurrentArray[i] = analogRead(SYSTEM_CURRENT_PIN);
  }
}

void CurrentSensing_UpdateCurrents()
{
  unsigned int battCurrentSum = 0;
  unsigned int systemCurrentSum = 0;

  /* shift out the oldest value */
  for(int i=ROLLING_AVERAGE_SIZE;i>1;i--)
  {
    battCurrentArray[i-1] = battCurrentArray[i-2];
    battCurrentSum+= battCurrentArray[i-1];
    
    systemCurrentArray[i-1] = systemCurrentArray[i-2];
    systemCurrentSum+= systemCurrentArray[i-1];
  }

  battCurrentArray[0] = analogRead(BATTERY_CURRENT_PIN);
  battCurrentSum+=battCurrentArray[0];
  systemCurrentArray[0] = analogRead(SYSTEM_CURRENT_PIN);
  systemCurrentSum+=systemCurrentArray[0];
  
  battCurrent = ADC_TO_MA((battCurrentSum/ROLLING_AVERAGE_SIZE));
  //Serial.println((battCurrentSum/ROLLING_AVERAGE_SIZE),DEC);
  //Serial.print(battCurrent,DEC);
  //Serial.println("mA batt");
  
  systemCurrent = ADC_TO_MA((systemCurrentSum/ROLLING_AVERAGE_SIZE));
  //Serial.println((systemCurrentSum/ROLLING_AVERAGE_SIZE),DEC);
  //Serial.print(systemCurrent,DEC);
  //Serial.println("mA system");
}

void CurrentSensing_FetchCurrent(char inWhich, unsigned char* outBuff)
{
  int current = (inWhich)?battCurrent:systemCurrent;

  outBuff[0] = (current<0)?1:0;

  if(current<0)
  {
    current=current*-1;
  }

  outBuff[1] = (current>>8);
  outBuff[2] = (current&0xFF);
}


