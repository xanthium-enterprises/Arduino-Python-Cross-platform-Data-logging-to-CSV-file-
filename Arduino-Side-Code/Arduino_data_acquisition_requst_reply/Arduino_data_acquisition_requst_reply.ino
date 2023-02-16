// Arduino based 4 channel DAQ system
// $ character starts the conversion 
// This sketch will read the temperature from all the 4 channels and convert it to equivalent temperatures   
// https://www.xanthium.in/lm-35-four-channel-arduino-data-acquisition-system-temperature-sensing
// Average Gain of LM35 amplifier board is 3.44


int AnalogPin_AN1 = A0;    // select the input pin for lm35
int AnalogPin_AN2 = A1;    // select the input pin for lm35
int AnalogPin_AN3 = A2;    // select the input pin for lm35
int AnalogPin_AN4 = A3;    // select the input pin for lm35

void setup() 
{
   Serial.begin(9600); //Data will be send to PC @9600bps

}

void loop() 
{
   char ReceivedByte  = "0"; //
   
   float temp1,temp2,temp3,temp4 = 0.0;
   
   if (Serial.available() > 0) //Wait for data reception
   {
     ReceivedByte = Serial.read();//Read data from Arduino Serial UART buffer

     if (ReceivedByte == '$')//Check received byte is $
     {
      temp1 = ReadAnalogChannel(AnalogPin_AN1);
      temp2 = ReadAnalogChannel(AnalogPin_AN2);
      temp3 = ReadAnalogChannel(AnalogPin_AN3);
      temp4 = ReadAnalogChannel(AnalogPin_AN4);

      Serial.print(temp1);
      Serial.print('-');
      Serial.print(temp2);
      Serial.print('-');
      Serial.print(temp3);
      Serial.print('-');
      Serial.print(temp4);
      Serial.print('-');
      Serial.println();
      
     } //end of if
     else
     {
       Serial.println("INVALID");
       Serial.println("use $ to start conversion");
     }
   }

}

// float ReadAnalogChannel(int analogpin)
// Read's value from the specified Analog pin (int analogpin),
// Each pin read three times in aloop to an array and averages the temperature value
// returns the temperature value in a float variable.

float ReadAnalogChannel(int analogpin)
{
  float SensorValue[3] = {0.0,0.0,0.0}; // Array to store 3 consecutive values 
  float AvgSensorValue = 0.0;           // Variable to store the average of 3 consecutive analog  values 
  float temperature = 0.0;              // Variable to store temperature in Celsius

  // Make three consecutivereadings from the specified analog pin
  for(int i =0;i<3;i++)
  {
    SensorValue[i] = analogRead(analogpin); //Read 3 consecutive analog  values and store it in array
    delay(10);
  }

  //Calculate the average of three sensor values
  AvgSensorValue = ((SensorValue[0] + SensorValue[1] + SensorValue[2]) /3);

  //Convert the average ADC value to temperature in Celsius 
  temperature = AvgSensorValue * (5.0/1024.0);// 10 bit adc,1024 divisons,
  temperature = temperature/3.44;
  temperature = temperature *100;
  
  return temperature; //return calculated temperature in celsius,float variable
}
