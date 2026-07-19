use aes_gcm::aead::generic_array::GenericArray;
use tokio_tungstenite::connect_async;
use  tauri::{AppHandle,Emitter};
use tokio::spawn;
use std::fmt::format;
use std::path::Path;
use std::io::{BufRead, BufReader, Write};
use std::process::{Command, Stdio};
use aes_gcm::{aead::{Aead, KeyInit}, Aes256Gcm};
use futures_util::StreamExt;
use rand::RngCore;
use std::fs::File;
use argon2::{
  password_hash::{
    rand_core::OsRng,
    PasswordHash,PasswordHasher, PasswordVerifier, SaltString
  },
  Argon2
};
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![ping, inicio])
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_os::init())
    .setup(|app| {
      let ruta = Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().to_path_buf();
      let python_path = {
        let venv      = ruta.join(".venv").join("Scripts").join("pythonw.exe");
        let venv_exe  = ruta.join(".venv").join("Scripts").join("python.exe");
        if venv.exists() { venv }
        else if venv_exe.exists() { venv_exe }
        else { Path::new("pythonw").to_path_buf() }
      };
      match Command::new(&python_path)
        .arg("-m")
        .arg("core.server")
        .current_dir(&ruta)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
      {
        Ok(mut child) => {
          let stdout = child.stdout.take();
          let stderr = child.stderr.take();
          tauri::async_runtime::spawn(async move {
            if let Some(out) = stdout {
              let reader = BufReader::new(out);
              for line in reader.lines() {
                if let Ok(texto) = line {
                  print!("{}", texto);
                  std::io::stdout().flush().ok();
                }
              }
            }
          });
          tauri::async_runtime::spawn(async move {
            if let Some(err) = stderr {
              let reader = BufReader::new(err);
              for line in reader.lines() {
                if let Ok(texto) = line {
                  eprint!("{}", texto);
                }
              }
            }
          });
        }
        Err(e) => {
          eprintln!("Error al lanzar Python: {:?}", e);
        }
      }

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
struct SecYar{
  pickerp: String,
  user: String,
  saltk: Vec<u8>,
  pickers: String,
}
impl SecYar {
  fn new(usuario: String) -> Self {
    Self {
      pickerp: String::new(),
      user: usuario,
      saltk: Vec::new(),
      pickers: String::new(),
    }
  }
  fn picker(&mut self, password: String, usuario: String ) -> Result<String, String> {
    self.pickerp = password.clone();
    self.user = usuario.clone();
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    let picker = argon2.hash_password(password.as_bytes(), &salt).map_err(|e| format!("Error al hashear: {}", e))?.to_string();
    println!("datos recibidos: {}", picker);
    Ok(picker)
  }
  fn checkpicker(&mut self, picker_almacenado: String) -> Result<bool, String> {
    let argon2 =Argon2::default();
    let picker = PasswordHash::new(&picker_almacenado).map_err(|e| format!("Error al leer hash: {}", e))?;
    self.pickers = picker_almacenado.clone();
    Ok(argon2.verify_password(self.pickerp.as_bytes(), &picker).is_ok())
  }
  fn generatepickerk(&mut self) -> Result<Vec<u8>, String>{
    let mut pickerk = vec![0u8; 32];
    OsRng.fill_bytes(&mut pickerk);
    self.saltk = pickerk.clone();
    Ok(pickerk)
  }
  fn generatepickern(&mut self) -> Result<[u8; 12], String>{
    let mut pickern= [0u8; 12];
    OsRng.fill_bytes(&mut pickern);
    Ok(pickern)
    }
  fn ecppicker(&mut self) -> Result<Vec<u8>, String>{
    let pickern = self.generatepickern()?;
    let pickerno = GenericArray::from_slice(&pickern);
    let picker = &self.saltk[..];
    let pickerc = Aes256Gcm:: new_from_slice(picker).map_err(|e| format!("Error key: {}", e))?;
    let ecppicker = pickerc.encrypt(pickerno, self.pickerp.as_bytes()).map_err(|e| format!("Error Encrypt {}",e))?;
    let mut resultado= Vec::new();
    resultado.extend_from_slice(&pickern);
    resultado.extend_from_slice(&self.saltk);
    resultado.extend_from_slice(&ecppicker);
    Ok(resultado)
  }
  fn save(&mut self) -> Result<Vec<u8>, String>{
    let ruta=Path::new("config").join("users").join(&self.user).join("password");
    let data = self.ecppicker().map_err(|e|format!("Data not upload by {}",e))?;
    let mut file = File::create(&ruta).map_err(|e| format!("File not created by {}", e))?;
    file.write_all(&data).map_err(|e| format!("File couldn't be written {}", e))?;
    Ok(data)
  }
}