/*
 * ==========================================================================
 * File         : PillPal.ino
 * Description  : 
 * Author       : Ricard
 * Date         : DD/MM/YYYY
 * Version      : PillPalV1
 * ==========================================================================
 * Additional Notes:
 * - 
 * - 
 * ==========================================================================
 */
#include "encoders.h"
#include "motors.h"
#include "dispenser.h"
#include "mqtt.h"
#include "tempSensor.h"
#include "globals.h"


void setup() {
  Serial.begin(9600);
  pinMode(MQTT_LED_STATUS_PIN, OUTPUT);
  pinMode(WIFI_LED_STATUS_PIN, OUTPUT);

  digitalWrite(MQTT_LED_STATUS_PIN, HIGH);
  digitalWrite(WIFI_LED_STATUS_PIN, HIGH);

  // Encoders
  initializeEncoders();

  // Motors
  initializeMotors();

  // Mqtt client
  initializeMqtt();

  // Stepper
  initializeDispenser();

  // DHT11
  initializeDHT11();


}

void loop() {
  loopMqtt();
}
