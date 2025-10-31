import { createContext, useContext, useEffect, useState } from "react";
import {
  getCurrentUser,
  loginUser,
  logoutUser,
  registerUser,
} from "../api/auth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // để chờ khi gọi getCurrentUser

  useEffect(() => {
    const loadUser = async () => {
      try {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
          setUser(JSON.parse(storedUser));
        } else {
          const userData = await getCurrentUser();
          setUser(userData);
          localStorage.setItem("user", JSON.stringify(userData));
        }
      } catch (err) {
        console.warn("Không thể lấy thông tin người dùng:", err);
        setUser(null);
        localStorage.removeItem("user");
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (email, password, role) => {
    const userDataFromAPI = await loginUser(email, password, role);
    const userData = {
      ...userDataFromAPI,
      role: userDataFromAPI.usertype,
      email: userDataFromAPI.teacher_email || userDataFromAPI.useremail || userDataFromAPI.email, // chuẩn hoá lại field
    };
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const register = async (name, email, password) => {
    await registerUser(name, email, password);
    // ❗ Optional: tự login sau khi đăng ký
    // const userData = await loginUser(email, password);
    // setUser(userData);
    // localStorage.setItem("user", JSON.stringify(userData));
  };

  const logout = async () => {
    await logoutUser();
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
