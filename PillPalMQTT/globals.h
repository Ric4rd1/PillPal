// LEDs
#define MQTT_LED_STATUS_PIN 23
#define WIFI_LED_STATUS_PIN 15

// MQTT flags
extern String instruction;
extern int value;
extern bool newCommand;


// Dispsenser
extern unsigned short int nextSlot;

//Motors
extern bool isMoving;

// Encoders
extern volatile int  n1; // counts for encoder 1.
extern volatile int  n2; // counts for encoder 1.