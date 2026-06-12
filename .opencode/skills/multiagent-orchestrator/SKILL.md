---
name: multiagent-orchestrator
description: |
  Multi-agent orchestration with background parallel tasks and shared memory.
  Use when delegating work to other agents in parallel (investigar, revisar código,
  analizar archivos) without blocking the conversation with the user.
  Triggers: multiagent, orchestrador, background task, parallel agent, detach,
  investiga en paralelo, revisa mientras, lanza en background, task.json, memory.json
---

# Multi-agent Orchestrator

Hay **dos formas** de lanzar agentes en background:

| Script | Líneas | Cuándo usarlo |
|--------|:------:|---------------|
| `run-agent.py` | **~65** (fast path) | Un solo agente, sin dependencias. **Recomendado.** |
| `multiagent.py` | ~470 (full) | Múltiples agentes con DAG de dependencias o `--watch` |

> ⚡ `multiagent.py --agent X --prompt Y --detach` **delega automáticamente** a `run-agent.py`.

## Archivos clave

| Path | Propósito |
|------|-----------|
| `.opencode/agent/run-agent.py` | Fast path monocanal (~65 líneas) |
| `.opencode/agent/multiagent.py` | Orquestador multi-agente completo |
| `.multiagent/memory.json` | Memoria compartida (persiste entre sesiones) |
| `.multiagent/logs/` | Logs por tarea |

## Modos de uso

### 1. Single-agent background (`--detach`) — lanzar y olvidar

```bash
python .opencode/agent/run-agent.py --agent <nombre> --prompt "<tarea>" --detach
```

- Devuelve el control **inmediatamente**
- El proceso corre aunque el TUI se cierre
- Útil para: investigar, revisar código, análisis pesados
- Crea `.multiagent/memory.json` con status + output

### 2. Batch con dependencias

```json
{
  "parallel": 2,
  "tasks": [
    {"id": "r1", "agent": "rust-expert",   "prompt": "analiza Cargo.toml",   "deps": []},
    {"id": "t1", "agent": "typescript-expert", "prompt": "analiza package.json", "deps": []},
    {"id": "s1", "agent": "python-expert",  "prompt": "genera reporte",       "deps": ["r1", "t1"]}
  ]
}
```

```bash
python .opencode/agent/multiagent.py tasks.json
```

Round 1: `r1` + `t1` en paralelo. Round 2: `s1` cuando ambos terminan.

### 3. Observador en vivo (`--watch`)

```bash
python .opencode/agent/multiagent.py --watch
```

Notifica en terminal cuando un agente cambia de estado. Opcional `--notify` para Windows Toast.

## Memoria compartida

Los agentes se coordinan vía `.multiagent/memory.json`:

```json
{
  "agents": {
    "python-expert": {
      "status": "completed",
      "messages": ["2026-06-09: creado reporte"],
      "output": { "files": ["reporte.md"], "api": "funcion_x" }
    }
  }
}
```

- Cada agente **escribe solo en su sección**
- Cada agente **lee todas las secciones** para contexto
- Persiste entre sesiones — los agentes acumulan conocimiento

## Protocolo para agentes

Cuando quieras delegar trabajo en background:

1. Usa `bash` para lanzar con `--detach`:
   - **Un solo agente:** `python .opencode/agent/run-agent.py --agent X --prompt "..." --detach`
   - **Múltiples agentes:** `python .opencode/agent/multiagent.py tasks.json --detach`
2. Sigue conversando con el usuario (el proceso corre solo)
3. Minutos después, lee `.multiagent/memory.json` y reporta los resultados

### NO uses para

- Tareas simples que puedes responder ya
- Lo que el usuario necesita ver inmediatamente
- Tareas que modifican los mismos archivos que estás editando tú

---

## 💰 Cost Model (no ignores los tokens)

Los agentes consumen tokens. Cada `--detach` cuesta dinero. Si no lo monitoreas, te puedes llevar una sorpresa.

### Reglas prácticas

| Situación | Qué modelo usar | Costo relativo |
|-----------|----------------|----------------|
| Investigar docs, buscar en web | Modelo barato (fast) | 🟢 Bajo |
| Revisar código, análisis simple | Modelo mediano (balanced) | 🟡 Medio |
| Generar arquitectura, debug complejo | Modelo premium (quality) | 🔴 Alto |

### Cómo aplica

```bash
# barato — investigación (single agent, fast path)
python .opencode/agent/run-agent.py --agent python-expert --prompt "..."

# premium — arquitectura
python .opencode/agent/run-agent.py --agent rust-expert --prompt "..."
```

### Anti-patrones de costo

- ❌ Lanzar 5 agentes premium para tareas que hace un grep
- ❌ Contextos larguísimos "por si acaso" — pon solo lo necesario
- ❌ No revisar memory.json y relanzar lo mismo
- ✅ Usa `--profile fast` por defecto, `quality` solo cuando toca

---

## 🔄 Estrategia de Error Recovery

Los agentes fallan. Timeouts, alucinaciones, APIs caídas. **No es excepción, es operación normal.**

### Pirámide de recuperación

```
         ╱  Escalar al humano  ╲       ← si nada funciona
        ╱─── Circuit breaker ───╲      ← evitar loops infinitos
       ╱───── Fallback path ────╲      ← ruta alternativa
      ╱─────── Retry + backoff ──╲     ← reintentar con espera
     ╱───────── Log + checkpoint ─╲    ← guardar estado antes
```

### Implementación práctica

```python
# Ejemplo de retry con backoff
import time, random

def lanzar_con_reintento(comando, max_intentos=3):
    for intento in range(max_intentos):
        try:
            resultado = ejecutar(comando)
            return resultado
        except TimeoutError:
            espera = (2 ** intento) + random.uniform(0, 1)
            log(f"Intento {intento+1} falló, esperando {espera:.1f}s...")
            time.sleep(espera)
    escalar_al_humano(f"Fallo tras {max_intentos} intentos: {comando}")
```

### Lo que NO hacer

- ❌ Reintentar sin límite — adiós tokens
- ❌ Ignorar el error y seguir como si nada — builds rotos, datos corruptos
- ❌ Asumir que el agente siempre devuelve JSON válido
- ✅ Siempre validar el output del agente antes de usarlo

---

## 🧬 Agent Identity (cada agente necesita personalidad)

Un agente sin identidad arranca en blanco cada vez. Con identidad, recuerda qué es, qué sabe hacer y cómo quiere que le hablen.

### Archivo de identidad por agente

```
.opencode/
  agents/
    python-expert/
      identity.md    ← quién es, qué sabe, cómo responder
    rust-expert/
      identity.md
```

### Ejemplo `identity.md`

```markdown
# python-expert
## Rol
Experto en Python para Yartis. Escribo código limpio con type hints.

## Lo que sé
- faster-whisper, pyaudio, noisereduce
- asyncio, websockets, FastAPI
- numpy, scipy para audio

## Cómo respondo
- Primero explico, luego codeo
- Siempre pongo type hints
- Si algo es riesgo de seguridad, lo digo antes

## Memoria
- Prefiero uv sobre pip
- El proyecto usa Python 3.13+
- No toco Rust ni TypeScript
```

### Por qué funciona

- ✅ El agente sabe su alcance — no se sale de su dominio
- ✅ El tono es consistente entre sesiones
- ✅ No repite errores que ya aprendió
- ✅ Puedes darle instrucciones permanentes sin repetirlas

---

## 🧠 Arquitectura de Memoria (no solo memory.json)

Un agente que olvida todo cada noche no acumula experiencia. Necesitas **capas** de memoria.

### Las 4 capas

| Capa | Qué guarda | Dónde | Se borra |
|------|-----------|-------|----------|
| **Sesión** | Contexto de la conversación actual | RAM del prompt | Al cerrar |
| **Working** | Tareas de hoy, decisiones recientes | `.multiagent/working/` | Diario o semanal |
| **Largo plazo** | Conocimiento curado que persiste | `.multiagent/memory.json` | Nunca (manual) |
| **Procedural** | Cómo hacer tareas específicas | `.opencode/agents/*/identity.md` | Nunca |

### Cómo implementarlo en Yartis

```
.multiagent/
  memory.json          ← largo plazo (persiste siempre)
  working/
    2026-06-10.md      ← tareas de hoy
  logs/
    tarea-001.log
```

### Reglas

- **memory.json** — solo información curada, no basura. Si un agente alucinó, no lo guardes.
- **working/** — útil para sesiones largas, se archiva al terminar el día.
- **identity.md** — lo más estable, solo cambia cuando el rol del agente evoluciona.

---

## ✅ Evaluación (¿cómo sabes que tu agente funciona?)

Sin evaluaciones, estás adivinando. No necesitas nada fancy — una checklist basta.

### Evaluación mínima por agente

```markdown
## Test: python-expert investiga librería X

### Prompt de prueba
"Busca la última versión de noisereduce y dime si es compatible con Python 3.13"

### Criterios de aceptación
- [ ] Devuelve un número de versión
- [ ] Menciona compatibilidad con CPython
- [ ] No alucina features que no existen

### Resultado
- [ ] Pasa
- [ ] Falla parcial (describir)
- [ ] Falla total
```

### Pipeline de eval (opcional)

```
1. Tienes 5 prompts de prueba por agente → los corres a mano
2. Cuando confías, automatizas: script que lanza los 5 y compara outputs
3. Cuando cambias algo, re-corres los 5 para ver si algo se rompió
```

### Señales de que necesitas evaluación

- El agente a veces funciona y a veces no, y no sabes por qué
- Cambiaste el prompt y no sabes si mejoró o empeoró
- El agente alucina respuestas con confianza

---

## 🧠 Cómo aprender a hacer agentes (y no autosabotearte)

*Sección escrita para Yartis, basada en experiencia real construyendo un sistema multiagente.*

### 🚧 Los 10 pecados del que construye agentes

| # | Pecado | Síntoma | Solución |
|---|--------|---------|----------|
| 1 | **Querer hacer el agente perfecto** | Pasas días diseñando cuando podrías estar probando | Haz el agente más estúpido que funcione, luego mejora |
| 2 | **No tener un caso real** | Construyes un framework genérico que no resuelve nada | Cada agente nace de un problema concreto, no al revés |
| 3 | **No leer el output del agente** | Lanzas tareas y nunca revisas los resultados | memory.json existe para eso — léelo siempre |
| 4 | **Poner todos los huevos en un agente** | Un solo agente hace de todo y explota | Divide y vencerás: un agente = una responsabilidad |
| 5 | **Ignorar los errores** | El agente falla y sigues como si nada | Los logs están en `.multiagent/logs/`. Revísalos. Retry + backoff. |
| 6 | **Sobreingeniería temprana** | DAGs, colas, Redis, workers... para una app que aún no existe | `--detach` es suficiente para empezar |
| 7 | **No pedir ayuda al agente** | Te quedas atorado horas sin delegar | Si algo es investigable, lanza un agente |
| 8 | **Ignorar el costo de tokens** | Lanzas 5 agentes premium para tareas simples y el presupuesto vuela | Perfil `fast` por defecto, `quality` solo cuando toca |
| 9 | **Sin identidad ni memoria persistente** | El agente repite errores, no recuerda preferencias, arranca en blanco | Dale `identity.md` + capas de memoria (sesión/working/largo plazo) |
| 10 | **Sin evaluación** | No sabes si el agente mejoró o empeoró cuando cambias algo | 5 prompts de prueba por agente, correr antes/después de cambios |

### 🧪 Cómo aprender de verdad (no solo leer)

1. **Empieza con un agente que haga UNA cosa** — que busque en Google y te traiga resultados. Nada más.
2. **Luego dale memoria** — que recuerde lo que ya investigó.
3. **Luego ponle dependencias** — que espere a que otro agente termine.
4. **Luego ponle un loop** — que se autoejecute cada cierto tiempo.

**La regla de oro:** si tu agente no resuelve un problema que TENÍAS ayer, es overengineering.

### 🔄 Lecciones del proyecto Yartis

- **Los agentes paralelos se pisaron** porque ambos se llamaban `python-expert` y compartían memory.json. Lección: **nombres únicos por tarea.**
- **El modo `--detach` funciona** pero hay que acordarse de revisar los resultados después.
- **Los agentes alucinan si no les das suficiente contexto** en el prompt.
- **Un diagrama de 63 nodos salva más tiempo que 10 agentes corriendo.** El mapa mental primero, los agentes después.
- **Cada agente necesita identidad** — sin `identity.md`, el agente no sabe su alcance ni cómo responder.
- **Error recovery no es opcional** — los agentes fallan en silencio. Retry + backoff + logs o se pierde el trabajo.
- **Los tokens no son gratis** — lanzar 3 agentes premium porque sí cuesta como 30 ejecuciones de código local.

### 📚 Orden recomendado para aprender

```
1. Haz prompts manuales           →  entiendes qué funciona
2. Automatiza con --detach        →  aprendes a delegar
3. Ponles memoria compartida      →  aprendes coordinación
4. Haz un pipeline con deps       →  aprendes orquestación
5. Refina y simplifica            →  aprendes a no sobreingenieriar
```

### 🚩 Bandera roja de autosabotaje

Si te encuentras diciendo cualquiera de estas, **para**:

- "Voy a hacer un framework de agentes primero"
- "Necesito una cola de mensajes Kafka para esto"
- "Mejor espero a tener el diseño perfecto"
- "Esto se puede resolver con un script de 10 líneas pero voy a usar agentes"

### ✅ Checklist diario para no sabotearse

- [ ] ¿Estoy resolviendo un problema real que tengo AHORA?
- [ ] ¿Puedo hacerlo más simple?
- [ ] ¿Ya revisé el output del último agente que lancé?
- [ ] ¿Le puse un nombre único a la tarea?
- [ ] Si falla, ¿tengo logs para saber por qué?
- [ ] ¿Esto reemplaza o complementa lo que ya tengo?
- [ ] ¿Estoy usando el perfil de modelo adecuado (fast vs quality)?
- [ ] ¿El agente tiene identity.md con su alcance y reglas?
- [ ] Si cambio algo, ¿tengo una evaluación para saber si mejoró?
