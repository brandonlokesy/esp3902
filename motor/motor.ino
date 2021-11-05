/*******************************************************************************
   THIS SOFTWARE IS PROVIDED IN AN "AS IS" CONDITION. NO WARRANTY AND SUPPORT
   IS APPLICABLE TO THIS SOFTWARE IN ANY FORM. CYTRON TECHNOLOGIES SHALL NOT,
   IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR CONSEQUENTIAL
   DAMAGES, FOR ANY REASON WHATSOEVER.
 ********************************************************************************
   DESCRIPTION:

   This example shows how to drive 2 motors using the PWM and DIR pins with
   2-channel motor driver.


   CONNECTIONS:

   Arduino D3  - Motor Driver PWM 1 Input
   Arduino D4  - Motor Driver DIR 1 Input
   Arduino D9  - Motor Driver PWM 2 Input
   Arduino D10 - Motor Driver DIR 2 Input
   Arduino GND - Motor Driver GND


   AUTHOR   : Kong Wai Weng
   COMPANY  : Cytron Technologies Sdn Bhd
   WEBSITE  : www.cytron.io
   EMAIL    : support@cytron.io

 *******************************************************************************/

#include <CytronMotorDriver.h>


// Configure the motor driver.
CytronMD dcmotor(PWM_DIR, 3, 4);  // PWM 1 = Pin 3, DIR 1 = Pin 4.
CytronMD vmotor(PWM_DIR, 11, 12); // PWM 2 = Pin 9, DIR 2 = Pin 10.
int incomingData;

const long onInterval = 500;
const long offInterval = 10000;
bool dcFlag = false;
unsigned long currentMillis = 0;
unsigned long previousMillis = 0;

// The setup routine runs once when you press reset.
void setup() {
  Serial.begin(9600);
  previousMillis = millis();
}

void activatedc(){
  while(1){
    incomingData = Serial.read();
    vmotor.setSpeed(255);
    if (incomingData == 'Q'){
      dcmotor.setSpeed(0);
      vmotor.setSpeed(0);
      break;
      }
    currentMillis = millis();
    if(dcFlag == false && currentMillis - previousMillis >= offInterval){
        previousMillis = currentMillis;
        dcFlag = true;
        dcmotor.setSpeed(60);
        }
    else if(dcFlag == true && currentMillis - previousMillis >= onInterval){
          previousMillis = currentMillis;
          dcFlag = false;
          dcmotor.setSpeed(0);
          }
    }
}

// The loop routine runs over and over again forever.
void loop() {

  if (Serial.available() > 0) {
    incomingData = Serial.read();

    switch(incomingData) {
    case 'F':
      dcmotor.setSpeed(40);
      break;

    case 'Q':
      dcmotor.setSpeed(0);
      break;

    case 'V':
      vmotor.setSpeed(255);
      break;

    case 'S':
      vmotor.setSpeed(0);
      break;

    case 'W':
      activatedc();
      break;
    }
  }
}
