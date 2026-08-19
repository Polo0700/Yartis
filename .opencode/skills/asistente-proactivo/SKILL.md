---
name: asistente-proactivo
description: "Asistente IA que habla sin que le pidan — detecta contexto, prioriza, y avisa solo cuando importa."
---

# Asistente Proactivo 

## Visión

Invertir el flujo: que el **agente IA te hable a ti** sin necesidad de que tú le pidas nada.

```
Flujo normal (Reactivo):  Tú preguntas  →  Yo respondo
Flujo nuevo (Proactivo):  Yo detecto    →  Yo te aviso
```

## Cómo funciona

Un loop en background que ejecuta continuamente:

```
Mientras el usuario trabaja:
  1. Observar contexto actual
     - ¿Qué archivos se modificaron?
     - ¿Hay errores en la terminal?
     - ¿Cuánto tiempo lleva sin hablar?
     - ¿Hay procesos bloqueados?
     - ¿Es un buen momento para interrumpir?

  2. Evaluar relevancia (umbral de silencio)
     - Si el usuario está en flow (escribiendo seguido) → NO interrumpir
     - Si el usuario está en pausa (>2 min sin acción) → se puede hablar
     - Si es una alerta real (error, bug, peligro) → prioridad alta

  3. Entregar mensaje corto
     - "Oye, ya terminó el build"
     - "Encontré algo raro en server.py"
     - "¿Sabías que OpenCode tiene X feature?"
     - Silencio si no hay nada útil que decir
```

## Reglas de No-Molestar

| Regla | Explicación |
|-------|-------------|
| **No interrumpas en flow** | Si detectas ediciones frecuentes, espera |
| **Mensajes < 15 palabras** | Proactivo no significa charlatán |
| **Máximo 1 cada 10 min** | Spam mata la utilidad |
| **Prioridad de temas** | Errores > sugerencias > tips > trivial |
| **Calles de aprendizaje** | No repetir tips que ya sabes |

## Integración con Yartis

- Yartis podría tener un modo "Proactivo" donde él habla primero
- Ejemplo: termina de transcribir y dice *"Oye, encontré esto en la documentación"*
- O cuando llevas horas sin commit: *"¿Confirmamos lo que llevas?"*

## Estados del agente

```
 Durmiendo  —  esperando contexto interesante
 Evaluando  —  viendo si vale la pena hablar
 Hablando   —  te está diciendo algo
 Callado    —  aprendió que no debía hablar aquí
```

## Notas

- Skill pendiente de implementar
- La parte más difícil no es detectar contexto, sino **saber callarse**
- Inspirado en JARVIS con Tony Stark, Kid A en el taller, y el multiagent `--detach`
