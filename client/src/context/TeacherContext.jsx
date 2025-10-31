import { createContext, useContext, useEffect, useState } from "react";
import { fetchAllTeachers } from "../api/teachers";

// 🎯 Tạo context
const TeacherContext = createContext(null);

// 🎯 Provider component
export const TeacherProvider = ({ children }) => {
  const [teachers, setTeachers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadTeachers = async () => {
      try {
        const data = await fetchAllTeachers();
        setTeachers(data);
      } catch (err) {
        console.error("Lỗi khi tải danh sách giáo viên:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    loadTeachers();
  }, []);

  return (
    <TeacherContext.Provider value={{ teachers, setTeachers, loading, error }}>
      {children}
    </TeacherContext.Provider>
  );
};

// 🎯 Custom hook dùng trong component
export const useTeachers = () => {
  const context = useContext(TeacherContext);
  if (!context) {
    throw new Error("useTeachers must be used within a TeacherProvider");
  }
  return context;
};

// (Tuỳ chọn) export context nếu cần
export { TeacherContext };
