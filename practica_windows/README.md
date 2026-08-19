# Curso de Windows — Procesos y Ventanas

Campo de entrenamiento estilo **Rust Book**: primero aprendes a ESCRIBIR,
después aprendes a CAZAR bugs. Cada capítulo es una pieza de la función
final `obtener_ruta_absoluta_mediante_proceso`.

## Reglas del juego

1. Abre `capitulo_XX.py` (empieza por el 01)
2. Lee la  **documentacion** del capitulo (firmas, parametros, que devuelve)
3. Escribe TU programa desde cero en un archivo nuevo (NO copies codigo pegado)
4. Ejecutalo y mira el resultado real
5. Responde en el chat:
   - Que escribiste?
   - Que hizo?
   - Que aprendiste (anatomia: linea por linea)?
6. El planeador revisa la anatomia contigo y te pasa al siguiente capitulo

## Capitulos

| Nivel | # | Tema |
|-------|---|------|
| FACIL | 01 | Hello, Windows! — EnumWindows (hwnd, callback) |
| FACIL | 02 | El titulo es la puerta — GetWindowTextW |
| MEDIO | 03 | Conectando procesos y ventanas — GetWindowThreadProcessId |
| MEDIO | 04 | La verdad visible — IsWindowVisible |
| MEDIO-DIFICIL | 05 | Lo que miras ahora — GetForegroundWindow |
| DIFICIL | 06 | La ruta absoluta — Shell.Application (LocationURL) |
| DIFICIL | 07 | Tu obra maestra — obtener_ruta_absoluta_mediante_proceso |

## El metodo (igual que practica_bugs, pero para Windows)

-  **Lee** la documentacion de la API (firma, parametros, que devuelve)
-  **Escribe** tu codigo desde cero (aqui se aprende de verdad)
-  **Anatomia**: repasa con el planeador linea por linea
-  **Verifica** ejecutando con `.venv\Scripts\python.exe`
-  **Reto final**: los capitulos 01-07 te dan la funcion completa

## Nota

Usa SIEMPRE `.venv\Scripts\python.exe` desde la raiz del repo.
Ejecutar: `.venv\Scripts\python.exe practica_windows/mi_capitulo_01.py`
