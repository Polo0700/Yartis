use tokio_tungstenite::connect_async;
use futures_util::{StreamExt};
use  tauri::{AppHandle,Emitter};
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![ping, inicio])
    .setup(|app| {
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
  let  (stream, _) =  connect_async("ws://localhost:8765").await.map_err(|e| e.to_string())?;
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
  Ok(())
}