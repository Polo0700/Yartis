use aes_gcm::aead::generic_array::GenericArray;
use futures_util::stream::SplitSink;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio_tungstenite::tungstenite::Message;
use tokio_tungstenite::{MaybeTlsStream, WebSocketStream, connect_async};
use std::path::Path;
use std::io::{BufRead, BufReader, Write};
use std::process::{Command, Stdio};
use aes_gcm::{aead::{Aead, KeyInit}, Aes256Gcm};
use futures_util::{SinkExt, StreamExt};
use rand::RngCore;
use std::fs::File;
use tokio::net::TcpStream;
use futures_util::stream::SplitStream;
use tauri::{Emitter, Manager};
use tokio::time::{sleep, Duration};
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
    .invoke_handler(tauri::generate_handler![ping, enviar_msg])
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
      let handle = app.handle().clone();
      tauri::async_runtime::spawn(async move {
        // tomar la conexion 
        let connect = loop { 
          match connection(handle.clone()).await{ 
            Ok(con) => break con,
            Err(e) => {
              eprint!("cannot connect {}, we are retrying",e);
              sleep(Duration::from_secs(1)).await;
            }
          }
        };
        let connect = Arc::new(Mutex::new(connect));
        handle.manage(connect.clone());

        loop {
          let mut c = connect.lock().await;
          c.get().await;
        }
      });
      Ok(())
      // darle un espacio
      // abrirla usando connection
      // -para abrir la connection ocupo llamar la funcion de connection
      // -despues ya es todo pq la funcion por si sola ya hace las conexiones y las guarda en el struct
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
type WsSink = SplitSink<WebSocketStream<MaybeTlsStream<TcpStream>>, Message>;
type WsStream = SplitStream<WebSocketStream<MaybeTlsStream<TcpStream>>>;
struct Connect {
  escritura: WsSink, 
  lectura: WsStream,
  handle: tauri::AppHandle,
}
  async fn connection(handle: tauri::AppHandle)->Result<Connect, String>{
    let connection = match connect_async("ws://localhost:8765").await{
      Ok((con,_res) ) => con,
      Err(e) => return Err(format!("cannot connec: {}",e)),
    };
    let (send, get) = connection.split();
    Ok(Connect{
      escritura: send, 
      lectura: get,
      handle: handle,
    })
  }
#[tauri::command]
fn ping() -> String {
  "pong".to_string()
}
impl Connect {

  async fn send(&mut self, msg:Message)-> Result<(), String>{
    self.escritura.send(msg).await.map_err(|e| format!("Error al enviar mensaje: {}", e))
  }
  async fn get(&mut self){
    while let Some(msg) = self.lectura.next().await{
      if let Ok(Message::Text(texto)) = msg {
        let texto_string = texto.to_string();
        if let Err(e) = self.handle.emit("message", texto_string){
          eprint!("Error al enviar mensaje: {}",e);
        }
      }
    }
  }
}
#[tauri::command]
async fn enviar_msg(estado: tauri::State<'_, Arc<Mutex<Connect>>>, msg: String) -> Result<(), String> {
  let mut envio = estado.lock().await;
  envio.send(Message::Text(msg.into())).await.map_err(|e| format!("Error al enviar mensaje: {}", e))?;
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