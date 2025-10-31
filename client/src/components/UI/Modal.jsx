const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 0, left: 0,
        width: "100%", height: "100%",
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
        animation: "fadeIn 0.3s ease",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "24px",
          borderRadius: "14px",
          width: "100%",
          maxWidth: "520px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          animation: "zoomIn 0.3s ease",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "16px" }}>
          <h3 style={{ margin: 0 }}>{title}</h3>
          <button onClick={onClose} style={{
            fontSize: "18px",
            fontWeight: "bold",
            border: "none",
            background: "none",
            cursor: "pointer"
          }}>×</button>
        </div>
        <div>{children}</div>
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes zoomIn {
          from { transform: scale(0.9); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default Modal;