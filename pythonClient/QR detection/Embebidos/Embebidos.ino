#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>

const char* WIFI_SSID = "Hw";
const char* WIFI_PASS = "hbsv0393";

WebServer server(80);

static auto hiRes = esp32cam::Resolution::find(800, 600);

void serveStream() {
  WiFiClient client = server.client();

  String response = "HTTP/1.1 200 OK\r\n";
  response += "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n";
  server.sendContent(response);

  while (client.connected()) {
    auto frame = esp32cam::capture();
    if (frame == nullptr) {
      Serial.println("CAPTURE FAIL");
      continue;
    }

    String header = "--frame\r\nContent-Type: image/jpeg\r\nContent-Length: " + String(frame->size()) + "\r\n\r\n";
    server.sendContent(header);
    frame->writeTo(client);
    server.sendContent("\r\n");

    delay(100); // Ajusta el retardo si el stream es muy rápido o lento
  }
}

void handleStream() {
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveStream();
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.print("http://");
  Serial.println(WiFi.localIP());
  Serial.println("  /stream");

  server.on("/stream", handleStream);

  server.begin();
}

void loop() {
  server.handleClient();
}
