from IOTsystem.mqtt.messageQueue import messageQueue
from IOTsystem.mqtt.mqtt import MQTTClient
import time

class IOTSystem:
    def __init__(self):
        self.queue = messageQueue()

    def start(self):   
        self.queue.mqttClient.start()
        try:
            while True:
                self.queue.process_instructions()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.queue.data.save_data()
            self.queue.mqttClient.stop()
            # self.queue.mqttClient.stop()
            print("Data saved and client stopped.")

if __name__ == "__main__":
    system = IOTSystem()
    system.start()
