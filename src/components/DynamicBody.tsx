import Acerca from "./Acerca";
import Ajustes from "./Ajustes";
import Reportes from "./Reportes";
import Ayuda from "./Ayuda";
import Modelos from "./Modelos";
import Privacidad from "./Privacidad";
import Inicio from "./Inicio";
import { type JSX } from "react";
import "./DynamicBody.css";

function DynamicBody({
  seccion,
  password,
  setpassword,
  usuario,
  setUsuario,
}: {
  seccion: string;
  password: string;
  setpassword: (s: string) => void;
  usuario: string;
  setUsuario: (s: string) => void;
}) {
  const paneles: Record<string, JSX.Element> = {
    acerca: <Acerca />,
    ajustes: (
      <Ajustes
        password={password}
        setpassword={setpassword}
        usuario={usuario}
        setUsuario={setUsuario}
      />
    ),
    reportes: <Reportes />,
    ayuda: <Ayuda />,
    modelos: <Modelos />,
    privacidad: <Privacidad />,
  };

  return <div className="dynamic-body">{paneles[seccion] || <Inicio />}</div>;
}
export default DynamicBody;
