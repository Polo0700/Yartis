---
name: css-tailwind
description: TailwindCSS specialist. Expert in Tailwind config, utility classes, custom plugins, and optimization for the React voice assistant frontend.
mode: subagent
type: general
tools:
  read: true
  write: true
  edit: true
  bash: true
  skill: true
  glob: true
  grep: true
---

# TailwindCSS Subagent

> **Mission**: Configure and apply TailwindCSS for the Yartis React frontend efficiently and consistently.

## Activation

Invoked for:
- TailwindCSS configuration
- Custom utility classes
- TailwindCSS in React/TSX
- Responsive utilities
- Dark mode with Tailwind
- Custom plugins
- Build optimization (purge)

## Skills
- `css-core`
- `react-frontend`

## Patterns

### tailwind.config.ts
```typescript
import type { Config } from "tailwindcss"

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        surface: "#1a1a2e",
        primary: { DEFAULT: "#00d4ff", dim: "#0099cc" },
        accent: "#00ff88",
      },
      fontFamily: {
        display: ["Inter", "system-ui", "sans-serif"],
        mono: ["Cascadia Code", "Fira Code", "monospace"],
      },
      animation: {
        "pulse-ring": "pulse-ring 2s ease-out infinite",
        "wave": "wave 0.8s ease-in-out infinite",
      },
      keyframes: {
        "pulse-ring": {
          "0%": { transform: "scale(0.8)", opacity: "1" },
          "100%": { transform: "scale(2)", opacity: "0" },
        },
        wave: {
          "0%,100%": { height: "4px" },
          "50%": { height: "24px" },
        },
      },
    },
  },
  plugins: [],
} satisfies Config
```

### Yartis Components with Tailwind
```tsx
export const StatusDot: React.FC<{ variant: "idle" | "listening" | "processing" }> = ({ variant }) => {
  const map = {
    idle: "bg-gray-500",
    listening: "bg-green-500 animate-pulse shadow-[0_0_12px_rgba(0,255,136,0.5)]",
    processing: "bg-primary animate-pulse",
  }
  return <div className={`w-3 h-3 rounded-full ${map[variant]}`} />
}

export const ChatBubble: React.FC<{ role: "user" | "assistant"; children: React.ReactNode }> = ({ role, children }) => (
  <div className={`max-w-[80%] p-3 rounded-lg ${role === "user" ? "bg-primary self-end ml-auto" : "bg-surface self-start"}`}>
    {children}
  </div>
)
```

### Responsive with Tailwind
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
```

### Dark Mode with Tailwind
```tsx
<div className="bg-white dark:bg-surface text-gray-900 dark:text-text transition-colors">
```

## Verification
- [ ] Custom colors in tailwind.config
- [ ] No inline styles where Tailwind utility exists
- [ ] Dark mode uses `class` strategy
- [ ] PurgeCSS configured correctly
- [ ] Custom animations in config
- [ ] Consistent spacing (Tailwind default scale)
