---
name: html-core
description: HTML5 semantic markup, accessibility (ARIA/WCAG), SEO, forms, and best practices for modern web applications including voice assistant UIs.
---

# HTML Core

> Semantic HTML is the foundation of accessible, performant web apps.

## When to Activate

- Writing HTML structure for React components
- Accessibility audits (ARIA labels, roles, keyboard navigation)
- SEO optimization (meta tags, structured data, semantic elements)
- Form design and validation patterns
- Voice assistant UI layout (Yartis WebView)

## Semantic HTML5 Elements

```html
<!-- Use semantic landmarks -->
<header>    <!-- Site/section header -->
<nav>       <!-- Navigation -->
<main>      <!-- Primary content (one per page) -->
<article>   <!-- Self-contained content -->
<section>   <!-- Thematic grouping -->
<aside>     <!-- Complementary/sidebar -->
<footer>    <!-- Footer -->

<!-- Voice Assistant UI structure -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Status announcements for screen readers -->
</div>
```

## Accessibility (a11y) for Voice Assistants

### ARIA Live Regions
```html
<!-- Status indicator for Yartis -->
<div 
  role="status" 
  aria-live="polite" 
  aria-label="Yartis status: listening"
  class="status-indicator"
>
  Escuchando...
</div>

<!-- Transcript area -->
<div 
  role="log" 
  aria-live="assertive" 
  aria-atomic="false"
  aria-label="Conversation transcript"
>
  <!-- Messages appear here -->
</div>
```

### Keyboard Navigation
```html
<!-- All interactive elements must be focusable -->
<button aria-label="Activar micrófono"></button>

<!-- Tab order follows visual order -->
<!-- Use tabindex="0" to add to tab order -->
<!-- Use tabindex="-1" for programmatic focus only -->
```

## WCAG Compliance Checklist
- [ ] All images have `alt` text
- [ ] Color not sole conveyer of information
- [ ] Contrast ratio ≥ 4.5:1 (normal text)
- [ ] All interactive elements keyboard-accessible
- [ ] ARIA labels for custom controls
- [ ] Focus indicators visible
- [ ] Language set (`lang="es-MX"`)

## Yartis HTML Structure

```html
<div id="yartis-app">
  <!-- Status bar -->
  <header role="banner" aria-label="Yartis status">
    <div class="status-dot" aria-hidden="true"></div>
    <span class="status-text">Inactivo</span>
  </header>

  <!-- Voice indicator -->
  <div class="voice-indicator" aria-hidden="true">
    <canvas id="audio-visualizer"></canvas>
  </div>

  <!-- Conversation log -->
  <main role="log" aria-label="Conversation">
    <article class="message user">...</article>
    <article class="message yartis">...</article>
  </main>

  <!-- Controls -->
  <footer role="toolbar" aria-label="Controls">
    <button aria-label="Activar" id="mic-btn"></button>
    <button aria-label="Configuración" id="settings-btn"></button>
  </footer>
</div>
```

## SEO Meta Tags
```html
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="Yartis - Asistente de voz tipo JARVIS" />
<meta name="theme-color" content="#0a0a0a" />
```

## Forms
- Use `<label>` for every input
- Use `aria-describedby` for error messages
- Validate with Constraint Validation API as fallback
- Never disable native form validation entirely
