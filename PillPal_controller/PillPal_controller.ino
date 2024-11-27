#include <WiFi.h>
#include <PubSubClient.h>

#define VRX_PIN  33 // ESP32 pin connected to VRX pin
#define VRY_PIN  32 // ESP32 pin connected to VRY pin
#define button 15 // Pin para el boton del joystick

bool send;


int xValue = 0; // To store value of the X axis
int yValue = 0; // To store value of the Y axis

int motorSpeedLeft = 0;
int motorSpeedRight = 0;

// Ajustes de deadband basados en los datos en reposo
const int deadbandMin = 1850;  
const int deadbandMax = 1950;  

// Configuración Wi-Fi y MQTT
const char* ssid = "Hw";
const char* password = "hbsv0393";
const char* mqtt_server = "192.168.43.104";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32ClientJoy")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  
    if (!client.connected()) {
      reconnect();
    }
    client.loop();

    // Leer los valores analógicos de los ejes X y Y
    xValue = analogRead(VRX_PIN);
    yValue = analogRead(VRY_PIN);

    // Inicializar velocidades de motor en 0
    motorSpeedLeft = 0;
    motorSpeedRight = 0;

    // Control del eje X (giro) fuera del deadband
    if (xValue < deadbandMin || xValue > deadbandMax) {
      int mappedX = map(xValue, 0, 4095, 240, -240);
      motorSpeedLeft += mappedX;
      motorSpeedRight -= mappedX;
    }

    // Control del eje Y (avanzar/reversa) fuera del deadband
    if (yValue < deadbandMin || yValue > deadbandMax) {
      if (yValue > deadbandMax) {
        // Dirección hacia adelante
        motorSpeedLeft += map(yValue, deadbandMax + 1, 4095, 0, 240);
        motorSpeedRight += map(yValue, deadbandMax + 1, 4095, 0, 240);
      } else if (yValue < deadbandMin) {
        // Dirección hacia atrás
        motorSpeedLeft += map(yValue, 0, deadbandMin - 1, -240, 0);
        motorSpeedRight += map(yValue, 0, deadbandMin - 1, -240, 0);
      }
    }

    // Limitar la velocidad del motor
    motorSpeedLeft = constrain(motorSpeedLeft, -240, 240);
    motorSpeedRight = constrain(motorSpeedRight, -240, 240);

    // Ajuste de umbral mínimo si los motores están en movimiento
    if (motorSpeedLeft > 0) motorSpeedLeft = max(motorSpeedLeft, 200);
    if (motorSpeedLeft < 0) motorSpeedLeft = min(motorSpeedLeft, -200);

    if (motorSpeedRight > 0) motorSpeedRight = max(motorSpeedRight, 200);
    if (motorSpeedRight < 0) motorSpeedRight = min(motorSpeedRight, -200);

    // Formatear y enviar el mensacje al tópico MQTT
    char message[50];
    if (motorSpeedRight > 100) motorSpeedRight -= 40;

    snprintf(message, sizeof(message), "JS%d,%d", motorSpeedLeft, motorSpeedRight);
    client.publish("ESP/joy", message);

    // Imprimir valores en el monitor serial
    Serial.print("x = ");
    Serial.print(xValue);
    Serial.print(", y = ");
    Serial.print(yValue);
    Serial.print(", Left Motor = ");
    Serial.print(motorSpeedLeft);
    Serial.print(", Right Motor = ");
    Serial.println(motorSpeedRight);

    delay(500);
  }