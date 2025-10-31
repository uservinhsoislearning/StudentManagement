import { AuthProvider, useAuth } from "./context/AuthContext";
import { ParentProvider } from "./context/ParentContext";
import { StudentProvider } from "./context/StudentContext";
import { TeacherProvider } from "./context/TeacherContext";
import AppRoutes from "./routes/AppRoutes";
import "./styles/global.css";

const AppWrapper = () => {
  const { loading } = useAuth();

  if (loading) {
    return <p style={{ textAlign: "center", marginTop: "50px" }}>Đang tải thông tin người dùng...</p>;
  }

  return <AppRoutes />;
};

const App = () => {
  return (
    <AuthProvider>
      <StudentProvider>
        <TeacherProvider>
          <ParentProvider>
            <AppWrapper />
          </ParentProvider>
        </TeacherProvider>
      </StudentProvider>
    </AuthProvider>
  );
};

export default App;