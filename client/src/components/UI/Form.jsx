const Form = ({ children, onSubmit }) => {
  return (
    <form
      onSubmit={onSubmit}
      style={{
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 6px 20px rgba(0,0,0,0.1)",
        backgroundColor: "white",
        maxWidth: "500px",
        margin: "0 auto",
        animation: "fadeInUp 0.4s ease",
      }}
    >
      {children}
      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </form>
  );
};

export default Form;