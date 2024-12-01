from datetime import datetime, timedelta

class PillConfiguration:
    def __init__(self, name, passcode, freq, hora_inicial, dias, notas, virtual_clock):
        self.name = name
        self.passcode = passcode
        self.freq = int(freq)  # Frecuencia en horas
        # Combina la fecha actual con la hora inicial proporcionada
        today = virtual_clock.get_time().date()
        time_only = datetime.strptime(hora_inicial, "%H:%M").time()
        self.hora_inicial = datetime.combine(today, time_only)

        self.dias = int(dias)  # Días de duración
        self.notas = notas
        self.virtual_clock = virtual_clock  # Referencia al reloj virtual
        self.next_dispense = self.hora_inicial  # Siguiente hora de dispensación

    def calculate_next_dispense(self):
        """Calcula la próxima hora de dispensación usando el reloj virtual."""
        now = self.virtual_clock.get_time()
        dispense_time = datetime.combine(now.date(), self.hora_inicial.time())
        while dispense_time < now:  # Ajustar si ya pasó
            dispense_time += timedelta(hours=self.freq)
            self.next_dispense = dispense_time
            print(f'new dispense time is: {self.next_dispense}')
        return dispense_time

    def update_initial_time(self, new_time):
        """Actualiza la hora inicial."""
        self.hora_inicial = datetime.strptime(new_time, "%H:%M")
        self.next_dispense = self.calculate_next_dispense()

    def __repr__(self):
        return (f"PillConfiguration(name={self.name}, passcode={self.passcode} freq={self.freq}h, "
                f"hora_inicial={self.hora_inicial.time()}, dias={self.dias}, notas={self.notas}, "
                f"next_dispense={self.next_dispense})")