from IOTsystem.mqtt.messageQueue import messageQueue
from IOTsystem.mqtt.mqtt import MQTTClient
import time

class IOTSystem:
    def __init__(self):
        self.queue = messageQueue()

    def start(self):   
        self.queue.mqttClient.start()
        try:
            while True:
                self.queue.process_instructions()
                self.queue.process_return_data()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.queue.data.save_data()
            self.queue.mqttClient.stop()
            self.queue.pillScheduler.espCam.stop()
            self.queue.pillScheduler.stop()
            print("Data saved and client stopped.")

    def print_pillpal_ascii(self):
        print(r"""
            .PPPPPPPP..IIII..LLLL........LLLL........PPPPPPPPP..AAAAAAA..LLLL........
            .PPPPPPPPP.IIII..LLLL........LLLL........PPPPPPPPPP.AAAAAAAA.LLLL........
            .PPPP..PPP.IIII..LLLL........LLLL........PPPP..PPP.AAA...AAA.LLLL........
            .PPPPPPPPP.IIII..LLLL........LLLL........PPPPPPPPP.AAA...AAA.LLLL........
            .PPPPPPPP..IIII..LLLL........LLLL........PPPPPPPP..AAAAAAAAA.LLLL........
            .PPP.......IIII..LLLL........LLLL........PPPP......AAAAAAAAA.LLLL........
            .PPP.......IIII..LLLLLLLLLL..LLLLLLLLLL..PPPP......AAA...AAA.LLLLLLLLLL..
            .PPP.......IIII..LLLLLLLLLL..LLLLLLLLLL..PPPP......AAA...AAA.LLLLLLLLLL..
            .........................................................................
            .............your.personal.medical.assistant.............................
                """)

if __name__ == "__main__":
    system = IOTSystem()
    system.print_pillpal_ascii()
    system.start()
