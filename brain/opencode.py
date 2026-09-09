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
from core.herramientas_crud import Herramientas
from core.errores import obtener_error

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
SISTEMA = "INSTRUCCION: NO herramientas, NO ejecutar. Leer archivos hazlo directo. Si piden crear/modificar/eliminar/mover archivos o directorios responde SOLO con el formato: 0x0x0Polo0700|accion|tipo|ruta|datos|explicacion|respuesta_rapida La accion es crear, modificar, eliminar o mover. El tipo es archivo o directorio. La ruta es donde esta o va. Los datos para crear es el contenido del archivo, para eliminar van vacio, para modificar texto_viejo$$texto_nuevo separado por $$, para mover es la ruta_final. Si un campo no se necesita se escribe none. En explicacion escribe none. La respuesta_rapida es una frase corta que se dice en voz alta mientras se ejecuta la accion, ejemplos: va, lo estoy creando o un momento. Sigue SIEMPRE el formato completo con todos los campos separados por pipe y la respuesta_rapida al final. Para eliminar usa papelera de reciclaje. Leer archivos hazlo directo sin usar 0x0x0Polo0700. Respuestas cortas sin saludos. REGLA CRITICA: Responde SOLO en texto plano. NUNCA uses emojis, markdown, asteriscos, negritas, guiones decorativos, ni formato alguno. Tu respuesta sera leida en voz alta por un sintetizador de voz. Si pones un emoji el sintetizador lo dice en voz alta y suena horrible."


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
        self.accionador = Herramientas()
        self.handler = obtener_error

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
            if self.output.endswith("1"):
                verificacion = self.output.split("|")
                if len(verificacion) < 7:
                    bandera = "Error"
                    error = self.handler("E_FORMATO")
                    cmd = [
                        "opencode.cmd",
                        "run",
                        "--continue",
                        f"Error en formato. {error['mensaje']}, {error['solucion']}",
                    ]
                    result = await asyncio.to_thread(
                        subprocess.run,
                        cmd,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                    )
                    return bandera
                seccion = self.output.split("|", 6)
                utilidad_script = seccion
                seccion = [seccion[0], seccion[1], seccion[4]]
                respuesta = self.confirma.clasificar(seccion)
                if respuesta != 1:
                    return None
                if utilidad_script[1] == "crear":
                    if utilidad_script[2] == "directorio":
                        cmd = self.accionador.crear_directorio(
                            utilidad_script[3], utilidad_script[4]
                        )
                    if utilidad_script[2] == "archivo":
                        cmd = self.accionador.crear_archivo(
                            utilidad_script[3], utilidad_script[4]
                        )
                    res = [
                        "opencode.cmd",
                        "run",
                        "--continue",
                        f"{cmd}",
                    ]
                    await asyncio.to_thread(
                        subprocess.run,
                        res,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                    )
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
        if "0x0x0Polo0700" in self.output:
            return utilidad_script[6]
        return self.output
