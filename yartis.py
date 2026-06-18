import argparse
import os
from core.wake import wake
from brain.opencode import peticion
import pyttsx3
import soundfile as sf
import sounddevice as sd


parser = argparse.ArgumentParser()
parser.add_argument("--cpu", action="store_true", help="Forzar CPU aunque haya GPU")
args = parser.parse_args()
if args.cpu:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""


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
            data, fs = sf.read("assets/bell_starMod.wav")
            sd.play(data, fs)
            sd.wait()
            print("Wake word detectada, procesando petición...")
            print("Yartis escuchando peticion")
            respuesta = self.peticion.ejecutar()
            print("Yartis para de escuchar peticion")
            print(f"Respuesta de Yartis: {respuesta}")
            self.hablar(respuesta)


if __name__ == "__main__":
    try:
        app = yartis()
        app.iniciar()
    except (KeyboardInterrupt, SystemExit):
        print("\nYartis cerrado por el usuario")
    except Exception as e:
        print(f"\nYartis cerrado: {e}")
