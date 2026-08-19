import time

import noisereduce as nr
import numpy as np
import sounddevice as sd
import soundfile as sf

import reduce_noise

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
        self.engine = reduce_noise.AudioEngine(16000)

    def startMic(self):
        self.microfono = sd.InputStream(
            samplerate=self.Rate,
            blocksize=self.chunk,
            channels=self.channels,
            dtype=self.Dtype,
            callback=self.recordSilence,
        )

        data, fs = sf.read("assets/bell_starMod.wav")
        sd.play(data, fs)
        sd.wait()
        self.microfono.start()
        print("microfono encendido")
        while self.microfonoACT:
            time.sleep(0.1)
        self.stopMic()
        song, pr = sf.read("assets/Exit_main_processed.wav")
        sd.play(song, pr)
        sd.wait()
        print("microfono apagado")
        return self.audio

    def stopMic(self):
        if self.microfono:
            self.microfono.stop()
            self.microfono.close()
            self.microfono = None

    def readMic(self, indata):
        if self.microfono:
            self.buffer.append(indata.copy())
            if self.buffer:
                audio = np.concatenate(self.buffer).flatten()
                resultado = self.engine.reduce_noise(audio.tolist())
                self.audio = np.array(audio, dtype=np.float32) / 32768.0
                return audio

    def recordSilence(self, indata, *args):
        self.readMic(indata)
        volumen = np.abs(indata).mean()
        if self.microfono:
            if volumen < self.umbral_silencio:
                self.pasos_silencio += 1
                # Debug cada ~1s
                if self.pasos_silencio % 15 == 1:
                    print(
                        f"  [..] silencio: paso {self.pasos_silencio}/{self.pasos_silencio_limite}",
                        flush=True,
                    )
                if self.pasos_silencio >= self.pasos_silencio_limite:
                    print(f"  [..] Silencio detectado, cerrando mic", flush=True)
                    self.microfonoACT = False
                    self.pasos_silencio = 0
                    return
            else:
                if self.pasos_silencio > 0:
                    print(
                        f"  [!] Voz detectada! vol={volumen:.0f} (reset silencio)",
                        flush=True,
                    )
                self.pasos_silencio = 0
