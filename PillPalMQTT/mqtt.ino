#include <WiFi.h>
#include <PubSubClient.h>
#include <queue>
#include "motors.h"
#include "encoders.h"
#include "mqtt.h" 
#include "globals.h"


// Instances Wi-Fi and MQTT clients
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Command structure
struct Command {
    String instructionCmd;
    int valueCmd;
};

// Globals
std::queue<Command> commandQueue;  // Queue to store commands
bool isMoving = false;             // Flag for ongoing movement

String instruction = "";
int value = -1;

int motorLeft;
int motorRight;

int valueAux;

// Callback functions for MQTT messages
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message recieved on topic: ");
    Serial.println(topic);

    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    Serial.print("Message: ");
    Serial.println(message);

    

    String instructionAux = message.substring(0,2);
    valueAux = message.substring(2).toInt();
    
    if(instructionAux == "JS"){
      int comaIndex = message.indexOf(',');
        if (comaIndex != -1) {
          motorLeft = message.substring(2, comaIndex).toInt(); // "123"
          motorRight = message.substring(comaIndex + 1).toInt(); // "456"
    
        } else{
          valueAux = message.substring(2).toInt();
      }
    }

    Serial.print("Instruction:#");
    Serial.print(instructionAux);
    Serial.println("#");
    Serial.print("Value: ");
    Serial.println(valueAux);

    // Add the command to the queue
    Command newCommand = {instructionAux, valueAux};
    commandQueue.push(newCommand);

}

// Connect to the broker
void reconnect() {
    while (!mqttClient.connected()) {
        Serial.print("Trying to connect to Broker MQTT...");
        if (mqttClient.connect("ESP32Client")) {
            Serial.println("Connected");
            mqttClient.subscribe("Py/routine");
            mqttClient.subscribe("ESP/joy");
        } else {
            Serial.print("Failed, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" Trying again in 5 seconds...");
            delay(5000);
        }
    }
}

void initializeMqtt() {

    // Connect to Wi Fi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        digitalWrite(WIFI_LED_STATUS_PIN, HIGH);
    }
    Serial.print("Connected to Wi-Fi: ");
    Serial.println(ssid);
    digitalWrite(WIFI_LED_STATUS_PIN, LOW);

    // Configure MQTT server
    mqttClient.setServer(mqttServer, mqttPort);
    mqttClient.setCallback(callback);
}

void loopMqtt() {
    if (!mqttClient.connected()) {
        reconnect();
        digitalWrite(MQTT_LED_STATUS_PIN, HIGH);
    }
    mqttClient.loop();
    digitalWrite(MQTT_LED_STATUS_PIN, LOW);

    
    // Process the command queue
    if (!commandQueue.empty() && !isMoving) {
        Command currentCommand = commandQueue.front();
        commandQueue.pop();  // Remove the command from the queue
        instruction  = currentCommand.instructionCmd;
        value = currentCommand.valueCmd;

        if(currentCommand.instructionCmd == "JS"){
          setMotorSpeeds(motorLeft, motorRight);
        }

        if (currentCommand.instructionCmd == "MF") {
            resetCounts();
            isMoving = true;  // Set moving flag
            currentCommand.valueCmd = value;
            Serial.println("got to queue");
            Serial.print("Value in MQTT queue: ");
            Serial.println(value);
        }

        if(currentCommand.instructionCmd == "DP"){
          dispensePills();
        }

        if(currentCommand.instructionCmd == "RP"){
          loadPills();
          
        }

        if(currentCommand.instructionCmd == "TP"){
          String t = String(readTemp());
          t = "TP" + t;
          mqttClient.publish("ESP/confirm", t.c_str());
        }

        if(currentCommand.instructionCmd == "HP"){
          String h = String(readHumid());
          h = "HP" + h;
          mqttClient.publish("ESP/confirm", h.c_str());
        }
        

    }

    if(isMoving){
      if(instruction == "MF")
        moveToDistance(value);
      
      /*
      Serial.println("got to movement");
      Serial.print("Value in MQTT loop: ");
      Serial.println(value);
      */
    }

}