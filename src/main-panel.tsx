import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App_panel from "./Apppanel.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App_panel />
  </StrictMode>,
);
