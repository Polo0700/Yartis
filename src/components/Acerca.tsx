import "./Acerca.css";

function Acerca() {
  return (
    <div className="acerca">
      <h1>Acerca de Yartis</h1>
      <p>Asistente de voz con IA.</p>

      <div className="acerca-card">
        <h3>Versión</h3>
        <p>0.1.0</p>
      </div>

      <div className="acerca-card">
        <h3>Componentes</h3>
        <ul>
          <li>Wake word: openwakeword</li>
          <li>STT: faster-whisper</li>
          <li>TTS: Piper</li>
          <li>Filtrado de audio: Rust (RNNoise)</li>
          <li>Backend: OpenCode</li>
        </ul>
      </div>
    </div>
  );
}

export default Acerca;
