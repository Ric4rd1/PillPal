/*
 * ==========================================================================
 * File         : mqtt.h
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
#pragma once
#include <Arduino.h>
// Wi-Fi network config
//const char* ssid = "INFINITUM9DBD";
//const char* password = "Aa1Sp5Kh7g";
const char* ssid = "Hw";
const char* password = "hbsv0393";

// broker MQTT config
const char* mqttServer = "192.168.43.55";
const int mqttPort = 1883;

void callback(char* topic, byte* payload, unsigned int length);
void reconnect();

void initializeMqtt();
void loopMqtt();