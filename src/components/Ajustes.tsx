import "./Ajustes.css";
import { invoke } from "@tauri-apps/api/core";
import { platform } from "@tauri-apps/plugin-os";
import { useState, useEffect } from "react";

function Ajustes({
  password,
  setpassword,
  usuario,
  setUsuario,
}: {
  password: string;
  setpassword: (s: string) => void;
  usuario: string;
  setUsuario: (s: string) => void;
}) {
  const [sistema, sistemaSet] = useState("");
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("darkMode") === "true";
  });

  useEffect(() => {
    (async () => {
      const os = await platform();
      sistemaSet(os);
    })();
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    localStorage.setItem("darkMode", String(darkMode));
  }, [darkMode]);

  return (
    <div className="ajustes">
      <h1>Ajustes</h1>

      <div className="ajustes-section">
        <h3>Apariencia</h3>
        <div className="ajustes-toggle" onClick={() => setDarkMode(!darkMode)}>
          <span>Modo oscuro</span>
          <div className="ajustes-toggle-switch" />
        </div>
      </div>

      <div className="ajustes-section">
        <h3>Audio</h3>
        <label>
          Volumen del micrófono:
          <input type="range" min="0" max="100" />
        </label>
        <label>
          Reducción de ruido (Rust):
          <input type="checkbox" />
        </label>
      </div>

      <div className="ajustes-section">
        <h3>Wake Word</h3>
        <label>
          Sensibilidad:
          <input type="range" min="0" max="1" step="0.1" defaultValue="0.3" />
        </label>
      </div>

      <div className="ajustes-section">
        <h3>Modelos</h3>
        <label>
          Whisper:
          <select>
            <option>tiny</option>
            <option>base</option>
            <option>small</option>
            <option>medium</option>
          </select>
        </label>
      </div>

      <div className="ajustes-section">
        <h3>Voz</h3>
        <button>Grabar voz de referencia</button>
        <button>Voces guardadas</button>
      </div>

      {sistema === "windows" && (
        <div className="ajustes-section">
          <h3>Contraseña (Linux)</h3>
          <p>
            Guarda tu contraseña para que OpenCode no la pida en cada petición.
          </p>
          <label>
            Modo:
            <select>
              <option value="session">Pedir cada sesión</option>
              <option value="permanent">Guardar permanentemente</option>
            </select>
          </label>
          <label>
            Usuario:
            <input
              type="text"
              placeholder="Escribe tu usuario"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
            />
          </label>
          <label>
            Contraseña:
            <input
              type="password"
              placeholder="Escribe tu contraseña"
              value={password}
              onChange={(e) => setpassword(e.target.value)}
            />
          </label>
          <button
            onClick={() => invoke("verify_picker", { password, usuario })}
          >
            Guardar contraseña
          </button>
        </div>
      )}
    </div>
  );
}

export default Ajustes;
