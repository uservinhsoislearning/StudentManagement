import { createContext, useContext, useState, useEffect } from "react";
import { fetchStudents } from "../api/students";

// 🎯 Tạo Context
const StudentContext = createContext(null);

// 🎯 Provider Component
export const StudentProvider = ({ children }) => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadStudents = async () => {
      try {
        const data = await fetchStudents();
        setStudents(data);
      } catch (err) {
        console.error("Lỗi khi tải danh sách học sinh:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    loadStudents();
  }, []);

  return (
    <StudentContext.Provider value={{ students, setStudents, loading, error }}>
      {children}
    </StudentContext.Provider>
  );
};

// 🎯 Custom hook dùng trong component
export const useStudents = () => {
  const context = useContext(StudentContext);
  if (!context) {
    throw new Error("useStudents must be used within a StudentProvider");
  }
  return context;
};

// 🎯 (Tuỳ chọn) Export context riêng nếu bạn cần truy cập trực tiếp
export { StudentContext };
