---
name: typescript-core
description: TypeScript configuration, strict typing, discriminated unions, type guards, generics, and Tauri/WebSocket type definitions for the Yartis project.
---

# TypeScript Core

> Strict TypeScript with discriminated unions and type-safe Tauri/WebSocket integration.

## When to Activate

- Configuring tsconfig (strict mode, paths)
- Defining types for Tauri commands/events
- WebSocket message types
- React component props (strict + branded types)
- Type guards and discriminated unions

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Yartis Type Definitions

### WebSocket Messages
```typescript
// Discriminated union for all WS messages
type WsMessage = 
  | { type: "transcript"; text: string; confidence: number }
  | { type: "response"; text: string; audio?: string }
  | { type: "status"; state: YartisState }
  | { type: "error"; code: string; message: string }

type YartisState = "idle" | "listening" | "processing" | "speaking" | "error"

// Type guards
function isTranscript(msg: WsMessage): msg is WsMessage & { type: "transcript" } {
  return msg.type === "transcript"
}
```

### Tauri Events
```typescript
// Events emitted from Rust to React
interface TauriEventMap {
  "yartis-status": { state: YartisState }
  "yartis-response": { text: string }
  "yartis-transcript": { text: string; partial: boolean }
  "yartis-error": { code: string; message: string }
}

// Type-safe listener
function listenToYartis<K extends keyof TauriEventMap>(
  event: K,
  handler: (payload: TauriEventMap[K]) => void
): Promise<UnlistenFn> {
  return listen(event, (e) => handler(e.payload as TauriEventMap[K]))
}
```

### React Component Props
```typescript
// Use branded types for safety
type StatusDotVariant = "idle" | "listening" | "processing" | "speaking"

interface StatusDotProps {
  variant: StatusDotVariant
  size?: "sm" | "md" | "lg"
  className?: string
}

interface ChatMessageProps {
  role: "user" | "yartis"
  text: string
  timestamp: Date
}
```

### Speech Synthesis
```typescript
interface SpeechState {
  speaking: boolean
  paused: boolean
  text: string
  lang: string  // "es-MX" | "en-US"
}

// Type-safe utterance config
const createUtterance = (text: string, lang = "es-MX"): SpeechSynthesisUtterance => {
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = lang
  utterance.rate = 1.0
  utterance.pitch = 1.0
  return utterance
}
```

## Utility Types
```typescript
// Result type for fallible operations
type Result<T, E = Error> = 
  | { ok: true; value: T }
  | { ok: false; error: E }

// Async state
type AsyncState<T> = 
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: string }

// Branded types for domain primitives
type Email = string & { readonly __brand: "email" }
type UserId = string & { readonly __brand: "userId" }
```
