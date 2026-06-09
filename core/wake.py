import time

import sounddevice as sd
import openwakeword
from openwakeword import Model
from . import config


class wake:
    def __init__(self):
        rutas = openwakeword.get_pretrained_model_paths()
        self.rate = config.RATE
        self.frame = config.WAKE_FRAME
        self.channels = config.CHANNELS
        self.dtype = config.DTYPE
        self.wordSearch = config.WAKE_WORD
        self.stream = sd.InputStream(
            samplerate=self.rate,
            blocksize=self.frame,
            channels=self.channels,
            dtype=self.dtype,
            callback=self.word,
        )
        self.modelo = Model(
            wakeword_model_paths=[r for r in rutas if self.wordSearch in r]
        )

    def word(self, indata, *args):
        frame = indata[:, 0].copy()
        resultado = self.modelo.predict(frame)
        print(f"Score: {resultado}")
        if any(
            resultado.get(k, 0) > config.WAKE_THRESHOLD
            for k in resultado
            if self.wordSearch in k
        ):
            print("Despertador activado")
            raise sd.CallbackStop()

    def iniciar(self):
        self.stream.start()
        while self.stream.active:
            time.sleep(0.1)
        self.stream.stop()
        self.stream.close()
