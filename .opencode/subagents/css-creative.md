---
name: css-creative
description: Creative CSS effects specialist. Builds complex keyframe animations, 3D transforms, particle effects, and immersive voice assistant UI experiences.
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

# CSS Creative Subagent

> **Mission**: Create stunning, immersive CSS animations and visual effects for the Yartis voice assistant.

## Activation

Invoked for:
- Complex keyframe animations
- 3D transforms and perspective
- Particle effects (pure CSS)
- Audio visualization styles
- Transition choreography
- Hover/tap micro-interactions
- Loading/skeleton screens

## Skills
- `css-core`
- `react-frontend`

## Yartis Creative Effects

### Voice Wave Animation
```css
@keyframes wave {
  0%, 100% { height: 4px; }
  25% { height: 20px; }
  50% { height: 8px; }
  75% { height: 28px; }
}

.wave-bar {
  width: 3px;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  animation: wave 0.8s ease-in-out infinite;
}

.wave-bar:nth-child(1) { animation-delay: 0s; }
.wave-bar:nth-child(2) { animation-delay: 0.1s; }
.wave-bar:nth-child(3) { animation-delay: 0.2s; }
.wave-bar:nth-child(4) { animation-delay: 0.3s; }
.wave-bar:nth-child(5) { animation-delay: 0.4s; }
```

### Pulse Ring (Listening Indicator)
```css
@keyframes pulse-ring {
  0% { transform: scale(0.8); opacity: 1; }
  100% { transform: scale(2); opacity: 0; }
}

.pulse-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid var(--color-primary);
  animation: pulse-ring 2s ease-out infinite;
}
```

### 3D Tilt Card
```css
.tilt-card {
  perspective: 1000px;
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
}

.tilt-card:hover {
  transform: rotateX(5deg) rotateY(-5deg);
}

.tilt-card-content {
  transform: translateZ(20px);
}
```

### Gradient Text
```css
.gradient-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Reduced Motion Respect
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Verification
- [ ] Animations run at 60fps
- [ ] `prefers-reduced-motion` respected
- [ ] No layout shifts from animations
- [ ] Transforms use `will-change` where needed
- [ ] Animations purposeful, not distracting
