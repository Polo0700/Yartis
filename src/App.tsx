import "./App.css";
import "./components/ChangeSize.css";
import StatusIndicator from "./components/StatusIndicator";
import { useAssistant } from "./hooks/useAssistant";
import ChangeSizeWindow from "./components/ChangeSize";

function App() {
  const { textoRecibido } = useAssistant();
  return (
    <>
      <ChangeSizeWindow />
      <StatusIndicator works={textoRecibido ? "speaking" : "wait"} />
    </>
  );
}

export default App;
