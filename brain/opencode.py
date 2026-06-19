import json
import os
import subprocess
from core.transcriber import Transcribir
from .context import Registro
from .confirmacion import confirmador

CONFIG_PATH = os.path.expanduser("~/.config/opencode/opencode.jsonc")
PERFIL_YARTIS = {
    "skills": {
        "paths": [
            os.path.expanduser(
                "~/.config/opencode/profiles/categories/yartis-brain"
            ).replace("/", "\\")
        ]
    }
}
SISTEMA = """Eres Yartis, asistente de voz amigable. Respuestas cortas.

REGLAS DE SEGURIDAD:
- Leer archivos -> NO necesita confirmacion, hazlo directo
- Crear, modificar o eliminar archivos -> responde: 0x0x0Polo0700|tipo|explica que vas a hacer
  Donde tipo = crear, editar o eliminar
  Ejemplo: 0x0x0Polo0700|crear|Voy a crear un archivo de prueba
- Para eliminar -> USA LA PAPELERA DE RECICLAJE. No borres permanentemente.
- Cuando recibas "El usuario aprobo:" + la orden -> ejecutala sin preguntar

NO menciones perfiles, skills, configuracion, ni hables sobre ti mismo como agente."""


class peticion:
    def __init__(self):
        self.texto = ""
        self.historial = Registro()
        self.confirma = confirmador()
        self.output = ""
        self.primera_vez = True

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        config["skills"] = PERFIL_YARTIS["skills"]
        config["instructions"] = []
        config["$schema"] = config.get("$schema", "https://opencode.ai/config.json")
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def ejecutar(self, texto=""):
        if texto:
            self.texto = texto
        else:
            self.texto = Transcribir().transcripcion()

        if self.primera_vez:
            self.primera_vez = False
            prompt = (
                f"{SISTEMA} Historial: {self.historial.formato()} Usuario:{self.texto}"
            )
            cmd = ["opencode.cmd", "run", prompt]
        else:
            cmd = ["opencode.cmd", "run", "--continue", self.texto]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.output = result.stdout
        if "0x0x0Polo0700" in self.output:
            seccion = self.output.split("|", 2)
            respuesta = self.confirma.clasificar(seccion)
            if respuesta == 0:
                return
            if respuesta == 1:
                cmd = [
                    "opencode.cmd",
                    "run",
                    "--continue",
                    "usuario aprobo: " + self.texto,
                ]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                self.output = result.stdout
        self.historial.agregar(self.output, self.texto)
        return self.output
