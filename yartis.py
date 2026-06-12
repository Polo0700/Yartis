from core.wake import wake
from brain.opencode import peticion


class yartis:
    def __init__(self):
        self.peticion = peticion()

    def iniciar(self):
        while True:
            self.wake = wake()
            print("Yartis está escuchando...")
            self.wake.iniciar()
            print("Wake word detectada, procesando petición...")
            print("Yartis escuchando peticion")
            respuesta = self.peticion.ejecutar()
            print("Yartis para de escuchar peticion")
            print(f"Respuesta de Yartis: {respuesta}")
