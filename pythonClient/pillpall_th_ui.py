import customtkinter as ctk
import paho.mqtt.client as mqtt
from tkinter import messagebox

# Configuración del cliente MQTT
client = mqtt.Client()

# Variables para almacenar temperatura y humedad
temperatura = ""
humedad = ""

# Función que se ejecuta cuando te conectas al broker MQTT
def on_connect(client, userdata, flags, reasonCode, properties=None):
    print(f"Conectado con código de resultado {reasonCode}")
    client.subscribe("ESP/confirm")

# Función que se ejecuta cuando se recibe un mensaje en un tópico suscrito
def on_message(client, userdata, msg):
    global temperatura, humedad
    mensaje = f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}"
    print(mensaje)
    
    # Procesar el mensaje recibido
    if "°C" in mensaje:  # Si el mensaje contiene temperatura
        temperatura = mensaje.split(": ")[1]  # Extraer el valor de temperatura
        label_temp.configure(text=f"Temperatura: {temperatura}")  # Actualizar etiqueta
    elif "%" in mensaje:  # Si el mensaje contiene humedad
        humedad = mensaje.split(": ")[1]  # Extraer el valor de humedad
        label_hum.configure(text=f"Humedad: {humedad}")  # Actualizar etiqueta
    
    messagebox.showinfo("Pill Pall", mensaje)

# Configuración y conexión al broker MQTT
client.on_connect = on_connect
client.on_message = on_message

# Función para enviar los mensajes MQTT
def enviar_mensaje(instruction):
    if instruction == "MF":
        value = entry_valor.get()
        if value.isdigit():
            message = instruction + value
        else:
            messagebox.showerror("Error", "Debes ingresar un valor numérico para 'MF'.")
            return
    else:
        message = instruction

    client.publish("Py/routine", message)
    print(f"Enviado: {message}")

# Conectar al broker y iniciar el loop
def conectar_broker():
    try:
        client.connect("localhost", 1883, 60)
        client.loop_start()
        status_label.configure(text="Conectado al Broker", fg_color="green")
    except Exception as e:
        status_label.configure(text=f"Error de conexión: {e}", fg_color="red")

# Inicializar la ventana principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Control Pill Pall")
ventana.geometry("600x400")  # Ajustar el tamaño de la ventana

# Título
titulo = ctk.CTkLabel(ventana, text="Enviar Comandos a Pill Pall", font=("Arial", 20))
titulo.grid(row=0, column=0, columnspan=2, pady=10)

# Entrada para el valor de la instrucción "MF"
label_valor = ctk.CTkLabel(ventana, text="Mover hacia adelante", font=("Arial", 12))
label_valor.grid(row=2, column=0, padx=10, pady=5, columnspan=2)
entry_valor = ctk.CTkEntry(ventana, placeholder_text="Ingrese valor", font=("Arial", 12))
entry_valor.grid(row=1, column=1, padx=10, pady=5)

# Botón para mover hacia adelante
btn_mf = ctk.CTkButton(ventana, text="↑", font=("Arial", 20), width=60, height=60,
                        command=lambda: enviar_mensaje("MF"))
btn_mf.grid(row=1, column=0, padx=10, pady=10)

# Botones para dispensar y recargar pastillas
btn_dp = ctk.CTkButton(ventana, text="Dispensar", font=("Arial", 12), width=60, height=60,
                        command=lambda: enviar_mensaje("DP"))
btn_dp.grid(row=3, column=0, padx=10, pady=10)

btn_rp = ctk.CTkButton(ventana, text="Recargar", font=("Arial", 12), width=60, height=60,
                        command=lambda: enviar_mensaje("RP"))
btn_rp.grid(row=3, column=1, padx=10, pady=10)

# Botones para leer temperatura y humedad
btn_tp = ctk.CTkButton(ventana, text="Leer Temperatura", font=("Arial", 12),
                        command=lambda: enviar_mensaje("TP"))
btn_tp.grid(row=2, column=2, padx=10, pady=10)

btn_hp = ctk.CTkButton(ventana, text="Leer Humedad", font=("Arial", 12),
                        command=lambda: enviar_mensaje("HP"))
btn_hp.grid(row=2, column=3, padx=10, pady=10)

# Área de lectura de temperatura y humedad
label_temp = ctk.CTkLabel(ventana, text="Temperatura: - °C", font=("Arial", 12))
label_temp.grid(row=1, column=2, pady=5)

label_hum = ctk.CTkLabel(ventana, text="Humedad: - %", font=("Arial", 12))
label_hum.grid(row=1, column=3, pady=5)

# Etiqueta para el estado de conexión
status_label = ctk.CTkLabel(ventana, text="Desconectado", fg_color="red", font=("Arial", 12))
status_label.grid(row=5, column=0, columnspan=2, pady=10)

# Botón para conectar al broker
conectar_btn = ctk.CTkButton(ventana, text="Conectar al Broker", font=("Arial", 12), command=conectar_broker)
conectar_btn.grid(row=6, column=0, columnspan=2, pady=10)

# Ejecutar la ventana principal de CustomTkinter
ventana.mainloop()

# Desconexión del cliente MQTT al cerrar la interfaz
client.loop_stop()
client.disconnect()
