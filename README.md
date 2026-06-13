# 🎙️ Yartis — Asistente de Voz tipo JARVIS

Asistente conversacional activado por voz con wake word "YARTIS".

## Stack

| Capa | Tecnología |
|------|-----------|
| 🧠 Cerebro | OpenCode |
| 🎤 Wake word | openwakeword |
| 🔊 STT | faster-whisper (GPU) |
| 🦀 Orquestador | Tauri (Rust) |
| ⚛️ UI | React + TypeScript + Vite |
| 🗣️ TTS | Web Speech API |

## Pipeline

```
Wake word → Grabar → Reducción de ruido → Whisper → OpenCode → Tauri → React → TTS
```

## Rama activa

La funcionalidad actual está en `feature/sala-pruebas`. Main es la base estable.

## Licencia

MIT
