import Menu from "./components/Menu";
import DynamicBody from "./components/DynamicBody";
import InitialSettings from "./components/InitialSettings";
import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
function Apppanel() {
  const [conf, setConf] = useState(false);
  useEffect(() => {
    if (localStorage.getItem("darkMode") === "true") {
      document.body.classList.add("dark-mode");
    }
  }, []);
  useEffect(() => {
    const check = async () => {
      try {
        const usuario = await invoke<string>("leer_usuario");
        const existe = await invoke("check_config", { usuario });
        if (existe) {
          setConf(true);
        }
      } catch {
        // no registrado aún
        setConf(true); // modo prueba: si no hay config, dejar pasar
      }
    };
    if (!conf) {
      check();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const [seccion, setSeccion] = useState("inicio");
  const [password, setPassword] = useState("");
  const [usuario, setUsuario] = useState("");
  return (
    <>
      {conf ? (
        <>
          <Menu seccionActiva={seccion} onCambio={setSeccion} />
          <DynamicBody
            seccion={seccion}
            password={password}
            setpassword={setPassword}
            usuario={usuario}
            setUsuario={setUsuario}
          />
        </>
      ) : (
        <InitialSettings onFinish={() => setConf(true)} />
      )}
    </>
  );
}
export default Apppanel;
