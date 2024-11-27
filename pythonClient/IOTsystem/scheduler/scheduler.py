import threading
import time
from datetime import datetime, timedelta
from typing import List
import pandas as pd
from IOTsystem.scheduler.pillConfiguration import PillConfiguration
from IOTsystem.qr.qrDetection import CamaraESP

class VirtualClock:
    def __init__(self, start_time=None, speed=1):
        """Inicializa el reloj virtual."""
        self.start_time = start_time or datetime.now()
        self.speed = speed  # Velocidad relativa del reloj
        self.real_start_time = datetime.now()

    def get_time2(self):
        """Calcula el tiempo actual del reloj virtual y devuelve una cadena en formato 'GT<hora>,<minutos>'."""
        elapsed_real_time = datetime.now() - self.real_start_time
        elapsed_virtual_time = elapsed_real_time * self.speed
        virtual_time = self.start_time + elapsed_virtual_time
        
        # Convertir a formato GT<hora>,<minutos>
        return f"GT{virtual_time.hour},{virtual_time.minute:02d}"
    
    def get_time(self):
        """Calcula el tiempo actual del reloj virtual."""
        elapsed_real_time = datetime.now() - self.real_start_time
        elapsed_virtual_time = elapsed_real_time * self.speed
        return self.start_time + elapsed_virtual_time

    def advance_time(self, params):
        try:
            hours, minutes = params
            """Avanza el tiempo virtual manualmente."""
            self.start_time += timedelta(hours=int(hours), minutes=int(minutes))
            return "FTOK"
        except ValueError as ve:
            print(f'Error de Formato FT: {ve}')
            return f'FTErr {ve}'

class PillScheduler:
    def __init__(self, data_frame: pd.DataFrame, virtual_clock, mqtt_client):
        """
        Inicializa el PillScheduler con un DataFrame de pandas y un reloj virtual.
        
        :param data_frame: DataFrame con columnas 'nombre' y 'configuracion_pastillas'.
        :param virtual_clock: Instancia de VirtualClock para manejar el tiempo simulado.
        """
        self.virtual_clock = virtual_clock
        self.pill_configs: List[PillConfiguration] = []
        self.running = False
        self.qr_detected = False
        self.qr_event = threading.Event()
        self.mqtt_client = mqtt_client
        self.data_frame = data_frame
        self.load_configurations(data_frame)

        # ESP camera
        self.espCam = CamaraESP(0,qr_event=self.qr_event) # Using Webcam
        #self.espCam = CamaraESP(qr_event=self.qr_event) # Using WEBSERVER
        self.espCam.start()

    def set_qr_detected(self):
        """
        Marca que el QR ha sido detectado y activa el evento.
        """
        self.qr_detected = True
        self.qr_event.set()

    def load_configurations(self, data_frame: pd.DataFrame):
        """
        Carga las configuraciones desde un DataFrame.
        """
        for _, row in data_frame.iterrows():
            if pd.notna(row["configuracion_pastillas"]):
                name = row["nombre"]
                passcode = row["Passcode"]
                freq, hora_inicial, dias, notas = row["configuracion_pastillas"].split("#")
                pill = PillConfiguration(
                    name=name,
                    passcode=passcode,
                    freq=int(freq),
                    hora_inicial=hora_inicial,
                    dias=int(dias),
                    notas=notas,
                    virtual_clock=self.virtual_clock,
                )
                self.pill_configs.append(pill)
        
        print("Loaded configurations ------>")
        print(self.pill_configs)

    def add_configuration(self, name: str, freq: int, hora_inicial: str, dias: int, notas: str):
        """
        Agrega un nuevo objeto PillConfiguration a la lista de configuraciones.
        """

        if name not in self.data_frame["nombre"].values:
            print(f"Error: No se encontró el nombre '{name}' en la configuración.")
            return
        
        passcode = self.data_frame.loc[self.data_frame["nombre"] == name, "Passcode"].values[0]
    
        # Crear el objeto PillConfiguration
        pill = PillConfiguration(
            name=name,
            passcode=passcode,
            freq=freq,
            hora_inicial=hora_inicial,
            dias=dias,
            notas=notas,
            virtual_clock=self.virtual_clock,
        )

        # Añadir el objeto a la lista de configuraciones
        self.pill_configs.append(pill)
        print(f"Configuración añadida para {name}: {freq}#{hora_inicial}#{dias}#{notas}")
        print(self.pill_configs) # debug

    def check_and_dispense(self):
        """
        Verifica si es hora de dispensar y espera la detección de un QR.
        """
        while self.running:
            now = self.virtual_clock.get_time()
            for pill in self.pill_configs:
                if pill.next_dispense <= now:
                    print(f"Es hora de dispensar para {pill.name}, esperando QR...")
                    self.qr_detected = False
                    self.qr_event.clear()  # Reinicia el evento para esta ronda

                    try:
                        self.espCam.detect_qr_code(str(pill.name)+str(pill.passcode))
                        
                        # Espera la detección del QR
                        self.qr_event.wait()
    
                        print(f"Dispensando pastillas para {pill.name}. Notas: {pill.notas}")
                        self.mqtt_client.publish("Py/routine", "DP")
                        pill.calculate_next_dispense()  # Recalcula la siguiente hora de dispensación
                    except TimeoutError as e:
                        print(f"Error: {e}")
                        print(f"No se escaneó el QR para {pill.name}. Intentando en la siguiente ronda.")
            time.sleep(1)  # Ajusta según sea necesario

    def start(self):
        """
        Inicia el scheduler en un hilo separado.
        """
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.check_and_dispense)
            thread.daemon = True
            thread.start()

    def stop(self):
        """
        Detiene el scheduler.
        """
        self.running = False