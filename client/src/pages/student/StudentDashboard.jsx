import { useEffect, useState } from "react";
import {
  FaBookOpen,
  FaCalendarAlt,
  FaStar,
} from "react-icons/fa";
import { fetchStudentDashboard } from "../../api/dashboard";
import { fetchStudentByEmail } from "../../api/students";
import { useAuth } from "../../context/AuthContext";
import styles from "./StudentDashboard.module.css";

const StudentDashboard = () => {
  const { user } = useAuth();
  const [studentId, setStudentId] = useState(null);
  const [dashboard, setDashboard] = useState({
    enrolledCourses: 0,
    upcomingExams: 0,
    assignmentsPending: 0,
  });

  useEffect(() => {
    const fetchInfo = async () => {
      try {
        if (!user?.email) return;

        const student = await fetchStudentByEmail(user.email);
        if (!student) {
          console.warn("❌ Không tìm thấy student với email:", user.email);
          return;
        }

        setStudentId(student.student_id);
        const dashData = await fetchStudentDashboard(student.student_id);
        setDashboard(dashData);
      } catch (err) {
        console.error("❌ Lỗi khi tải dashboard:", err);
      }
    };

    fetchInfo();
  }, [user]);

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>🎓 Trang tổng quan học sinh</h1>

      <div className={styles.grid}>
        <div className={styles.card}>
          <FaBookOpen className={styles.icon} />
          <h3>Số lớp đang học</h3>
          <p>{dashboard.enrolledCourses}</p>
        </div>

        <div className={styles.card}>
          <FaStar className={styles.icon} />
          <h3>Bài tập chưa nộp</h3>
          <p>{dashboard.assignmentsPending}</p>
        </div>

        <div className={styles.card}>
          <FaCalendarAlt className={styles.icon} />
          <h3>Kỳ thi sắp tới</h3>
          <p>{dashboard.upcomingExams}</p>
        </div>
      </div>


    </div>
  );
};

export default StudentDashboard;