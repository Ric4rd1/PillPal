from queue import Queue 
from IOTsystem.dataFrame.dataFrame import DataFrame
from IOTsystem.mqtt.mqtt import MQTTClient

class messageQueue:
    def __init__(self):
        self.queue = Queue()
        self.data = DataFrame()
        self.mqttClient = MQTTClient(self.queue)
        

    def put(self, message):
        self.queue.put(message)

    def process_instructions(self):
        while not self.queue.empty():
            instruction = self.queue.get()
            command = instruction[:2]
            params = instruction[2:].split(',')

            print("Params: ",params)

            if command == "NP":  # Nuevo perfil
                print("Adding new patient profile")
                mes = self.data.add_patient_profile(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "CP":  # Configuración de pastillas
                mes  = self.data.configure_dispensing(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "QR":  # Generar QR
                mes = self.data.generate_qr(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "HD":  # Historial de dosis
                #self.data.send_dosage_history()
                pass

datasito = DataFrame()
datasito.test()