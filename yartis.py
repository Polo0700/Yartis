import argparse
import asyncio
import os
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd
import websockets
from piper import PiperVoice

from brain.opencode import peticion
from core.wake import wake

parser = argparse.ArgumentParser()
parser.add_argument("--cpu", action="store_true", help="Forzar CPU aunque haya GPU")
args = parser.parse_args()
if args.cpu:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""


class yartis:
    def __init__(self):
        self.peticion = peticion()
        self.tts = PiperVoice.load(
            str(
                Path(__file__).parent / "core" / "models" / "es_Es-sharvard-medium.onnx"
            )
        )
        self.websocketURL = "ws://localhost:8765"

    async def hablar(self, texto):
        print(f"Yartis dice: {texto}")
        with wave.open("temp.wav", "w") as wav:
            self.tts.synthesize_wav(texto, wav)
        with wave.open("temp.wav", "r") as wav:
            data = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
            rate = wav.getframerate()
        sd.play(data, rate)
        stream = sd.get_stream()
        res = "0x0x0Polo0701Audio"
        try:
            async with websockets.connect(self.websocketURL) as websocket:
                await websocket.send(res)
        except Exception as e:
            print(f"Error al enviar mensaje al servidor: {e}")
        while stream.active:
            duracion = len(data) / rate
            if stream.time > duracion * 0.98:
                res = "0x0x0Polo0700Audio"
                try:
                    async with websockets.connect(self.websocketURL) as websocket:
                        await websocket.send(res)
                except Exception as e:
                    print(f"Error al enviar mensaje al servidor: {e}")
                break
        sd.wait()
        sd.stop()

    async def iniciar(self):
        while True:
            self.wake = wake()
            await self.hablar("Esperando Wake word")
            self.wake.iniciar()
            await self.hablar("Yartis está escuchando...")
            print("Wake word detectada, procesando petición...")
            print("Yartis escuchando peticion")
            respuesta = await self.peticion.ejecutar()
            if not respuesta or respuesta == "Error":
                continue
            try:
                respuestaf = f"0x0x0Polo0702VozRes|{respuesta}"
                async with websockets.connect(self.websocketURL) as websocket:
                    await websocket.send(respuestaf)
                    respuesta = await websocket.recv()
            except Exception as e:
                print(f"Error al recibir respuesta del servidor: {e}")
            print("Yartis para de escuchar peticion")
            print(f"Respuesta de Yartis: {respuesta}")
            await self.hablar(respuesta)


if __name__ == "__main__":
    try:
        app = yartis()
        asyncio.run(app.iniciar())
    except (KeyboardInterrupt, SystemExit):
        print("\nYartis cerrado por el usuario")
    except Exception as e:
        print(f"\nYartis cerrado: {e}")
