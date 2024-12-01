# PillPal 🩺💊  
Welcome to PillPal! A home medical assistant designed to improve medication management. PillPal combines innovative hardware and software to ensure users take their medications on time and safely.  

## 🚀 Project Description  
PillPal is a medication dispensing robot that leverages MQTT and data processing technologies to:  
- Dispense medications according to prescriptions.  
- Notify users about medication schedules.  
- Provide remote control and real-time monitoring via an MQTT network for patients under medication.  

## 📂 Project Structure  
The project is divided into three main components, each with specific responsibilities:  

1. **Node-Red GUI (Client)**:  
   - Monitors the robot's status.  
   - Sends medication delivery instructions.  
   - Provides an intuitive graphical interface for user interaction.  

2. **Python Client**:  
   - Sends instructions to the microcontroller.  
   - Processes information received from the robot.  
   - Publishes results to the graphical interface for real-time updates.  

3. **ESP32 Client**:  
   - Acts as a "slave" device that executes instructions from the Python client.  
   - Handles measurement and actuation tasks, such as dispensing medications.  

## ⚙️ Technologies Used  
- **Language**: Python, Arduino/C++  
- **Protocols**: MQTT,   
- **Hardware**: ESP32 and additional components for medication dispensing.  
- **Libraries**:  
  - `paho-mqtt` for MQTT communication.  
  - `queue` for task management.  
  - `pandas` for DataFrame handling.  
  - `qrcode` for generating QR codes with medication information.  

