---
name: git-workflow
description: |
  Git workflow, commit conventions, and branch strategy for Yartis.
  Use when making commits, creating branches, reviewing diffs, managing
  RASTRECK.md streaks, and organizing the repository history.
  Triggers: git, commit, branch, PR, push, RASTRECK, racha, repo.
---

# Git Workflow — Yartis

## Conventional Commits

```
feat:       nueva funcionalidad (minor)
fix:        corrección de bug (patch)
refactor:   cambio de código sin funcionalidad nueva
docs:       documentación
style:      formato, linting (sin cambio funcional)
test:       tests
chore:      tareas de mantenimiento
ci:         CI/CD
perf:       optimización de rendimiento
```

## Formato

```
<tipo>(<scope>): <descripción breve>

[opcional: cuerpo con detalles]

[opcional: footer con breaking changes o issues]
```

### Ejemplos
```
feat(core): agregar noise reduction por spectral gating
fix(ws): reconexión automática cuando Python se cae
refactor(src-tauri): mover sidecar a módulo separado
docs: actualizar README con pipeline completo
```

## Branch strategy

```
main           ← releases estables
  │
  └── feat/nombre    ← features nuevas
  └── fix/nombre     ← fixes
  └── refactor/nombre ← refactors
```

Por ahora, mientras el proyecto es pequeño, se puede trabajar directo en `main` con commits pequeños y atómicos.

## Commits atómicos

Cada commit debe:
- Hacer **una sola cosa**
- Pasar `cargo test` / `pytest` antes de commitear
- Tener mensaje descriptivo

**Bien:**
```
feat(core): agregar transcripción con faster-whisper
```

**Mal:**
```
cambios varios
```

## RASTRECK.md

El archivo `RASTRECK.md` en la raíz lleva el registro diario de racha:

```markdown
# RASTRECK — Yartis

| Fecha     | ⭐  | Resumen |
|-----------|-----|---------|
| 2026-06-08| ⭐ 1 | Config inicial del proyecto |
| 2026-06-09| ⭐ 2 | Migración Rust a core/src-tauri + skills |
```

### Reglas
- ⭐ N = días **consecutivos** programando
- Si un día no se programa, reinicia a ⭐ 1
- Agregar fila CADA día que se programe
- Resumen breve de lo que se logró

## Antes de commitear

```bash
# Ver qué cambió
git status
git diff

# Rust checks (si aplica)
cd core/src-tauri && cargo check && cargo clippy && cd ../..

# Python checks
uv run pytest tests/ -v

# Commit
git add -A
git commit -m "feat(scope): descripción"

# Push (si aplica)
git push
```

## Qué NO hacer

- ❌ Commits gigantes sin descripción clara
- ❌ `git add -A` sin revisar primero
- ❌ Pushear a main sin verificar que compila
- ❌ Mensajes como "arreglos", "cambios", "update"
- ❌ Forzar push con `--force`
