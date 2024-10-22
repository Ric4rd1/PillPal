#include <DHT.h>
#include "tempSensor.h"

DHT dht(DHTPIN, DHTTYPE);

void initializeDHT11(){
  // initialize DHT sensor
  dht.begin();
}

float readTemp(){
  return dht.readTemperature();
}

float readHumid(){
  return dht.readHumidity();
}