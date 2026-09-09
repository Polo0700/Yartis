"""Prueba: habla y ve el volumen que capta el microfono"""
import sounddevice as sd
import numpy as np
import time

print("Habla normal durante 5s... (di algo como 'hola probando')")
print("=" * 40)

def callback(indata, *args):
    vol = np.abs(indata).mean()
    bar = "█" * min(int(vol / 10), 50)
    print(f"  vol={vol:6.0f} |{bar}")

stream = sd.InputStream(16000, 1024, 1, dtype="int16", callback=callback)
stream.start()
time.sleep(5)
stream.stop()
stream.close()
print("FIN")
