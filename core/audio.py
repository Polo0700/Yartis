import time
import sounddevice as sd
import numpy as np
import noisereduce as nr
from . import config


class Audio_Work:
    def __init__(self):
        # Parametros iniciales
        self.Rate = config.RATE
        self.chunk = config.CHUNK
        self.channels = config.CHANNELS
        self.Dtype = config.DTYPE
        self.microfono = None
        self.buffer = []
        self.pasos_silencio = 0
        self.umbral_silencio = config.UMBRAL_SILENCIO
        self.pasos_silencio_limite = config.PASOS_SILENCIO_LIMITE
        self.microfonoACT = True
        self.callback = None
        self.audio = None

    def startMic(self):
        self.microfono = sd.InputStream(
            samplerate=self.Rate,
            blocksize=self.chunk,
            channels=self.channels,
            dtype=self.Dtype,
            callback=self.recordSilence,
        )
        self.microfono.start()
        print("microfono encendido")
        while self.microfonoACT:
            time.sleep(0.1)
        self.stopMic()
        print("microfono apagado")
        return self.audio

    def stopMic(self):
        if self.microfono:
            self.microfono.stop()
            self.microfono.close()
            self.microfono = None
            self.reduceNoise()

    def readMic(self, indata):
        if self.microfono:
            self.buffer.append(indata.copy())

    def recordSilence(self, indata, *args):
        self.readMic(indata)
        volumen = np.abs(indata).mean()
        if self.microfono:
            if volumen < self.umbral_silencio:
                self.pasos_silencio += 1
                if self.pasos_silencio >= self.pasos_silencio_limite:
                    self.microfonoACT = False
                    self.pasos_silencio = 0
                    return
            else:
                self.pasos_silencio = 0

    def reduceNoise(self):
        if self.buffer:
            audio = np.concatenate(self.buffer).flatten()
            audio = audio.astype(np.float32) / 32768.0
            audio = nr.reduce_noise(y=audio, sr=self.Rate)
            self.audio = audio
            print(audio)
            return self.audio
