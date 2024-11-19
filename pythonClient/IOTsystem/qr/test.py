import cv2
import numpy as np
import time
import threading
import IOTsystem.qr.config as c
# Inicia la captura de la webcam
# cap = cv2.VideoCapture(c.WEBSERVER)
cap = cv2.VideoCapture(0)

# Bloque para sincronizar el acceso a la variable 'frame'
frame_lock = threading.Lock()
stop_camara = False
frame = None

def loopCamara(cap):
    global frame
    while not stop_camara:
        ret, temp_frame = cap.read()
        if not ret:
            print("Error al obtener la imagen de la cámara")
            break

        # Voltear la imagen
        temp_frame = cv2.flip(temp_frame, -1)

        # Actualizar 'frame' dentro de un bloqueo
        with frame_lock:
            frame = temp_frame

        # Terminar si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camaraThread = threading.Thread(target = loopCamara, args=(cap,))
camaraThread.start()

def detect_qr_code(name: str, code: int):

    return isQRexpected(name)

def isQRexpected(qr_expected):
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecode(frame)
    
    if bbox is not None and data:
        print(f"QR Code detected: {data}")
        if data == qr_expected:
            return 1
    return 0

try:
    while True:
        # Leer el frame dentro de un bloqueo
        with frame_lock:
            if frame is not None:
                cv2.imshow('Webcam', frame)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_camara = True
            cap.release()
            cv2.destroyAllWindows()
            camaraThread.join()
            break
except KeyboardInterrupt:
    stop_camara = True
    cap.release()
    cv2.destroyAllWindows()
    camaraThread.join()