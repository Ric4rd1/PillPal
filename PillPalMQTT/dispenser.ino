#include <Stepper.h>
#include "dispenser.h"
#include "globals.h"

#define IN1 19
#define IN2 18
#define IN3 5
#define IN4 17

// initialize the stepper
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);
unsigned short int nextSlot = 1;

void initializeDispenser(){
  myStepper.setSpeed(10);
  
}

void dispensePills(){
  if(nextSlot != 9){
    nextSlot++;
    myStepper.step(slotRotation); // Rotate 45 degrees clockwise

    if (nextSlot == 8){
      nextSlot++;
      myStepper.step(slotRotation); // Rotate extra 45° to complete full rotation
    }
  }
}

void loadPills(){
  for(int i= 1; i<= 6; i++){
    delay(3000);
    myStepper.step(-slotRotation);
  }
  nextSlot = 1;
  isMoving = false;
}