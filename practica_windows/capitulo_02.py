# ============================================================
# CAPITULO 02 — "El titulo es la puerta" (dificultad: FACIL)
# Tema: GetWindowTextW, buffer, Unicode
# ============================================================
#
#  LECTURA — Lee esto ANTES de escribir tu codigo.
#
# ------------------------------------------------------------
# 1. EL PROBLEMA: un hwnd no dice nada
# ------------------------------------------------------------
# En el capitulo 01 aprendiste a enumerar ventanas, pero solo
# viste NUMEROS (el hwnd). Un numero como 123456 no te dice
# si es VS Code, Brave o el explorador.
#
# Para saber QUE ventana es, necesitas su TITULO. Y Windows
# tiene una funcion para eso: GetWindowTextW.
#
# ------------------------------------------------------------
# 2. GETWINDOWTEXTW (firma)
# ------------------------------------------------------------
# GetWindowTextW copia el titulo de una ventana a un BUFFER
# (un espacio de memoria donde Windows puede escribir texto).
#
# Firma (en C):
#   int GetWindowTextW(
#       HWND hWnd,          <- de cual ventana quieres el titulo
#       LPWSTR lpString,    <- donde Windows va a escribir el titulo
#       int nMaxCount       <- cuantas letras caben como maximo
#   );
#
# Devuelve: cuantas letras realmente escribio (0 si no hay titulo).
#
# En Python con ctypes:
#   user32.GetWindowTextW(hwnd, buffer, capacidad)
#
# ------------------------------------------------------------
# 3. EL DETALLE RARO: EL BUFFER
# ------------------------------------------------------------
# "Buffer" suena tecnico pero es simple: es como una HOJA DE
# PAPEL en blanco. Le dices a Windows: "escribe el titulo de
# esta ventana AQUI, en esta hoja. Te caben hasta N letras."
#
# En Python se crea con ctypes:
#   buffer = ctypes.create_unicode_buffer(capacidad)
#
#   - create_unicode_buffer  -> crea una "hoja" para texto Unicode
#   - capacidad              -> cuantas letras caben (ej: 512)
#
# Despues de llamar a GetWindowTextW, el titulo queda dentro
# de buffer. Para leerlo:  buffer.value
#
# (Si te preguntas de donde sale el numero de letras que caben:
#  no lo sabes ANTES — por eso eliges un tamaño generoso como
#  512. En el capitulo 06 veras la manera de preguntarle primero
#  a Windows cuanto mide el titulo, pero por ahora 512 basta.)
#
# ------------------------------------------------------------
# 4. LA "W" AL FINAL — UNICODE
# ------------------------------------------------------------
# Hay dos versiones de casi toda funcion de texto en Windows:
#   - GetWindowTextA  (A = ANSI, texto simple, espanol puede fallar)
#   - GetWindowTextW  (W = Wide, Unicode, soporta TODOS los idiomas)
#
# Siempre usa la W. Tu app va a manejar titulos en espanol,
# emojis, simbolos... la W los entiende todos.
#
# ------------------------------------------------------------
# 5. LAS PIEZAS NUEVAS DE ctypes QUE NECESITAS
# ------------------------------------------------------------
#   buffer = ctypes.create_unicode_buffer(512)   <- la hoja de papel
#   user32.GetWindowTextW(hwnd, buffer, 512)     <- Windows escribe
#   titulo = buffer.value                        <- lees lo escrito
#
# Nota: en este capitulo NO necesitas declarar tipos del callback
# (ya lo hiciste en el 01). Solo agregas la lectura del titulo
# DENTRO de tu callback de siempre.
#
# ============================================================
# TU RETO - ESCRIBE TU PROGRAMA
# ============================================================
#
# Crea un archivo nuevo:  practica_windows/mi_capitulo_02.py
#
# Modifica TU script del capitulo 01 (EnumWindows + callback)
# para que ahora, ademas de imprimir el hwnd, imprima el TITULO
# de cada ventana. Al final, sigue contando cuantas ventanas hay.
#
# Escribe un script que:
#   1. Enumere las ventanas (tu codigo del cap 01)
#   2. Dentro del callback, lea el titulo con GetWindowTextW
#   3. Imprima algo como:  hwnd=123456  titulo="VS Code"
#   4. Al final, imprima cuantas ventanas encontro
#
# NO mires soluciones en internet. Usa SOLO la documentacion de
# arriba + tu codigo del capitulo 01.
#
# Cuando lo tengas, ejecutalo:
#   .venv\Scripts\python.exe practica_windows/mi_capitulo_02.py
#
# Preguntas para despues de ejecutar:
#   - Cuantas ventanas tienen TITULO y cuantas titulo vacio?
#   - Ves las ventanas de la demo (VS Code, Brave, Settings)?
#   - Por que crees que muchas ventanas tienen titulo vacio?
#     (Pista: piensa en el 204 del capitulo 01...)

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

ventanas = []
buffer = ctypes.create_unicode_buffer(512)
print(type(buffer))


@ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def callback(hwnd, lparam):
    user32.GetWindowTextW(hwnd, buffer, 512)
    titulo = buffer.value
    print(titulo)
    print(hwnd)
    ventanas.append(hwnd)
    return True


user32.EnumWindows(callback, 0)
print(len(ventanas))
