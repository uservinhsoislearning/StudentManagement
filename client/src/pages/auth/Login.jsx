import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import logo from "../../assets/bachkhoa-logo.png"; // đảm bảo logo ở đúng path
import { useAuth } from "../../context/AuthContext";
import styles from "./Login.module.css";

const Login = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await login(email, password, role);
      // Không navigate ở đây nữa
    } catch (err) {
      setError(err.message || "Đăng nhập thất bại!");
    }
  };

  // 👉 Tự động navigate sau khi user được set
  const location = useLocation();

  useEffect(() => {
    if (user && user.role && location.pathname === "/login") {
      navigate(`/${user.role.toLowerCase()}`); // ✅ dùng backticks để tạo template string
    }
  }, [user, location, navigate]);

  return (
    <div className={styles.container}>
      <img src={logo} alt="Bách Khoa" className={styles.logo} />

      <div className={styles.card}>
        <h2 className={styles.title}>Đăng nhập</h2>
        {error && <p style={{ color: "red" }}>{error}</p>}

        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <label className={styles.label}>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className={styles.input}
            />
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.label}>Mật khẩu:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className={styles.input}
            />
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.label}>Chọn vai trò:</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className={styles.select}
            >
              <option value="admin">Quản trị viên</option>
              <option value="teacher">Giáo viên</option>
              <option value="student">Sinh viên</option>
            </select>
          </div>

          <button type="submit" className={styles.button}>
            Đăng nhập
          </button>
        </form>

        <div className={styles.link}>
          <p>Nếu bạn chưa có tài khoản, <a href="http://localhost:5173/register">tạo</a>, hoặc vui lòng liên hệ quản trị viên.</p>
        </div>
      </div>
    </div>
  );
};

export default Login; 