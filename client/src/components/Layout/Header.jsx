import { useAuth } from "../../context/AuthContext";
import styles from "./Header.module.css";

const Header = () => {
  console.log("👉 Header rendered at", window.location.pathname);

  const { user, logout } = useAuth();

  return (
    <header className={styles.header}>
      <h1 className={styles.title}>🎓 Hệ thống quản trị sinh viên</h1>
      <div className={styles.userBox}>
        <span>
          Xin chào, <strong>{user?.username || "User"}</strong>!
        </span>
        <button className={styles.logout} onClick={logout}>
          Đăng xuất
        </button>
      </div>
    </header>
  );
};

export default Header;