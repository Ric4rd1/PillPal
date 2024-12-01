import cv2
import numpy as np
import time
import threading
import IOTsystem.qr.config as c

class CamaraESP():
    def __init__(self, webserver = c.WEBSERVER, qr_event=None):
        self.webserver = webserver
        self.cap = cv2.VideoCapture(self.webserver)
        self.stop_camara = False
        self.frame = None
        self.cameraThread = None
        self.cameraShowThread = None
        self.qrDetectionThread = None
        self.frame_lock = threading.Lock()
        self.qr_event = qr_event  # Evento para liberar hilos esperando

    def loop_start(self):
        while not self.stop_camara:
            ret, temp_frame = self.cap.read()
            if not ret:
                print("Error al obtener la imagen de la cámara")
                time.sleep(1)  # Espera breve antes de volver a intentar
                break

            # Voltear la imagen
            temp_frame = cv2.flip(temp_frame, -1)

            # Actualizar 'frame' dentro de un bloqueo
            with self.frame_lock:
                self.frame = temp_frame

            # Terminar si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    def start(self):
        if not self.cameraThread or not self.cameraThread.is_alive():
            self.cameraThread = threading.Thread(target=self.loop_start)
            self.cameraThread.start()
            print("STARTING CAMERA ... ")

    def start_qr_detection(self):
        if not self.qrDetectionThread or not self.qrDetectionThread.is_alive():
            self.qrDetectionThread = threading.Thread(target=self.detect_qr_code_scheduler)
            self.qrDetectionThread.start()

    def stop(self):
        if self.cap.isOpened():
            self.stop_camara = True
            time.sleep(0.2) # Wait for the camera to shutdown
            self.cap.release()
            cv2.destroyAllWindows()
        if self.cameraThread and self.cameraThread.is_alive():
            self.cameraThread.join()
        '''
        self.stop_camara = True
        self.cap.release()
        cv2.destroyAllWindows()
        self.cameraThread.join()'''

    def show(self):
        if not self.cameraShowThread or not self.cameraShowThread.is_alive():
            self.cameraShowThread = threading.Thread(target=self.show_loop)
            self.cameraShowThread.start()

        

    def show_loop(self):
        try:
            while True:
                # Leer el frame dentro de un bloqueo
                with self.frame_lock:
                    if self.frame is not None:
                        cv2.imshow('Webcam', self.frame)

                # Salir si se presiona 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_camara = True
                    self.cap.release()
                    cv2.destroyAllWindows()
                    self.cameraThread.join()
                    break
        except KeyboardInterrupt:
            self.stop_camara = True
            self.cap.release()
            cv2.destroyAllWindows()
            self.cameraThread.join()

    def detect_qr_code(self, passcode: str, timeout: int = 30) -> bool:
        try:
            qr_decoder = cv2.QRCodeDetector()
            start_time = time.time()
            while True:
                with self.frame_lock:
                    # Verificar que el frame no sea None
                    if self.frame is None:
                        continue

                    # Intentar detectar y decodificar el QR
                    data, bbox, _ = qr_decoder.detectAndDecode(self.frame)

                if bbox is not None and data:
                    print(f"QR Code detected: {data}")
                    if data == passcode:
                        #callback()
                        if self.qr_event:
                            self.qr_event.set()
                            print("QR event set!")
                        return True
                    
                # Verificar timeout
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Se agotó el tiempo para escanear el QR: {passcode}")
                
                    
        except TimeoutError as e:
            print(f"No se escaneó el QR para {passcode}. Intentando en la siguiente ronda.")
            return False
        except Exception as e:
            print(f"Error inesperado durante la detección de QR: {e}")
            return False
        
        
    '''            
    def detect_qr_code_scheduler(self, passcode: str) -> bool:
        # Funcion que funciona con scheduler
        qr_decoder = cv2.QRCodeDetector()
        while True:
            with self.frame_lock:
                if self.frame is None:
                    continue
                data, bbox, _ = qr_decoder.detectAndDecode(self.frame)
            
            if bbox is not None and data:
                print(f"QR Code detected: {data}")
                if data == passcode:
                    self.pill_scheduler.set_qr_detected()
                    return True
        '''

def printSuccess():
    print("QR detected succesful!!!")

if __name__ == "__main__":
    myCamera = CamaraESP(0)
    myCamera.start()
    #myCamera.show_loop()
    myCamera.detect_qr_code("Ricard8766", printSuccess)
    print("Program finished")
    myCamera.stop()


    
