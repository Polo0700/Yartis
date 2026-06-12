---
name: tauri-websocket
description: |
  WebSocket client patterns for Tauri v2 with automatic reconnection.
  Use when connecting Rust to Python sidecar via WebSocket, handling
  reconnection with exponential backoff, and bridging WS messages to
  the React frontend via Tauri events.
  Triggers: WebSocket, tokio-tungstenite, reconnect, ws, stream.
---

# WebSocket Client (Rust) — Yartis

## Patrón base (actual)

```rust
use tokio_tungstenite::connect_async;
use futures_util::StreamExt;
use tauri::{AppHandle, Emitter};

#[tauri::command]
async fn inicio(app: AppHandle) -> Result<(), String> {
    let (stream, _) = connect_async("ws://localhost:8765")
        .await
        .map_err(|e| e.to_string())?;

    let (_escritura, mut lectura) = stream.split();

    while let Some(Ok(msg)) = lectura.next().await {
        match msg.to_text() {
            Ok(texto) => {
                if let Err(e) = app.emit("mensaje", texto) {
                    eprintln!("fallo al emitir {e}")
                }
            }
            Err(e) => eprintln!("Error WS: {e}")
        }
    }
    Ok(())
}
```

## Con reconexión automática (backoff exponencial)

```rust
use tokio_tungstenite::connect_async;
use futures_util::StreamExt;
use tauri::{AppHandle, Emitter};
use tokio::time::{sleep, Duration};

const MAX_RETRIES: u32 = 10;
const BASE_DELAY_MS: u64 = 500;

#[tauri::command]
async fn inicio(app: AppHandle) -> Result<(), String> {
    tauri::async_runtime::spawn(async move {
        loop {
            match conectar_y_escuchar(&app).await {
                Ok(()) => {
                    info!("WS: conexión cerrada normalmente, reintentando...");
                }
                Err(e) => {
                    error!("WS: error: {e}, reintentando...");
                }
            }
            sleep(Duration::from_secs(2)).await;
        }
    });
    Ok(())
}

async fn conectar_y_escuchar(app: &AppHandle) -> Result<(), String> {
    for intento in 0..MAX_RETRIES {
        match connect_async("ws://localhost:8765").await {
            Ok((stream, _)) => {
                info!("WS: conectado en intento {intento}");
                let (_escritura, mut lectura) = stream.split();

                while let Some(msg) = lectura.next().await {
                    match msg.map_err(|e| e.to_string()).and_then(|m| {
                        m.to_text().map(|t| t.to_string()).map_err(|e| e.to_string())
                    }) {
                        Ok(texto) => {
                            if let Err(e) = app.emit("mensaje", &texto) {
                                error!("emit: {e}");
                            }
                        }
                        Err(e) => {
                            error!("WS msg: {e}");
                            break; // reconnect
                        }
                    }
                }
                return Err("WS: stream ended".into());
            }
            Err(e) => {
                let delay = BASE_DELAY_MS * 2u64.pow(intento);
                warn!("WS: intento {intento} falló: {e}, reintentando en {delay}ms");
                if intento < MAX_RETRIES - 1 {
                    sleep(Duration::from_millis(delay)).await;
                }
            }
        }
    }
    Err("WS: max retries alcanzado".into())
}
```

## Con crate `ws-reconnect-client` (más limpio)

```toml
[dependencies]
ws-reconnect-client = "0.1"
```

```rust
use ws_reconnect_client::{WsClient, WsClientBuilder};
use futures_util::StreamExt;
use tauri::{AppHandle, Emitter};

#[tauri::command]
async fn inicio(app: AppHandle) -> Result<(), String> {
    tauri::async_runtime::spawn(async move {
        let client = WsClientBuilder::default()
            .url("ws://localhost:8765")
            .max_retries(10)
            .retry_delay_ms(1000)
            .build()
            .await
            .expect("WS client build");

        let mut stream = client.stream();
        while let Some(Ok(text)) = stream.next().await {
            if let Err(e) = app.emit("mensaje", &text) {
                error!("emit: {e}");
            }
        }
    });
    Ok(())
}
```

## Con crate `stream-tungstenite` (backoff presets)

```toml
[dependencies]
stream-tungstenite = "0.2"
```

```rust
use stream_tungstenite::StreamConfig;
use futures_util::StreamExt;
use tauri::{AppHandle, Emitter};

async fn ws_loop(app: AppHandle) {
    let mut config = StreamConfig::standard(); // .fast(), .conservative()
    config.url("ws://localhost:8765");

    let mut stream = config.connect().await.unwrap();

    while let Some(msg) = stream.next().await {
        match msg {
            Ok(text) => {
                if let text::Text(t) = text {
                    let _ = app.emit("mensaje", &t);
                }
            }
            Err(e) => error!("WS error: {e}"),
        }
    }
}
```

## Enviar datos al sidecar Python

Si Rust necesita enviar comandos al Python (ej: "detener", "reiniciar"):

```rust
use tokio_tungstenite::connect_async;
use futures_util::{StreamExt, SinkExt};
use tokio::sync::Mutex;

struct WsState {
    writer: Mutex<Option<SplitSink<WebSocketStream<...>, Message>>>,
}

#[tauri::command]
async fn enviar_comando(app: AppHandle, comando: String) -> Result<(), String> {
    let state = app.state::<WsState>();
    let mut guard = state.writer.lock().await;
    if let Some(writer) = guard.as_mut() {
        writer
            .send(Message::Text(comando.into()))
            .await
            .map_err(|e| e.to_string())?;
    }
    Ok(())
}
```

## Eventos Tauri vs WebSocket

| Acción | Mecanismo |
|--------|-----------|
| Rust → React (texto respuesta) | `app.emit("mensaje", texto)` |
| React → Rust (comandos UI) | `#[tauri::command]` + `invoke()` |
| Rust → Python (sidecar) | WebSocket send |
| Python → Rust (respuesta) | WebSocket recv |

## Errores comunes

1. **Olvidar spawn**: El loop WS debe ir en `tauri::async_runtime::spawn`, no directo en el command (bloquearía el IPC).
2. **No reconectar**: El `while let Some(Ok(msg))` termina si la conexión se cae. Siempre poner un loop exterior.
3. **Perder el writer**: Guardar `SplitSink` en estado manejado con `Mutex` si necesitas enviar desde commands.
