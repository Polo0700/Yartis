# Yartis — Asistente de Voz tipo JARVIS

Asistente conversacional con wake word "YARTIS". Pipeline: wake word → grabación → FFT + noise reduction → Whisper (GPU) → OpenCode → Tauri → React → speechSynthesis.

## Stack
| Capa | Tecnología |
|------|-----------|
| Gestión | uv + pyproject.toml |
| Wake word | openwakeword (modelo custom) |
| Noise reduction | noisereduce (spectral gating / FFT) |
| STT | faster-whisper `small` (GPU) |
| Cerebro | OpenCode |
| TTS | Web Speech API (React WebView) |
| Orquestador | Tauri (Rust) — lanza/maneja Python |
| UI | React (dentro de WebView de Tauri) |

## Pipeline
1. Tauri lanza Python (sidecar)
2. Python: wake word → graba → noise reduction → Whisper → OpenCode
3. Python envía respuesta a Tauri (WebSocket)
4. Tauri reenvía al WebView React
5. React: efectos visuales + speechSynthesis.speak()
6. Loop

## Ecosistema de Agentes
| Agente | Rol |
|--------|-----|
| `python-expert` | **Default** — audio, wake word, whisper, opencode |
| `rust-expert` | Rust/Tauri: sidecar, WS, comandos |
| `html-expert` | HTML5 + CSS semántico, accesibilidad, layouts |
| `typescript-expert` | TypeScript + React: componentes, hooks, tipos |

### Delegar tareas
```python
task(subagent_type="general", description="...", prompt="...")
```
O derivar con `@python-expert`, `@rust-expert`, etc.

## Estructura (resumen)
- `core/` — Motor audio (audio.py, wake.py, transcriber.py, config.py, src-tauri/)
- `brain/` — Procesamiento (opencode.py, context.py)
- `src/` — Frontend React (App.tsx, components/, hooks/, types/)
- `tests/` — Pruebas (test_context.py, test_server.py, test_wake.py)
- Raíz: `yartis.py`, `pyproject.toml`, `package.json`
