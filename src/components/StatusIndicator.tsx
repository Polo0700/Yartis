import "./StatusIndicator.css";
function StatusIndicator({ works }: { works: string }) {
  return (
    <div className={`status-indicator ${works}`}>
      <div className="circle"></div>
      <div className="wave wave-1"></div>
      <div className="wave wave-2"></div>
      <div className="wave wave-3"></div>
    </div>
  );
}
export default StatusIndicator;
