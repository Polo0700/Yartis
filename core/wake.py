import time

import numpy as np
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
        self._frame_count = 0
        # Duración: cuantos frames seguidos sobre el umbral para activar
        self._consecutive_high = 0
        self._min_consecutive = 4  # ~320ms a 1280samples/16000Hz

    def word(self, indata, *args):
        frame = indata[:, 0].copy()
        resultado = self.modelo.predict(frame)
        self._frame_count += 1

        if config.DEBUG:
            now = time.time()
            if not hasattr(self, "_last_print") or now - self._last_print >= 1.0:
                scores = {k: f"{v:.3f}" for k, v in resultado.items()}
                print(f"[{self._frame_count:3d}] Scores: {scores}")
                self._last_print = now

        for k in resultado:
            if self.wordSearch in k:
                v = resultado.get(k, 0)

                # Contar frames seguidos sobre el umbral
                if v > config.WAKE_THRESHOLD:
                    self._consecutive_high += 1
                    if self._consecutive_high >= self._min_consecutive:
                        if config.DEBUG:
                            print(
                                f"[!] Wake: {self._consecutive_high} frames seguidos sobre umbral"
                            )
                        self.detected = True
                        raise sd.CallbackStop()
                else:
                    # Se cayó del umbral → reiniciar contador
                    self._consecutive_high = 0

    def iniciar(self):
        self.detected = False
        try:
            self.stream.start()
            while self.stream.active and not self.detected:
                time.sleep(0.05)
        except Exception as e:
            print(f"Stream cerrado: {e}")
        finally:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"The microphone was closed unexpected {e}")
            # Dar tiempo a Windows para soltar el dispositivo de audio
            time.sleep(0.5)
