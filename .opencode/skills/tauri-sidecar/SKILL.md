---
name: tauri-sidecar
description: |
  Tauri v2 Python sidecar lifecycle management for Yartis voice assistant.
  Use when spawning, managing, or killing Python processes from Tauri.
  Covers sidecar spawn with tauri-plugin-shell, PyInstaller double-process
  workaround, dev-mode shortcuts, and cleanup on window close.
  Triggers: sidecar, Python process, spawn, kill, child process, external bin.
---

# Tauri v2 Sidecar (Python) — Yartis

## Patrón oficial con `tauri-plugin-shell`

### 1. Añadir dependencias
```bash
cargo add tauri-plugin-shell
```

### 2. Registrar en `lib.rs`
```rust
fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        // ...
        .run(tauri::generate_context!())
}
```

### 3. Configurar `tauri.conf.json`
```json
{
  "bundle": {
    "externalBin": ["binaries/yartis"]
  }
}
```
El binary debe nombrarse con target triple: `binaries/yartis-x86_64-pc-windows-msvc.exe`

### 4. Permisos (`capabilities/default.json`)
```json
{
  "permissions": [
    "core:default",
    "shell:allow-execute",
    "shell:allow-spawn",
    "shell:allow-kill"
  ]
}
```

### 5. Spawn desde Rust
```rust
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandEvent;

#[tauri::command]
async fn iniciar_sidecar(app: AppHandle) -> Result<(), String> {
    let sidecar = app.shell()
        .sidecar("binaries/yartis")
        .map_err(|e| e.to_string())?;

    let (mut rx, child) = sidecar
        .spawn()
        .map_err(|e| e.to_string())?;

    // Guardar child para cleanup
    // app.manage(SidecarState(Mutex::new(Some(child))));

    tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(bytes) => {
                    let text = String::from_utf8_lossy(&bytes);
                    info!("[sidecar] {text}");
                }
                CommandEvent::Stderr(bytes) => {
                    let text = String::from_utf8_lossy(&bytes);
                    warn!("[sidecar:err] {text}");
                }
                CommandEvent::Terminated(payload) => {
                    info!("[sidecar] terminado: {:?}", payload);
                    break;
                }
                _ => {}
            }
        }
    });

    Ok(())
}
```

## ⚠️ PyInstaller doble proceso

`child.kill()` solo mata el bootloader, no el Python real.

### Solución 1: `kill_on_drop`
```rust
// tauri-plugin-shell soporta kill_on_drop (PR merged Dec 2025)
// El child se mata automáticamente al dropear
```

### Solución 2: `sysinfo` para árbol de procesos
```toml
[dependencies]
sysinfo = "0.33"
```

```rust
use sysinfo::{System, Pid};

fn kill_process_tree(pid: u32) {
    let mut system = System::new();
    system.refresh_all();

    // Matar hijos primero
    let children: Vec<Pid> = system.processes()
        .iter()
        .filter(|(_, p)| p.parent().map(|pp| pp.as_u32() == pid).unwrap_or(false))
        .map(|(pid, _)| *pid)
        .collect();

    for child_pid in children {
        if let Some(proc) = system.process(child_pid) {
            proc.kill();
        }
    }

    // Matar proceso principal
    if let Some(proc) = system.process(Pid::from_u32(pid)) {
        proc.kill();
    }
}
```

### Solución 3 (Windows): `taskkill /f`
```rust
#[cfg(target_os = "windows")]
fn kill_windows_tree(pid: u32) {
    std::process::Command::new("taskkill")
        .args(&["/f", "/t", "/pid", &pid.to_string()])
        .output()
        .ok();
}
```

## Dev mode shortcut

En desarrollo, lanzar Python directamente sin PyInstaller:

```rust
#[tauri::command]
async fn iniciar_sidecar(app: AppHandle) -> Result<(), String> {
    #[cfg(debug_assertions)]
    {
        // Modo dev: lanzar Python directamente
        let child = std::process::Command::new("uv")
            .args(["run", "python", "yartis.py"])
            .spawn()
            .map_err(|e| e.to_string())?;

        app.manage(SidecarState(Mutex::new(Some(child))));
    }

    #[cfg(not(debug_assertions))]
    {
        // Modo release: sidecar empaquetado
        let sidecar = app.shell()
            .sidecar("binaries/yartis")
            .map_err(|e| e.to_string())?;
        let (mut rx, child) = sidecar.spawn().map_err(|e| e.to_string())?;
        app.manage(SidecarState(Mutex::new(Some(child))));
        // spawn rx handler...
    }

    Ok(())
}
```

## Cleanup al cerrar ventana

```rust
.on_window_event(|window, event| {
    if let tauri::WindowEvent::CloseRequested { .. } = event {
        let app = window.app_handle();
        if let Some(state) = app.try_state::<SidecarState>() {
            let mut guard = state.0.lock().unwrap();
            if let Some(mut child) = guard.take() {
                let pid = child.id();
                kill_process_tree(pid);
                let _ = child.kill();
            }
        }
    }
})
```
