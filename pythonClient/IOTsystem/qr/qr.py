import qrcode
import random

def generateQRpassword(name: str):
    numCode = str(random.randint(1000, 9999))
    qr_data = name + numCode

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
    img.save("qrCodes/"+name+".png")

    print("Código QR generado y guardado como '" +str(name)+ ".png'.")
    return "QROK"
