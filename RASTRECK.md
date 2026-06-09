# 🔥 Yardis — Racha de código

| Fecha | Puntos | ¿Qué logré? |
|-------|--------|-------------|
| 31-May-2026 | ⭐ 1 | `brain/context.py` completo + primer test unitario ✅ |
| 01-Jun-2026 | ⭐ 2 | Diseño de `brain/opencode.py` + creación de `connect.py` + regla de la hora en AGENTS.md |
| 02-Jun-2026 | ⭐ 3 | `core/audio.py` reescrito con callback + detección de silencio + noise reduction. `core/transcriber.py` reescrito con lógica propia. Descubrimiento de `opencode run` para el puente con OpenCode. ✅ |
| 03-Jun-2026 | ⭐ 4 | Pipeline funcional tras DEPURACIÓN REAL. Bugs corregidos de verdad: audio normalizado a float32 para Whisper, encoding utf-8 en subprocess, umbral de silencio ajustado (500→150), modelo small. `context.py` ahora guarda a historial.txt cuando el FIFO se llena. ✅ |
| 04-Jun-2026 | ⭐ 5 | Wake word "alexa" funciona. Investigué fonética y elegí **YARTIS** como wake word definitiva. Creé workspace easy-oww en D:, descargué 17.5GB de datasets. Pendiente: grabar samples + entrenar modelo personalizado. ✅ |
| 05-Jun-2026 | ⭐ 6 | Arquitectura final definida: Tauri orquesta, Python sidecar, React UI + TTS. Corregí AGENTS.md (IA tenía amnesia). Creé debug rooms: alpha/, beta/, v1_0/. Scaffold Tauri + React en beta/ con `npm create tauri-app` + `cargo tauri init`. Primer comando Rust `ping` funcionando desde React con `invoke`. ✅ |
| 06-Jun-2026 | ⭐ 7 | Fundamentos de Rust: ownership, `String` vs `&str`, `Command` para procesos, `Read` trait. Decisión de arquitectura: **WebSocket** para comunicación Rust ↔ Python (en vez de sidecar). Creación de `core/server.py` con handler WebSocket básico. ⚡ |
| 07-Jun-2026 | ⭐ 8 | Diagnóstico de error rust-analyzer (no encuentra Cargo.toml en raíz). Confirmación de proyecto Tauri existente en `beta/Yartis/`. Plan claro: entrenar wake word custom → subir a git → integrar con Rust. Pendiente: grabar samples de "YARTIS" y entrenar modelo. ✅ |
| 08-Jun-2026 | ⭐ 9 | 🦀 **Rust en serio**: `lib.rs` completado con conexión WebSocket + split + while let + emit a React. Perfil `rust-expert.md` creado. Skill `rust-engineer` instalado. Plugin **Superpowers** instalado. Regla de pausa de dudas agregada. Conceptos: `Result`, `?`, pattern matching, `while let`, `split`, `emit`. ✅ |

