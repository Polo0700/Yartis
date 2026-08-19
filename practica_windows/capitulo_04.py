# ============================================================
# CAPITULO 04 — "La verdad visible" (dificultad: MEDIO)
# Tema: IsWindowVisible, filtrar ventanas invisibles
# ============================================================
#
#  LECTURA — Lee esto ANTES de escribir tu codigo.
#
# ------------------------------------------------------------
# 1. EL PROBLEMA: 204 ventanas, pero solo ves 10
# ------------------------------------------------------------
# En el capitulo 03 viste que hay 204 ventanas. Pero si miras
# tu pantalla ahora, solo ves: VS Code, el explorador, tal vez
# WhatsApp, el sistema de audio, alguna barra...
#
# Las demas ventanas son INVISIBLES:
#   - "Default IME" (sistema de entrada, oculto)
#   - "Battery Meter" (panel de control oculto)
#   - ventanas de fondo de cada app
#   - ventanas del explorer que no estas usando
#
# Tu funcion va a necesitar SABER QUE VES y QUE NO. Para eso
# existe una funcion que te dice la verdad: IsWindowVisible.
#
# ------------------------------------------------------------
# 2. ISWINDOWVISIBLE (firma)
# ------------------------------------------------------------
# IsWindowVisible responde: "esta ventana, se ve o no se ve?"
#
# Firma (en C):
#   BOOL IsWindowVisible(
#       HWND hWnd  <- de cual ventana quieres saber
#   );
#
# Devuelve: TRUE (1) si es visible, FALSE (0) si no.
# NO puede fallar. Si el hwnd es invalido, simplemente da FALSE.
#
# En Python con ctypes:
#   visible = user32.IsWindowVisible(hwnd)
#   if visible:
#       print("esta ventana se ve")
#
# Eso es TODO. No necesita buffer, no necesita byref, no necesita
# DWORD. Solo le pasas el hwnd y te dice 0 o 1.
#
# ------------------------------------------------------------
# 3. POR QUE ESTA ENMEDIO DE LA ESCALERA
# ------------------------------------------------------------
# No es facil porque es nuevo. Es facil tecnicamente.
# Es MEDIO porque cambia tu mentalidad:
#
#   Cap 01-03: "dame todo, yo veo"
#   Cap 04:    "dame solo lo que importa"
#
# Es la primera vez que FILTRAS. Y eso es exactamente lo que
# tu herramienta de archivos necesita (el param opcional que
# propusiste ayer).
#
# ------------------------------------------------------------
# 4. LA CONEXION CON TU HERRAMIENTA
# ------------------------------------------------------------
# IsWindowVisible = "filtrar ventanas por visibilidad"
# Parametro opcional = "filtrar archivos por nombre"
#
# Misma idea:
#   - Sin filtro: dame todo
#   - Con filtro: dame solo lo que cumple la condicion
#
# En ventanas: if IsWindowVisible(hwnd): es el filtro
# En archivos: if nombre not in excluir: es el filtro
#
# ------------------------------------------------------------
# 5. QUE YA SABES (y que usas)
# ------------------------------------------------------------
# Todo del capitulo 03:
#   - EnumWindows + callback
#   - GetWindowTextW + buffer
#   - GetWindowThreadProcessId + pid + psutil
#
# Solo agregas UNA linea nueva:
#   visible = user32.IsWindowVisible(hwnd)
#
# ============================================================
# TU RETO - ESCRIBE TU PROGRAMA
# ============================================================
#
# Crea un archivo nuevo: practica_windows/mi_capitulo_04.py
#
# Modifica TU script del capitulo 03 para que:
#   1. Enumere ventanas (EnumWindows + callback)
#   2. Lea el titulo (GetWindowTextW)
#   3. Lea el pid + app (GetWindowThreadProcessId + psutil)
#   4. NUEVO: Pregunte si es visible (IsWindowVisible)
#   5. SOLO imprima las que son visibles Y tienen titulo
#   6. Al final, cuente cuantas hay
#
# El resultado esperado es algo como:
#   hwnd=22868  app=Code.exe  titulo="capitulo_04.py - Yartis - Visual Studio Code"  [VISIBLE]
#   hwnd=8744   app=explorer.exe  titulo="Downloads - File Explorer"  [VISIBLE]
#   hwnd=20420  app=WhatsApp.Root.exe  titulo="WhatsApp"  [VISIBLE]
#   ...
#   Total visibles: 12 (de 204 totales)
#
# TRAMPA EN EL CAMINO: buffer.value puede tener titulo vacio ""
# para ventanas visibles (barras, widgets). Decide si las
# incluyes o las excluyes.
#
# NO mires soluciones en internet. Usa SOLO la documentacion de
# arriba + tus codigos anteriores.
#
# Ejecutalo:
#   .venv\Scripts\python.exe practica_windows/mi_capitulo_04.py
#
# Preguntas para despues de ejecutar:
#   - Cuantas ventanas visibles vs totales? (12 vs 204?)
#   - Reconoces todas las visibles? (VS Code, Brave, WhatsApp, Explorer)
#   - Hay alguna visible que NO reconozcas?

import ctypes
from ctypes import wintypes

import psutil

user32 = ctypes.windll.user32

ventanas = []
buffer = ctypes.create_unicode_buffer(512)
print(type(buffer))


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
