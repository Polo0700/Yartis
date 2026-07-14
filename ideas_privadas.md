# Ideas Privadas

## Ahorro de tokens en desarrollo

**codebase-memory-mcp** — Servidor MCP que indexa codebases en un grafo de conocimiento.

- **Qué hace:** Parsea código fuente con tree-sitter y crea un grajo de funciones, clases, llamadas, imports, etc.
- **Por qué sirve:** Cuando OpenCode/Claude Code necesita entender el código, hace una query al grafo en vez de leer 15-30 archivos. Ahorra ~120x tokens por query.
- **Para Yartis:** Útil cuando el proyecto crezca con 10+ servicios. Sin el grafo, cada búsqueda del agente gasta miles de tokens.
- **Link:** https://github.com/DeusData/codebase-memory-mcp
- **Soporte:** OpenCode ya es compatible, solo hay que configurar el MCP server.
- **Costo:** Gratis, corre local, sin API keys.

## Modo Desarrollador con codebase-memory-mcp

**Idea:** Instalar codebase-memory-mcp pero solo activarlo cuando el usuario enciende "modo desarrollador" en opciones.

- **Por qué:** No tiene sentido correr un indexador de código cuando el usuario solo usa Yartis para voz, música, etc.
- **Cómo:**
  - Toggle en UI React para activar/desactivar modo dev
  - Tauri (Rust) levanta/apaga el MCP server según el toggle
  - OpenCode usa las queries del grafo solo en modo dev
- **Ventajas:**
  - Sin carga de RAM cuando no se necesita
  - El usuario decide cuándo usarlo
  - No rompe el flujo normal de Yartis
- **Estado:** Idea pendiente

## Agent Reach — Internet para el asistente

**Link:** https://github.com/Panniantong/Agent-Reach

- **Qué hace:** Le da a un agente AI la capacidad de leer y buscar en múltiples plataformas de internet (Twitter, YouTube, Reddit, GitHub, Bilibili, XiaoHongShu, etc.) sin pagar APIs.
- **Plataformas:** Web, YouTube, Twitter, Reddit, GitHub, Bilibili, XiaoHongShu, LinkedIn, Facebook, Instagram, RSS, búsqueda general (Exa)
- **Para Yartis:** Si Yartis tiene internet, podría buscar info en redes sociales, resumir videos, leer RSS, buscar en la web.
- **Costo:** Gratis, corre local, sin API keys (excepto proxies para servidores ~$1/mes)
- **Soporte:** Compatible con cualquier agente que ejecute comandos (Claude Code, OpenCode, Cursor, etc.)
- **Instalación:** `pip install agent-reach` o darle el link al agente y se auto-instala
- **Estado:** INSTALADO (v1.5.0)
- **Canales activos (6/15):** GitHub, YouTube, V2EX, RSS, Web (Jina Reader), Bilibili (parcial)
- **Pendiente:** Búsqueda web (mcporter + Exa), Twitter, Reddit, Facebook, Instagram, XiaoHongShu

## YouTube Timestamp Finder (feature para Yartis)

**Flujo:**
1. Usuario pregunta: "¿cuándo tengo que tirar por Himeko Nova?"
2. OpenCode detecta keywords → envía al script
3. Script busca keywords en subtítulos → extrae solo texto relevante con timestamps
4. Modelo lee solo ese texto → escupe el timestamp exacto

**Ahorro:** En vez de leer 500 líneas de subtítulos, lee 5-10 líneas relevantes.

**Implementación:**
- Script Python que descarga subtítulos y busca por keywords
- Extrae contexto alrededor de las coincidencias (±30 segundos)
- Devuelve timestamp + texto limpio
- OpenCode procesa el resultado y le dice al usuario el momento exacto

**Estado:** Pendiente de implementar por el usuario

## Strix — Pentesting con AI

**Link:** https://github.com/usestrix/strix

- **Qué hace:** Agentes autónomos de AI que hacen pentesting a tu app — encuentran vulnerabilidades, generan exploits PoC, y proponen patches.
- **Vulnerabilidades detectadas:** SQL injection, XSS, SSRF, auth bypass, IDOR, business logic flaws, JWT attacks, cloud misconfigs, API security, etc.
- **Stack:** Python + Docker (sandbox) + Multi-agente
- **Para Yartis:** Cuando tenga servicios (correo, telegram, auth), usar Strix para testear que no tenga vulnerabilidades de seguridad.
- **Costo:** Gratis (necesita API key de LLM para los agentes)
- **Uso:** `strix --target ./yartis-app`
- **Estado:** INSTALADO (v1.0.4) en WSL + Docker v29.6.1 en Windows
- **Pendiente:** Configurar API key de LLM para empezar a usar
- **Nota:** Strix se instaló en WSL (Linux), no en Windows nativo. Se ejecuta con `wsl -e strix`

## Yartis CPU vs GPU (dos versiones)

**Idea:** Tener dos versiones de Yartis según el hardware del usuario.

**Yartis CPU:**
- faster-whisper (modo CPU)
- Piper TTS
- openwakeword
- Funciona en cualquier PC sin GPU
- Más ligero, menos requisitos

**Yartis GPU:**
- Parakeet (NVIDIA CUDA) — 4x más rápido que Whisper
- Modelos más grandes
- Requiere GPU NVIDIA
- Para usuarios con hardware potente

**Por qué:** No todos tienen GPU NVIDIA. Con dos versiones, Yartis llega a más usuarios.

**Link Parakeet:** https://github.com/Zackriya-Solutions/meetily (usa Parakeet)
**Link faster-whisper:** https://github.com/SYSTRAN/faster-whisper

**Estado:** Idea pendiente

## PDF → Markdown para ahorrar tokens

**Idea:** Cuando un usuario pase un documento PDF, convertirlo a Markdown antes de pasárselo a OpenCode.

**Por qué:** Leer un PDF directamente gasta muchos tokens. Leer Markdown gasta mucho menos.

**Implementación:**
- Usar PyMuPDF para extraer texto del PDF
- Convertir a Markdown limpio
- OpenCode lee el Markdown en vez del PDF

**Código básico:**
```python
import pymupdf

doc = pymupdf.open("documento.pdf")
text = ""
for page in doc:
    text += page.get_text()
```

**Link:** https://github.com/interviewstreet/hiring-agent (usa PyMuPDF para PDF → MD)

**Estado:** Idea pendiente

## YouTube Summarizer con Mistral (sin gastar tokens de OpenCode)

**Idea:** Resumir videos de YouTube usando Mistral gratis en vez de OpenCode.

**Flujo:**
1. Descargar subtítulos — yt-dlp (sin modelo)
2. Filtrar texto — Búsqueda simple (sin modelo)
3. Resumir con Mistral — Gratis (sin modelo local)
4. Consultas del usuario — Mistral responde

**Ventajas:**
- OpenCode no ve el video ni los subtítulos
- Mistral es gratis (1B tokens/mes)
- No ocupa RAM local
- El usuario puede preguntar sobre el video

**Ejemplo de uso:**
```
Usuario: "¿de qué trata el video?"
Yartis: "El video explica cómo crear una API con Python"
```

**Link:** https://github.com/diegosouzapw/OmniRoute (Gateway AI con Mistral gratis)

**Estado:** Idea pendiente

## OmniRoute — Gateway AI para Yartis

**Link:** https://github.com/diegosouzapw/OmniRoute

- **Qué hace:** Gateway AI que conecta 250+ providers a un solo endpoint. Auto-fallback, compresión de tokens (15-95%), 90+ providers gratis.
- **Para Yartis:** Usar OmniRoute como router de LLMs en vez de depender de un solo provider. Así no nos quedamos sin tokens.
- **Tokens gratis:** ~1.6B tokens/mes (Mistral 1B, Gemini 60M, Groq 15M, etc.)
- **Instalación:** `npm install omniroute`
- **Estado:** PENDIENTE DE INSTALAR

## Roadmap Completo V4-V7 (Autoaprendizaje + Excalidraw + Video On-Demand + Plataforma de Notas)

**Archivo:** `ROADMAP.md` — Documento oficial con todo el roadmap detallado.

**Resumen ejecutivo:**
- **V4:** Autoaprendizaje (detectar vacíos → buscar → generar script → validar → guardar) + Explicador de código con IA local
- **V5:** Excalidraw interactivo (coordenadas → vectores → interactividad) + Búsqueda de videos (yt-dlp) + Generador de sitios de estudio
- **V6:** Motor de renderizado de video on-demand (guion → TTS → frames PNG → FFmpeg → MP4)
- **V7:** Plataforma de Notas Interactiva (competencia NotebookLM con videoteca local)

**Estado:** Roadmap documentado. Pendiente de implementar a partir del V3.

## Automatización web con Mistral + Playwright (sin tokens de OpenCode)

**Idea:** Usar Mistral gratis para interpretar la intención del usuario y generar código Playwright, ejecutar con Python.

**Flujo:**
1. Usuario dice: "Click login"
2. Mistral interpreta → genera código Playwright
3. Python ejecuta → 0 tokens adicionales

**Ventajas:**
- Mistral gratis interpreta (1B tokens/mes)
- Playwright ejecuta sin tokens
- OpenCode no participa
- Más preciso que PageAgent

**Ejemplo de uso:**
```
Usuario: "Llená el formulario con mi nombre"
Mistral: Interpreta → genera código Playwright
Python: Ejecuta → formulario llenado
```

**Link:** https://github.com/alibaba/page-agent (referencia, pero usamos Playwright)

**Estado:** Idea pendiente
