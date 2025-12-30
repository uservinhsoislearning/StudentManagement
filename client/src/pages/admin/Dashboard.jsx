import { useEffect, useState } from "react";
import { 
  FaUserGraduate, 
  FaChalkboardTeacher, 
  FaUserFriends, 
  FaExclamationTriangle 
} from "react-icons/fa";
import { fetchAdminDashboard } from "../../api/dashboard";
import styles from "./AdminDashboard.module.css";

const AdminDashboard = () => {
  const [data, setData] = useState({
    totalStudents: 0,
    totalTeachers: 0,
    totalParents: 0,
    reportsPending: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetchAdminDashboard();
        setData(res);
      } catch (err) {
        console.error("❌ Lỗi khi tải dashboard:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Configuration for the cards
  // We use bg (background) and color (text) for dynamic styling
  const statsCards = [
    {
      id: 1,
      label: "Tổng sinh viên",
      value: data.totalStudents,
      icon: <FaUserGraduate />,
      bg: "#eff6ff",    // Light Blue
      color: "#2563eb", // Blue
    },
    {
      id: 2,
      label: "Tổng giáo viên",
      value: data.totalTeachers,
      icon: <FaChalkboardTeacher />,
      bg: "#f0fdf4",    // Light Green
      color: "#16a34a", // Green
    },
    {
      id: 3,
      label: "Báo cáo cần xử lý",
      value: data.reportsPending,
      icon: <FaExclamationTriangle />,
      bg: "#fef2f2",    // Light Red
      color: "#dc2626", // Red
    },
  ];

  if (loading) return <div className={styles.container}>Loading...</div>;

  return (
    <div className={styles.container}>
      {/* Header Section */}
      <div className={styles.header}>
        <h2 className={styles.title}>Dashboard Quản trị viên</h2>
        <p className={styles.subtitle}>Tổng quan về hệ thống và số liệu thống kê.</p>
      </div>

      {/* Stats Grid */}
      <div className={styles.statsGrid}>
        {statsCards.map((stat) => (
          <div key={stat.id} className={styles.card}>
            {/* Colored Icon Box */}
            <div 
              className={styles.iconWrapper} 
              style={{ backgroundColor: stat.bg, color: stat.color }}
            >
              {stat.icon}
            </div>
            
            {/* Text Content */}
            <div className={styles.content}>
              <span className={styles.cardLabel}>{stat.label}</span>
              <h3 className={styles.cardValue}>{stat.value}</h3>
            </div>
          </div>
        ))}
      </div>

      {/* Placeholder for future Charts or Tables */}
      {/* <div className={styles.section}>
         <h3>Biểu đồ thống kê...</h3>
      </div> */}
    </div>
  );
};

export default AdminDashboard;