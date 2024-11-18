import IOTsystem.mqtt.config as c
import paho.mqtt.client as mqtt

# Mqtt client for handling incoming messages from Node/routine

class MQTTClient:
    def __init__(self, queue, 
                 ipAddress = c.IPADDRESS, 
                 port = c.PORT, 
                 keepAlive = c.KEEPALIVE):
        
        self.queue = queue
        self.ipAddress = ipAddress
        self.port = port
        self.keepAlive = keepAlive
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.ipAddress, self.port, self.keepAlive)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to Broker with code result: " + str(rc))
        # Subscripe to topics
        self.client.subscribe("Node/routine")
        self.client.subscribe("Node/confirm")
        self.client.subscribe("ESP/routine")
        self.client.subscribe("ESP/confirm")

    def on_message(self, client, userdata, msg):
        print(f"Message received in {msg.topic}: {msg.payload.decode()}")
        self.queue.put(msg.payload.decode())

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
    
    def publish(self, topic, message):
        self.client.publish(topic, message)

    def send_dosage_history(self):
        ''' 
        Aqui Envia el historial de dosis
        
        '''
        self.client.publish("Py/routine", "HDOK")


