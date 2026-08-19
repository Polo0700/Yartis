import asyncio
import json
import os
import subprocess
from core.transcriber import Transcribir
from .context import Registro
from .confirmacion import confirmador
import pyttsx3
from .clasificador import Clasificador
from servicios.musica import music
import ntplib
import datetime
import spacy

nlp = spacy.load("es_core_news_sm")
# instancia compartida de música (singleton)
reproductor = music()

FRASES_VOLUMEN = {
    "mitad": 50,
    "moderado": 50,
    "normal": 50,
    "bajo": 20,
    "suave": 20,
    "tranquilo": 20,
    "alto": 80,
    "fuerte": 80,
    "máximo": 100,
    "completo": 100,
    "tope": 100,
    "mínimo": 0,
    "cero": 0,
    "silencio": 0,
}

PALABRAS_A_NUMEROS = {
    "cero": 0,
    "un": 1,
    "una": 1,
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    "dieciseis": 16,
    "diecisiete": 17,
    "dieciocho": 18,
    "diecinueve": 19,
    "veinte": 20,
    "veintiuno": 21,
    "veintidos": 22,
    "veintitres": 23,
    "veinticuatro": 24,
    "veinticinco": 25,
    "veintiseis": 26,
    "veintisiete": 27,
    "veintiocho": 28,
    "veintinueve": 29,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100,
}


def texto_a_numero(texto):
    """Convierte 'treinta y cinco' → 35"""
    texto = texto.strip().lower()
    if texto in PALABRAS_A_NUMEROS:
        return PALABRAS_A_NUMEROS[texto]
    if " y " in texto:
        partes = texto.split(" y ")
        if partes[0] in PALABRAS_A_NUMEROS and partes[1] in PALABRAS_A_NUMEROS:
            return PALABRAS_A_NUMEROS[partes[0]] + PALABRAS_A_NUMEROS[partes[1]]
    return None


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
SISTEMA = "INSTRUCCION: NO herramientas, NO ejecutar. Leer archivos hazlo directo.  Si piden crear/modificar/eliminar/mover archivos responde SOLO: 0x0x0Polo0700|crear|ruta|contenido|explicacion| 0x0x0Polo0700|eliminar|ruta|explicacion 0x0x0Polo0700|modificar|ruta|texto_viejo$$texto_nuevo|explicacion Para eliminar contenido va vacio. Para modificar texto_viejo$$texto_nuevo separado por $$. 0x0x0Polo0700|Mover|Ruta_inicial|Ruta_Final. Leer archivos hazlo directo. Para eliminar papelera reciclaje. Respuestas cortas sin saludos. si hay alguna informacion innecesaria para la peticion solo responde en su lugar por seccion como un ' ' estilo 0x0x0Polo0700|crear|D://users|es un ejemplo|' '|' ' REGLA CRITICA: Responde SOLO en texto plano. NUNCA uses emojis, markdown, asteriscos, negritas, guiones decorativos, ni formato alguno. Tu respuesta sera leida en voz alta por un sintetizador de voz. Si pones un emoji el sintetizador lo dice en voz alta y suena horrible."


class peticion:
    def __init__(self):
        self.texto = ""
        self.historial = Registro()
        self.confirma = confirmador()
        self.output = ""
        self.primera_vez = True
        self.division = ""
        self.res = ""
        self.lec = pyttsx3.init()
        self.tts = Transcribir()
        self.clasificacion = Clasificador()

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        config["skills"] = PERFIL_YARTIS["skills"]
        config["instructions"] = [
            "Eres asistente de voz. NO menciones perfiles. Respuestas cortas."
        ]
        config["$schema"] = config.get("$schema", "https://opencode.ai/config.json")
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    async def ejecutar(self, texto=""):
        if texto:
            self.texto = texto
        else:
            self.texto = self.tts.transcripcion()
        if not self.texto:
            return
        intencion, _ = self.clasificacion.clasificar(self.texto)
        if intencion != "NO_RECONOCIDO":
            if intencion == "MUSICA":
                reproductor.play(self.texto)
                return "Entendido, reproduciendo música"
            if intencion == "PAUSA":
                reproductor.pause()
                return "Entendido, música pausada"
            if intencion == "REANUDAR":
                reproductor.resume()
                return "Entendido, reanudando música"
            if intencion == "SIGUIENTE":
                reproductor.next()
                return "Entendido, siguiente canción"
            if intencion == "ANTERIOR":
                reproductor.previously()
                return "Entendido, canción anterior"
            if intencion == "VOLUMEN":
                doc = nlp(self.texto)
                for token in doc.ents:
                    if token.label_ == "CARDINAL":
                        valor = texto_a_numero(token.text)
                        reproductor.volumen(valor / 100)
                return "Entendido, ajusté el volumen"
            if intencion == "HORA":
                try:
                    cliente = ntplib.NTPClient()
                    respuesta = cliente.request("pool.ntp.org", timeout=3)
                    hora_local = datetime.datetime.fromtimestamp(respuesta.tx_time)
                except Exception:
                    hora_local = datetime.datetime.now()
                return f"Son las {hora_local.strftime('%H:%M')}"
        if self.primera_vez:
            self.primera_vez = False
            prompt = f"{SISTEMA} --- Usuario:{self.texto}"
            cmd = ["opencode.cmd", "run", prompt]
        else:
            cmd = ["opencode.cmd", "run", "--continue", self.texto]
        result = await asyncio.to_thread(
            subprocess.run,
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.output = result.stdout
        if "0x0x0Polo0700" in self.output:
            seccion = self.output.split("|", 5)
            utilidad_script = seccion
            seccion = [seccion[0], seccion[1], seccion[4]]
            respuesta = self.confirma.clasificar(seccion)
            if respuesta != 1:
                return None
            if utilidad_script[1] == "crear":
                if utilidad_script[2] == "directorio":
                    cmd = [
                        "mkdir",
                        f"{utilidad_script[1]}",
                        f"{utilidad_script[2]}",
                    ]
                if utilidad_script[2] == "archivo":
                    cmd = ["comando de crear archivo que no se xD"]
                    await asyncio.to_thread(subprocess.run, cmd)
            elif utilidad_script[1] == "eliminar":
                cmd = ["mv", f"{utilidad_script[2]}", "papelera"]
                await asyncio.to_thread(subprocess.run, cmd)
            elif utilidad_script[1] == "modificar":
                if utilidad_script[2] == "directorio":
                    cmd = ["mkdir", f"{seccion[1]}", f"{seccion[2]}"]
                if utilidad_script[2] == "archivo":
                    if utilidad_script[3] == "nombre":
                        cmd = ["comando para cambiar nombre de archivo"]
                    elif utilidad_script[3] == "contenido":
                        cmd = ["comando de recrear el archivo que no se xD"]
                        await asyncio.to_thread(subprocess.run, cmd)
            elif utilidad_script[1] == "mover":
                cmd = ["mv", f"{utilidad_script[2]}", f"{utilidad_script[6]}"]
                await asyncio.to_thread(subprocess.run, cmd)
        if "1x1x1Polo0700" in self.output:
            preguntas = []
            result = self.output.split("|")
            total_preguntas = int(result[-1])
            while len(preguntas) != total_preguntas:
                resultres = self.output.split("|")
                resultres.pop(-1)
                resultres.pop(0)
                for pregunta in resultres:
                    self.lec.say(pregunta)
                    dato = self.tts.transcripcion()
                    if not dato:
                        continue
                    preguntas.append(dato)

            cmd = [
                "opencode.cmd",
                "run",
                "--continue",
                "Respuestas del usuario: " + str(preguntas),
            ]
            result = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            preguntas = []
        self.historial.agregar(self.output, self.texto)
        return self.output
