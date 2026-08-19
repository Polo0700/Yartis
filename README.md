#  Yartis — Asistente de Voz tipo JARVIS

Asistente conversacional activado por voz. Dice "YARTIS" y responde.

## Stack

| Capa | Tecnología |
|------|-----------|
|  Cerebro | OpenCode (LLM) + sentence-transformers (clasificador de intenciones) |
|  Wake word | openwakeword (modelo custom "yartis") |
|  STT | faster-whisper (GPU/CPU) |
|  TTS | Piper TTS (local, modelo español `es_Es-sharvard-medium`) |
|  Orquestador | Tauri (Rust) — WebSocket con Python |
|  UI | React + TypeScript + Vite |
|  Música | yt-dlp + sounddevice (reproduce de YouTube) |
|  Audio | noisereduce (reducción de ruido), sounddevice (grabación) |
|  Voz | speechbrain (reconocimiento/identificación de voz) |
|  NLP | spaCy (extracción de entidades), sentence-transformers (clasificación) |

## Pipeline

```
Wake word "Yartis" → Grabar audio → Reducción de ruido → Whisper (transcripción)
    → Clasificador de intenciones → OpenCode (LLM) → WebSocket → Tauri → React UI
    → Piper TTS → Reproducir respuesta
```

## Features

- **Wake word personalizado** — Detecta "Yartis" con openwakeword (modelo ONNX custom)
- **Clasificador de intenciones** — sentence-transformers para detectar: música, correo, calendario, telegram, navegador, control de reproducción
- **Reproducción de música** — Descarga y reproduce audio de YouTube con yt-dlp
- **Control de música** — Pausa, reanudar, siguiente, anterior, volumen (con NLP para entender "sube el volumen al 50")
- **Reducción de ruido** — Filtro de ruido ambiental en tiempo real
- **Identificación de voz** — Verifica que eres tú quien habla (speechbrain ECAPA-TDNN)
- **Confirmación de acciones** — Pregunta antes de ejecutar comandos destructivos (crear/eliminar/modificar archivos)
- **Memoria conversacional** — tiktoken para gestión de contexto (límite 4096 tokens)
- **UI reactiva** — Indicador de estado visual con animaciones
- **Modo CPU/GPU** — Flag `--cpu` para forzar CPU en Whisper/torch

## Comandos de voz soportados

| Intención | Ejemplos |
|-----------|----------|
|  Música | "pon música", "reproduce rock", "pon algo de jazz" |
| ⏸ Pausa | "pausa", "para la música", "silencio" |
| ▶ Reanudar | "reanuda", "continúa", "sigue" |
| ⏭ Siguiente | "siguiente canción", "salta esta", "adelante" |
| ⏮ Anterior | "canción anterior", "vuelve atrás", "regresa" |
|  Volumen | "sube el volumen", "volumen al 50", "más bajo" |
|  Correo | "envía un correo", "manda un email" |
|  Calendario | "qué eventos tengo", "agenda una reunión" |
|  Telegram | "manda un mensaje por telegram", "dile a Juan que..." |
|  Navegador | "abre el navegador", "busca en internet" |

## Estructura

```
yartis.py            → Entry point principal
core/                → Motor Python
  ├── audio.py       → Grabación de audio, reducción de ruido, detección de silencio
  ├── wake.py        → Detección de wake word "Yartis"
  ├── transcriber.py → Transcripción con faster-whisper
  ├── server.py      → Servidor WebSocket (asincrono)
  ├── config.py      → Configuración (rate, modelos, umbrales)
  └── models/        → Modelos ONNX (wake word, Piper TTS)
brain/               → Procesamiento inteligente
  ├── opencode.py    → Integración con OpenCode (LLM), manejo de comandos
  ├── clasificador.py→ Clasificador de intenciones (sentence-transformers)
  ├── context.py     → Memoria conversacional (tiktoken, historial)
  ├── confirmacion.py→ Sistema de confirmación antes de acciones destructivas
  └── voice_id.py    → Identificación de voz del usuario (speechbrain)
servicios/           → Servicios externos
  └── musica.py      → Reproducción de música desde YouTube (yt-dlp)
src/                 → Frontend React
  ├── App.tsx        → Componente principal
  ├── components/    → StatusIndicator, ChangeSize, Menu
  └── hooks/         → useAssistant (escucha eventos de Tauri)
src-tauri/           → Rust/Tauri
  └── src/lib.rs     → Orquestador, WebSocket cliente, lanzamiento de Python
assets/              → Recursos (sonidos, modelos, canciones)
tests/               → Pruebas
tools/               → Herramientas auxiliares
scripts/             → Scripts de automatización
```

## Requisitos

- Python 3.13+
- Node.js 18+
- Rust (para Tauri)
- GPU opcional (acelera Whisper y torch)
- uvicorn, websockets, fastapi

## Desarrollo

```bash
# Instalar dependencias Python
uv sync

# Instalar dependencias Node
npm install

# Frontend (solo UI)
npm run dev

# Tauri (app completa con Python backend)
cargo tauri dev

# Modo CPU (sin GPU)
python yartis.py --cpu
```

## Configuración

Los parámetros principales están en `core/config.py`:

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `WHISPER_MODEL` | `small` | Modelo de Whisper (tiny/base/small/medium/large) |
| `WHISPER_DEVICE` | `cpu` | Dispositivo (`cpu` o `cuda`) |
| `WAKE_THRESHOLD` | `0.3` | Sensibilidad del wake word (0-1) |
| `UMBRAL_SILENCIO` | `50` | Umbral para detectar silencio |
| `PASOS_SILENCIO_LIMITE` | `35` | Frames de silencio antes de cerrar mic |
| `DEBUG` | `True` | Mostrar scores de audio en consola |

## Racha

Ver [`RASTRECK.md`](RASTRECK.md) para el registro diario de código.
