# Yartis — Asistente de Voz tipo JARVIS

## Descripción del proyecto
Asistente de voz conversacional tipo JARVIS con wake word "YARTIS". Pipeline: wake word → grabación → FFT + noise reduction → Whisper (GPU) → OpenCode → Tauri → React → speechSynthesis.

## Stack

| Capa | Tecnología |
|------|-----------|
| Gestión | uv + pyproject.toml |
| Wake word | openwakeword (modelo custom "YARTIS") |
| Noise reduction | noisereduce (spectral gating / FFT) |
| STT | faster-whisper `small` (GPU) |
| Cerebro | OpenCode |
| TTS | Web Speech API (React WebView) |
| Orquestador | Tauri (Rust) — lanza/maneja Python |
| UI | React (dentro de WebView de Tauri) |

## Estructura del proyecto

```
Yartis/
├── core/                  # Motor base de audio
│   ├── audio.py           # FFT + noise reduction + grabación
│   ├── wake.py            # openwakeword (modelo custom)
│   ├── transcriber.py     # faster-whisper wrapper
│   └── config.py          # Config centralizada
├── brain/                 # Procesamiento inteligente
│   ├── opencode.py        # Bridge con OpenCode
│   └── context.py         # Memoria de conversación (FIFO 4096 tokens)
├── skills/                # Plugins expandibles
├── yartis.py              # Pipeline Python (sidecar de Tauri)
├── pyproject.toml         # Dependencias y metadata
├── .venv/                 # Entorno virtual (uv)
├── tests/                 # Pruebas unitarias
│   ├── test_context.py
│   ├── test_server.py
│   └── test_wake.py
```

## Pipeline completo

```
┌─────────────────────────────────────────────────┐
│  TAURI (Rust) — Orquestador                     │
│  ┌──────────┐   ┌──────────────┐   ┌─────────┐  │
│  │ Python   │   │ Tauri (Rust) │   │ React   │  │
│  │ sidecar  │──▶│ orquesta     │──▶│ WebView │  │
│  │          │   │ y recibe     │   │ efectos │  │
│  │ 1. wake  │   │ respuesta    │   │ + TTS   │  │
│  │ 2. grab  │   │              │   │         │  │
│  │ 3. whis  │   │              │   │         │  │
│  │ 4. open  │   │              │   │         │  │
│  └──────────┘   └──────────────┘   └─────────┘  │
└─────────────────────────────────────────────────┘

Pasos:
1. Tauri lanza Python (sidecar)
2. Python: wake word → graba → noise reduction → Whisper → OpenCode
3. Python envía respuesta a Tauri (WebSocket)
4. Tauri recibe y reenvía al WebView React
5. React pone efectos visuales + speechSynthesis.speak()
6. Loop
```

## Flujo de trabajo

1. El usuario activa con wake word "YARTIS"
2. Python graba audio hasta detectar silencio
3. Whisper transcribe a texto
4. OpenCode procesa la solicitud
5. La respuesta viaja por WebSocket a Rust
6. Rust emite el texto a React
7. React muestra y sintetiza la voz

## Comandos útiles

```powershell
# Ejecutar con uv
uv run python yartis.py

# Agregar dependencia
uv add <paquete>

# Sincronizar
uv sync

# Ejecutar pruebas
uv run pytest tests/ -v
```
