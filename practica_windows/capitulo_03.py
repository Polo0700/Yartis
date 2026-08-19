# ============================================================
# CAPITULO 03 — "Conectando procesos y ventanas" (dificultad: MEDIO)
# Tema: GetWindowThreadProcessId, pid, psutil
# ============================================================
#
#  LECTURA — Lee esto ANTES de escribir tu codigo.
#
# ------------------------------------------------------------
# 1. EL PROBLEMA: el titulo no dice DE QUIEN es
# ------------------------------------------------------------
# En el capitulo 02 aprendiste a leer el titulo de cada ventana.
# Pero hay un problema: "Default IME" tiene titulo, "Battery Meter"
# tiene titulo... y ninguno es una app que el usuario use.
#
# Para saber DE QUE APP es una ventana, necesitas saber a que
# PROCESO pertenece. Un proceso = una app corriendo (VS Code,
# Brave, WhatsApp...). Y cada proceso tiene un pid.
#
# Recuerda del capitulo 01:
#   - hwnd identifica una VENTANA
#   - pid  identifica un PROCESO (una app)
#   - un proceso puede tener MUCHAS ventanas
#
# ------------------------------------------------------------
# 2. GETWINDOWTHREADPROCESID (firma)
# ------------------------------------------------------------
# GetWindowThreadProcessId responde: "esta ventana, de que
# proceso es?"
#
# Firma (en C):
#   DWORD GetWindowThreadProcessId(
#       HWND hWnd,            <- de cual ventana quieres saber
#       LPDWORD lpdwProcessId <- donde Windows va a ESCRIBIR el pid
#   );
#
# Devuelve: el THREAD id (id del hilo, no lo usaremos).
# El PID sale en el segundo argumento (lpdwProcessId).
#
# En Python con ctypes:
#   pid = wintypes.DWORD()                        <- caja vacia para el pid
#   user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
#   el_pid = pid.value                            <- leer el pid de la caja
#
# ------------------------------------------------------------
# 3. EL DETALLE RARO: "DONDE WINDOWS VA A ESCRIBIR"
# ------------------------------------------------------------
# Nota como GetWindowTextW usaba un BUFFER (la hoja de papel),
# y GetWindowThreadProcessId usa otra cosa: un DWORD.
#
# Un DWORD es un numero entero de 32 bits (como un int pequeno).
# Se crea como una "caja vacia":
#   pid = wintypes.DWORD()
#
# Y cuando Windows necesita ESCRIBIR en ella (poner el pid),
# se la pasas con ctypes.byref():
#   ctypes.byref(pid)   <- "mira, la caja esta AQUI, escribe ahi"
#
# Despues lees el contenido:
#   pid.value           <- el pid que Windows escribio
#
# (byref = "by reference" = "por referencia" = le pasas la
#  DIRECCION de la caja, no una copia. Es la forma de decirle
#  a Windows "escribe aqui, yo espero.")
#
# ------------------------------------------------------------
# 4. PSUTIL: DE pid A NOMBRE DE APP
# ------------------------------------------------------------
# Un pid solo es un numero (ej: 22868). Para saber el NOMBRE
# de la app (ej: "Code.exe") usamos psutil, una libreria de
# Python que ya usas en tu proyecto.
#
#   import psutil
#   proceso = psutil.Process(pid)
#   proceso.name()     <- "Code.exe"
#   proceso.exe()      <- ruta completa del ejecutable
#
# OJO: psutil.Process(pid) puede lanzar una excepcion si el
# proceso ya murio entre que lo viste y lo consultas.
# (Eso pasa seguido en Windows: procesos que nacen y mueren.)
#
# ------------------------------------------------------------
# 5. LAS PIEZAS NUEVAS QUE NECESITAS
# ------------------------------------------------------------
#   pid = wintypes.DWORD()
#   user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
#   nombre = psutil.Process(pid.value).name()   # ojo: puede fallar
#
# ============================================================
# TU RETO - ESCRIBE TU PROGRAMA
# ============================================================
#
# Crea un archivo nuevo:  practica_windows/mi_capitulo_03.py
#
# Modifica TU script del capitulo 02 para que, ademas del hwnd
# y el titulo, imprima el NOMBRE DE LA APP de cada ventana.
#
# Escribe un script que:
#   1. Enumere las ventanas (tu codigo del cap 01)
#   2. Lea el titulo (tu codigo del cap 02)
#   3. Lea el pid con GetWindowThreadProcessId
#   4. Convierta el pid a nombre de app con psutil
#   5. Imprima algo como:
#        hwnd=123456  pid=22868  app=Code.exe  titulo="VS Code"
#   6. Al final, cuente cuantas ventanas hay
#
# TRAMPA EN EL CAMINO: psutil.Process(pid).name() puede fallar
# para procesos que murieron. Piensa como protegerte.
# (Pista: recuerda la leccion del try/except de hoy...)
#
# NO mires soluciones en internet. Usa SOLO la documentacion de
# arriba + tus codigos anteriores.
#
# Cuando lo tengas, ejecutalo:
#   .venv\Scripts\python.exe practica_windows/mi_capitulo_03.py
#
# Preguntas para despues de ejecutar:
#   - Que apps reconoces por su nombre? (Code.exe, Brave.exe...)
#   - Cuantas "Default IME" tienen nombre de app raro?
#   - Cuales apps abiertas tienes AHORA (VS Code, Brave, WhatsApp)?

import ctypes
from ctypes import wintypes

import psutil

user32 = ctypes.windll.user32

ventanas = []
buffer = ctypes.create_unicode_buffer(512)
print(type(buffer))


@ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def callback(hwnd, lparam):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        pid_f = psutil.Process(pid.value).name()
        print(pid_f)
    except Exception as e:
        print(f"Error {e}")
    user32.GetWindowTextW(hwnd, buffer, 512)
    titulo = buffer.value
    print(titulo)
    print(hwnd)
    print(" ")
    ventanas.append(hwnd)
    return True


user32.EnumWindows(callback, 0)
print(len(ventanas))
