import { useEffect, useState } from "react";
import { fetchClassDetails, } from "../../api/classes";
import { fetchTeacherClassesByEmail } from "../../api/teachers";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";
import { useAuth } from "../../context/AuthContext";

const ManageClasses = () => {
  const { user } = useAuth();
  const [classes, setClasses] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSemester, setSelectedSemester] = useState("Tất cả");
  const [selectedClassDetail, setSelectedClassDetail] = useState(null);

  useEffect(() => {
    if (user?.email) {
      fetchTeacherClassesByEmail(user.email).then((data) => {
        setClasses(
          data.map((cls, i) => ({
            ...cls,
            name: cls.class_name,
            subject: cls.subject || "—",
            semester: `2024-${cls.class_semester || (i % 2) + 1}`,
            id: cls.class_id,
          }))
        );
      });
    }
  }, [user]);

  const handleShowClassDetails = async (classId) => {
    try {
      const detail = await fetchClassDetails(classId);
      setSelectedClassDetail(detail);
    } catch (err) {
      console.error("❌ Không thể tải thông tin lớp:", err);
      alert("Không thể tải chi tiết lớp học.");
    }
  };

  const filteredClasses = classes.filter((cls) => {
    const matchSearch =
      cls.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cls.subject.toLowerCase().includes(searchTerm.toLowerCase());

    const matchSemester =
      selectedSemester === "Tất cả" || cls.semester === selectedSemester;

    return matchSearch && matchSemester;
  });

  const semesters = ["Tất cả", ...new Set(classes.map((cls) => cls.semester))];

  const tableData = filteredClasses.map((cls) => ({
    ID: cls.id,
    "Tên lớp": cls.name,
    "Học kỳ": cls.semester,
    "Hành động": (
      <Button variant="outline" onClick={() => handleShowClassDetails(cls.id)}>
        Chi tiết
      </Button>
    ),
  }));

  return (
    <div style={{ padding: "24px" }}>
      <h2>Quản lý Lớp học</h2>

      <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: "10px", marginBottom: "20px" }}>
        <div style={{ display: "flex", gap: "10px" }}>
          <select
            value={selectedSemester}
            onChange={(e) => setSelectedSemester(e.target.value)}
            style={{ padding: "8px" }}
          >
            {semesters.map((sem) => (
              <option key={sem} value={sem}>
                {sem}
              </option>
            ))}
          </select>
          <Input
            placeholder="Tìm kiếm theo tên lớp hoặc môn học"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {filteredClasses.length === 0 ? (
        <p>⚠️ Không có lớp nào được tìm thấy.</p>
      ) : (
        <Table
          columns={["ID", "Tên lớp", "Học kỳ", "Hành động"]}
          data={tableData}
        />
      )}

      {selectedClassDetail && (
        <div style={{ marginTop: "32px", borderTop: "1px solid #ccc", paddingTop: "20px" }}>
          <h3>📘 Chi tiết lớp học</h3>
          <p><strong>Môn học:</strong> {selectedClassDetail.course_name}</p>
          <h4>Lịch học:</h4>
          <ul>
            {selectedClassDetail.schedule.map((s, idx) => (
              <li key={idx}>
                📅 {s.day_of_week} — ⏰ {s.start_time} → {s.end_time}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ManageClasses;