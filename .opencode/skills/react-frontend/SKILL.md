---
name: react-frontend
description: |
  React 19 + TypeScript frontend patterns for Tauri v2 WebView.
  Use when building UI components, event listeners from Rust, speechSynthesis
  TTS, visual feedback animations, and TailwindCSS styling for Yartis.
  Triggers: React, TypeScript, TTS, speechSynthesis, TailwindCSS, Vite, WebView.
---

# React Frontend — Yartis (Tauri WebView)

## Stack
- React 19 + TypeScript
- Vite (bundler, HMR on localhost:3000)
- TailwindCSS (estilos)
- @tauri-apps/api (bridge con Rust)

## Escuchar eventos de Rust

```typescript
import { listen } from "@tauri-apps/api/event";

// Escuchar mensajes del backend Rust
const unlisten = await listen<string>("mensaje", (event) => {
  const texto = event.payload;
  console.log("Respuesta:", texto);
  speak(texto); // sintetizar voz
});

// cleanup al desmontar
unlisten();
```

## Invocar comandos Rust

```typescript
import { invoke } from "@tauri-apps/api/core";

// Llamar un comando Rust
const respuesta = await invoke<string>("ping");
// "pong"

await invoke("iniciar"); // iniciar sidecar + WS
await invoke("detener"); // detener sidecar
```

## SpeechSynthesis TTS

```typescript
function speak(text: string) {
  if (!window.speechSynthesis) return;

  // Cancelar speech anterior si sigue hablando
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "es-MX";
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  // Seleccionar voz en español si existe
  const voices = window.speechSynthesis.getVoices();
  const spanishVoice = voices.find(v => v.lang.startsWith("es"));
  if (spanishVoice) utterance.voice = spanishVoice;

  window.speechSynthesis.speak(utterance);
}
```

## Estructura de componentes

```
src/
├── main.tsx          # Entry point
├── App.tsx           # Componente raíz
├── components/
│   ├── StatusBar.tsx # Indicador de estado (escuchando/procesando/respondiendo)
│   ├── ChatBubble.tsx # Burbuja de conversación
│   ├── VoiceIndicator.tsx # Animación de voz activa
│   └── Controls.tsx  # Botones de control
├── hooks/
│   ├── useTauriEvent.ts  # Hook para escuchar eventos Rust
│   ├── useSpeech.ts      # Hook para TTS
│   └── useAppState.ts    # Estado global
├── types/
│   └── index.ts      # Tipos compartidos
└── styles/
    └── index.css     # TailwindCSS + animaciones
```

## Hook useTauriEvent

```typescript
import { useEffect } from "react";
import { listen, UnlistenFn } from "@tauri-apps/api/event";

export function useTauriEvent<T>(
  eventName: string,
  handler: (payload: T) => void
) {
  useEffect(() => {
    let unlisten: UnlistenFn;
    const setup = async () => {
      unlisten = await listen<T>(eventName, (event) => {
        handler(event.payload);
      });
    };
    setup();
    return () => { if (unlisten) unlisten(); };
  }, [eventName, handler]);
}
```

## Animación con TailwindCSS

```tsx
// Indicador de "escuchando" con pulso
function VoiceIndicator({ active }: { active: boolean }) {
  return (
    <div className={`
      w-4 h-4 rounded-full transition-all duration-300
      ${active
        ? "bg-green-500 animate-pulse shadow-lg shadow-green-500/50"
        : "bg-gray-500"
      }
    `} />
  );
}
```

## Tipos compartidos

```typescript
// types/index.ts
export interface AppState {
  status: "idle" | "listening" | "processing" | "speaking";
  message: string;
  error?: string;
}

export interface StatusPayload {
  status: AppState["status"];
  message?: string;
}
```

## Errores comunes

1. **listen no funciona:** El evento debe emitirse desde Rust con `app.emit("nombre", payload)`. El nombre debe coincidir exactamente.
2. **speechSynthesis cortado:** Llamar `cancel()` antes de `speak()` para evitar superposición.
3. **invoke sin await:** Todos los comandos Rust async necesitan `await`.
4. **HMR no actualiza:** Si el backend Rust cambia, Tauri reinicia automáticamente. Si el frontend no, revisar Vite.
