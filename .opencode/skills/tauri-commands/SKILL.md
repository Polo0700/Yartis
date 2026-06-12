---
name: tauri-commands
description: |
  Tauri v2 command patterns with proper error handling, state management,
  and async lifecycle for Yartis. Covers thiserror enums with Serialize,
  managed state with Arc<RwLock>/Mutex, event emission, and plugin setup.
  Triggers: tauri::command, AppHandle, invoke, emit, managed state, thiserror.
---

# Tauri v2 Commands — Yartis

## Estructura de lib.rs

```rust
use tauri::{AppHandle, Emitter, Manager};
use tokio_tungstenite::connect_async;
use futures_util::StreamExt;

mod commands;
mod error;
mod ws;

pub use error::YartisError;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build())
        .plugin(tauri_plugin_shell::init())
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![
            commands::ping,
            commands::iniciar,
            commands::detener,
        ])
        .setup(|app| {
            // Inicializar sidecar aquí si se quiere al arrancar
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Error handling con `thiserror`

```toml
[dependencies]
thiserror = "2"
serde = { version = "1", features = ["derive"] }
```

```rust
// error.rs
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum YartisError {
    #[error("WebSocket error: {0}")]
    Ws(String),

    #[error("Sidecar error: {0}")]
    Sidecar(String),

    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Comando desconocido: {0}")]
    Unknown(String),
}

// Tauri commands requieren Serialize en el error
impl Serialize for YartisError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        serializer.serialize_str(self.to_string().as_ref())
    }
}
```

## State management

```rust
// Estado global de la app
use tokio::sync::Mutex;

struct AppState {
    sidecar_pid: Mutex<Option<u32>>,
    ws_connected: Mutex<bool>,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            sidecar_pid: Mutex::new(None),
            ws_connected: Mutex::new(false),
        }
    }
}
```

### Acceder desde commands

```rust
#[tauri::command]
async fn get_status(state: tauri::State<'_, AppState>) -> Result<serde_json::Value, YartisError> {
    let pid = state.sidecar_pid.lock().await;
    let connected = state.ws_connected.lock().await;
    Ok(serde_json::json!({
        "sidecar_running": pid.is_some(),
        "ws_connected": *connected,
    }))
}
```

## Command patterns

### Sincrónico simple
```rust
#[tauri::command]
fn ping() -> String {
    "pong".to_string()
}
```

### Async con AppHandle
```rust
#[tauri::command]
async fn iniciar(app: AppHandle) -> Result<(), YartisError> {
    // app es clonable, se puede mover a un spawn
    tauri::async_runtime::spawn(async move {
        // lógica async aquí
        let _ = app.emit("evento", "valor");
    });
    Ok(())
}
```

### Con managed state
```rust
#[tauri::command]
async fn detener(
    app: AppHandle,
    state: tauri::State<'_, AppState>,
) -> Result<(), YartisError> {
    let mut pid = state.sidecar_pid.lock().await;
    if let Some(p) = pid.take() {
        // matar proceso
        kill_process_tree(p);
    }
    Ok(())
}
```

### Eventos al frontend
```rust
use tauri::Emitter;

// Emitir a React
app.emit("mensaje", "texto de respuesta").ok();

// Escuchar desde React:
// listen("mensaje", (event) => { console.log(event.payload) })
```

## Plugin setup pattern

```rust
// Registrar plugins en el Builder
.plugin(tauri_plugin_log::Builder::default()
    .level(log::LevelFilter::Info)
    .build())
.plugin(tauri_plugin_shell::init())
```

## Múltiples comandos en módulos separados

```
src/
├── main.rs
├── lib.rs
├── commands/
│   ├── mod.rs
│   ├── audio.rs      # comandos de audio
│   └── sidecar.rs    # comandos de sidecar
├── ws/
│   ├── mod.rs
│   └── client.rs     # WebSocket client
└── error.rs          # YartisError
```

### commands/mod.rs
```rust
pub mod audio;
pub mod sidecar;

pub use super::error::YartisError;
```

## Ventana y cleanup

```rust
.on_window_event(|window, event| {
    if let tauri::WindowEvent::CloseRequested { .. } = event {
        let app = window.app_handle();
        // cleanup: matar sidecar, cerrar WS, etc.
        info!("Yartis cerrando...");
    }
})
```

## Frontend invoke

```typescript
// React: llamar comandos Rust
import { invoke } from "@tauri-apps/api/core";

const response = await invoke<string>("ping");
// "pong"

await invoke("iniciar");
await invoke("detener");

const status = await invoke<{sidecar_running: boolean, ws_connected: boolean}>("get_status");
```

## Checklist de comando nuevo

- [ ] ¿Necesita `async`? (IO, red, sleep → sí)
- [ ] ¿Retorna `Result`? (casi siempre sí, para propagar errores)
- [ ] ¿Error type implementa `Serialize`? (necesario para Tauri)
- [ ] ¿Necesita `AppHandle`? (si emite eventos o accede a managed state)
- [ ] ¿Necesita `tauri::State`? (si accede a estado global)
- [ ] Registrado en `invoke_handler`?
