# 🗺️ Yartis — Roadmap de Desarrollo

> *"Un asistente de voz que no solo responde, sino que aprende, enseña, crea contenido y genera experiencias de estudio completas."*

---

## Estado Actual

| Versión | Estado | Descripción |
|---------|--------|-------------|
| **V1** | ✅ Completado | Pipeline básico: wake word → grabación → Whisper → OpenCode → TTS |
| **V2** | 🔄 En progreso | WebSocket Hub + Clasificador local + Servicios (Música, Correo, Calendario, Telegram, Navegador) |
| **V3** | ⏳ Pendiente | Servicios completos + estabilidad |
| **V4** | ⏳ Pendiente | Autoaprendizaje + Explicador de código |
| **V5** | ⏳ Pendiente | Excalidraw interactivo + Búsqueda de videos + Generador de sitios |
| **V6** | ⏳ Pendiente | Motor de renderizado de video on-demand |
| **V7** | ⏳ Pendiente | Plataforma de Notas Interactiva (competencia NotebookLM) |

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

## V3 — Estabilidad + Servicios Completos

**Objetivo:** Todos los servicios funcionando de forma confiable. Preparar la base para autoaprendizaje.

| Paso | Estado | Detalle |
|------|--------|---------|
| Servicios V2 completados y estables | ⏳ | Todos los servicios del V2 funcionando y probados |
| Sistema de logs y recuperación de errores | ⏳ | Logs por servicio, retry automático, notificación al usuario cuando algo falla |
| Configuración persistente | ⏳ | Preferencias del usuario guardadas (voz, servicios favoritos, historial) |
| Tests automatizados | ⏳ | Cobertura mínima de los servicios core |
| Preparar infraestructura para V4 | ⏳ | Módulo de búsqueda web, sandbox para scripts, sistema de caché de scripts |

---

## V4 — Autoaprendizaje + Explicador de Código

**Objetivo:** Yartis detecta cuándo no sabe algo, busca la respuesta, genera un script, lo valida, lo guarda permanentemente, y luego lo explica al estudiante con voz.

### 4.1 Detección de Vacíos de Conocimiento

```
Usuario pregunta algo → Clasificador detecta que NO hay servicio preprogramado
→ Se activa el módulo de autoaprendizaje
```

| Paso | Estado | Detalle |
|------|--------|---------|
| Detectar "no sé" / vacío de conocimiento | ⏳ | Cuando el usuario pregunta un teorema, fórmula o problema que no está en los scripts locales |
| Buscar base teórica en internet | ⏳ | Usar agent-reach o web search para encontrar la teoría detrás del problema |
| Generar script Python en tiempo real | ⏳ | LLM genera un script que resuelve el problema específico |
| Validación en sandbox | ⏳ | Ejecutar el script en sandbox aislado, comparar resultados con ejercicios resueltos de fuentes confiables |
| Guardado permanente | ⏳ | Si la validación es exitosa, guardar el script en módulos locales para reutilización futura |
| Cache de scripts aprendidos | ⏳ | Indexar scripts por tema/palabras clave para búsqueda rápida |

### 4.2 Explicador de Código con IA Local

```
Script generado → LLM local lee el código paso a paso
→ Genera explicación conceptual → TTS la pronounce
```

| Paso | Estado | Detalle |
|------|--------|---------|
| Lector de código paso a paso | ⏳ | LLM local lee cada línea del script validado |
| Generador de explicaciones conceptuales | ⏳ | Traduce la lógica de variables a lenguaje humano: "Esta variable guarda la velocidad, y aquí la multiplicamos por el tiempo para obtener la distancia" |
| Integración con pipeline TTS | ⏳ | La explicación se envía por el pipeline de texto a voz de Yartis |
| Modo interactivo | ⏳ | El estudiante puede cambiar valores en la explicación y ver cómo cambia el resultado |

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
| V3 | V2 + logs + tests + config persistente |
| V4 | V3 + agent-reach (búsqueda) + sandbox + LLM local (Ollama/Mistral) |
| V5 | V4 + Excalidraw API + React + yt-dlp (videos) + generador HTML |
| V6 | V5 + FFmpeg + renderizado PNG + sincronización audio/video |
| V7 | V6 + React (UI completa) + SQLite/localDB + búsqueda semántica |

---

## 📊 Resumen Visual

```
V1 ✅ → V2 🔄 → V3 ⏳ → V4 ⏳ → V5 ⏳ → V6 ⏳ → V7 ⏳
Pipeline    Servicios  Estabilidad Auto-       Excalidraw  Renderizado  Plataforma
básico      + clasif.  + tests    aprendizaje  + videos    de video     de notas
                                   + explicador  + sitios    on-demand
```

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
*Creado por: Gemini (recopilación) + OpenCode (estructura)*
