const Input = ({ label, name, type = "text", value, onChange, placeholder, required = false }) => {
  return (
    <div style={{ marginBottom: "14px" }}>
      {label && (
        <label style={{ display: "block", fontWeight: "600", marginBottom: "6px" }}>
          {label}
        </label>
      )}
      <input
        name={name} // ✅ thêm dòng này
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        style={{
          width: "100%",
          padding: "10px 12px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          fontSize: "15px",
          transition: "border-color 0.3s ease",
        }}
        onFocus={(e) => (e.target.style.borderColor = "#2563eb")}
        onBlur={(e) => (e.target.style.borderColor = "#ccc")}
      />
    </div>
  );
};

export default Input;