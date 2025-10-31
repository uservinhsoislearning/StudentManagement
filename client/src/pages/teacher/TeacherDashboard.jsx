import { useEffect, useState } from "react";
import { fetchTeacherDashboard } from "../../api/dashboard";
import { fetchTeacherByEmail, } from "../../api/teachers";
import { useAuth } from "../../context/AuthContext";
import styles from "./TeacherDashboard.module.css";

const TeacherDashboard = () => {
  const { user } = useAuth();
  const [data, setData] = useState({
    totalClasses: 0,
    assignmentsDue: 0,
    attendancePending: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        if (!user?.email) return;

        const teacher = await fetchTeacherByEmail(user.email);
        if (!teacher) {
          setError("❌ Không tìm thấy giáo viên.");
          return;
        }

        const res = await fetchTeacherDashboard(teacher.teacher_id);
        setData(res);
      } catch (err) {
        setError("❌ Không thể tải dữ liệu tổng quan.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [user]);

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Dashboard Giáo viên</h2>
      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : error ? (
        <p className={styles.error}>{error}</p>
      ) : (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <h3>Lớp học</h3>
            <p>{data.totalClasses}</p>
          </div>
          <div className={styles.statCard}>
            <h3>Bài tập sắp đến hạn</h3>
            <p>{data.assignmentsDue}</p>
          </div>
          <div className={styles.statCard}>
            <h3>Điểm danh chưa hoàn tất</h3>
            <p>{data.attendancePending}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherDashboard;