# 🎙️ Yartis — Asistente de Voz tipo JARVIS

Asistente conversacional activado por voz. Dice "YARTIS" y responde.

## Stack

| Capa | Tecnología |
|------|-----------|
| 🧠 Cerebro | OpenCode |
| 🎤 Wake word | openwakeword (modelo custom) |
| 🔊 STT | faster-whisper (GPU) |
| 🦀 Orquestador | Tauri (Rust) — WebSocket con Python |
| ⚛️ UI | React + TypeScript + Vite |
| 🗣️ TTS | Web Speech API (React WebView) |

## Pipeline

```
Wake word → Grabar → Reducción de ruido → Whisper → OpenCode → Tauri → React → TTS
```

## Estructura

```
core/           → Motor Python (audio, wake, transcripción, servidor WS)
brain/          → Procesamiento (OpenCode, contexto, memoria)
src/            → Frontend React (componentes, hooks)
src-tauri/      → Rust/Tauri (WebSocket cliente, comandos)
src/hooks/      → Hooks personalizados (useAssistant)
src/components/ → Componentes UI (StatusIndicator, ChatBubble, etc.)
```

## Desarrollo

```bash
# Frontend
npm run dev

# Tauri
cargo tauri dev
```

## Racha

Ver [`RASTRECK.md`](RASTRECK.md) para el registro diario de código.
