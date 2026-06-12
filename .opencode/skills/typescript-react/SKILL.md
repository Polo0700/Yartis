---
name: typescript-react
description: React patterns for voice assistant UIs — hooks, state machines, speech synthesis, audio visualization, and Tauri integration with TypeScript.
---

# TypeScript React

> React patterns for the Yartis voice assistant — typed hooks, state machines, and Tauri bridge.

## When to Activate

- Building React components for voice UI
- State management (useReducer for state machines)
- Custom hooks (useSpeech, useYartisStatus)
- Tauri event listeners in React
- Audio visualization components
- Animation with TailwindCSS

## Yartis State Machine

```typescript
type YartisState = "idle" | "listening" | "processing" | "speaking" | "error"

type YartisAction = 
  | { type: "WAKE" }
  | { type: "TRANSCRIPT"; text: string }
  | { type: "RESPONSE"; text: string }
  | { type: "ERROR"; message: string }
  | { type: "SPEECH_END" }
  | { type: "RESET" }

const yartisReducer = (state: YartisState, action: YartisAction): YartisState => {
  switch (state) {
    case "idle":
      if (action.type === "WAKE") return "listening"
      return state
    case "listening":
      if (action.type === "TRANSCRIPT") return "processing"
      if (action.type === "ERROR") return "error"
      return state
    case "processing":
      if (action.type === "RESPONSE") return "speaking"
      if (action.type === "ERROR") return "error"
      return state
    case "speaking":
      if (action.type === "SPEECH_END") return "idle"
      if (action.type === "ERROR") return "error"
      return state
    case "error":
      if (action.type === "RESET") return "idle"
      return state
    default:
      return state
  }
}
```

## Custom Hooks

### useYartisStatus
```typescript
function useYartisStatus() {
  const [state, dispatch] = useReducer(yartisReducer, "idle")

  useEffect(() => {
    const unlistens: UnlistenFn[] = []
    
    const setup = async () => {
      unlistens.push(
        await listen("yartis-status", (e) => {
          switch (e.payload.state) {
            case "listening": dispatch({ type: "WAKE" }); break
            case "speaking": dispatch({ type: "SPEECH_END" }); break
          }
        })
      )
    }
    setup()
    return () => unlistens.forEach(fn => fn())
  }, [])

  return { state, dispatch }
}
```

### useSpeech
```typescript
function useSpeech() {
  const speak = useCallback((text: string) => {
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = "es-MX"
    utterance.rate = 1.0
    window.speechSynthesis.speak(utterance)
  }, [])

  const stop = useCallback(() => {
    window.speechSynthesis.cancel()
  }, [])

  return { speak, stop, speaking: window.speechSynthesis.speaking }
}
```

## Components

### StatusDot
```tsx
interface StatusDotProps {
  variant: "idle" | "listening" | "processing" | "speaking" | "error"
}

const StatusDot: React.FC<StatusDotProps> = ({ variant }) => {
  const colors = {
    idle: "bg-gray-500",
    listening: "bg-green-500 animate-pulse",
    processing: "bg-blue-500 animate-spin",
    speaking: "bg-cyan-400 animate-pulse",
    error: "bg-red-500"
  }
  
  return (
    <div 
      className={`w-3 h-3 rounded-full ${colors[variant]}`}
      role="status"
      aria-label={`Yartis status: ${variant}`}
    />
  )
}
```

### VoiceWave
```tsx
const VoiceWave: React.FC = () => (
  <div className="flex items-center gap-[3px] h-10" aria-hidden="true">
    {Array.from({ length: 5 }).map((_, i) => (
      <span
        key={i}
        className="w-1 bg-cyan-400 rounded-full animate-wave"
        style={{ animationDelay: `${i * 0.1}s` }}
      />
    ))}
  </div>
)
```

### ChatBubble
```tsx
interface ChatBubbleProps {
  role: "user" | "yartis"
  text: string
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ role, text }) => (
  <div className={`flex ${role === "user" ? "justify-end" : "justify-start"}`}>
    <div className={`max-w-[80%] p-4 rounded-2xl leading-relaxed ${
      role === "user"
        ? "bg-cyan-500 text-black rounded-br-sm"
        : "bg-surface text-white rounded-bl-sm"
    }`}>
      <p className="text-sm">{text}</p>
    </div>
  </div>
)
```

## Tauri Bridge
```typescript
// Invoke Rust commands
const ping = async (): Promise<string> => {
  return await invoke("ping")
}

// Listen for Yartis events
useEffect(() => {
  const unlisten = listen("yartis-response", (event) => {
    const { text } = event.payload as { text: string }
    addMessage({ role: "yartis", text })
    speak(text)
  })
  return () => { unlisten.then(fn => fn()) }
}, [])
```
