import pandas as pd
from IOTsystem.qr.qr import generateQRpassword

class DataFrame:
    def __init__(self, csv_file = "pacientes.csv"):
        self.csv_file = csv_file
        self.data = pd.read_csv(csv_file)

    def inDataFrame(self, name: str) -> bool:
        if name in self.data["nombre"].values:
            return True
        else:
            return False
        
    def getIndex(self, name: str) -> int:
        if not self.inDataFrame(name):
            return None
        else:
            idx = self.data[self.data["nombre"] == name].index
            return idx

    def add_patient_profile(self, params):
        try:
            nombre, edad, sexo, historial_medico, telefono, contactos = params

            if self.inDataFrame(nombre):
                print(f'Error, paciente {nombre} ya existe en base de datos')
                return f'NPErr Paciente {nombre} existente en base de datos'
            
            new_data = {
                "id": len(self.data) + 1,
                "nombre": nombre,
                "edad": int(edad),
                "sexo": sexo,
                "historial_medico": historial_medico,
                "numero_telefono": telefono,
                "contactos": contactos,
                "configuracion_pastillas": "",
                "Historial de Dosis": ""
            }
        
            self.data = self.data._append(new_data, ignore_index=True)
            #print(self.data.to_string())
            return "NPOK"
        except ValueError as ve:
            print(f'Error de Formato NP: {ve}')
            return f'NPErr {ve}'
        # self.client.publish("Py/routine", "NPOK")

    def load_data(self):
        self.data = pd.read_csv(self.csv_file)

    def save_data(self):
        self.data.to_csv(self.csv_file, index=False)

    def configure_dispensing(self, params):
        try: 
            nombre, freq, hora_inicial, dias, notas = params
            if not self.inDataFrame(nombre):
                print(f'Error, paciente {nombre} no existe en base de datos')
                return f'NPErr Paciente {nombre} no existente en base de datos'

            idx = self.getIndex(nombre)

            if not idx.empty:
                self.data.at[idx[0], "configuracion_pastillas"] = f"{freq}#{hora_inicial}#{dias}#{notas}"
                print(self.data.to_string())
                #self.client.publish("Py/routine", "CPOK")
        except ValueError as ve:
            print(f'Error de Formato CP: {ve}')
            return f'CPErr {ve}'

    def generate_qr(self, params):
        try:
            name = params[0]
            if not self.inDataFrame(name):
                return f'Paciente {name} no esta en la base de datos'
            else:
                mes = generateQRpassword(name)
                return mes
        except ValueError as ve:
            print(f'Error de Formato QR: {ve}')
            return f'CPErr {ve}'


    def test(self):
        print("this is a test")

if __name__ == "__main__":
    datacit = DataFrame()
    datacit.test()