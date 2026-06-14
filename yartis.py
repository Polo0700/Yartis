from core.wake import wake
from brain.opencode import peticion
import pyttsx3


class yartis:
    def __init__(self):
        self.peticion = peticion()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 150)

    def hablar(self, texto):
        print(f"Yartis dice: {texto}")
        self.tts.say(texto)
        self.tts.runAndWait()

    def iniciar(self):
        self.hablar("Yartis iniciado")
        while True:
            self.wake = wake()
            print("Yartis está escuchando...")
            self.wake.iniciar()
            print("Wake word detectada, procesando petición...")
            print("Yartis escuchando peticion")
            respuesta = self.peticion.ejecutar()
            print("Yartis para de escuchar peticion")
            print(f"Respuesta de Yartis: {respuesta}")
            self.hablar(respuesta)


if __name__ == "__main__":
    app = yartis()
    app.iniciar()
