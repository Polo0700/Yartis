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
        microfono = Audio_Work()
        microfono.startMic()

        segmento, info = self.transcriptor.transcribe(
            audio=microfono.audio,
            beam_size=self.opciones,
            language="es",
            word_timestamps=True,
        )
        textof = " ".join(valor.text for valor in segmento)
        return textof
