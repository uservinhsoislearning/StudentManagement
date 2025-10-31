import { useEffect, useState } from "react";
import { fetchAllParents, fetchParentDashboard } from "../../api/parents";
import { useAuth } from "../../context/AuthContext";
import styles from "./ParentDashboard.module.css";

const fetchParentByEmail = async (email) => {
  const parents = await fetchAllParents();
  return parents.find((p) => p.email === email);
};

const ParentDashboard = () => {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState({
    children: [],
    messages: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      if (!user?.email) return;

      try {
        const parent = await fetchParentByEmail(user.email);
        if (!parent) {
          console.warn("❌ Không tìm thấy parent với email:", user.email);
          return;
        }

        const data = await fetchParentDashboard(parent.parent_id);
        setDashboard(data);
      } catch (err) {
        console.error("Lỗi khi tải dashboard phụ huynh:", err);
        setError("❌ Không thể tải dữ liệu tổng quan.");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [user]);

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>🎓 Dashboard Phụ huynh</h2>

      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : error ? (
        <p className={styles.error}>{error}</p>
      ) : (
        <div className={styles.statsGrid}>
          <div className={styles.card}>
            <h3>📨 Thông báo học tập</h3>
            <p>{dashboard.messages}</p>
          </div>

          <div className={styles.card}>
            <h3>👨‍👩‍👧‍👦 Các con</h3>
            {Array.isArray(dashboard.children) && dashboard.children.length > 0 ? (
              <ul>
                {dashboard.children.map((child, idx) => (
                  <li key={idx}>
                    <strong>{child.name}</strong> – Tiến độ: {child.progress}
                  </li>
                ))}
              </ul>
            ) : (
              <p>Không có dữ liệu học sinh.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ParentDashboard;