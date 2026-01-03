import { useRef, useState } from "react";
import {
  addAssignment,
  addAssignmentWithFile,
  fetchAssignments,
} from "../../api/teachers";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";
import styles from "./Assignments.module.css"; // ⬅️ import CSS module

const Assignments = () => {
  const [groupedByClass, setGroupedByClass] = useState({});
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedClass, setSelectedClass] = useState(null);
  const [newAssignment, setNewAssignment] = useState({
    text_content: "",
    deadline: "",
    is_exam: false,
    file: null,
  });
  const scrollRefs = useRef({});

  const handleLoadClassAssignments = async () => {
    const classId = searchTerm.trim();
    if (!classId) return alert("Vui lòng nhập mã lớp!");
    try {
      const assignments = await fetchAssignments(classId);
      setGroupedByClass((prev) => ({ ...prev, [classId]: assignments }));
      setSelectedClass(classId);
      setTimeout(() => {
        scrollRefs.current[classId]?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err) {
      alert("❌ Không thể tải bài tập.");
    }
  };

  const handleAddAssignment = async (classId) => {
    if (!newAssignment.text_content || !newAssignment.deadline) {
      alert("Vui lòng nhập đầy đủ nội dung và hạn chót");
      return;
    }

    try {
      if (newAssignment.file) {
        await addAssignmentWithFile(classId, newAssignment);
      } else {
        await addAssignment(classId, newAssignment);
      }

      alert("✅ Đã thêm bài tập");
      setNewAssignment({ text_content: "", deadline: "", is_exam: false, file: null });

      const assignments = await fetchAssignments(classId);
      setGroupedByClass((prev) => ({ ...prev, [classId]: assignments }));
    } catch {
      alert("❌ Không thể thêm bài tập");
    }
  };

  return (
    <div className={styles.container}>
      <h2>Quản lý Bài tập theo Lớp</h2>

      <div style={{ display: "flex", gap: "12px", marginBottom: "16px" }}>
        <Input
          placeholder="Nhập mã lớp..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button onClick={handleLoadClassAssignments}>Tìm kiếm</Button>
      </div>

      {selectedClass && groupedByClass[selectedClass] && (
        <div ref={(el) => (scrollRefs.current[selectedClass] = el)} style={{ marginTop: "40px" }}>
          <h3>Lớp {selectedClass} - Thêm bài tập</h3>

          <div className={styles.formGrid}>
            <Input
              placeholder="Nội dung bài tập"
              value={newAssignment.text_content}
              onChange={(e) =>
                setNewAssignment((prev) => ({
                  ...prev,
                  text_content: e.target.value,
                }))
              }
            />

            <Input
              type="datetime-local"
              value={newAssignment.deadline}
              onChange={(e) =>
                setNewAssignment((prev) => ({
                  ...prev,
                  deadline: e.target.value,
                }))
              }
            />

            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(e) =>
                setNewAssignment((prev) => ({
                  ...prev,
                  file: e.target.files[0],
                }))
              }
            />

            <div className={styles.checkboxGroup}>
              <input
                type="checkbox"
                id="is_exam"
                checked={newAssignment.is_exam}
                onChange={(e) =>
                  setNewAssignment((prev) => ({
                    ...prev,
                    is_exam: e.target.checked,
                  }))
                }
              />
              <label htmlFor="is_exam" style={{ fontWeight: "bold" }}>
                Là bài kiểm tra?
              </label>
            </div>

            <Button
              onClick={() => handleAddAssignment(selectedClass)}
              className={styles.buttonFullWidth}
            >
              Thêm bài tập
            </Button>

          </div>

          <Table
            columns={["ID", "Nội dung", "Hạn chót", "File", "KT?"]}
            data={groupedByClass[selectedClass].map((a) => ({
              "ID": a.assignment_id,
              "Nội dung": a.text_content,
              "Hạn chót": new Date(a.deadline).toLocaleString("vi-VN"),
              File: a.file ? (
                <a href={a.file} target="_blank" rel="noreferrer">
                  Tải xuống
                </a>
              ) : (
                "Không"
              ),
              "KT?": a.is_exam ? "✅" : "❌",
            }))}
          />
        </div>
      )}
    </div>
  );
};

export default Assignments;