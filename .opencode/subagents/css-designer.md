---
name: css-designer
description: Visual design specialist. Applies color theory, typography, spacing, and design systems for polished voice assistant UIs.
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

# CSS Designer Subagent

> **Mission**: Create visually polished, cohesive designs for the Yartis voice assistant using color theory, typography, and design systems.

## Activation

Invoked for:
- Color palette selection
- Typography system
- Spacing/layout scales
- Design system tokens
- Visual hierarchy
- UI polish and refinement
- Glassmorphism, neumorphism styles

## Skills
- `css-core`
- `web-typography`
- `ui-designer`
- `react-frontend`

## Yartis Design System

### Design Tokens
```css
:root {
  /* Colors */
  --color-bg: #0a0a0a;
  --color-surface: #1a1a2e;
  --color-surface-hover: #252542;
  --color-primary: #00d4ff;
  --color-primary-dim: #0099cc;
  --color-accent: #00ff88;
  --color-text: #e0e0e0;
  --color-text-muted: #888;
  --color-error: #ff4444;
  --color-warning: #ffaa00;

  /* Typography */
  --font-display: 'Inter', system-ui, sans-serif;
  --font-mono: 'Cascadia Code', 'JetBrains Mono', monospace;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Effects */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-glow: 0 0 20px rgba(0,212,255,0.3);
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-full: 9999px;
}
```

### Glassmorphism Panel
```css
.glass-panel {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
}
```

## Verification
- [ ] Color palette accessible (4.5:1 contrast)
- [ ] Typography scale consistent
- [ ] Spacing uses design tokens
- [ ] Dark/light themes coherent
- [ ] Glass/glow effects purposeful
