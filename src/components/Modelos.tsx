import "./Modelos.css";

function Modelos() {
  return (
    <div className="modelos">
      <h1>Modelos</h1>

      <div className="modelos-section">
        <h3>Whisper (STT)</h3>
        <ul>
          <li>tiny — rápido, menor precisión</li>
          <li>base — balance</li>
          <li><strong>small — seleccionado</strong></li>
          <li>medium — lento, mayor precisión</li>
        </ul>
      </div>

      <div className="modelos-section">
        <h3>Clasificador</h3>
        <ul>
          <li>paraphrase-multilingual-MiniLM-L12-v2</li>
        </ul>
      </div>

      <div className="modelos-section">
        <h3>Voice ID</h3>
        <ul>
          <li>ECAPA-TDNN (speechbrain)</li>
          <li>Voces registradas: 0</li>
        </ul>
      </div>
    </div>
  );
}

export default Modelos;
