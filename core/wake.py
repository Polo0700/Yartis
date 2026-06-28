import time

import sounddevice as sd

from openwakeword import Model
from . import config


class wake:
    def __init__(self):
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
        self.modelo = Model(wakeword_model_paths=[config.WAKE_MODEL_PATH])

    def word(self, indata, *args):
        frame = indata[:, 0].copy()
        resultado = self.modelo.predict(frame)
        if config.DEBUG:
            now = time.time()
            if not hasattr(self, "_last_print") or now - self._last_print >= 1.0:
                scores = {k: f"{v:.3f}" for k, v in resultado.items()}
                print(f"📡 Scores: {scores}")
                self._last_print = now
        if any(
            resultado.get(k, 0) > config.WAKE_THRESHOLD
            for k in resultado
            if self.wordSearch in k
        ):
            print("Despertador activado")
            self.detected = True  # flag antes de CallbackStop
            raise sd.CallbackStop()

    def iniciar(self):
        self.detected = False
        try:
            self.stream.start()
            while self.stream.active and not self.detected:
                time.sleep(0.05)
            print("sali de la wake")
        except Exception as e:
            print(f"Stream cerrado: {e}")
        finally:
            try:
                self.stream.stop()
                self.stream.close()
            except:
                pass
            # Dar tiempo a Windows para soltar el dispositivo de audio
            time.sleep(0.5)
