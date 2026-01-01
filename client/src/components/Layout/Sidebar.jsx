import {
  FaBars,
  FaBook,
  FaCalendarAlt,
  FaChalkboardTeacher,
  FaChartBar,
  FaClipboardList,
  FaHome,
  FaUserGraduate,
} from "react-icons/fa";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import styles from "./Sidebar.module.css";

const Sidebar = ({ collapsed, setCollapsed }) => {
  const { user } = useAuth();
  if (!user) return null;

  const toggleSidebar = () => setCollapsed(!collapsed);

  const menuConfig = {
    admin: [
      { label: "Dashboard", path: "/admin", icon: <FaHome /> },
      { label: "QL Học sinh", path: "/admin/manage-students", icon: <FaUserGraduate /> },
      { label: "QL Giáo viên", path: "/admin/manage-teachers", icon: <FaChalkboardTeacher /> },
      // { label: "QL Môn học", path: "/admin/manage-subjects", icon: <FaBook /> },
      { label: "QL Học kỳ", path: "/admin/manage-semesters", icon: <FaCalendarAlt /> },
      { label: "QL Lớp học phần", path: "/admin/manage-course-classes", icon: <FaClipboardList /> },
      { label: "QL Lớp", path: "/admin/manage-classes", icon: <FaClipboardList /> },

      { label: "Tạo tài khoản", path: "/admin/manage-register", icon: <FaUserGraduate /> },
      { label: "Báo cáo", path: "/admin/reports", icon: <FaChartBar /> },
    ],
    teacher: [
      { label: "Dashboard", path: "/teacher", icon: <FaHome /> },
      { label: "QL Lớp giảng dạy", path: "/teacher/manage-classes", icon: <FaClipboardList /> },
      { label: "Điểm danh", path: "/teacher/attendance", icon: <FaCalendarAlt /> },
      { label: "Bài tập", path: "/teacher/assignments", icon: <FaBook /> },
      { label: "Chấm bài tập", path: "/teacher/grading", icon: <FaBook /> },

      { label: "Quản lý điểm", path: "/teacher/grades", icon: <FaChartBar /> },
    ],
    student: [
      { label: "Dashboard", path: "/student", icon: <FaHome /> },
      { label: "Khoá học", path: "/student/courses", icon: <FaBook /> },
      { label: "Nộp bài tập", path: "/student/submit-assignment", icon: <FaBook /> },
      { label: "Thời khoá biểu", path: "/student/schedule", icon: <FaCalendarAlt /> },
      { label: "Kết quả học tập", path: "/student/grades", icon: <FaChartBar /> },
      { label: "Đăng ký học phần", path: "/student/register-courses", icon: <FaClipboardList /> },
    ],
  };

  const roleMenu = menuConfig[user.role.toLowerCase()] || [];

  return (
    <aside
      className={styles.sidebar}
      style={{
        width: collapsed ? "60px" : "220px",
        transition: "width 0.3s ease",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: collapsed ? "center" : "space-between",
          padding: "12px 16px",
        }}
      >
        {!collapsed && <h3 className={styles.logo}>🎓 BK System</h3>}
        <button
          onClick={toggleSidebar}
          style={{
            background: "none",
            border: "none",
            fontSize: "18px",
            cursor: "pointer",
            color: "#b22222",
          }}
        >
          <FaBars />
        </button>
      </div>

      <nav className={styles.nav}>
        {roleMenu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end
            className={({ isActive }) => (isActive ? styles.active : styles.link)}
            style={{
              display: "flex",
              alignItems: "center",
              padding: "10px 16px",
              gap: "12px",
              whiteSpace: "nowrap",
              overflow: "hidden",
              transition: "all 0.3s",
            }}
          >
            <span className={styles.icon}>{item.icon}</span>
            {!collapsed && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;