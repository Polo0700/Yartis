# ============================================================
# CAPITULO 01 — "Hello, Windows!" (dificultad: FACIL)
# Tema: EnumWindows, hwnd, callback
# ============================================================
#
#  LECTURA — Lee esto ANTES de escribir tu codigo.
#
# ------------------------------------------------------------
# 1. QUE ES UNA VENTANA EN WINDOWS?
# ------------------------------------------------------------
# Una ventana es TODO lo que ves en pantalla: una app abierta,
# un cuadro de dialogo, un boton, una barra de titulo... cada
# elemento de la interfaz es tecnicamente "una ventana".
#
# Windows es un sistema OPERADO POR VENTANAS (de ahi el nombre).
# Cada ventana pertenece a UN proceso (la app que la creo).
#
# ------------------------------------------------------------
# 2. QUE ES UN hwnd?
# ------------------------------------------------------------
# hwnd = "handle to a window" = "numero identificador de ventana".
#
# Es un NUMERO ENTERO que Windows usa para referirse a una ventana
# concreta. Como un DNI: cada ventana tiene uno unico mientras vive.
#
# Cuando le pides algo a Windows ("dame el titulo de esa ventana"),
# tu le pasas el hwnd y el sabe a cual te refieres.
#
# Un pid identifica un PROCESO (una app corriendo).
# Un hwnd identifica una VENTANA (una pieza de la interfaz).
# Un proceso puede tener MUCHAS ventanas (y cada ventana muchas
# pestañas — pero eso viene en capitulos mas avanzados).
#
# ------------------------------------------------------------
# 3. QUE ES EnumWindows? (firma)
# ------------------------------------------------------------
# EnumWindows es una funcion de la API de Windows (user32.dll)
# que lista TODAS las ventanas del sistema.
#
# Firma (en C):
#   BOOL EnumWindows(
#       WNDENUMPROC lpEnumFunc,   <- puntero a tu callback
#       LPARAM lParam             <- dato extra que quieras pasar
#   );
#
# En Python con ctypes:
#   user32.EnumWindows(callback, 0)
#
# ------------------------------------------------------------
# 4. QUE ES EL CALLBACK? (la parte rara)
# ------------------------------------------------------------
# EnumWindows NO te devuelve una lista directamente. En su lugar,
# tu le das una FUNCION TUYA (callback), y Windows la llama una vez
# por cada ventana que encuentre.
#
# Ejemplo de la vida real: es como pedirle a un conserje que te
# muestre los departamentos del edificio. En vez de traerte una
# lista escrita en papel, el conserje te LLAMA POR CADA departamento:
#   - "Dep 1" (te llama)
#   - "Dep 2" (te llama)
#   - "Dep 3" (te llama)
#   ...hasta que termina.
#
# Tu callback se ejecuta UNA VEZ POR VENTANA. Windows te pasa
# el hwnd de cada ventana, y TU decides que hacer con el.
#
# Tu callback debe devolver True (seguir enumerando) o False
# (detenerse). Si devuelves True siempre, recorres todas.
#
# Firma del callback (en C):
#   BOOL CALLBACK EnumWindowsProc(
#       HWND hwnd,     <- el identificador de la ventana actual
#       LPARAM lParam  <- el dato extra que le pasaste a EnumWindows
#   );
#
# En Python con ctypes, el callback se declara asi:
#   @ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
#   def mi_callback(hwnd, lparam):
#       ...
#       return True
#
# ------------------------------------------------------------
# 5. LAS 3 PIEZAS DE ctypes QUE NECESITAS
# ------------------------------------------------------------
#   import ctypes
#   from ctypes import wintypes
#   user32 = ctypes.windll.user32
#
#   - ctypes.windll.user32  -> la puerta a las funciones de Windows
#   - wintypes.HWND         -> el tipo "identificador de ventana"
#   - wintypes.BOOL         -> el tipo "verdadero/falso"
#
# Nota: user32 es el modulo de Windows que maneja VENTANAS.
# (Existe tambien kernel32, que maneja procesos/memoria — lo veras
# en capitulos futuros cuando toquemos el pid.)
#
# ============================================================
# TU RETO - ESCRIBE TU PROGRAMA
# ============================================================
#
# Crea un archivo nuevo:  practica_windows/mi_capitulo_01.py
#
# Escribe un script que:
#   1. Importe ctypes y wintypes
#   2. Abra user32
#   3. Defina un callback que reciba (hwnd, lparam) y que por cada
#      ventana simplemente imprima el hwnd
#   4. Llame a EnumWindows con tu callback
#   5. Al final, imprima cuantas ventanas encontro
#
# NO mires soluciones en internet. Usa SOLO la documentacion de
# arriba. La idea es que escribas el codigo TU, no que lo copies.
#
# Cuando lo tengas, ejecutalo:
#   .venv\Scripts\python.exe practica_windows/mi_capitulo_01.py
#
# Preguntas para despues de ejecutar:
#   - Cuantas ventanas salieron?
#   - Los numeros son grandes o pequenos?
#   - Reconoces alguna de las ventanas que vimos en la demo?
#     (VS Code, Brave, Settings, el explorador...)

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

ventanas = []


@ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def callback(hwnd, lparam):
    print(hwnd)
    ventanas.append(hwnd)
    return True


user32.EnumWindows(callback, 0)
print(len(ventanas))
