import datetime

import tiktoken


class Registro:
    def __init__(self):
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.NUM = 0
        self.HISTORIAL_IA = []
        self.HISTORIAL_USUARIO = []
        self.TOKENS_MAX = 4096
        self.TOKENS_USADOS = []

    def agregar(self, RES_IA, RES_USUARIO):
        self.TOKENS_USADOS.append(
            len(self.enc.encode(RES_IA)) + len(self.enc.encode(RES_USUARIO))
        )

        self.NUM += len(self.enc.encode(RES_IA) + self.enc.encode(RES_USUARIO))
        while self.NUM >= self.TOKENS_MAX:
            if len(self.HISTORIAL_IA) <= 0 and len(self.HISTORIAL_USUARIO) <= 0:
                break
            self.NUM -= self.TOKENS_USADOS[0]
            ia = self.HISTORIAL_IA.pop(0)
            usuario = self.HISTORIAL_USUARIO.pop(0)
            self.TOKENS_USADOS.pop(0)
            resultado = self.formato(ia, usuario)
            with open("historial.txt", "a", encoding="utf-8") as f:
                f.write(" ")
                f.write(
                    f" --- Historial guardado automáticamente {datetime.datetime.now()}---\n"
                )
                f.write(resultado + "\n")
            ia = None
            usuario = None
        self.HISTORIAL_IA.append(RES_IA)
        self.HISTORIAL_USUARIO.append(RES_USUARIO)

    def formato(self, ia="", usuario=""):
        resultado = ""
        if ia and usuario:
            resultado = f"Usuario: {usuario}\nIA: {ia}\n"
            return resultado
        else:
            for i in range(len(self.HISTORIAL_USUARIO)):
                resultado += f"Usuario: {self.HISTORIAL_USUARIO[i]}\n"
                resultado += f"IA: {self.HISTORIAL_IA[i]}\n"
            return resultado

    def memoria(self):
        with open("historial_Temporal.txt", "w", encoding="utf-8") as f:
            f.write(self.formato())
