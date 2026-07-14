# 🗺️ Yartis — Roadmap de Desarrollo

> *"Un asistente de voz que no solo responde, sino que aprende, enseña, crea contenido y genera experiencias de estudio completas."*

---

## Estado Actual

| Versión | Estado | Descripción |
|---------|--------|-------------|
| **V1** | ✅ Completado | Pipeline básico: wake word → grabación → Whisper → OpenCode → TTS |
| **V2** | 🔄 En progreso | WebSocket Hub + Clasificador local + Servicios (Música, Correo, Calendario, Telegram, Navegador) |
| **V3** | ⏳ Pendiente | **MODO JARVIS** — Escucha ambiental continua + Detección de intención pasiva + Sesiones persistentes |
| **V4** | ⏳ Pendiente | Autoaprendizaje + Explicador de código |
| **V5** | ⏳ Pendiente | Excalidraw interactivo + Búsqueda de videos + Generador de sitios |
| **V6** | ⏳ Pendiente | Motor de renderizado de video on-demand |
| **V7** | ⏳ Pendiente | Plataforma de Notas Interactiva (competencia NotebookLM) |
| **V8/1.0** | ⏳ Pendiente | **RELEASE FINAL** — Pulido, testeo completo, listo para el mundo |

---

## V2 — WebSocket Hub + Clasificador Local (EN PROGRESO)

**Objetivo:** Yartis interpreta la intención del usuario localmente y ejecuta servicios sin gastar tokens de OpenCode.

| Paso | Estado | Detalle |
|------|--------|---------|
| server.py como WebSocket HUB | ✅ | `core/server.py` — orquesta comunicación Rust ↔ Python |
| yartis.py como cliente WebSocket | ✅ | `yartis.py` — cliente que se conecta al hub |
| Clasificador local con sentence-transformers | ✅ | Modelo `paraphrase-multilingual-MiniLM-L12-v2`. Intenta: MUSICA, CORREO, CALENDARIO, TELEGRAM, NAVEGADOR |
| Servicio de Música (reproductor real) | ⏳ | Reemplazar `prueba.py` con servicio real (yt-dlp o similar). Conectar output a TTS |
| Servicio de Correo | ⏳ | Pendiente |
| Servicio de Calendario | ⏳ | Pendiente |
| Servicio de Telegram | ⏳ | Pendiente |
| Servicio de Navegador | ⏳ | Pendiente |
| Herramientas propias (CRUD sin OpenCode) | ✅ | `opencode.py` con `0x0x0Polo0700|accion|ruta|contenido|explicacion`. Confirmador aprueba, ejecuta directo. 0 tokens |
| Meta-servicio Música v2.1 (multi-fuente) | ⏳ | yt-dlp + MusicBrainz + TheAudioDB + Last.fm + Genius + SoundCloud + Jamendo. Cache local |

**Filosofía V2:** El LLM solo orquesta. Los scripts ejecutan todo. El usuario tiene control total de tokens.

---

## V3 — MODO JARVIS: Escucha Ambiental Continua

**Objetivo:** Invertir el flujo. Yartis no espera a que le hablen — **escucha siempre, detecta intención, y habla cuando vale la pena**. El salto de asistente reactivo a compañero proactivo.

### Los 5 Niveles de JARVIS

```
NIVEL 1: Wake word clásica (V2)
  → "YARTIS" → graba → responde

NIVEL 2: Escucha continua + detección de intención (V3)
  → Modelo ligero 24/7 → detecta "YARTIS" en cualquier parte de la frase

NIVEL 3: Voice ID + Buffer inteligente (V3)
  → Sabe QUIÉN habla → guarda chunks del dueño → contexto completo

NIVEL 4: Voces frecuentes (V8)
  → Aprende voces nuevas automáticamente → recomienda agregar

NIVEL 5: Contexto + prioridad dinámica (1.0)
  → Entiende la DINÁMICA de la conversación → prioriza por contexto
```

### Nivel 1 — Wake Word Clásica (V2)

```
🎤 Off  →  "YARTIS"  →  🎤 On  →  Procesa  →  Responde
                   ↑ wake word obligatoria
```

**Ya implementado.** Simple, bajo consumo, privacidad total.

---

### Nivel 2 — Escucha Continua + Detección de Intención (V3)

```
🎤 Siempre escuchando (modelo ligero, quantizado, ~50MB)
   │
   ├─ Ruido ambiental → ignora → sigue dormido 🟢
   │
   ├─ "hola" → detecta saludo → responde naturalmente 🔵
   │
   ├─ "chatarra" (palabra clave de usuario) → sesión abierta 🔴
   │    → micrófono queda prendido
   │    → usuario habla libremente
   │    → al finalizar: limpieza de ruido → procesa → responde
   │
   └─ silencio largo → vuelve a dormir 🟢
```

**Opcional** — el usuario elige si activar este modo o quedarse con la wake word clásica.

---

### Nivel 3 — Voice ID + Buffer Inteligente (V3)

```
🎤 Audio 24/7
   │
   ▼
🦀 RUST (filtrado rápido en tiempo real)
   ├─ Voice ID: ¿Es el DUEÑO? → 🟢 Guarda chunks
   ├─ Voice ID: ¿Es OTRO? → ⚪ Ignora
   │
   ▼
BUFFER INTELIGENTE:
   ├─ Empezás a hablar → chunks se acumulan en temp
   ├─ Decís "YARTIS" → 🟡 buffer se CONGELA (no se libera)
   ├─ Seguís hablando → chunks siguen entrando al buffer
   └─ Dejás de hablar → 🔴 PROCESA TODO el buffer
   │
   ▼
🐍 PYTHON
   ├─ Whisper transcribe el audio completo (chunks unidos)
   ├─ Modelo local lee TODO el contexto
   ├─ Entiende: "estaba explicando X, yartis me preguntó Y"
   ├─ Genera prompt limpio → OpenCode
   └─ OpenCode responde → Piper TTS habla
```

**Flujo completo:**
```
Tú:        "oye la integral de x² es x³/3, ¿no?"  ← chunks guardados
Amigo:     "no creo, revisalo"                      ← ignorado (no es dueño)
Tú:        "Yartis, ¿cuánto es la integral de x²?" ← detecta nombre → congela
Tú:        "¿verdad que es así?"                    ← agrega al buffer
Silencio   → procesa TODO                            ← transcribe + modelo + OpenCode
Yartis:    "La integral de x² es x³/3 + C. Tenés razón, tu amigo estaba equivocado"
```

**El modelo local sabe el contexto COMPLETO** — no solo la pregunta, sino todo lo que viniste hablando.

---

### Nivel 4 — Voces Frecuentes (V8)

```
🎤 Audio 24/7 con Voice ID
   │
   ├─ Voz desconocida #1 aparece en 12 audios esta semana
   ├─ Yartis detecta que es SIEMPRE la misma voz
   │
   ▼
💡 "Oye, noto que hay una persona que aparece seguido en tus audios.
    ¿Querés que la agregue a tu lista de voces?"
   │
   ▼
TÚ:      "Sí, es mi novia"
Yartis:  "¿Cómo se llama?"
TÚ:      "María"
Yartis:  ✅ "María" agregada a la lista de voces
```

**Después de esto:**
```
María:    "¿Yartis, qué tiempo hace mañana?"
Yartis:   🟢 Ya conozco a María → procesa como si fuera el usuario
```

---

### Nivel 5 — Contexto + Prioridad Dinámica (1.0)

```
NIVELES DE PRIORIDAD:

1️⃣  DUEÑO (tú) + voz fuerte (cerca del mic)
    → Máxima prioridad, siempre

2️⃣  DUEÑO (tú) + voz suave (lejos del mic)
    → Alta prioridad

3️⃣  VOZ REGISTRADA + voz fuerte + te habla A TI
    → Media prioridad

4️⃣  VOZ REGISTRADA + voz suave + tema no relacionado
    → Baja prioridad

5️⃣  VOZ DESCONOCIDA
    → Ignorar siempre
```

**Filtrado inteligente por contexto:**
```
ESCENARIO 1: Mamá al teléfono (tema no relacionado)
  Tú:      "Yartis, ¿cuánto es 2+2?"
  Mamá:    "Sí mi amor, el supermercado tiene descuento..." (al fondo)
  → Yartis IGNORA a mamá (no es contigo, tema diferente)

ESCENARIO 2: Mamá te habla directamente
  Tú:      "Yartis, ¿qué tiempo hace?"
  Mamá:    "Yartis, ¿cuándo viene tu papá?" (misma sala)
  → Yartis te responde a TI primero (dueño = prioridad)

ESCENARIO 3: Solo mamá (tú no estás)
  Mamá:    "Yartis, pon música"
  → Yartis PROCESA a mamá (es registrada + no estás presente)
```

**Regla de oro:** Si el DUEÑO está hablando → solo importa él. Los externos se procesan SOLO cuando el dueño no está hablando o cuando hablan DIRECTAMENTE a él.

### Coordinación entre dispositivos Yartis (BLE + Bluetooth)

**Problema:** Si hay 2+ Yartis en la misma habitación, ambas se activan cuando alguien dice "YARTIS".

**Solución:** Coordinación por Bluetooth Low Energy (BLE) — sempre activo, casi 0 batería.

```
TRES CAPAS DE COORDINACIÓN:

CAPA 1: BLE (siempre activo, ~0 batería)
  ├─ Descubre otras Yartis en la red local
  ├─ Intercambia IDs de dispositivos
  ├─ "¿Quién es el dueño de esta voz?"
  └─ Decide quién responde

CAPA 2: BLUETOOTH NORMAL (si BLE detecta otra Yartis)
  ├─ Conexión estable para coordinación pesada
  ├─ Estado compartido (quién habló, qué pidió)
  └─ Se apaga cuando termina la interacción

CAPA 3: AUDIO-BASED (fallback final, sin red)
  ├─ "Si escucho a OTRA Yartis hablando → me callo"
  └─ Coordinación por oído puro
```

**BLE es la pieza clave:**
- Siempre escuchando pero dormido (consumo ~0.01mW)
- Se despierta SOLO cuando detecta "YARTIS"
- Coordina con otras Yartis en la red
- Vuelve a dormir después

**Reglas de coordinación:**
```
¿Los dueños están en la misma red y se tienen registrados?
  │
  ├─ SÍ → Coordinar por BLE/BT
  │       "Hola, yo tengo a tu hermana registrada"
  │       → Se ponen de acuerdo quién responde
  │
  └─ NO → Ignorarse mutuamente
          "No conozco a ese usuario"
          → Cada Yartis solo responde a su dueño
```

**Crates Rust para BLE:**
| Crate | SO | Notas |
|-------|-----|-------|
| `btleplug` | Cross-platform | Recomendado — funciona en Windows, Linux, macOS |
| `bluer` | Linux | BlueZ bindings |
| `windows-rs` | Windows | WinRT API |

**Escenarios resueltos:**
```
CASO 1: Familia (misma casa)
  TU PC ──────── Yartis #1 (tú eres dueño)
  HERMANA PC ─── Yartis #2 (ella es dueña)
  HERMANA: "Yartis, ¿qué hora es?"
  → BLE coordina → Solo HERMANA PC responde

CASO 2: Amigos (misma habitación, sin registrarse)
  TU PC ──────── Yartis #1 (tú eres dueño)
  AMIGO PC ───── Yartis #2 (él es dueño)
  AMIGO: "Yartis, ¿qué hora es?"
  → No se tienen registrados → Se ignoran → Solo AMIGO PC responde

CASO 3: Sin WiFi ni Bluetooth
  → Fallback audio: "Si escucho al otro hablando, me callo"
```

---

### Arquitectura Técnica del Modo JARVIS

```
┌─────────────────────────────────────────────────┐
│                 AUDIO CRUDO (micrófono)          │
│              24/7 • bajo consumo CPU              │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│        🦀 RUST — FILTRADO EN TIEMPO REAL         │
│  • Voice ID por chunk (SpeechBrain ECAPA-TDNN)   │
│  • Buffer circular (guardar/liberar chunks)      │
│  • Detección de "YARTIS" en stream               │
│  • Unión de chunks (concatenar audio)            │
│  • Filtrado de silencio/ruido                    │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│        🐍 PYTHON — PROCESAMIENTO                 │
│  • Whisper transcribe audio completo             │
│  • Modelo local analiza contexto completo        │
│  • Genera prompt limpio con palabras del usuario  │
│  • OpenCode genera respuesta                     │
│  • Piper TTS habla la respuesta                  │
└─────────────────────────────────────────────────┘
```

### Componentes nuevos para V3

| Componente | Descripción | Dependencias |
|------------|-------------|--------------|
| `core/ambient_listener.py` | Loop de escucha continua con modelo ligero | Silero VAD, sounddevice |
| `core/keyword_spotter.py` | Detección de "YARTIS" en cualquier posición de la frase | Silero VAD + modelo custom |
| `core/intent_classifier.py` | Clasificador de intención (saludo/petición/ignorar) | Modelo quantizado ONNX |
| `core/session_manager.py` | Manejo de sesiones abiertas (grabar → limpiar → procesar) | audio.py existente |
| `core/voice_isolator.py` | Aislamiento de voz del usuario (limpiar ruido de fondo) | noisereduce existente |
| `core/buffer_manager.py` | Buffer circular de chunks con congelación | Rust-side |
| `brain/voice_id.py` | Voice ID por chunk (ya existe, extender para stream) | SpeechBrain ECAPA-TDNN |

### Configuración del usuario

```json
{
  "modo_jarvis": {
    "enabled": true,
    "nivel": 3,
    "palabra_clave": "chatarra",
    "umbral_confianza": 0.7,
    "max_sesion_segundos": 30,
    "saludos_automaticos": true,
    "horario_activo": "08:00-23:00",
    "no_molestar": ["reuniones", "gaming"],
    "voces_registradas": ["mamá", "papá", "María"],
    "voces_frecuentes_auto": true,
    "prioridad_dinamica": true
  }
}
```

### Reglas de No-Molestar (JARVIS)

| Regla | Explicación |
|-------|-------------|
| **No interrumpas en flow** | Si el usuario está hablando seguido, espera pausa |
| **Mensajes < 15 palabras** | Proactivo no significa charlatán |
| **Máximo 1 interrupción cada 10 min** | Spam mata la utilidad |
| **Prioridad** | Emergencia > Petición > Saludo > Trivial |
| **Horario** | No hablar fuera del horario configurado |
| **Aprendizaje** | No repetir cosas que el usuario ya sabe |

### Lo que cambia en el pipeline actual

```
ANTES:  wake("YARTIS") → graba(3s) → transcribe → responde
AHORA:  ambient(modelo ligero) → detecta(intención) → responde O sesión
```

La wake word "YARTIS" **no desaparece** — se convierte en una de varias formas de activar. Pero ahora también puedes:
- Decir "hola" y que te responda sin wake word
- Usar tu palabra clave para sesiones largas
- Simplemente hablar y que él detecte si te refiere a él
- Que Yartis sepa el contexto aunque no le hayas hablado directamente

### Fase 2: Servicios + Estabilidad (paralelo a JARVIS)

| Paso | Estado | Detalle |
|------|--------|---------|
| Servicios V2 completados y estables | ⏳ | Todos los servicios del V2 funcionando y probados |
| Sistema de logs y recuperación de errores | ⏳ | Logs por servicio, retry automático |
| Configuración persistente | ⏳ | Preferencias del usuario guardadas |
| Tests automatizados | ⏳ | Cobertura mínima de los servicios core |
| Preparar infraestructura para V4 | ⏳ | Módulo de búsqueda web, sandbox para scripts |

---

## V4 — Skills Generales: Web, Pantalla, Acciones

**Objetivo:** Yartis puede hacer cosas en internet y en la computadora del usuario. Navegar webs, leer pantallas, abrir apps, buscar información, ejecutar tareas complejas.

| Paso | Estado | Detalle |
|------|--------|---------|
| Navegador web integrado | ⏳ | Abrir páginas, buscar, leer contenido, hacer resúmenes |
| Lectura de pantalla | ⏳ | Capturar lo que el usuario ve y entenderlo |
| Ejecución de tareas | ⏳ | Abrir apps, mover archivos, configurar cosas |
| Integración con servicios web | ⏳ | Gmail, Calendar, YouTube, redes sociales |
| Ejecución autónoma | ⏳ | "Oye, busca los mejores restaurantes cerca y dame opciones" |

---

## V5 — Excalidraw + Videos + Generador de Sitios

**Objetivo:** Visualización matemática interactiva, búsqueda de videos como contingencia, y generación autónoma de sitios de estudio completos.

### 5.1 Integración con Excalidraw

```
Script Python genera coordenadas → Se inyectan como vectores en Excalidraw
→ Estudiante modifica valores → Gráfica cambia en tiempo real + IA explica
```

| Paso | Estado | Detalle |
|------|--------|---------|
| Generador de coordenadas desde scripts | ⏳ | Scripts Python calculan puntos, vectores, curvas para problemas matemáticos |
| Inyección dinámica en Excalidraw | ⏳ | Coordenadas se inyectan como elementos vectoriales en el lienzo |
| Interactividad en tiempo real | ⏳ | El estudiante modifica valores en la UI → la gráfica se recalcula y redibuja |
| Explicación vocal de cambios | ⏳ | Cuando cambia un valor, la IA explica por voz qué cambió y por qué |
| Exportación de lienzos | ⏳ | Guardar lienzos como PNG, SVG o JSON de Excalidraw |

### 5.2 Búsqueda y Curación de Videos (Contingencia)

```
Estudiante no entiende → Solicita apoyo visual
→ Yartis busca en YouTube → Filtra → Recomienda
```

| Paso | Estado | Detalle |
|------|--------|---------|
| Detección de "no entiendo" | ⏳ | Cuando el estudiante pide explícitamente videos o la explicación no fue suficiente |
| Búsqueda en YouTube con yt-dlp | ⏳ | Buscar videos educativos del contenido específico |
| Filtrado y ranking | ⏳ | Evaluar calidad: duración, views, rating, relevancia del título |
| Recomendación al estudiante | ⏳ | Presentar los 3-5 mejores videos con resumen de cada uno |
| Resumen de contenido del video | ⏳ | Descargar subtítulos y resumir de qué trata cada video |

### 5.3 Generador Autónomo de Sitios de Estudio

```
Sesión de estudio completa → OpenCode genera sitio web interactivo
→ HTML/CSS/JS con todo: explicación, código, Excalidraw, videos embebidos
```

| Paso | Estado | Detalle |
|------|--------|---------|
| Template de sitio de estudio | ⏳ | HTML/CSS/JS responsive con layout educativo |
| Inyectar explicación del tema | ⏳ | El contenido generado por la IA se vuelca en el sitio |
| Playground de código interactivo | ⏳ | El script Python se embebe en un editor interactivo (tipo CodePen/JSFiddle) |
| Lienzo Excalidraw embebido | ⏳ | El lienzo vectorial se integra en el sitio |
| Videos YouTube embebidos | ⏳ | Los videos recomendados se incrustan con iframe |
| Guardado local | ⏳ | Exportar como archivo HTML único o carpeta de proyecto |
| Despliegue opcional | ⏳ | Opción de subir a hosting (GitHub Pages, Netlify, etc.) para compartir |

---

## V6 — Motor de Renderizado de Video On-Demand

**Objetivo:** Cuando no existan videos adecuados en internet, Yartis se convierte en **creador de contenido educativo**. Genera videos explicativos completos con animación matemática y narración por voz.

### Pipeline de renderizado

```
1. LLM redacta guion corto
2. TTS genera audio narrado
3. Python calcula frames como coordenadas vectoriales Excalidraw
4. Renderiza PNGs secuenciales (simulando animación matemática fluida)
5. FFmpeg compila PNGs a MP4 30FPS
6. Sincroniza audio + animación
7. Entrega video final al estudiante
```

| Paso | Estado | Detalle |
|------|--------|---------|
| Generador de guiones | ⏳ | LLM local redacta guion corto y didáctico para el tema específico |
| Síntesis de voz del guion | ⏳ | Pipeline TTS de Yartis genera el audio narrado |
| Calculadora de frames vectoriales | ⏳ | Script Python calcula las coordenadas de cada frame como elementos Excalidraw |
| Renderizador de frames PNG | ⏳ | Exportar cada frame como imagen PNG secuencial |
| Compilador de video con FFmpeg | ⏳ | `ffmpeg -i frame_%04d.png -i audio.mp3 -c:v libx264 -pix_fmt yuv420p output.mp4` |
| Sincronización audio-video | ⏳ | Alinear duración de frames con duración de audio narrado |
| Calidad y exportación | ⏳ | Resolución configurable (720p/1080p), exportar MP4 final |

### Detalles técnicos del renderizado

- **Formato de frames:** PNG secuenciales (`frame_0001.png`, `frame_0002.png`, ...)
- **FPS:** 30 frames por segundo
- **Codificación:** H.264 (libx264) para compatibilidad universal
- **Audio:** MP3 o AAC sincronizado
- **Resolución:** 1920×1080 (full HD) por defecto, configurable
- **Animación:** Cada frame es una "escena" de Excalidraw con elementos que aparecen/mueven/escalen

---

## V7 — Plataforma de Notas Interactiva (Competencia NotebookLM)

**Objetivo:** Una aplicación que organiza todo el material de estudio del usuario en un solo lugar. Notas, código interactivo, lienzos vectoriales, y especialmente los **videos generados on-demand** para que el usuario pueda repasar y buscar semánticamente en su propia videoteca educativa local.

### Funcionalidades

| Paso | Estado | Detalle |
|------|--------|---------|
| Organización por libretas/materias | ⏳ | Estructura tipo notebook: Matemáticas, Física, Programación, etc. |
| Almacenamiento visual de notas | ⏳ | Cada nota se muestra como card con preview del contenido |
| Código interactivo guardado | ⏳ | Los scripts generados se guardan con su playground interactivo |
| Lienzos vectoriales guardados | ⏳ | Los Excalidraw se almacenan y se pueden reabrir/editar |
| Videoteca educativa local | ⏳ | Todos los videos generados on-demand se guardan localmente |
| Búsqueda semántica | ⏳ | Buscar en todo el material por significado, no solo por palabras clave |
| Repaso inteligente | ⏳ | Sistema de repaso espaciado (spaced repetition) para reforzar aprendizaje |
| Exportación y compartición | ⏳ | Compartir libretas completas con compañeros |

---

## 🔧 Stack Técnico por Versión

| Versión | Stack Principal |
|---------|----------------|
| V2 | Python + WebSocket + sentence-transformers + yt-dlp |
| V3 | V2 + Silero VAD + keyword spotting + session manager |
| V4 | V3 + agent-reach + Playwright/Selenium + screen capture |
| V5 | V4 + Excalidraw API + React + sandbox + LLM local |
| V6 | V5 + FFmpeg + renderizado PNG + sincronización audio/video |
| V7 | V6 + SQLite/localDB + búsqueda semántica + spaced repetition |
| V8/1.0 | V7 + btleplug (BLE) + coordinación multi-dispositivo + sesiones paralelas |

---

## 📊 Resumen Visual

```
V1 ✅ → V2 🔄 → V3 ⏳ → V4 ⏳ → V5 ⏳ → V6 ⏳ → V7 ⏳ → V8/1.0 ⏳
Pipeline    Servicios  JARVIS     Skills      Educación    Renderizado  Plataforma  RELEASE
básico      + clasif.  Escucha    generales   + matemáticas de video     de notas    FINAL
                       Continua   (web/screen) Excalidraw  on-demand
```

---

## V8/1.0 — RELEASE FINAL

**Objetivo:** Pulir todo, testear todo, documentar todo. Yartis listo para el mundo. Incluye coordinación multi-dispositivo con BLE.

| Paso | Estado | Detalle |
|------|--------|---------|
| Testeo completo de todas las versiones | ⏳ | Cada feature probada de extremo a extremo |
| Rendimiento optimizado | ⏳ | CPU, RAM, latencia en todos los modos |
| Documentación de usuario | ⏳ | Guía de instalación, configuración, uso |
| Instalador multiplataforma | ⏳ | Windows, Linux, macOS |
| Feedback de usuarios reales | ⏳ | Beta testing con usuarios externos |
| Bugs finales | ⏳ | Los últimos ajustes antes del release |
| **Coordinación multi-dispositivo (BLE)** | ⏳ | Descubrimiento de Yartis en la red, coordinación por Bluetooth Low Energy, priorización de dispositivos |
| **Sesiones paralelas** | ⏳ | Múltiples usuarios pidiendo cosas al mismo tiempo, scheduling por prioridad + tiempo estimado |
| **Fallback sin red** | ⏳ | Coordinación por audio ("si escucho al otro hablando, me callo") |

---

## 🧠 Filosofía del Proyecto

1. **El LLM solo orquesta** — los scripts ejecutan todo. Control total de tokens.
2. **Aprendizaje incremental** — cada versión construye sobre la anterior.
3. **Local primero** — todo corre en la máquina del usuario cuando es posible.
4. **Validación antes de confiar** — scripts se validan en sandbox antes de guardarse.
5. **El estudiante tiene el control** — puede modificar, entender, y compartir todo lo que genera.

---

## 📝 Notas de Implementación

- **Agent Reach** ya está instalado (v1.5.0) — sirve para la búsqueda web del V4
- **Strix** está instalado en WSL — para pentesting cuando haya servicios
- **Excalidraw** tiene API pública para inyección de elementos vectoriales
- **FFmpeg** se puede instalar con `winget install ffmpeg`
- **Ollama** para LLM local sin costo de tokens
- **yt-dlp** ya se usa en el proyecto para música — extenderlo a videos educativos

---

*Última actualización: 14-Jul-2026*
*Creado por: Gemini (recopilación) + OpenCode (estructura) + Usuario (visión JARVIS)*
