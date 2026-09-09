import wave
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf
from piper import PiperVoice
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from core.audio import Audio_Work
from core.transcriber import Transcribir


class confirmador:
    def __init__(self):
        frases = [
            "sí",
            "sí dale",
            "dale",
            "adelante",
            "ok",
            "okay",
            "confirma",
            "hazlo",
            "está bien",
            "simón",
            "sale",
            "vale",
            "dalo por hecho",
            "apruebo",
            "confirmo",
            "procede",
            "ejecuta",
            "hazlo sin miedo",
            "sí hazlo",
            "correcto",
            "de una",
            "dalo",
            "perfecto",
            "claro que sí",
            "no",
            "no hagas",
            "para",
            "cancela",
            "detente",
            "mejor no",
            "no quiero",
            "no hagas nada",
            "cancela todo",
            "nada",
            "no lo hagas",
            "no confirmo",
            "no apruebo",
            "detén",
            "suelta",
            "espera no",
            "para ahí",
            "no es necesario",
            "mejor no hagas nada",
            "no nada",
            "olvídalo",
            "déjalo así",
            "no hace falta",
            "ni lo intentes",
        ]
        etiquetas = [1] * 24 + [0] * 24
        self.vectorizer = TfidfVectorizer()
        x = self.vectorizer.fit_transform(frases)
        self.modelo = LogisticRegression()
        self.modelo.fit(x, etiquetas)
        self.respuesta = ""
        self.textoConfirmacion = ""
        self.textoUsuario = ""
        self.micro = Audio_Work()
        self.transcriptor = Transcribir()
        self.tts = PiperVoice.load(
            str(
                Path(__file__).parent.parent
                / "core"
                / "models"
                / "es_Es-sharvard-medium.onnx"
            )
        )

    def hablar(self, texto):
        with wave.open("temp_confirm.wav", "w") as wav:
            self.tts.synthesize_wav(texto, wav)
        with wave.open("temp_confirm.wav", "r") as wav:
            data = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
            rate = wav.getframerate()
        sd.play(data, rate)
        sd.wait()
        sd.stop()

    def clasificar(self, seccion):
        self.textoUsuario = seccion
        if self.textoUsuario is None:
            return 0
        if len(self.textoUsuario) < 3:
            return 0
        self.textoUsuario = self.textoUsuario[2]
        self.textoConfirmacion = self.preguntar()
        vector = self.vectorizer.transform([self.textoConfirmacion])
        prediccion = self.modelo.predict(vector)[0]
        return prediccion

    def preguntar(self):
        # Alerta sonora igual que la de entrada
        data, fs = sf.read("assets/bell_starMod.wav")
        sd.play(data, fs)
        sd.wait()
        self.hablar("¿Estas seguro que quieres que " + self.textoUsuario)
        self.respuesta = self.transcriptor.transcripcion()

        if self.respuesta:
            return self.respuesta
        else:
            self.hablar("no respondiste nada")
            self.preguntar()
