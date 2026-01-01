import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/bachkhoa-logo.png"; 
import styles from "./Login.module.css"; // Tận dụng style của trang Login

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");

    try {
      // Gọi method POST vào API chung mà chúng ta đã thống nhất
      const response = await fetch("http://localhost:8000/api/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ useremail: email }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || "Vui lòng kiểm tra email để lấy link reset!");
      } else {
        setError(data.error || "Có lỗi xảy ra, vui lòng thử lại.");
      }
    } catch (err) {
      setError("Không thể kết nối đến server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <img src={logo} alt="Bách Khoa" className={styles.logo} />

      <div className={styles.card}>
        <h2 className={styles.title}>Quên mật khẩu</h2>
        <p style={{ textAlign: "center", marginBottom: "20px", fontSize: "14px" }}>
          Nhập email đăng ký của bạn để nhận hướng dẫn đặt lại mật khẩu.
        </p>

        {/* Hiển thị thông báo thành công hoặc lỗi */}
        {message && <div style={{ color: "green", textAlign: "center", marginBottom: "10px" }}>{message}</div>}
        {error && <div style={{ color: "red", textAlign: "center", marginBottom: "10px" }}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <label className={styles.label}>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className={styles.input}
              placeholder="Nhập email của bạn"
            />
          </div>

          <button type="submit" className={styles.button} disabled={loading}>
            {loading ? "Đang gửi..." : "Gửi yêu cầu"}
          </button>
        </form>

        <div className={styles.link}>
          <Link to="/login">Quay lại trang đăng nhập</Link>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;