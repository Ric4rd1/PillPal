import cv2
# pip install opencv-python
import numpy as np
# pip install numpy
import time

# Dirección IP del servidor web de la ESP32 CAM
url = 'http://172.20.10.6/stream' 


def callback(x):
    pass

# Función para detectar y decodificar códigos QR
def detect_qr_code(frame, qr_expected):
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecode(frame)
    
    if bbox is not None and data:
        print(f"QR Code detected: {data}")
        if data == qr_expected:
            return 1
    return 0


# Inicia la captura de la webcam
cap = cv2.VideoCapture(url)

# QR específico que estamos esperando detectar
qr_expected = "qr_especifico_123"
last_check_time = time.time()

while True:
    # Lee la imagen de la webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)

    if not ret:
        print("Error al obtener la imagen de la cámara")
        break

    current_time = time.time()

    if current_time - last_check_time >= 1:
        # Detectar código QR en el frame
        result = detect_qr_code(frame, qr_expected)

        # Imprimir 1 si se detecta el QR específico, 0 si no
        print(result)

        # Actualizar el tiempo de la última verificación
        last_check_time = current_time

    cv2.imshow('Webcam', frame)

    # Muestra la imagen en tiempo real
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
