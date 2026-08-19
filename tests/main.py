import os

# CUDA deshabilitado temporalmente (incompatible con drivers 13.0)
# Cuando tengas CUDA funcionando, borra o comenta esta línea:
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from brain.opencode import peticion


class main:
    def __init__(self):
        self.texto = ""
        self.output = ""

    def main(self):
        self.output = peticion().ejecutar(self.texto)
        print(self.output)


if __name__ == "__main__":
    app = main()
    app.main()
