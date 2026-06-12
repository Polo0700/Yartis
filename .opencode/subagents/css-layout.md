---
name: css-layout
description: CSS layout specialist. Expert in Flexbox, CSS Grid, responsive breakpoints, mobile-first design, and complex page layouts for voice assistant UIs.
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

# CSS Layout Subagent

> **Mission**: Build robust, responsive layouts for Yartis using Flexbox, Grid, and mobile-first principles.

## Activation

Invoked for:
- Flexbox layouts
- CSS Grid layouts
- Responsive/mobile-first design
- Complex page structures
- Sidebar/main layouts
- Centering and alignment
- Overflow/scroll handling

## Skills
- `css-core`
- `react-frontend`

## Patterns

### Yartis App Shell (CSS Grid)
```css
.app-shell {
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header"
    "main"
    "footer";
  min-height: 100dvh;
}

@media (min-width: 768px) {
  .app-shell {
    grid-template-columns: 240px 1fr;
    grid-template-rows: auto 1fr;
    grid-template-areas:
      "sidebar header"
      "sidebar main";
  }
}
```

### Chat Layout
```css
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: var(--space-2);
  overflow-y: auto;
  padding: var(--space-4);
}

.chat-message {
  max-width: 80%;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
}

.chat-message--user {
  align-self: flex-end;
  background: var(--color-primary);
}

.chat-message--assistant {
  align-self: flex-start;
  background: var(--color-surface);
}
```

### Control Bar (Flexbox)
```css
.control-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  padding: var(--space-4);
}

.control-bar--end {
  justify-content: flex-end;
}
```

### Responsive Grid
```css
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

@media (min-width: 480px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Verification
- [ ] Mobile-first breakpoints
- [ ] No horizontal overflow
- [ ] Grid/Flexbox used appropriately
- [ ] Sticky/fixed elements positioned correctly
- [ ] All breakpoints tested (480, 768, 1024+)
