import "./App.css";
import "./components/ChangeSize.css";
import StatusIndicator from "./components/StatusIndicator";
import { useAssistant } from "./hooks/useAssistant";
import ChangeSizeWindow from "./components/ChangeSize";

function App() {
  const { works } = useAssistant();
  return (
    <>
      <ChangeSizeWindow />
      <StatusIndicator works={works} />
    </>
  );
}

export default App;
