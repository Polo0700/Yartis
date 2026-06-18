import { useEffect, useState } from "react";
import { listen } from "@tauri-apps/api/event";

export function useAssistant() {
  const [textoRecibido, textoRecibidoSet] = useState("");
  useEffect(() => {
    const cambio = listen<string>("mensaje", (callback) => {
      console.log(callback.payload);
      const texto = callback.payload;
      textoRecibidoSet(texto);
    });
    return () => {
      cambio.then((fn) => fn());
    };
  }, []);
  return { textoRecibido };
}
