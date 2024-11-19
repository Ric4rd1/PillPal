import cv2
import numpy as np
import time
import threading
import IOTsystem.qr.config as c

class CamaraESP():
    def __init__(self, webserver = c.WEBSERVER):
        self.webserver = webserver
        self.cap = cv2.VideoCapture(self.webserver)
        self.stop_camara = False
        self.frame = None
        self.cameraThread = None
        self.frame_lock = threading.Lock()

    def loop_start(self):
        while not self.stop_camara:
            ret, temp_frame = self.cap.read()
            if not ret:
                print("Error al obtener la imagen de la cámara")
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

    def stop(self):
        self.stop_camara = True
        self.cap.release()
        cv2.destroyAllWindows()
        self.cameraThread.join()

    def show(self):
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

    def detect_qr_code(self, passcode: str, callback) -> bool:
        qr_decoder = cv2.QRCodeDetector()
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
                    callback()
                    return True

def printSuccess():
    print("QR detected succesful!!!")

if __name__ == "__main__":
    myCamera = CamaraESP(0)
    myCamera.start()
    #myCamera.show()
    myCamera.detect_qr_code("Ricard1683", printSuccess)
    print("Program finished")
    myCamera.stop()


    
