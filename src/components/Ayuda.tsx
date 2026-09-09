import "./Ayuda.css";

function Ayuda() {
  return (
    <div className="ayuda">
      <h1>Ayuda</h1>

      <div className="ayuda-section">
        <h3>Cómo usar Yartis</h3>
        <ul>
          <li>Dí <strong>"Yartis"</strong> para activarlo</li>
          <li>Habla tu comando</li>
          <li>Yartis procesará y responderá</li>
        </ul>
      </div>

      <div className="ayuda-section">
        <h3>Comandos disponibles</h3>
        <ul>
          <li>"Reproduce [canción]" — música</li>
          <li>"Abre [app]" — lanzar aplicación</li>
          <li>"Busca [algo]" — búsqueda web</li>
        </ul>
      </div>

      <div className="ayuda-section">
        <h3>Atajos de teclado</h3>
        <ul>
          <li>Ctrl+Q — cerrar</li>
        </ul>
      </div>
    </div>
  );
}

export default Ayuda;
