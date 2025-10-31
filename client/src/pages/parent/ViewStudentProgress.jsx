import { useEffect, useState } from "react";
import { fetchStudentProgress } from "../../api/parents";
import { getSemesters } from "../../api/semesters";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";
import styles from "./ViewStudentProgress.module.css";
const ViewStudentProgress = () => {
  const [progressData, setProgressData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [semesters, setSemesters] = useState([]);
  const [semesterId, setSemesterId] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    getSemesters().then(setSemesters);
  }, []);

  useEffect(() => {
    fetchStudentProgress({ semesterId }).then((data) => {
      setProgressData(data);
      setSearchTerm(""); // reset tìm kiếm khi đổi học kỳ
    });
  }, [semesterId]);

  useEffect(() => {
    const filtered = progressData.filter(
      (item) =>
        item.studentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.subject.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredData(filtered);
  }, [progressData, searchTerm]);

  return (
    <div className={styles.container}>
      <h2>Tiến độ học tập của con</h2>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", marginBottom: "16px" }}>
        <select value={semesterId} onChange={(e) => setSemesterId(e.target.value)}>
          <option value="">-- Chọn học kỳ --</option>
          {semesters.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>

        <Input
          placeholder="Tìm theo tên học sinh hoặc môn học"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <Table
        columns={["Họ và tên", "Môn học", "Điểm trung bình", "Trạng thái"]}
        data={filteredData.map((item) => ({
          "Họ và tên": item.studentName,
          "Môn học": item.subject,
          "Điểm trung bình": item.averageScore ?? "—",
          "Trạng thái": item.status,
        }))}
      />
    </div>
  );
};

export default ViewStudentProgress;