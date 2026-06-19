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
| 09-Jun-2026 | ⭐ 10 | 🦀 Continuación Rust — ajustes finos en WebSocket y sidecar |
| 10-Jun-2026 | ⭐ 11 | 🐍 Pulido Python — limpieza de código en core/audio.py y brain/ |
| 11-Jun-2026 | ⭐ 12 | ⚛️ Primeros pasos con React — componentes ChangeSize + setup Tauri |
| 12-Jun-2026 | ⭐ 13 | 🔧 React + ajustes varios |
| 13-Jun-2026 | ⭐ 14 | 🎨 **UI del asistente**: Hook `useAssistant` con ciclo demo de estados (wait→hearing→processing→speaking). Componente `StatusIndicator` con círculo tipo JARVIS + ondas expansivas por CSS. Estructura separada: hook (lógica) / componente (vista) / CSS (animaciones). Pendiente: conectar en App.tsx y probar. ✅ |
| 14-Jun-2026 | ⭐ 15 | 🧠 **OpenCode como cerebro de Yartis**: diagnóstico del AGENTS.md global que preguntaba perfil en cada llamada. Creado perfil `yartis-brain` con skill Yartis dedicada (sin skills de desarrollo). `brain/opencode.py` usa `--continue` para mantener sesión limpia. Bugfix: `ejecutar(texto)` ya no ignora el texto (no regraba si recibe parámetro). Script `test_mano.py` con TTS para pruebas rápidas. ✅ |
| 17-Jun-2026 | ⭐ 16 | 🛡️ **Robustez + sidecar Tauri**: try/except en `yartis.py` y `wake.py`. DEBUG mode en `config.py`. Sidecar python en `lib.rs` con `tauri_plugin_shell` + WS emite eventos a React. Silenciado debug de audio. Actualizado `prompt.json` con nuevo estado. ✅ |
| 17-Jun-2026 | ⭐ 17 | 🔌 **useAssistant conectado + GPU toggle**: Hook `useAssistant` con `listen` real desde Tauri, cleanup con promesas. `App.tsx` con ternario para estado speaking/wait. `yartis.py` con `argparse --cpu` para toggle de GPU. Aprendizaje: Promises, `.then()`, IPC, ternarios. ✅ |
| 18-Jun-2026 | ⭐ 18 | 🛡️ **Sistema de confirmacion**: System prompt con reglas CONFIRMAR|tipo|detalle (CRUD con leer=auto, eliminar=papelera). Esqueleto `brain/confirmacion.py` con clase confirmador. Prueba de apertura de navegador via PowerShell exitosa. ✅ |
| 18-Jun-2026 | ⭐ 18 | 📋 **Estado del proyecto documentado**: Revisados 8 archivos modificados, 10 problemas activos identificados (wake word, confirmación TF-IDF, GPU, sonidos), y 5 próximos pasos ordenados por prioridad. Racha al día. ✅ |
| 19-Jun-2026 | ⭐ 19 | 🛡️ **Sistema de confirmación completo**: TF-IDF + Logistic Regression en `brain/confirmacion.py`. Código de seguridad `0x0x0Polo0700`. Flujo: OpenCode responde → confirma con voz → clasifica → reenvía si aprueba. ✅ |

