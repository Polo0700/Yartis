from faster_whisper import WhisperModel
from . import config
from .audio import Audio_Work


class Transcribir:
    def __init__(self):
        self.modelo = config.WHISPER_MODEL
        self.dispositivo = config.WHISPER_DEVICE
        self.formato = config.WHISPER_COMPUTE
        self.opciones = config.WHISPER_BEAM
        self.transcriptor = WhisperModel(
            self.modelo, device=self.dispositivo, compute_type=self.formato
        )

    def transcripcion(self):
        import time as _time

        t0 = _time.time()
        microfono = Audio_Work()
        microfono.startMic()
        print(f"  [>] Grabacion: {_time.time() - t0:.1f}s", flush=True)
        if microfono.audio is None:
            print("  [X] Audio es None!", flush=True)
            return ""
        print(
            f"  [>] Audio shape: {microfono.audio.shape}, len: {len(microfono.audio)}",
            flush=True,
        )

        segmento, info = self.transcriptor.transcribe(
            audio=microfono.audio,
            beam_size=self.opciones,
            language="es",
            word_timestamps=True,
        )
        textof = " ".join(valor.text for valor in segmento)
        print(
            f"  [>] Transcrito: '{textof[:80]}' (en {_time.time() - t0:.1f}s)",
            flush=True,
        )
        return textof
