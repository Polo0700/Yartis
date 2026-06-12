---
name: python-websocket-server
description: |
  Python WebSocket server for Yartis: async server with websockets library,
  message handling, client management, heartbeat, reconnection support,
  and integration with the audio/transcription pipeline.
  Use when building the Python side of the WebSocket bridge, handling
  client connections, sending/receiving messages, or managing the
  sidecar communication with Rust/Tauri.
  Triggers: WebSocket, websockets, async server, WS server, sidecar,
  broadcast, heartbeat, client management.
---

# Python WebSocket Server — Yartis

## Stack
- `websockets` — async WebSocket server (stdlib `asyncio`)

## Server básico (actual)

```python
import asyncio
import websockets
from brain.opencode import peticion

class YartisServer:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port

    async def handler(self, websocket):
        """Maneja cada conexión entrante"""
        async for message in websocket:
            try:
                respuesta = peticion().ejecutar(message)
                await websocket.send(respuesta)
            except Exception as e:
                print(f"Error: {e}")

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"Server en ws://{self.host}:{self.port}")
            await asyncio.Future()  # corre forever
```

## Server con heartbeat y reconexión

```python
import asyncio
import json
import websockets
from datetime import datetime, timezone

CONNECTIONS: set[websockets.WebSocketServerProtocol] = set()
HEARTBEAT_INTERVAL = 30  # segundos

async def handler(websocket):
    CONNECTIONS.add(websocket)
    try:
        async for message in websocket:
            await process_message(websocket, message)
    finally:
        CONNECTIONS.remove(websocket)

async def process_message(websocket, message: str):
    try:
        data = json.loads(message)
        msg_type = data.get("type")

        if msg_type == "command":
            result = await execute_command(data.get("payload", {}))
            await websocket.send(json.dumps({
                "type": "response",
                "id": data.get("id"),
                "payload": {"status": "ok", "data": result},
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))

        elif msg_type == "ping":
            await websocket.send(json.dumps({"type": "pong"}))

    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            "type": "error",
            "payload": {"code": "PARSE_ERROR", "message": "JSON inválido"}
        }))

async def heartbeat():
    """Envía heartbeat a todos los clientes cada 30s"""
    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL)
        if CONNECTIONS:
            msg = json.dumps({
                "type": "event",
                "payload": {"event": "heartbeat"},
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            await asyncio.gather(
                *(conn.send(msg) for conn in CONNECTIONS.copy()),
                return_exceptions=True
            )

async def broadcast(event: str, data: any):
    """Envía un evento a todos los clientes conectados"""
    msg = json.dumps({
        "type": "event",
        "payload": {"event": event, "data": data},
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    await asyncio.gather(
        *(conn.send(msg) for conn in CONNECTIONS.copy()),
        return_exceptions=True
    )

async def start():
    async with websockets.serve(handler, "localhost", 8765):
        print("Yartis WS server ready on ws://localhost:8765")
        await asyncio.gather(
            heartbeat(),
            asyncio.Future()  # forever
        )
```

## Integración con whisper + wake word

```python
async def execute_command(payload: dict) -> str:
    action = payload.get("action")
    data = payload.get("data")

    if action == "transcribe":
        # data contiene audio bytes en base64...
        pass
    elif action == "process_text":
        from brain.opencode import peticion
        return peticion().ejecutar(data)
    elif action == "status":
        return "ready"
    else:
        raise ValueError(f"Unknown action: {action}")
```

## Cliente de prueba

```python
import asyncio
import websockets

async def test_client():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send('{"type":"command","payload":{"action":"status"}}')
        response = await ws.recv()
        print(f"Respuesta: {response}")

asyncio.run(test_client())
```

## Graceful shutdown

```python
import signal

async def start_with_shutdown():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: stop.set_result(None))

    async with websockets.serve(handler, "localhost", 8765):
        print("Server running. Press Ctrl+C to stop.")
        await stop

    print("Shutting down gracefully...")
    # Cerrar conexiones
    for conn in CONNECTIONS.copy():
        await conn.close()
    CONNECTIONS.clear()
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ConnectionClosedError` | Cliente se desconectó repentinamente | Capturar en el handler, remover de CONNECTIONS |
| `ConnectionRefusedError` | Puerto ocupado o Rust no conectó | Verificar que el server inició antes que Rust |
| Timeout | Latencia de red o proceso bloqueante | Usar `asyncio.wait_for()` con timeout |
| Mensaje sin procesar | JSON malformado | Validar con try/except antes de procesar |
