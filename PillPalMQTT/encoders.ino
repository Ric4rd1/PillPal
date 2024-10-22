/*
 * ==========================================================================
 * File         : encoders.cpp
 * Description  : 
 * Author       : Ricard
 * Date         : DD/MM/YYYY
 * Version      : V1
 * ==========================================================================
 * Additional Notes:
 * - 
 * - 
 * ==========================================================================
 */
#include "encoders.h"

// encoders aux variables
volatile byte ant1  = 0; // previous encoder 1. state
volatile byte act1  = 0; // actual encoder 1. state 
volatile byte act2  = 0; // previous encoder 2. state
volatile byte ant2  = 0; // actual encoder 2. state

void initializeEncoders(){
  // Encoder 1
  pinMode(CA1, INPUT);
  pinMode(CB1, INPUT);
  attachInterrupt(digitalPinToInterrupt(CA1), encoder1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(CB1), encoder1, CHANGE);

  //Encoder 2
  pinMode(CA2, INPUT);
  pinMode(CB2, INPUT);
  attachInterrupt(digitalPinToInterrupt(CA2), encoder2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(CB2), encoder2, CHANGE);
}

// Quad encoder precision
void encoder1(void)
{

  ant1=act1;
  
  if(digitalRead(CA1)) bitSet(act1,1); else bitClear(act1,1);            
  if(digitalRead(CB1)) bitSet(act1,0); else bitClear(act1,0);
  
  
  
  if(ant1 == 2 && act1 ==0) n1++;
  if(ant1 == 0 && act1 ==1) n1++;
  if(ant1 == 3 && act1 ==2) n1++;
  if(ant1 == 1 && act1 ==3) n1++;
  
  if(ant1 == 1 && act1 ==0) n1--;
  if(ant1 == 3 && act1 ==1) n1--;
  if(ant1 == 0 && act1 ==2) n1--;
  if(ant1 == 2 && act1 ==3) n1--;    
    

}

// Quad encoder precision
void encoder2(void)
{

  ant2=act2;
  
  if(digitalRead(CA2)) bitSet(act2,1); else bitClear(act2,1);            
  if(digitalRead(CB2)) bitSet(act2,0); else bitClear(act2,0);
  
  
  
  if(ant2 == 2 && act2 ==0) n2++;
  if(ant2 == 0 && act2 ==1) n2++;
  if(ant2 == 3 && act2 ==2) n2++;
  if(ant2 == 1 && act2 ==3) n2++;
  
  if(ant2 == 1 && act2 ==0) n2--;
  if(ant2 == 3 && act2 ==1) n2--;
  if(ant2 == 0 && act2 ==2) n2--;
  if(ant2 == 2 && act2 ==3) n2--;    
    

}

void resetCounts(){
  n1 = 0;
  n2 = 0;
}

double getRotation(int encoder){
    if(encoder == 1){
        P1 = (n1 * 360.0) / R;
        return P1;
    } 
    else if (encoder == 2){
        P2 = (n2 * 360.0) / R;
        return P2;
    } 
    else {
        // Use __func__ to print the function name automatically
        Serial.print("Error in function ");
        Serial.print(__func__);
        Serial.println(": Invalid Encoder number");
        return -1;  // Return -1 to indicate an error
    }
}

double getDistance(int encoder){
    if(encoder == 1){
        D1 = (P1/360)*pi*diameter;
        return D1;
    } 
    else if (encoder == 2){
        D2 = (P2/360)*pi*diameter;
        return D2;
    } 
    else {
        // Use __func__ to print the function name automatically
        Serial.print("Error in function ");
        Serial.print(__func__);
        Serial.println(": Invalid Encoder number");
        return -1;  // Return -1 to indicate an error
    }
}
