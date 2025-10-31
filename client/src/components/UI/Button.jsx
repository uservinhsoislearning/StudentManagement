const Button = ({
  children,
  onClick,
  type = "button",
  variant = "primary",
  disabled = false,
  style = {},
}) => {
  const baseStyle = {
    padding: "10px 16px",
    borderRadius: "8px",
    fontWeight: 600,
    cursor: disabled ? "not-allowed" : "pointer",
    transition: "all 0.3s ease",
    transform: disabled ? "none" : "scale(1)",
    backgroundColor:
      variant === "danger" ? "#ef4444" :
        variant === "secondary" ? "#e2e8f0" :
          variant === "outline" ? "white" : "#2563eb",
    color: variant === "outline" ? "#2563eb" : "white",
    border: variant === "outline" ? "1px solid #2563eb" : "none",
  };
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        ...baseStyle,
        ...style,
      }}
      onMouseEnter={(e) => {
        if (!disabled) e.currentTarget.style.transform = "scale(1.05)";
      }}
      onMouseLeave={(e) => {
        if (!disabled) e.currentTarget.style.transform = "scale(1)";
      }}
    >
      {children}
    </button>
  );
};

export default Button;