/*
 * ==========================================================================
 * File         : file_name.cpp
 * Description  : Brief description of the file's purpose and functionality.
 * Author       : Author's name
 * Date         : DD/MM/YYYY
 * Version      : File or software version
 * ==========================================================================
 * Additional Notes:
 * - Specific instructions on how to use the file.
 * - Any relevant comments on future modifications or limitations.
 * ==========================================================================
 */
#pragma once

const int MA1 = 12; // Input signal A from motor 1.
const int MB1 = 14; // Input signal B from motor 1.

const int MA2 = 4; // Input signal A from motor 2.
const int MB2 = 2; // Input signal B from motor 2.

const int PWM1 = 27; // Input signal pwm for motor 1. 
const int PWM2 = 26; // Input signal pwm for motor 2. 

// Global variables for control
unsigned long lastTime = 0;  
unsigned long sampleTime = 100;
float min_speed = 140;
float max_speed = 240;
float speed1, speed2;

// Distance control
double rotations1, rotations2;
double distance, disRef;
float speed = 0;
float k = 5;
float error = 0;

// Speed control
float prevDistance1 = 0;
float realSpeed1 = 0;
float newDistance1 = 0;
float diference1 = 0;
float integralError1 = 0;  // Error acumulado para rueda 1

float prevDistance2 = 0;
float realSpeed2 = 0;
float newDistance2 = 0;
float diference2 = 0;
float integralError2 = 0;  // Error acumulado para rueda 2

float kp1 = .51;
float ki1 = 0.02;  // Ganancia integral rueda 1
float kp2 = .5;
float ki2 = 0.01;  // Ganancia integral rueda 2

void initializeMotors();

void setMotorSpeeds(float speed1, float speed2);

void adjustMotorSpeeds(float &speed1, float &speed2);

void moveToDistance(double referenceDistance);
void speedControl(float referenceSpeed);