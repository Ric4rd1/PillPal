import qrcode

# Datos del QR que deseas generar
qr_data = "qr_especifico_123"

# Crea el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(qr_data)
qr.make(fit=True)

# Genera la imagen del QR
img = qr.make_image(fill='black', back_color='white')

# Guarda la imagen en un archivo
img.save(qr_data+".png")

print("Código QR generado y guardado como '" +str(qr_data)+ ".png'.")
