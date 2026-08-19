# ============================================================
# CAPITULO 05 — "Lo que miras ahora" (dificultad: FACIL)
# Tema: GetForegroundWindow, la ventana activa
# ============================================================
#
#  LECTURA — Lee esto ANTES de escribir tu codigo.
#
# ------------------------------------------------------------
# 1. EL PROBLEMA: de todas las visibles, cual esta activa?
# ------------------------------------------------------------
# En C04 aprendiste a filtrar ventanas visibles. Pero incluso
# entre las visibles, SOLO UNA esta activa: la que tiene el
# foco del teclado, la que el usuario esta usando AHORA MISMO.
#
# Ejemplo: tienes VS Code, Brave y WhatsApp visibles. Pero
# el foco esta en VS Code (porque escribes codigo). Las otras
# dos estan "detras".
#
# ------------------------------------------------------------
# 2. GETFOREGROUNDWINDOW (firma)
# ------------------------------------------------------------
# GetForegroundWindow responde: "cual ventana tiene el foco?"
#
# Firma (en C):
#   HWND GetForegroundWindow(
#       VOID  <- no necesita ningun parametro
#   );
#
# Devuelve: el hwnd de la ventana que tiene el foco.
# Si no hay ventana activa, devuelve NULL (0).
#
# En Python con ctypes:
#   hwnd = user32.GetForegroundWindow()
#
# Eso es TODO. Sin parametros. Sin buffer. Sin byref.
# Solo llamas y te devuelve el hwnd.
#
# ------------------------------------------------------------
# 3. COMBINARLO CON LO QUE YA SABES
# ------------------------------------------------------------
# El hwnd solo no te dice nada. Pero puedes pasarlo por la
# misma cadena que ya dominas:
#
#   hwnd = user32.GetForegroundWindow()          <- cual es
#   user32.GetWindowTextW(hwnd, buffer, 512)     <- su titulo
#   user32.GetWindowThreadProcessId(hwnd, ...)   <- su pid
#   psutil.Process(pid).name()                   <- su app
#
# Resultado: sabes QUE app el usuario esta usando AHORA.
#
# ------------------------------------------------------------
# 4. POR QUE ES FACIL
# ------------------------------------------------------------
# No es nuevo tecnicamente — es una sola linea. Es facil porque:
#   - No necesita buffer
#   - No necesita byref
#   - No puede fallar (devuelve NULL si no hay)
#   - Ya sabes leer titulo, pid y app
#
# Lo unico nuevo es la idea: "del universo de ventanas,
# dame la una que importa".
#
# ============================================================
# TU RETO - ESCRIBE TU PROGRAMA
# ============================================================
#
# Crea un archivo nuevo: practica_windows/mi_capitulo_05.py
#
# Escribe un script que:
#   1. Obtenga la ventana activa (GetForegroundWindow)
#   2. Lea su titulo (GetWindowTextW)
#   3. Lea su pid + app (GetWindowThreadProcessId + psutil)
#   4. Imprima algo como:
#        ACTIVA: Code.exe - "capitulo_05.py - Yartis - Visual Studio Code"
#
# TRAMPA EN EL CAMINO: si el foco esta en tu terminal (la
# ventana donde ejecutas el script), vas a ver la terminal,
# no VS Code. Cambia a VS Code y ejecuta de nuevo.
#
# NO mires soluciones en internet. Usa SOLO la documentacion.
#
# Ejecutalo:
#   .venv\Scripts\python.exe practica_windows/mi_capitulo_05.py
#
# Preguntas para despues:
#   - Que app aparece como activa?
#   - Cambia el resultado si haces click en otra ventana y ejecutas de nuevo?
#   - Que pasa si ejecutas el script desde VS Code vs desde la terminal?

import ctypes
from ctypes import wintypes

import psutil

user32 = ctypes.windll.user32

ventanas = []
buffer = ctypes.create_unicode_buffer(512)
print(type(buffer))
bufferFuera = ctypes.create_unicode_buffer(512)

hwnd = user32.GetForegroundWindow()
pid = wintypes.DWORD()
user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
user32.GetWindowTextW(hwnd, bufferFuera, 512)
titulo = bufferFuera.value


@ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def callback(hwnd, lparam):
    visible = user32.IsWindowVisible(hwnd)
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        pid_f = psutil.Process(pid.value).name()
        print(pid_f)
    except Exception as e:
        print(f"Error {e}")
    user32.GetWindowTextW(hwnd, buffer, 512)
    titulo = buffer.value
    if not visible:
        print(" ")
    elif titulo:
        print(titulo)
        print(hwnd)
        print(" ")
        ventanas.append(hwnd)
        print(len(ventanas))
    else:
        print(" ")
    return True


user32.EnumWindows(callback, 0)
print(len(ventanas))
print(titulo)
