import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { useEffect, useState } from "react";
import * as XLSX from "xlsx";

import { getClassById } from "../../api/classes";
import { fetchStudentGradesById } from "../../api/students";
import Button from "../../components/UI/Button";
import Table from "../../components/UI/Table";

const CURRENT_STUDENT_ID = 1;

const Grades = () => {
  const [grades, setGrades] = useState([]);
  const [displayData, setDisplayData] = useState([]);

  useEffect(() => {
    const fetchGrades = async () => {
      try {
        const raw = await fetchStudentGradesById(CURRENT_STUDENT_ID);
        console.log("🎓 Raw grades:", raw);

        const enriched = await Promise.all(
          raw.map(async (g) => {
            try {
              const cls = await getClassById(g.class_field);
              return {
                class: cls.class_name,
                midterm: g.midterm,
                final: g.final,
                total: g.grade,
              };
            } catch (e) {
              return {
                class: `Lớp ${g.class_field}`,
                midterm: g.midterm,
                final: g.final,
                total: g.grade,
              };
            }
          })
        );

        setGrades(enriched);

        // ⚠️ Chuyển key cho đúng với columns trong Table
        const tableReady = enriched.map((g) => ({
          "Lớp": g.class,
          "Điểm giữa kỳ": g.midterm,
          "Điểm cuối kỳ": g.final,
          "Tổng điểm": g.total,
        }));

        setDisplayData(tableReady);
      } catch (err) {
        console.error("❌ Lỗi khi lấy bảng điểm:", err);
      }
    };

    fetchGrades();
  }, []);

  const handleExportExcel = () => {
    const ws = XLSX.utils.json_to_sheet(displayData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "BangDiem");
    XLSX.writeFile(wb, "BangDiemSinhVien.xlsx");
  };

  const handleExportPDF = () => {
    const doc = new jsPDF();
    autoTable(doc, {
      head: [["Lớp", "Điểm giữa kỳ", "Điểm cuối kỳ", "Tổng điểm"]],
      body: displayData.map((g) => [
        g["Lớp"],
        g["Điểm giữa kỳ"],
        g["Điểm cuối kỳ"],
        g["Tổng điểm"],
      ]),
    });
    doc.save("BangDiemSinhVien.pdf");
  };

  return (
    <div style={{ padding: "24px" }}>
      <h2>Kết quả học tập</h2>

      <div
        style={{
          marginBottom: "10px",
          display: "flex",
          justifyContent: "flex-end",
          gap: "10px",
        }}
      >
        <Button onClick={handleExportExcel}>📥 Xuất Excel</Button>
        <Button variant="outline" onClick={handleExportPDF}>
          🧾 Xuất PDF
        </Button>
      </div>

      <Table
        columns={["Lớp", "Điểm giữa kỳ", "Điểm cuối kỳ", "Tổng điểm"]}
        data={displayData}
      />
    </div>
  );
};

export default Grades;