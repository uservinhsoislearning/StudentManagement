import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import logo from "../../assets/bachkhoa-logo.png"; // đảm bảo logo ở đúng path
import { useAuth } from "../../context/AuthContext";
import styles from "./Login.module.css";

const Login = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [role, setRole] = useState("student");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await login(identifier, password, role);
      // Không navigate ở đây nữa
    } catch (err) {
      setError(err.message || "Đăng nhập thất bại!");
    }
  };

  // 👉 Tự động navigate sau khi user được set
  const location = useLocation();

  useEffect(() => {
    if (user && user.role && location.pathname === "/login") {
      navigate(`/${user.role.toLowerCase()}`);
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
            <label className={styles.label}>Email/Username</label>
            <input
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              required
              className={styles.input}
              placeholder="Nhập email hoặc username"
            />
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.label}>Password</label>
            {/* Wrapper div for relative positioning */}
            <div className={styles.passwordWrapper}>
              <input
                // Dynamic type based on state
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={styles.input}
                placeholder="Mật khẩu"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className={styles.toggleBtn}
              >
                {showPassword ? (
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" width="20" height="20">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" width="20" height="20">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          <div className={styles.inputGroup}>
            <label className={styles.label}>Vai trò</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className={styles.select}
            >
              <option value="admin">Admin</option>
              <option value="teacher">Giáo viên</option>
              <option value="student">Sinh viên</option>
            </select>
          </div>

          <button type="submit" className={styles.button}>
            Đăng nhập
          </button>
        </form>

        <div className={styles.link}>
          <p>Nếu bạn chưa có tài khoản, liên hệ Admin qua email vinhthanhtran03102004@gmail.com.</p>
          <a href="/forgot-password">Quên mật khẩu?</a>
        </div>
      </div>
    </div>
  );
};

export default Login; 