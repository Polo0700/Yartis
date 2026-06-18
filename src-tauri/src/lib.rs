use tauri_plugin_shell::ShellExt;
use tokio_tungstenite::connect_async;
use futures_util::{StreamExt};
use  tauri::{AppHandle,Emitter};
use tokio::spawn;
use std::env;
use std::path::Path;
use std::io::{Write, stdout};
use tauri_plugin_shell::process::CommandEvent;
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![ping, inicio])
    .plugin(tauri_plugin_shell::init())
    .setup(|app| {
      let ruta = Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().to_path_buf();
      let shell = app.shell();
      let (mut rx, child) = shell
      .command("python")
      .args(["yartis.py"])
      .current_dir(ruta)
      .spawn()
      .expect("Error de Yartis(python)");
      tauri::async_runtime::spawn(async move{
        let _child = child;
        loop {
          match  rx.recv().await {
            Some(CommandEvent::Stdout(line)) => {
              let  texto = String::from_utf8_lossy(&line);
              print!("{}", texto);
              stdout().flush().ok();
            }
            Some(CommandEvent::Stderr(line)) => {
              let  texto = String::from_utf8_lossy(&line);
              eprint!("{}", texto);
            }
            _ => break,
          }
        }
      });

      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }
      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
#[tauri::command]
fn ping() -> String {
  "pong".to_string()
}
#[tauri::command]
async fn inicio(obj : AppHandle)-> Result<(), String>{
  spawn(async move{
    if let  Ok((stream, _)) =  connect_async("ws://localhost:8765").await{
      let (_escritura, mut lectura) = stream.split();
      while let Some(Ok(msg)) = lectura.next().await{
        match msg.to_text(){

          Ok( texto)=>{
            if let Err(error_emitir) = obj.emit("mensaje", texto) {
              eprintln!("fallo al emitir {error_emitir}")
            }
          },
          Err(e) => {
            eprint!("Error en rust{e}")
          }
        }
      }
    }
    });
  Ok(())
}