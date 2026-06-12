---
name: websocket-protocol
description: |
  WebSocket message protocol between Rust (Tauri) and Python sidecar.
  Use when designing message formats, handling bidirectional communication,
  serialization schemas, error types, reconnection logic, and state
  synchronization between Rust and Python.
  Triggers: WebSocket, protocol, message format, JSON schema, serialization,
  Rust-Python communication, bidirectional.
---

# WebSocket Protocol — Rust ↔ Python

## Arquitectura

```
Python (sidecar) ──WS──▶ Rust (Tauri) ──emit──▶ React (WebView)
                        Rust ◀──invoke── React
Python ◀──WS── Rust
```

## Formato de mensajes (JSON)

### Request (Rust → Python)
```json
{
  "type": "command",
  "id": "uuid-unico",
  "payload": {
    "action": "procesar_texto",
    "data": "texto a procesar"
  },
  "timestamp": "2026-06-09T00:00:00Z"
}
```

### Response (Python → Rust)
```json
{
  "type": "response",
  "id": "uuid-del-request",
  "payload": {
    "status": "ok",
    "data": "texto de respuesta",
    "audio": null
  },
  "timestamp": "2026-06-09T00:00:01Z"
}
```

### Error (Python → Rust)
```json
{
  "type": "error",
  "id": "uuid-del-request",
  "payload": {
    "code": "WHISPER_ERROR",
    "message": "Error al transcribir audio"
  },
  "timestamp": "2026-06-09T00:00:01Z"
}
```

### Evento (Python → Rust, sin request)
```json
{
  "type": "event",
  "payload": {
    "event": "status_change",
    "data": {
      "status": "listening"
    }
  },
  "timestamp": "2026-06-09T00:00:00Z"
}
```

## Esquema Rust (con serde)

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum WsMessage {
    #[serde(rename = "command")]
    Command {
        id: String,
        payload: CommandPayload,
        timestamp: String,
    },
    #[serde(rename = "response")]
    Response {
        id: String,
        payload: ResponsePayload,
        timestamp: String,
    },
    #[serde(rename = "error")]
    Error {
        id: String,
        payload: ErrorPayload,
        timestamp: String,
    },
    #[serde(rename = "event")]
    Event {
        payload: EventPayload,
        timestamp: String,
    },
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CommandPayload {
    pub action: String,
    pub data: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ResponsePayload {
    pub status: String,
    pub data: serde_json::Value,
    pub audio: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ErrorPayload {
    pub code: String,
    pub message: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EventPayload {
    pub event: String,
    pub data: serde_json::Value,
}
```

## Esquema Python (con dataclasses + Pydantic)

```python
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime, timezone

class WsMessage(BaseModel):
    type: str  # "command" | "response" | "error" | "event"
    id: Optional[str] = None
    payload: dict[str, Any]
    timestamp: str = datetime.now(timezone.utc).isoformat()

def create_response(request_id: str, data: Any) -> str:
    msg = WsMessage(
        type="response",
        id=request_id,
        payload={"status": "ok", "data": data}
    )
    return msg.model_dump_json()

def create_error(request_id: str, code: str, message: str) -> str:
    msg = WsMessage(
        type="error",
        id=request_id,
        payload={"code": code, "message": message}
    )
    return msg.model_dump_json()

def create_event(event: str, data: Any) -> str:
    msg = WsMessage(
        type="event",
        payload={"event": event, "data": data}
    )
    return msg.model_dump_json()
```

## Flujo de conexión

```
Rust                         Python
  │                            │
  │─── connect_async ─────────▶│
  │◀── connection accepted ───│
  │                            │
  │─── {"type":"command",...}─▶│  (procesar texto)
  │                            │
  │◀── {"type":"response",...}─│  (respuesta)
  │                            │
  │◀── {"type":"event",...}────│  (status change)
  │                            │
```

## Estados del WebSocket

```
DISCONNECTED → CONNECTING → CONNECTED
     ↑              │
     └──────────────┘
        (reconnect)
```

## Manejo de errores comunes

| Situación | Comportamiento |
|-----------|---------------|
| Timeout de conexión | Reintentar con backoff exponencial (500ms, 1s, 2s, 4s...) |
| Conexión cerrada | Reintentar automáticamente |
| Mensaje malformado | Log + ignorar, no cerrar conexión |
| Timeout de respuesta | Reintentar el comando o reportar error |

## Heartbeat

```python
# Python sidecar envía heartbeat cada 30s
import asyncio, json

async def heartbeat(websocket):
    while True:
        await asyncio.sleep(30)
        await websocket.send(json.dumps({
            "type": "event",
            "payload": {"event": "heartbeat"},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }))
```
