/*
 * ==========================================================================
 * File         : motors.ino
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
#include "motors.h"
#include "globals.h"

void initializeMotors(){
  //Motors
  pinMode(MA1, OUTPUT);
  pinMode(MB1, OUTPUT);
  pinMode(MA2, OUTPUT);
  pinMode(MB2, OUTPUT);
  // Speed control
  pinMode(PWM1, OUTPUT); 
  pinMode(PWM2, OUTPUT);
}

// Set motor speeds, range (-255 - 255), negative will make it go bakwards
void setMotorSpeeds(float speed1, float speed2) {
    // Adjust speeds to ensure both motors run at the same speed
    // adjustMotorSpeeds(speed1, speed2);
    // Motor 1: Set direction and speed
    if (speed1 >= 0) {
        // Forward direction
        digitalWrite(MA1, HIGH);
        digitalWrite(MB1, LOW);
    } else {
        // Backward direction
        digitalWrite(MA1, LOW);
        digitalWrite(MB1, HIGH);
        speed1 = -speed1;  // Make speed1 positive for analogWrite
    }
    analogWrite(PWM1, speed1);  // Set speed (absolute value)

    // Motor 2: Set direction and speed
    if (speed2 >= 0) {
        // Forward direction
        digitalWrite(MA2, HIGH);
        digitalWrite(MB2, LOW);
    } else {
        // Backward direction
        digitalWrite(MA2, LOW);
        digitalWrite(MB2, HIGH);
        speed2 = -speed2;  // Make speed2 positive for analogWrite
    }
    analogWrite(PWM2, speed2);  // Set speed (absolute value)
}

void adjustMotorSpeeds(float &speed1, float &speed2) {
    // Get current rotation counts
    int count1 = n1; // Current count for motor 1
    int count2 = n2; // Current count for motor 2

    // Calculate the difference in speed (encoder counts)
    int speedDifference = count1 - count2;

    // Adjust the speeds based on the difference
    if (speedDifference > 0) {
        // Motor 1 is faster
        speed2 += abs(speedDifference) * 0.2; // Increase speed of motor 2 by a fraction of the difference
    } else if (speedDifference < 0) {
        // Motor 2 is faster
        speed1 += abs(speedDifference) * 0.2; // Increase speed of motor 1 by a fraction of the difference
    }

    // Clamp the speeds within a reasonable range
    if (speed1 > max_speed) speed1 = max_speed;
    if (speed2 > max_speed) speed2 = max_speed;
    if (speed1 < min_speed) speed1 = min_speed;
    if (speed2 < min_speed) speed2 = min_speed;
}
// Simple distance control
void moveToDistance(double referenceDistance) {
  // Set reference distance
  disRef = referenceDistance;

  if (millis() - lastTime >= sampleTime || lastTime == 0) {
    lastTime = millis();  

    rotations1 = getRotation(1);
    rotations2 = getRotation(2);

    // Calculate the average distance
    distance = (getDistance(1) + getDistance(2)) / 2.0;
    error = disRef - distance;
    speed = k * error;

    // Clamp speed within limits
    if (speed > max_speed) {
      speed = max_speed;
    } else if (speed < min_speed) {
      speed = min_speed;
    }

    float dif = speed*0.04;
    // If there is still an error, adjust motor speeds
    if (error > 1) {
      setMotorSpeeds(speed, speed+dif);  // Adjust speed for motor 2
    } else {
      setMotorSpeeds(0, 0);  // Stop motors when the reference is reached
      isMoving = false;
    }

    // Debugging info
    Serial.print("distance: "); Serial.println(distance);
    //Serial.print("Position in degrees motor 1: "); Serial.println(rotations1);
    //Serial.print("Position in degrees motor 2: "); Serial.println(rotations2);
  }
}

// Speed control with sampleTiime
void speedControl(float referenceSpeed) {
  if (millis() - lastTime >= sampleTime || lastTime == 0) {
    lastTime = millis();  

    // getSpeed
    newDistance1 = getDistance(1);
    newDistance2 = getDistance(2);
    diference1 = newDistance1 - prevDistance1;
    diference2 = newDistance2 - prevDistance2;
    realSpeed1 = diference1/(sampleTime/1000.0);
    realSpeed2 = diference2/(sampleTime/1000.0);

    float error1 = referenceSpeed - realSpeed1;
    float error2 = referenceSpeed - realSpeed2;

    // Acum of error for integral control
    integralError1 += error1 * (sampleTime / 1000.0);
    integralError2 += error2 * (sampleTime / 1000.0);

    // set speeds
    speed1 += kp1*error1 + ki1 * integralError1;
    speed2 += kp2*error2 + ki2 * integralError2;


    // Clamp speed within limits
    if (speed1 > max_speed) {
      speed1 = max_speed;
    } else if (speed1 < min_speed) {
      speed1 = min_speed;
    }

    if (speed2 > max_speed) {
      speed2 = max_speed;
    } else if (speed2 < min_speed) {
      speed2 = min_speed;
    }

    setMotorSpeeds(speed1, speed2);
    
    // Debugging info
    
    Serial.print("speed: "); Serial.print(speed1); Serial.print(" -- "); Serial.println(speed2);
    Serial.print("RealSpeed: "); Serial.print(realSpeed1); Serial.print(" -- "); Serial.println(realSpeed2);
    Serial.print("PrevDistance: "); Serial.print(prevDistance1); Serial.print(" -- "); Serial.println(prevDistance2);
    Serial.print("diference: "); Serial.print(diference1); Serial.print(" -- "); Serial.println(diference2);
    
    prevDistance1 = newDistance1;
    prevDistance2 = newDistance2;
  }
}

// Speed control without sampleTime
void speedControl2(float referenceSpeed) { 
  // getSpeed
  newDistance1 = getDistance(1);
  newDistance2 = getDistance(2);
  diference1 = newDistance1 - prevDistance1;
  diference2 = newDistance2 - prevDistance2;
  realSpeed1 = diference1/(sampleTime/1000.0);
  realSpeed2 = diference2/(sampleTime/1000.0);

  float error1 = referenceSpeed - realSpeed1;
  float error2 = referenceSpeed - realSpeed2;

  // Acum of error for integral control
  integralError1 += error1 * (sampleTime / 1000.0);
  integralError2 += error2 * (sampleTime / 1000.0);

  // set speeds
  speed1 += kp1*error1 + ki1 * integralError1;
  speed2 += kp2*error2 + ki2 * integralError2;


  // Clamp speed within limits
  if (speed1 > max_speed) {
    speed1 = max_speed;
  } else if (speed1 < min_speed) {
    speed1 = min_speed;
  }

  if (speed2 > max_speed) {
    speed2 = max_speed;
  } else if (speed2 < min_speed) {
    speed2 = min_speed;
  }

  setMotorSpeeds(speed1, speed2);
  
  // Debugging info
  
  Serial.print("speed: "); Serial.print(speed1); Serial.print(" -- "); Serial.println(speed2);
  Serial.print("RealSpeed: "); Serial.print(realSpeed1); Serial.print(" -- "); Serial.println(realSpeed2);
  Serial.print("PrevDistance: "); Serial.print(prevDistance1); Serial.print(" -- "); Serial.println(prevDistance2);
  Serial.print("diference: "); Serial.print(diference1); Serial.print(" -- "); Serial.println(diference2);
  
  prevDistance1 = newDistance1;
  prevDistance2 = newDistance2;

}

// Velocity and position control
void moveToDistance2(double referenceDistance) {
  // Set reference distance
  disRef = referenceDistance;

  if (millis() - lastTime >= sampleTime || lastTime == 0) {
    lastTime = millis();  

    // Calculate the average distance
    distance = (getDistance(1) + getDistance(2)) / 2.0;
    error = disRef - distance;
    speed = k * error;
    Serial.print("Speed error: "); Serial.println(speed);
    Serial.print("error: "); Serial.println(error);

    // Clamp speed within limits
    if (speed > max_speed) {
      speed = max_speed;
    } else if (speed < min_speed) {
      speed = min_speed;
    }
    Serial.print("Speed clamped: "); Serial.println(speed);
    speed = (speed*60)/240;
    speed = constrain(speed,50,80);
    Serial.print("Speed reference: "); Serial.println(speed);

    // If there is still an error, adjust motor speeds
    if (error > 1) {
      speedControl2(speed);
      Serial.println("----------------------");
    } else {
      setMotorSpeeds(0, 0);  // Stop motors when the reference is reached
      isMoving = false;
    }

    // Debugging info
    Serial.print("distance: "); Serial.println(distance);
    //Serial.print("Position in degrees motor 1: "); Serial.println(rotations1);
    //Serial.print("Position in degrees motor 2: "); Serial.println(rotations2);
  }
}

// Velocity control
void moveToDistance3(double referenceDistance) {
  // Set reference distance
  disRef = referenceDistance;

  if (millis() - lastTime >= sampleTime || lastTime == 0) {
    lastTime = millis();  

    // Calculate the average distance
    distance = (getDistance(1) + getDistance(2)) / 2.0;
    error = disRef - distance;
    Serial.print("error: "); Serial.println(error);

    if (error > 1) {
      speedControl2(40.0);
      Serial.println("----------------------");
    } else {
      setMotorSpeeds(0, 0);  // Stop motors when the reference is reached
      isMoving = false;
    }

    // Debugging info
    Serial.print("distance: "); Serial.println(distance);
  }
}