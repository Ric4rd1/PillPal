#pragma once
// Defines the number of steps per rotation
const int stepsPerRevolution = 2048;
// steps to rotate 1 slot (45°)
const int slotRotation = 256;
// Driver conections to esp32


void initializeDispenser();

void dispensePills();

void loadPills();