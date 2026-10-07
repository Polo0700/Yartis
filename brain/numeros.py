default = 10


def calculadorNumtoString(dato, limite=None):
    if limite == None:
        limite = default
    dato = str(dato)
    for i in range(0, limite, 1):
        valor = str(i)
        if valor == dato:
            return valor
