// hooks/useTeacher.js
import { useEffect, useState } from "react";
import { getAllTeachers } from "../api/admin"; // 🔁 Đảm bảo đường dẫn đúng

const useTeachers = () => {
  const [teachers, setTeachers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        const data = await getAllTeachers();
        setTeachers(data);
      } catch (err) {
        console.error("Lỗi khi tải danh sách giáo viên:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchTeachers();
  }, []);

  return { teachers, setTeachers, loading };
};

export default useTeachers;