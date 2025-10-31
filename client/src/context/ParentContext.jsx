import { createContext, useContext, useEffect, useState } from "react";
import { fetchAllParents } from "../api/parents";

// 🎯 Tạo context
const ParentContext = createContext(null);

// 🎯 Provider component
export const ParentProvider = ({ children }) => {
  const [parents, setParents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadParents = async () => {
      try {
        const data = await fetchAllParents();
        setParents(data);
      } catch (err) {
        console.error("Lỗi khi tải danh sách phụ huynh:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    loadParents();
  }, []);

  return (
    <ParentContext.Provider value={{ parents, setParents, loading, error }}>
      {children}
    </ParentContext.Provider>
  );
};

// 🎯 Custom hook dùng trong component
export const useParents = () => {
  const context = useContext(ParentContext);
  if (!context) {
    throw new Error("useParents must be used within a ParentProvider");
  }
  return context;
};

// (tuỳ chọn) export thêm context nếu cần
export { ParentContext };
