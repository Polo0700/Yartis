import subprocess
from core.transcriber import Transcribir
from .context import Registro


class peticion:
    def __init__(self):
        self.texto = ""
        self.historial = Registro()
        self.output = ""

    def ejecutar(self, texto=""):
        self.texto = texto
        self.texto = Transcribir().transcripcion()
        prompt = f"Historial: {self.historial.formato()} Nuevo mensaje:{self.texto}"
        print(self.texto)
        self.output = subprocess.run(
            ["opencode.cmd", "run", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.output = self.output.stdout
        self.historial.agregar(self.output, self.texto)
        return self.output
