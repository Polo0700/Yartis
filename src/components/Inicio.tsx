import "./Inicio.css";
import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
function Inicio() {
  const [msg, setMsg] = useState("");
  return (
    <div className="inicio">
      <div className="inicio-logo">Y</div>
      <h1 className="inicio-titulo">Bienvenido a Yartis</h1>
      <div className="start">
        <div className="start-text">Bienvenido</div>
        <div className="answer">
          <code className="answer-text"></code>
        </div>
        <div>
          <input
            placeholder="Preguntame lo que necesites"
            className="bar-input"
            value={msg}
            onChange={(e) => setMsg(e.target.value)}
          ></input>
          <button
            className="btn-input-inicio"
            onClick={() => invoke("enviar_msg", { msg })}
          >
            a
          </button>
        </div>
      </div>
      <div className="inicio-card">
        <h2>
          <span className="inicio-card-icon">🎙️</span>
          Habla con Yartis
        </h2>
        <p>
          Di <code>"Yartis"</code> para activarlo. Puedes pedirle que te ayude
          con cosas como:
        </p>
        <ul>
          <li>
            <code>"Yartis, ¿qué hora es?"</code>
          </li>
          <li>
            <code>"Yartis, pon música"</code>
          </li>
          <li>
            <code>"Yartis, qué tiempo hace"</code>
          </li>
          <li>
            <code>"Yartis, abre el navegador"</code>
          </li>
        </ul>
      </div>

      <div className="inicio-card">
        <h2>
          <span className="inicio-card-icon">⌨️</span>
          Escribe directamente
        </h2>
        <p>
          Si no puedes hablar, también puedes escribir tu mensaje en la ventana
          del asistente. Mismo resultado, sin voz.
        </p>
      </div>

      <div className="inicio-card">
        <h2>
          <span className="inicio-card-icon">⚙️</span>
          Configura tu experiencia
        </h2>
        <p>
          En el menú superior puedes ajustar modelos, privacidad, ver reportes y
          más.
        </p>
      </div>

      <p className="inicio-footer">
        Selecciona una opción del menú para comenzar.
      </p>
    </div>
  );
}

export default Inicio;
