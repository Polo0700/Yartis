# 🧠 Lógica de la IA — Yartis

Este archivo registra el razonamiento detrás de cada decisión técnica, orden de los pasos,
y el estado actual del pensamiento. Sirve para que en la siguiente sesión la IA sepa
exactamente en qué iba pensando y por qué.

---

## Arquitectura general

### ¿Por qué Tauri + Python (WebSocket)?
- **No sidecar**: Tauri tiene sidecar integrado, pero WebSocket es más flexible.
  El sidecar ejecuta un binario y se comunica por stdin/stdout — limitado.
  WebSocket permite conexión remota, reconexión, y es más fácil de depurar.
- **Tauri orquesta, Python hace audio**: Rust no tiene ecosistema de audio tan rico.
  Python tiene sounddevice, faster-whisper, noisereduce, openwakeword.
  La división natural es: Python hace el pipeline de audio + cerebro, Rust maneja la UI.
- **React para UI/TTS**: Web Speech API corre en el navegador/WebView.
  No necesita librerías externas, es nativo del browser.

### Pipeline final decidido
```
Wake word → grabación → noise reduction → Whisper (GPU) → OpenCode → TTS (Web Speech API)
```
Python: wake word + grabación + whisper + opencode → WebSocket → Rust → emit → React → TTS

---

## Decisiones técnicas con razonamiento

### `lib.rs` — WebSocket en Rust
- `connect_async("ws://localhost:8765")` — El servidor Python corre en ese puerto.
  Elegí `localhost` porque Tauri y Python corren en la misma máquina.
- `stream.split()` — Separa lectura y escritura aunque no usemos escritura aún.
  Lo hice desde el principio para no tener que refactorizar después cuando mandemos
  comandos a Python desde Rust.
- `while let Some(Ok(msg))` — Bloquea el hilo asíncrono esperando mensajes.
  Alternativa: `loop` con `match lectura.next().await`. Esta forma es más idiomática.
- `if let Err(e) = obj.emit(...)` — No usar `?` porque mataría el comando `inicio`
  si falla un solo emit. `eprintln!` registra pero no mata el loop.
- `map_err(|e| e.to_string())` en connect — Convierte `tokio_tungstenite::Error`
  a `String` porque los comandos de Tauri requieren `Result<(), String>`.
- Comando `ping` se mantiene como easter egg/test de comunicación básica.
- Se decidió NO hacer `_escritura` como variable con nombre (con guión bajo) para
  que Rust no se queje de variable no usada. Lo mismo para `_` en `(stream, _)`.

### `server.py` — Servidor WebSocket en Python
- Usa `websockets` (librería asíncrona), no `socket` (TCP crudo).
  `websockets` ya maneja handshake, enmarcado, ping/pong.
- `async for message in websocket:` — Loop infinito mientras la conexión viva.
  No necesita `while True` + `await websocket.recv()`, el `async for` es más limpio.
- Handler llama a `opencode.peticion().ejecutar(message)` y envía respuesta.
  Esto significa que cada mensaje del frontend (Rust) genera una llamada a OpenCode.

### `core/audio.py` — Grabación y noise reduction
- **Callback**: sounddevice llama a una función con cada chunk de audio.
  El callback recibe `indata` (numpy array), calcula RMS, y si supera el umbral,
  guarda en un buffer. Usamos una **bandera** (`grabando`) para comunicar el estado
  entre el callback (otro hilo) y el while principal.
- **Umbral de silencio**: Inicialmente 500, se bajó a 150 porque 500 era muy sensible.
  Si RMS < 150 por más de 1.5 segundos, se deja de grabar.
- **Normalización**: int16 → float32 dividiendo entre 32768. Whisper espera float32 [-1, 1].
- **Spectral gating** (noisereduce): FFT → calcular espectro de ruido → crear máscara →
  aplicar máscara → IFFT. El perfil de ruido se toma de los primeros frames (silencio).
- **16kHz mono**: Frecuencia estándar para voz humana. Whisper fue entrenado en 16kHz.

### `brain/context.py` — Memoria FIFO
- **Dos listas sincronizadas**: Una para mensajes del usuario, otra para respuestas de la IA.
  Se necesita saber quién dijo qué para formatear el prompt correctamente.
- **Cache de tokens**: `TOKENS_USADOS` evita recalcular len(enc.encode(texto)) en cada
  mensaje. Se actualiza cuando se agrega o elimina un mensaje.
- **Evicción FIFO**: Cuando se excede `MAX_TOKENS`, se elimina el par más viejo
  (mensaje + respuesta) con `pop(0)`. Se guarda en `historial.txt` con timestamp.
- **Persistencia**: Los mensajes viejos van a `historial.txt` para no perder contexto
  histórico, pero no saturar el prompt activo.

### `brain/opencode.py` — Bridge con OpenCode
- `subprocess.run(["opencode", "run", mensaje], capture_output=True, ...)` — Llama a
  OpenCode como CLI. Alternativa: API HTTP de OpenCode (no existe aún en ese momento).
- `encoding="utf-8", errors="replace"` — Previene `UnicodeDecodeError` si la salida
  contiene caracteres no UTF-8.
- Cada llamada crea una **sesión nueva** — no hay estado entre llamadas.
  TODO en el futuro: OpenCode podría tener persistencia de sesión.

### Wake word — openwakeword
- **openwakeword**: Funciona con modelos ONNX pre-entrenados. La wake word "alexa"
  viene por defecto. Para "YARTIS" se necesita entrenar modelo custom.
- **Fonética**: Y+T+S tienen sonidos fuertes → buena detección.
- **Frame**: 1280 samples por frame (80ms a 16kHz). Umbral: 0.02.
- **Pendiente**: Grabar ~100 samples de "YARTIS" + ~100 de ruido/falsos positivos →
  entrenar con `openwakeword train`.

### RASTRECK.md — Racha de código
- **Racha por proyecto**: Cada proyecto tiene su propio RASTRECK.md en su raíz.
- **Días consecutivos**: Si el usuario programa un día, suma ⭐. Si falta un día, reinicia.
- Propósito: motivación y registro de avance. No es métrica de productividad, es
  registro de consistencia.

---

## Orden de los pasos (y por qué)

1. **Python primero** (audio + whisper + opencode) — Tiene las piezas más complejas
   y era lo que el usuario ya conocía. Arrancar con lo conocido genera confianza.
2. **Rust/lib.rs después** — Una vez que Python funcionaba, el puente con Rust
   daba miedo porque Rust es nuevo para el usuario. Se hizo paso a paso:
   `ping` → WebSocket básico → split → emit.
3. **React listen** → SIGUIENTE. El frontend debe escuchar los eventos de Rust
   para cerrar el ciclo. Sin esto no se puede probar nada.
4. **Prueba pipeline** → Después de conectar React. Correr Python + Tauri juntos.
5. **README.md** → Antes del push público. El repo ya está en GitHub pero sin descripción.
6. **Wake word custom** → Es el feature más complejo y depende de grabar samples.

---

## 🌍 Reglas Globales de Trabajo

Estas reglas aplican a TODOS los agentes del sistema (planeador, python-expert, rust-expert, typescript-expert, etc.).

### Regla de Oro (en orden estricto)

1. **Explicar primero** — Antes de tocar cualquier archivo, el agente debe explicar
   el concepto en lenguaje simple. ¿Qué vamos a hacer? ¿Para qué sirve? ¿Cómo se
   conecta con lo demás? Si hay término técnico, se explica justo ahí.
2. **Preguntar** — "¿Dudas?" o "¿Queda claro?" El usuario debe confirmar que entendió.
3. **El usuario codea** — El agente indica **exactamente qué escribir y dónde**,
   pero es el usuario quien escribe el código en su editor. NO escribir código
   directamente en los archivos a menos que el usuario lo pida explícitamente.
4. **Nunca saltarse los pasos 1-3** — Aunque el concepto sea "obvio" o ya se haya
   explicado antes. Si se retoma en otra sesión, se da un resumen breve antes de avanzar.

### Reglas secundarias

- **Pausa de dudas**: Después de cada explicación o cambio, preguntar
  "¿Dudas?" o "¿Tiene sentido?" para que procese antes de seguir.
- **Regla de la hora**: Verificar hora local. Si >23:00, sugerir descanso UNA vez.
  Si decide seguir, no insistir. La IA no es su mamá.
- **Sinceridad**: No fingir que recuerdo algo que no me inyectaron. Si empiezo
  una sesión sin contexto, decirlo y pedir ayuda para orientarme.
- **Registrar en RASTRECK.md** al final de cada sesión.

---

## Errores y bugs ya corregidos

| Bug | Síntoma | Solución |
|-----|---------|----------|
| Whisper recibe int16 | Transcripción fallaba | Normalizar a float32 dividiendo entre 32768 |
| UnicodeDecodeError en subprocess | Caracteres raros en salida | `encoding="utf-8", errors="replace"` |
| RMS threshold 500 | No detectaba voz normal | Bajado a 150 |
| rust-analyzer no encuentra Cargo.toml | Sin autocompletado | `linkedProjects` en `.vscode/settings.json` apuntando a `beta/Yartis/src-tauri/Cargo.toml` |
| `eprint!` sin newline | Mensajes de error pegados | Cambiado a `eprintln!` |

---

## Estado actual del pensamiento

Fecha: 09-Jun-2026 ~4:00 AM

**¿Qué estoy pensando ahora?**
- El siguiente paso es enseñarle al usuario cómo `listen()` funciona en React/Tauri.
- `listen("mensaje", callback)` de `@tauri-apps/api/event` espejo de `obj.emit("mensaje", texto)` en Rust.
- El callback recibe un objeto `{ payload: string }` — el payload es lo que Rust emitió.
- Quiero explicarle que esto cierra el círculo: Python → WebSocket → Rust → emit → React.
- Una vez que React recibe el mensaje, puede mostrarlo en pantalla y usar `speechSynthesis.speak()`.
- Después de eso, probar todo junto. Si funciona, actualizar RASTRECK.md.

**Problemas conocidos pendientes de resolver:**
- El botón en Start.tsx llama a `ping` no a `inicio`. El comando `inicio` no se invoca nunca.
- Solución potencial: cambiar el botón para que llame a `inicio` en vez de `ping`.
- O mejor: que `inicio` se ejecute automáticamente al arrancar la app (en un `useEffect`).
- Si `inicio` falla (Python no corre), la app no debería crashear.

---

## Próximas sesiones — hoja de ruta

1. **🔗 Conectar React** → `listen("mensaje")` en Start.tsx
2. **🧪 Probar pipeline** → Python server + cargo tauri dev
3. **📝 README.md** → Descripción del proyecto
4. **🎤 Wake word custom** → Grabar samples + entrenar
5. **🤖 Agente Yardis** → `.opencode/agent/yardis.md`
6. **💬 Comentar código** → Documentación inline
