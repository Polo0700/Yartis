---
name: css-core
description: Modern CSS — layouts (Flexbox/Grid), responsive design, custom properties, animations, TailwindCSS, and dark theme for voice assistant UIs.
---

# CSS Core

> Modern CSS is powerful — layouts, animations, theming, all without preprocessors.

## When to Activate

- Layout design (Flexbox, Grid)
- Responsive/mobile-first design
- Dark theme and custom properties
- Animations and transitions
- TailwindCSS utility classes
- Voice assistant UI styling

## Layout Patterns

### Flexbox (one-dimensional)
```css
/* Centering */
.center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Status bar */
.status-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
```

### CSS Grid (two-dimensional)
```css
/* App layout */
.app-layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
}

/* Message list */
.messages {
  display: grid;
  gap: 1rem;
  overflow-y: auto;
}
```

## Custom Properties (Theming)

```css
:root {
  /* Dark theme (JARVIS-like) */
  --color-bg: #0a0a0a;
  --color-surface: #1a1a2e;
  --color-primary: #00d4ff;
  --color-text: #e0e0e0;
  --color-text-muted: #888;
  --color-success: #00ff88;
  --color-error: #ff4444;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  
  /* Typography */
  --font-mono: 'Cascadia Code', 'Fira Code', monospace;
  --font-sans: 'Inter', system-ui, sans-serif;
  
  /* Animations */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
}

/* Light theme support */
@media (prefers-color-scheme: light) {
  :root {
    --color-bg: #f5f5f5;
    --color-surface: #ffffff;
    --color-text: #1a1a1a;
  }
}
```

## Yartis Voice UI Patterns

### Status dot animation
```css
.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  transition: background var(--transition-normal);
}

.status-dot.idle {
  background: #666;
}

.status-dot.listening {
  background: var(--color-success);
  animation: pulse 1.5s ease-in-out infinite;
}

.status-dot.processing {
  background: var(--color-primary);
  animation: spin 1s linear infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--color-success); }
  50% { box-shadow: 0 0 0 8px transparent; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Voice wave animation
```css
.voice-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 40px;
}

.voice-wave span {
  width: 4px;
  background: var(--color-primary);
  border-radius: 2px;
  animation: wave 0.8s ease-in-out infinite alternate;
}

.voice-wave span:nth-child(2) { animation-delay: 0.1s; }
.voice-wave span:nth-child(3) { animation-delay: 0.2s; }
.voice-wave span:nth-child(4) { animation-delay: 0.3s; }
.voice-wave span:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
  from { height: 8px; }
  to { height: 32px; }
}
```

### Chat bubbles
```css
.message {
  max-width: 80%;
  padding: var(--space-md);
  border-radius: 12px;
  line-height: 1.5;
}

.message.user {
  align-self: flex-end;
  background: var(--color-primary);
  color: #000;
  border-radius: 12px 12px 0 12px;
}

.message.yartis {
  align-self: flex-start;
  background: var(--color-surface);
  border-radius: 12px 12px 12px 0;
}
```

## Responsive Design
```css
/* Mobile-first */
.container {
  padding: var(--space-md);
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Small screens: voice-first, hide non-essential UI */
@media (max-width: 480px) {
  .settings-panel { display: none; }
  .message { max-width: 90%; }
}
```

## TailwindCSS for React
```tsx
<div className="flex items-center gap-2 p-4 bg-surface rounded-xl">
  <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
  <span className="text-sm text-muted">Escuchando...</span>
</div>
```
