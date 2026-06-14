import "./ChangeSize.css";
import { getCurrentWebviewWindow } from "@tauri-apps/api/webviewWindow";
import { LogicalPosition, LogicalSize } from "@tauri-apps/api/dpi";
import React, { useEffect, useState } from "react";
const pestaña = getCurrentWebviewWindow();
function ChangeSizeWindow() {
  const [cambiarEstado, cambiarEstadoSet] = useState(true);
  useEffect(() => {
    pestaña.setSize(new LogicalSize(180, 180));
    pestaña.setPosition(new LogicalPosition(window.screen.width - 200, 20));
  }, []);
  if (cambiarEstado == false) {
    return null;
  }
  const handleDragStart = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest("button")) return;
    pestaña.startDragging();
  };
  return (
    <div className="popup">
      <div className="top" onMouseDown={handleDragStart}>
        <button onClick={() => pestaña.hide()}>fondo</button>
        <button onClick={() => cambiarEstadoSet(false)}>close</button>
      </div>
    </div>
  );
}
export default ChangeSizeWindow;
