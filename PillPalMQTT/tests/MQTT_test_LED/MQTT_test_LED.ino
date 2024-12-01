#include <WiFi.h>
#include <PubSubClient.h>

// Configuración de la red Wi-Fi
const char* ssid = "steren_2_4G";
const char* password = "password";

// Configuración del broker MQTT
const char* mqttServer = "192.168.1.7";
const int mqttPort = 1883;

// Pines del LED
const int ledPin = 23; // Cambia este valor si usas otro pin

// Instancias de cliente Wi-Fi y MQTT
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Estado del LED
bool ledState = LOW;

// Función de callback para mensajes MQTT
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Mensaje recibido en el tópico: ");
    Serial.println(topic);

    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    Serial.print("Mensaje: ");
    Serial.println(message);

    // Control del LED basado en el mensaje
    if (message == "ON" && ledState == LOW) {
        digitalWrite(ledPin, LOW);
        ledState = HIGH;
        mqttClient.publish("laptop/ricard", "LED is ON");
    } else if (message == "OFF" && ledState == HIGH) {
        digitalWrite(ledPin, HIGH);
        ledState = LOW;
        mqttClient.publish("laptop/ricard", "LED is OFF");
    }
}

// Conectar al broker MQTT
void reconnect() {
    while (!mqttClient.connected()) {
        Serial.print("Intentando conectar al broker MQTT...");
        if (mqttClient.connect("ESP32Client")) {
            Serial.println("Conectado");
            mqttClient.subscribe("esp32/LED");
        } else {
            Serial.print("Fallido, rc=");
            Serial.print(mqttClient.state());
            Serial.println(" Intentando de nuevo en 5 segundos");
            delay(5000);
        }
    }
}

void setup() {
    // Inicializar el puerto serie
    Serial.begin(115200);

    // Configurar el pin del LED
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);

    // Conectar a la red Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Conectado a Wi-Fi");

    // Configurar el servidor MQTT
    mqttClient.setServer(mqttServer, mqttPort);
    mqttClient.setCallback(callback);
}

void loop() {
    if (!mqttClient.connected()) {
        reconnect();
    }
    mqttClient.loop();
}
