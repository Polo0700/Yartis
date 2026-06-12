---
name: yartis-ci-cd
description: |
  CI/CD pipelines for Yartis project with Tauri v2 desktop app + Python sidecar.
  Use when setting up GitHub Actions, building releases, signing Windows installers,
  running Rust tests, PyInstaller packaging, and automated publishing.
  Triggers: CI/CD, GitHub Actions, release, build, deploy, PyInstaller, MSI, NSIS.
---

# CI/CD — Yartis (Tauri + Python sidecar)

## Estructura del release

```
Yartis/
├── core/
│   ├── src-tauri/       ← Rust compila a .exe nativo
│   ├── audio.py         ← Parte del sidecar Python
│   ├── transcriber.py
│   └── ...
├── brain/               ← También parte del sidecar
├── yartis.py            ← Entry point del sidecar
└── pyproject.toml       ← Dependencias Python
```

## Release workflow completo

```yaml
# .github/workflows/release.yml
name: Release
on:
  push: { tags: ["v*"] }
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: windows-latest
            target: x86_64-pc-windows-msvc
            bundle: "*.msi;*.exe"

    runs-on: ${{ matrix.platform }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: lts/*
          cache: "npm"

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Rust cache
        uses: swatinem/rust-cache@v2
        with:
          workspaces: "./core/src-tauri -> target"

      - name: Install npm deps
        run: npm ci

      - name: Build Python sidecar (PyInstaller)
        run: |
          pip install pyinstaller
          pyinstaller --onefile yartis.py
          mkdir -p core/src-tauri/binaries
          copy dist/yartis.exe core/src-tauri/binaries/yartis-${{ matrix.target }}.exe

      - name: Build Tauri
        uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: v__VERSION__
          releaseName: "Yartis v__VERSION__"
          releaseDraft: true
          args: --target ${{ matrix.target }}
```

## CI workflow (PR checks)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  check:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: lts/*, cache: "npm" }
      - uses: dtolnay/rust-toolchain@stable
      - uses: swatinem/rust-cache@v2
        with: { workspaces: './core/src-tauri -> target' }
      
      - run: npm ci
      - run: npm run build  # TypeScript check
      
      - name: Rust checks
        working-directory: core/src-tauri
        run: |
          cargo check
          cargo clippy --all-targets --all-features
          cargo test
      
      - name: Python checks
        run: |
          uv sync
          uv run pytest tests/ -v
```

## PyInstaller config para sidecar

```powershell
# pyinstaller build command
pyinstaller --onefile `
    --name yartis `
    --hidden-import whisper `
    --hidden-import openwakeword `
    --add-data ".venv/Lib/site-packages/openwakeword;openwakeword" `
    yartis.py
```

## tauri.conf.json para release

```json
{
  "bundle": {
    "active": true,
    "targets": ["msi", "nsis"],
    "externalBin": ["binaries/yartis"],
    "icon": ["core/src-tauri/icons/icon.ico"],
    "windows": {
      "wix": null,
      "nsis": {
        "installMode": "currentUser"
      }
    }
  }
}
```

## Windows signing (opcional)

```yaml
- name: Sign Windows installer
  env:
    AZURE_KEY_VAULT_URI: ${{ secrets.AZURE_KEY_VAULT_URI }}
    AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
    AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
    AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
  run: |
    # Usar Azure Code Signing o similar
```

## Versionado

- Formato: `v{major}.{minor}.{patch}` (ej. `v0.1.0`)
- Tags en Git para triggers de release
- Versión en `core/src-tauri/Cargo.toml` y `package.json`
