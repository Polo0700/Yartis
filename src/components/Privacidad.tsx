import "./Privacidad.css";

function Privacidad() {
  return (
    <div className="privacidad">
      <h1>Privacidad</h1>
      <p>Todo el procesamiento es local. No se envían datos a la nube.</p>

      <div className="privacidad-card">
        <h3>Datos locales</h3>
        <ul>
          <li>Audio: se procesa y descarta</li>
          <li>Voces: guardadas en voice_profiles/</li>
          <li>Historial: guardado localmente</li>
        </ul>
      </div>

      <div className="privacidad-card">
        <h3>Permisos</h3>
        <ul>
          <li>Micrófono — necesaria para grabar audio</li>
        </ul>
      </div>

      <button>Limpiar historial</button>
      <button>Eliminar voces guardadas</button>
    </div>
  );
}

export default Privacidad;
