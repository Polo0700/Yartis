import "./Menu.css";
import { useState } from "react";
import flecha from "../assets/flecha.svg";
function Menu({
  seccionActiva,
  onCambio,
}: {
  seccionActiva: string;
  onCambio: (s: string) => void;
}) {
  const [animSalida, setAnimSalida] = useState(false);
  const [Menu1Visible, setMenu1Visible] = useState(true);
  const [Menu2Visible, setMenu2Visible] = useState(false);
  const [flechaVisible, setFlechaVisible] = useState(true);
  const toggle = () => {
    setAnimSalida(true);
    setTimeout(() => {
      if (Menu1Visible == true) {
        setMenu1Visible(false);
        setMenu2Visible(true);
        setAnimSalida(false);
      } else if (Menu2Visible) {
        setMenu2Visible(false);
        setMenu1Visible(true);
        setAnimSalida(false);
      }
      if (flechaVisible == true) {
        setTimeout(() => {
          setFlechaVisible(false);
        }, 300);
        setTimeout(() => {
          setFlechaVisible(true);
        }, 300);
      }
    }, 600);
  };
  return (
    <div className="menu">
      {flechaVisible && (
        <button onClick={toggle} className={animSalida ? "principal" : ""}>
          <img
            src={flecha}
            className={animSalida ? "icono salida" : "icono"}
          ></img>
        </button>
      )}
      <div>
        {Menu1Visible && (
          <ul className={animSalida ? "salida menu-list" : "menu-list"}>
            <li>
              <button
                className={
                  seccionActiva === "inicio"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("inicio")}
              >
                Inicio
              </button>
            </li>
            <li>
              <button
                className={
                  seccionActiva === "acerca"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("acerca")}
              >
                Acerca
              </button>
            </li>
            <li>
              <button
                className={
                  seccionActiva === "ajustes"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("ajustes")}
              >
                Ajustes
              </button>
            </li>
            <li>
              <button
                className={
                  seccionActiva === "reportes"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("reportes")}
              >
                Reportes
              </button>
            </li>
          </ul>
        )}
      </div>
      {Menu2Visible && (
        <div>
          <ul className={animSalida ? "salida menu-list2" : "menu-list2"}>
            <li>
              <button
                className={
                  seccionActiva === "inicio"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("inicio")}
              >
                Inicio
              </button>
            </li>
            <li>
              <button
                className={
                  seccionActiva === "ayuda"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("ayuda")}
              >
                Ayuda
              </button>
            </li>
            <li>
              <button
                className={
                  seccionActiva === "modelos"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("modelos")}
              >
                Modelos
              </button>
            </li>
            <li>
              <button
                className={
                  seccionActiva === "privacidad"
                    ? "botonesSecundarios activo"
                    : "botonesSecundarios"
                }
                onClick={() => onCambio("privacidad")}
              >
                Privacidad
              </button>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
export default Menu;
