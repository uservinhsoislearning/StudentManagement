import { useEffect, useState } from "react";
import AdminLayout from "../../layouts/AdminLayout";
import Table from "../../components/UI/Table";
import  {fetchReports}  from "../../api/dashboard";

const Reports = () => {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetchReports().then(setReports);
  }, []);

  return (
    <AdminLayout>
      <h2>Quản lý Báo cáo</h2>
      <Table columns={["ID", "Loại", "Người gửi", "Nội dung", "Trạng thái"]} data={reports} />
    </AdminLayout>
  );
};

export default Reports;
