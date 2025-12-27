const Footer = () => {
  return (
    <footer
      style={{
        padding: "16px",
        backgroundColor: "#f3f4f6",
        color: "#4b5563",
        fontSize: "14px",
        textAlign: "center",
        borderTop: "1px solid #e5e7eb",
      }}
    >
      <p>
        © {new Date().getFullYear()}{" "}
        <strong style={{ color: "#b22222" }}>BK Student System</strong> — All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;