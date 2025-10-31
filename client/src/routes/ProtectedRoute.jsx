import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children, role = null }) => {
  const { user } = useAuth();

  // Nếu chưa có user => chưa đăng nhập
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (role && user.role.toLowerCase() !== role.toLowerCase()) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;