import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import "./InitialSettings.css";

type Step = "welcome" | "password" | "voice" | "done";

function InitialSettings({ onFinish }: { onFinish: () => void }) {
  const [step, setStep] = useState<Step>("welcome");
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const handleSave = async () => {
    if (password !== confirm) {
      alert("Las contraseñas no coinciden");
      return;
    }
    await invoke("save_picker", { usuario, picker: password });
    setStep("done");
  };

  return (
    <div className="initial-settings">
      {step === "welcome" && (
        <div className="step">
          <h1>Bienvenido a Yartis</h1>
          <p>Configura tu asistente de voz</p>
          <input
            type="text"
            placeholder="Tu nombre"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
          />
          <button onClick={() => setStep("password")}>Siguiente</button>
        </div>
      )}

      {step === "password" && (
        <div className="step">
          <h1>Crea tu contraseña</h1>
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="Confirmar contraseña"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />
          <button onClick={handleSave}>Siguiente</button>
        </div>
      )}

      {step === "voice" && (
        <div className="step">
          <h1>Graba tu voz</h1>
          <p>Yartis aprenderá a reconocerte</p>
          {/* TODO: grabación de voz */}
          <button onClick={() => setStep("done")}>Siguiente</button>
        </div>
      )}

      {step === "done" && (
        <div className="step">
          <h1>¡Listo!</h1>
          <button onClick={onFinish}>Empezar</button>
        </div>
      )}

      <div className="progress">
        {["welcome", "password", "voice", "done"].map((s) => (
          <div
            key={s}
            className={`dot ${step === s ? "active" : ""}`}
          />
        ))}
      </div>
    </div>
  );
}

export default InitialSettings;
