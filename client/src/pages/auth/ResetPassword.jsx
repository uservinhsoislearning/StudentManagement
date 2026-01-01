import { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import logo from "../../assets/bachkhoa-logo.png";
import styles from "./Login.module.css"; // Tận dụng style của trang Login

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  // Lấy token từ URL (ví dụ: .../reset-password?token=abcdef...)
  const token = searchParams.get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Kiểm tra nếu không có token thì báo lỗi ngay
  useEffect(() => {
    if (!token) {
      setError("Đường dẫn không hợp lệ hoặc thiếu Token.");
    }
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    if (password !== confirmPassword) {
      setError("Mật khẩu xác nhận không khớp!");
      return;
    }

    setLoading(true);

    try {
      // Gọi method PUT vào cùng API
      const response = await fetch("http://localhost:8000/api/auth/forgot-password", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            token: token, 
            new_password: password 
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || "Đổi mật khẩu thành công!");
        // Chờ 2 giây rồi chuyển về trang login
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else {
        setError(data.error || "Token hết hạn hoặc không hợp lệ.");
      }
    } catch (err) {
      setError("Lỗi kết nối đến server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <img src={logo} alt="Bách Khoa" className={styles.logo} />

      <div className={styles.card}>
        <h2 className={styles.title}>Đặt lại mật khẩu</h2>

        {message && <div style={{ color: "green", textAlign: "center", marginBottom: "10px", fontWeight: "bold" }}>{message}</div>}
        {error && <div style={{ color: "red", textAlign: "center", marginBottom: "10px" }}>{error}</div>}

        {/* Chỉ hiện form nếu có token */}
        {token ? (
            <form onSubmit={handleSubmit}>
            <div className={styles.inputGroup}>
                <label className={styles.label}>Mật khẩu mới:</label>
                <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={styles.input}
                placeholder="Nhập mật khẩu mới"
                />
            </div>

            <div className={styles.inputGroup}>
                <label className={styles.label}>Xác nhận mật khẩu:</label>
                <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className={styles.input}
                placeholder="Nhập lại mật khẩu mới"
                />
            </div>

            <button type="submit" className={styles.button} disabled={loading}>
                {loading ? "Đang xử lý..." : "Xác nhận thay đổi"}
            </button>
            </form>
        ) : (
            <div className={styles.link}>
                <p>Vui lòng sử dụng đường link được gửi trong email của bạn.</p>
            </div>
        )}

        <div className={styles.link}>
          <Link to="/login">Quay lại đăng nhập</Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;