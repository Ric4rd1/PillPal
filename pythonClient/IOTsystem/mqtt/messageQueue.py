import threading
from queue import Queue 
from IOTsystem.dataFrame.dataFrame import DataFrame
from IOTsystem.mqtt.mqtt import MQTTClient
from IOTsystem.scheduler.scheduler import VirtualClock, PillScheduler


class messageQueue:
    def __init__(self):
        self.queue = Queue()
        self.queueReturnData = Queue()
        self.data = DataFrame()
        self.mqttClient = MQTTClient(self.queue, self.queueReturnData)

        # Scheduler
        self.virtualClock = VirtualClock()
        self.pillScheduler = PillScheduler(self.data.data, self.virtualClock, self.mqttClient)
        self.pillScheduler.start()

        self.temperature = 0.0
        self.humidity = 0
        # Semáforo para sincronización de TH
        self.sync_event = threading.Event()
        self.pending_responses = 0
        self.response_lock = threading.Lock()
        

    def put(self, message):
        self.queue.put(message)

    def process_instructions(self):
        while not self.queue.empty():
            instruction = self.queue.get()
            command = instruction[:2]
            params = instruction[2:].split(',')

            print("Params: ",params)
            # -------------- Paciente -----------------------
            if command == "NP":  # Nuevo perfil
                print("Adding new patient profile")
                mes = self.data.add_patient_profile(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "CP":  # Configuración de pastillas
                mes  = self.data.configure_dispensing(params)
                if mes == "CPOK":
                    self.pillScheduler.add_configuration(self.data.data, params[0],params[1], params[2], params[3], params[4])   
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "QR":  # Generar QR
                mes = self.data.generate_qr(params)
                self.data.send_qr(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "HD":  # Historial de dosis
                #self.data.send_dosage_history()
                pass

            # ------------- Admin --------------------------
            if command == "IP": #Regresar info del paciente
                mes = self.data.get_pacient_info(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "OH": #Regresar historial de dosis ---------------Pendiente
                mes = self.data.get_pacient_dose_history(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "MM":
                mes = self.data.request_appointment(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "TH": #Regresar temperatura y humedad
                self.start_th_sequence()
            elif command == "FT": # Avanzar el reloj
                mes = self.virtualClock.advance_time(params)
                self.mqttClient.publish("Py/confirm", mes)
            elif command == "GT": # Regresar la hora actual del programa
                mes = self.virtualClock.get_time2() 
                self.mqttClient.publish("Py/confirm", mes)


    def start_th_sequence(self):
        with self.response_lock:
            self.pending_responses = 2  # TP y HP esperados
        self.sync_event.clear()
        self.mqttClient.publish("Py/routine", "TP")
        self.mqttClient.publish("Py/routine", "HP")

        # Lanza un hilo para manejar la espera sin bloquear
        threading.Thread(target=self.wait_for_th_responses, daemon=True).start()

    def wait_for_th_responses(self):
        # Espera a que todas las respuestas lleguen
        self.sync_event.wait()
        print(f"Temperature: {self.temperature}, Humidity: {self.humidity}")
        # Envía datos de regreso a Node RED
        self.mqttClient.publish("Py/confirm", f"TH{self.temperature},{self.humidity}")
                

    def process_return_data(self):
        while not self.queueReturnData.empty():
            try:
                instruction = self.queueReturnData.get()
                command = instruction[:2]
                params = instruction[2:].split(',')

                if command == "TP":
                    self.temperature = params[0]
                elif command == "HP":
                    self.humidity = params[0]

                with self.response_lock:
                    self.pending_responses -= 1
                    if self.pending_responses == 0:
                        self.sync_event.set()  # Libera el hilo en espera

            except ValueError as ve:
                print(f'Error de Formato en topico ESP/confirm: {ve}, mensaje: {instruction}')
            
