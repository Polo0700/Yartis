import "./ChangeSize.css";
import { getCurrentWebviewWindow } from "@tauri-apps/api/webviewWindow";
import { LogicalPosition, LogicalSize } from "@tauri-apps/api/dpi";
import { useEffect, useState } from "react";
function ChangeSizeWindow() {
  const [cambiarEstado, cambiarEstadoSet] = useState(true);
  useEffect(() => {
    const pestaña = getCurrentWebviewWindow();
    pestaña.setSize(new LogicalSize(180, 180));
    pestaña.setPosition(new LogicalPosition(window.screen.width - 200, 20));
  }, []);
  if (cambiarEstado == false) {
    return null;
  }
  return (
    <div className="popup">
      <span>Pop-up</span>
      <span>
        {window.screen.width} x {window.screen.height}
      </span>
      <button onClick={() => getCurrentWebviewWindow().hide()}>fondo</button>
      <button onClick={() => cambiarEstadoSet(false)}>close</button>
    </div>
  );
}
export default ChangeSizeWindow;
