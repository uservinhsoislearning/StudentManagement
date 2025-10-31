import { useEffect, useState } from "react";
import { fetchAdminDashboard } from "../../api/dashboard";

const AdminDashboard = () => {
  const [data, setData] = useState({
    totalStudents: 0,
    totalTeachers: 0,
    totalParents: 0,
    reportsPending: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetchAdminDashboard();
        setData(res);
      } catch (err) {
        console.error("❌ Lỗi khi tải dashboard:", err);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h2>Dashboard Quản trị viên</h2>
      <div>
        <p>Tổng số sinh viên: {data.totalStudents}</p>
        <p>Tổng số giáo viên: {data.totalTeachers}</p>
        <p>Tổng số phụ huynh: {data.totalParents}</p>
        <p>Báo cáo chưa xử lý: {data.reportsPending}</p>
      </div>
    </div>
  );
};

export default AdminDashboard;