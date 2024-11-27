import qrcode
import random
import ssl
import smtplib
import os
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import IOTsystem.qr.config as c

def generateQRpassword(name: str, numCode: str):
    #numCode = str(random.randint(1000, 9999))
    qr_data = name + numCode

    file_path = f"qrCodes/{name}.png"
    # Verificar si el archivo ya existe
    if os.path.exists(file_path):
        print(f"El archivo '{file_path}' ya existe. No se generará un nuevo código QR.")
        return "QR_ALREADY_EXISTS"

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
    img.save(file_path)

    print("Código QR generado y guardado como '" +str(name)+ ".png'.")
    return "QROK"

def sendQrcode(email_reciever, name):

    file_path = f'qrCodes/{name}.png'
    body = f"""
        <html>
        <body>
            <p>Dear {name},</p>
            <p>Thank you for joining <b>PillPal</b>! We’re excited to support you in managing your medication effectively and securely.</p>
            <p>As part of our secure delivery process, we’ve implemented a passcode authentication system to ensure your medication reaches you safely. Each time your pills are delivered, you will be required to provide the passcode generated for the specific delivery.</p>
            <p>Please find your unique passcode attached as a QR code below. Simply present it to the delivery agent for verification.</p>
            <p>If you have any questions or concerns, feel free to reach out to our support team at <a href="mailto:pillpal.service@gmail.com">pillpal.service@gmail.com</a>.</p>
            <p>Thank you for trusting PillPal with your health needs!</p>
            <p>Warm regards,</p>
            <p><b>The PillPal Team</b></p>
        </body>
        </html>
    """


    em = EmailMessage()
    em['From'] = c.EMAIL_SENDER
    em['To'] = email_reciever
    em['Subject'] = "💊PILLPAL💊 - Personal QR verification code!"
    # Make the message multipart
    em.add_alternative(body, subtype='html')

    # Attach the image file
    with open(file_path, 'rb') as attachment_file:
        file_data = attachment_file.read()
        file_name = attachment_file.name.split("/")[-1]

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(file_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
    em.attach(attachment)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(c.EMAIL_SENDER, c.EMAIL_PASSWORD)
        smtp.sendmail(c.EMAIL_SENDER, email_reciever, em.as_string())

    return "QROK"

def sendAppointmentEmail(email_reciever, name):
    appointment_link = c.GOOGLE_CALENDAR_LINK
    body = f"""
        <html>
        <body>
            <p>Dear {name},</p>
            <p>Your doctor has requested to schedule an appointment with you.</p>
            <p>To choose a convenient date and time based on the doctor's availability, please visit the link below:</p>
            <p><a href="{appointment_link}">Choose Your Appointment</a></p>
            <p>If you have any questions or need further assistance, feel free to reach out to us at <a href="mailto:pillpal.service@gmail.com">pillpal.service@gmail.com</a>.</p>
            <p>Thank you, and we look forward to assisting you!</p>
            <p>Best regards,</p>
            <p><b>The PillPal Team</b></p>
        </body>
        </html>
    """

    em = EmailMessage()
    em['From'] = c.EMAIL_SENDER
    em['To'] = email_reciever
    em['Subject'] = "💊PILLPAL💊 - Schedule Your Appointment"
    em.add_alternative(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(c.EMAIL_SENDER, c.EMAIL_PASSWORD)
        smtp.sendmail(c.EMAIL_SENDER, email_reciever, em.as_string())

    return "Appointment Email Sent"


if __name__ == "__main__":
    sendQrcode("ric4rd11@gmail.com", "Ricard")
    

