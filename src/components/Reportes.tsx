import "./Reportes.css";

function Reportes() {
  return (
    <div className="reportes">
      <h1>Reportes</h1>
      <p>Historial de interacciones.</p>
      <div className="reportes-card">
        <table>
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Comando</th>
              <th>Respuesta</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="empty">-</td>
              <td className="empty">Sin datos aún</td>
              <td className="empty">-</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Reportes;
