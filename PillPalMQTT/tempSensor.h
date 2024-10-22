// digital pin where DHT11 is connected
#define DHTPIN 13
// type of sensor
#define DHTTYPE DHT11

void initializeDHT11();

float readTemp();
float readHumid();