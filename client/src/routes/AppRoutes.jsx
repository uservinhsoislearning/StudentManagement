import { Route, Routes, Navigate} from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";

// Auth
import ForgotPassword from "../pages/auth/ForgotPassword";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";

// Admin pages
import AdminDashboard from "../pages/admin/Dashboard";
import ManageAllClasses from "../pages/admin/ManageAllClasses";
import ManageCourseClasses from "../pages/admin/ManageCourseClasses";
import ManageParents from "../pages/admin/ManageParents";
import ManageRegister from "../pages/admin/ManageRegister";
import ManageSemesters from "../pages/admin/ManageSemesters";
import ManageStudents from "../pages/admin/ManageStudents";
// import ManageSubjects from "../pages/admin/ManageSubjects";
import ManageTeachers from "../pages/admin/ManageTeachers";
import Reports from "../pages/admin/Reports";

// Teacher pages
import Assignments from "../pages/teacher/Assignments";
import Attendance from "../pages/teacher/Attendance";
import ClassDetail from "../pages/teacher/ClassDetail";
import GradesManagement from "../pages/teacher/GradesManagement";
import ManageClasses from "../pages/teacher/ManageClasses";
import Parent from "../pages/teacher/Parent";
import TeacherDashboard from "../pages/teacher/TeacherDashboard";
import TeacherGrading from "../pages/teacher/TeacherGrading";
// Student pages
import Courses from "../pages/student/Courses";
import Grades from "../pages/student/Grades";
import RegisterCourses from "../pages/student/RegisterCourses";
import Schedule from "../pages/student/Schedule";
import StudentDashboard from "../pages/student/StudentDashboard";
import SubmitAssignment from "../pages/student/SubmitAssignment";
// Parent pages
import Communication from "../pages/parent/Communication";
import ParentDashboard from "../pages/parent/ParentDashboard";
import ViewStudentProgress from "../pages/parent/ViewStudentProgress";

// Common pages (dùng chung cho nhiều role)
import Profile from "../pages/common/Profile";

// Layouts
import { useAuth } from "../context/AuthContext";
import AdminLayout from "../layouts/AdminLayout";
import ParentLayout from "../layouts/ParentLayout";
import StudentLayout from "../layouts/StudentLayout";
import TeacherLayout from "../layouts/TeacherLayout";
const RegisterWrapper = () => {
  const { user } = useAuth();
  if (!user) return <Login />; // chưa đăng nhập → yêu cầu login
  if (user.role !== "admin") return <h3 style={{ padding: "20px" }}>Bạn không có quyền truy cập</h3>;
  return <Register />;
};
const AppRoutes = () => {
  return (
    <Routes>
      {/*Navigate to login */}
      <Route path="/" element={<Navigate to="/login" replace />} /> 
      
      {/* Auth */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<RegisterWrapper />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Admin routes */}
      <Route path="/admin" element={<ProtectedRoute role="admin"><AdminLayout><AdminDashboard /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/manage-register" element={<ProtectedRoute role="admin"><AdminLayout><ManageRegister /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/manage-students" element={<ProtectedRoute role="admin"><AdminLayout><ManageStudents /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/manage-teachers" element={<ProtectedRoute role="admin"><AdminLayout><ManageTeachers /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/manage-parents" element={<ProtectedRoute role="admin"><AdminLayout><ManageParents /></AdminLayout></ProtectedRoute>} />
      {/* <Route path="/admin/manage-subjects" element={<ProtectedRoute role="admin"><AdminLayout><ManageSubjects /></AdminLayout></ProtectedRoute>} /> */}
      <Route path="/admin/manage-semesters" element={<ProtectedRoute role="admin"><AdminLayout><ManageSemesters /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/manage-classes" element={<ProtectedRoute role="admin"><AdminLayout><ManageAllClasses /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/manage-course-classes" element={<ProtectedRoute role="admin"><AdminLayout><ManageCourseClasses /></AdminLayout></ProtectedRoute>} />
      <Route path="/admin/reports" element={<ProtectedRoute role="admin"><AdminLayout><Reports /></AdminLayout></ProtectedRoute>} />

      {/* Teacher routes */}
      <Route path="/teacher" element={<ProtectedRoute role="teacher"><TeacherLayout><TeacherDashboard /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/manage-classes" element={<ProtectedRoute role="teacher"><TeacherLayout><ManageClasses /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/classes/:id" element={<ProtectedRoute role="teacher"><TeacherLayout><ClassDetail /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/attendance" element={<ProtectedRoute role="teacher"><TeacherLayout><Attendance /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/assignments" element={<ProtectedRoute role="teacher"><TeacherLayout><Assignments /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/grades" element={<ProtectedRoute role="teacher"><TeacherLayout><GradesManagement /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/grading" element={<ProtectedRoute role="teacher"><TeacherLayout><TeacherGrading /></TeacherLayout></ProtectedRoute>} />
      <Route path="/teacher/parents" element={<ProtectedRoute role="teacher"><TeacherLayout><Parent /></TeacherLayout></ProtectedRoute>} />
      {/* Student routes */}
      <Route path="/student" element={<ProtectedRoute role="student"><StudentLayout><StudentDashboard /></StudentLayout></ProtectedRoute>} />
      <Route path="/student/courses" element={<ProtectedRoute role="student"><StudentLayout><Courses /></StudentLayout></ProtectedRoute>} />
      <Route path="/student/submit-assignment" element={<ProtectedRoute role="student"><StudentLayout><SubmitAssignment /></StudentLayout></ProtectedRoute>} />
      <Route path="/student/schedule" element={<ProtectedRoute role="student"><StudentLayout><Schedule /></StudentLayout></ProtectedRoute>} />
      <Route path="/student/grades" element={<ProtectedRoute role="student"><StudentLayout><Grades /></StudentLayout></ProtectedRoute>} />
      <Route path="/student/register-courses" element={<ProtectedRoute role="student"><StudentLayout><RegisterCourses /></StudentLayout></ProtectedRoute>} />

      {/* Common route - profile */}
      <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />

      {/* Not found */}
      <Route path="*" element={<h2 style={{ padding: "20px" }}>404 - Không tìm thấy trang</h2>} />
    </Routes>
  );
};

export default AppRoutes;