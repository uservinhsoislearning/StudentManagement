import { useEffect, useState } from "react";
import { fetchStudents } from "../../api/students";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";

const ManageStudents = () => {
  const [students, setStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const allData = await fetchStudents();
        setStudents(Array.isArray(allData) ? allData : []);
      } catch (error) {
        console.error("❌ Lỗi khi tải dữ liệu sinh viên:", error);
        setStudents([]);
      }
    };

    fetchData();
  }, []);

  const filteredStudents = students.filter(
    (student) =>
      student.student_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.student_email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.student_id?.toString().includes(searchTerm)
  );

  const tableData = filteredStudents.map((student) => ({
    ID: student.student_id,
    "Họ và tên": student.student_name,
    Email: student.student_email,
    "Giới tính": student.student_gender,
    "Chuyên ngành": student.student_specialization,
    "Trường": student.student_school,
  }));

  return (
    <div>
      <h2>Danh sách Sinh viên</h2>

      <div style={{ display: "flex", gap: "10px", marginBottom: "16px" }}>
        <Input
          placeholder="Tìm theo ID, tên hoặc email"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button onClick={() => setSearchTerm("")}>Xoá tìm kiếm</Button>
      </div>

      {tableData.length > 0 ? (
        <Table
          columns={["ID", "Họ và tên", "Email", "Giới tính", "Chuyên ngành", "Trường"]}
          data={tableData}
        />
      ) : (
        <p style={{ padding: "10px", backgroundColor: "#f8f8f8", borderRadius: "4px" }}>
          ⚠️ Không tìm thấy sinh viên nào.
        </p>
      )}
    </div>
  );
};

export default ManageStudents;
