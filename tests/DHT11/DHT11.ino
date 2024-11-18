#include <DHT.h>

// digital pin where DHT11 is connected
#define DHTPIN 13
// type of sensor
#define DHTTYPE DHT11
// temp sensor object
DHT dht(DHTPIN, DHTTYPE);

float t, h;

void setup() {
  Serial.begin(9600);  
  // initialize DHT sensor
  dht.begin();
}

void loop() {
  // read temperature and humidity
  t = dht.readTemperature();
  h = dht.readHumidity();

  // Check if any reads failed and exit early (to try again).
  /*
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  */

  Serial.print("Temperature: "); Serial.print(t); Serial.println(" °C");
  Serial.print("Humidity: "); Serial.print(h); Serial.println(" %");
  
  delay(2000);  // Delay between reads to avoid overwhelming the sensor
}
