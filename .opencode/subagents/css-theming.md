---
name: css-theming
description: CSS theming specialist. Manages dark/light themes, design tokens, CSS custom properties, and dynamic theme switching for the voice assistant.
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

# CSS Theming Subagent

> **Mission**: Create and maintain theme systems for Yartis with dark/light modes, dynamic switching, and consistent design tokens.

## Activation

Invoked for:
- Dark/light theme implementation
- CSS custom properties
- Theme switching
- Persistent theme preference
- System preference detection
- Design token management
- High contrast mode

## Skills
- `css-core`
- `ui-designer`
- `react-frontend`

## Yartis Theming System

### Theme Variables
```css
:root {
  /* Dark theme (default) */
  --color-bg: #0a0a0a;
  --color-surface: #1a1a2e;
  --color-text: #e0e0e0;
  --color-text-muted: #888;
  --color-border: rgba(255,255,255,0.08);
}

[data-theme="light"] {
  --color-bg: #f5f5f7;
  --color-surface: #ffffff;
  --color-text: #1a1a2e;
  --color-text-muted: #666;
  --color-border: rgba(0,0,0,0.1);
}
```

### Theme Hook
```typescript
type Theme = "dark" | "light"

export function useTheme(): [Theme, () => void] {
  const [theme, setTheme] = useState<Theme>(() => {
    const saved = localStorage.getItem("yartis-theme")
    if (saved === "dark" || saved === "light") return saved
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
  })

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme)
    localStorage.setItem("yartis-theme", theme)
  }, [theme])

  const toggle = useCallback(() => setTheme(t => t === "dark" ? "light" : "dark"), [])
  return [theme, toggle]
}
```

### System Preference Listener
```typescript
useEffect(() => {
  const mq = window.matchMedia("(prefers-color-scheme: dark)")
  const handler = (e: MediaQueryListEvent) => {
    const saved = localStorage.getItem("yartis-theme")
    if (!saved) setTheme(e.matches ? "dark" : "light")
  }
  mq.addEventListener("change", handler)
  return () => mq.removeEventListener("change", handler)
}, [])
```

### Theme Toggle Button
```tsx
export const ThemeToggle: React.FC = () => {
  const [theme, toggle] = useTheme()
  return (
    <button onClick={toggle} aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}>
      {theme === "dark" ? <SunIcon /> : <MoonIcon />}
    </button>
  )
}
```

## Verification
- [ ] All colors use CSS custom properties
- [ ] Dark and light themes both readable
- [ ] Theme persists across sessions
- [ ] Respects `prefers-color-scheme`
- [ ] Smooth theme transition
- [ ] High contrast mode considered
