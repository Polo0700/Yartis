import "./App.css";
import "./components/ChangeSize.css";
import ChangeSizeWindow from "./components/ChangeSize.tsx";
import "./components/StatusIndicator.css";
import StatusIndicator from "./components/StatusIndicator";
import { invoke } from "@tauri-apps/api/core";
import { useState, useEffect } from "react";
import { useAssistant } from "./hooks/useAssistant.ts";

function App() {
  const [conf, setConf] = useState(false);
  const { textoRecibido } = useAssistant();
  const EventTrigger: Record<string, string> = {
    "0x0x0Polo0700Audio": "wait",
    "0x0x0Polo0701Audio": "speaking",
  };
  const works = EventTrigger[textoRecibido] ?? "unworking";
  useEffect(() => {
    const check = async () => {
      try {
        const usuario = await invoke<string>("leer_usuario");
        const existe = await invoke("check_config", { usuario });
        if (existe) {
          setConf(true);
          await invoke("show_popup");
        } else {
          await invoke("hide_popup");
        }
      } catch {
        setConf(true); // modo prueba: si no hay config, dejar pasar
      }
    };
    if (!conf) {
      check();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <>
      {conf && (
        <>
          <StatusIndicator works={works} />
          <ChangeSizeWindow />
        </>
      )}
    </>
  );
}

export default App;
