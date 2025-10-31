import { format } from "date-fns";
import { useState } from "react";
import { getStudentsInClass } from "../../api/classes";
import {
  createAttendanceList,
  getAttendanceList,
  sendAttendanceByEmail,
  toggleStudentAttendance,
} from "../../api/teachers";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";

const Attendance = () => {
  const [classId, setClassId] = useState("");
  const [students, setStudents] = useState([]);
  const [date, setDate] = useState(format(new Date(), "yyyy-MM-dd"));
  const [loadingCreate, setLoadingCreate] = useState(false);
  const [loadingFetch, setLoadingFetch] = useState(false);
  const [showTable, setShowTable] = useState(false);
  const [editable, setEditable] = useState(false);

  const handleCreateAttendanceList = async () => {
    if (!classId) return alert("Vui lòng nhập mã lớp!");
    setLoadingCreate(true);
    try {
      await createAttendanceList(classId);
      const list = await getStudentsInClass(classId);
      const formatted = list.map((s) => ({
        id: s.student_id,
        name: s.student_name,
        present: true,
      }));
      setStudents(formatted);
      setShowTable(true);
      setEditable(true); // ✅ Cho phép chỉnh sửa
    } catch (err) {
      alert("❌ Lỗi khi tạo danh sách điểm danh");
      console.error(err);
    } finally {
      setLoadingCreate(false);
    }
  };

  const handleLoadAttendanceStatus = async () => {
    if (!classId) return alert("Vui lòng nhập mã lớp!");
    setLoadingFetch(true);
    try {
      const [studentsRaw, attendanceRaw] = await Promise.all([
        getStudentsInClass(classId),
        getAttendanceList(classId),
      ]);

      const merged = studentsRaw.map((s) => {
        const match = attendanceRaw.find((a) => a.student === s.student_id);
        return {
          id: s.student_id,
          name: s.student_name,
          present: match ? match.is_present : true,
        };
      });

      setStudents(merged);
      setShowTable(true);
      setEditable(false); // ✅ Chỉ xem, không chỉnh sửa
    } catch (err) {
      alert("❌ Không thể hiển thị điểm danh: " + err.message);
      console.error(err);
    } finally {
      setLoadingFetch(false);
    }
  };

  const handleStatusChange = async (id) => {
    try {
      const res = await toggleStudentAttendance(classId, id);
      const message = res?.message || "";

      setStudents((prev) =>
        prev.map((s) =>
          s.id === id
            ? {
              ...s,
              present: message.includes("NOT present") ? false : true,
            }
            : s
        )
      );
    } catch (err) {
      alert("❌ Lỗi cập nhật trạng thái điểm danh");
      console.error(err);
    }
  };

  const handleSendAttendance = async () => {
    try {
      await sendAttendanceByEmail(classId, date, students);
      alert("✅ Gửi điểm danh qua email thành công!");
    } catch (err) {
      alert("❌ Lỗi gửi email: " + err.message);
    }
  };

  const handleCloseAttendance = () => {
    setShowTable(false);
    setStudents([]);
  };

  return (
    <div style={{ padding: "24px" }}>
      <h2>Điểm danh sinh viên</h2>

      <div
        style={{
          display: "flex",
          gap: "12px",
          marginBottom: "16px",
          flexWrap: "wrap",
        }}
      >
        <Input
          label="Mã lớp"
          value={classId}
          onChange={(e) => setClassId(e.target.value)}
          placeholder="Nhập mã lớp"
        />
        <Input
          type="date"
          label="Ngày điểm danh"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <Button onClick={handleCreateAttendanceList} disabled={loadingCreate}>
          {loadingCreate ? "Đang tạo..." : "📋 Tạo danh sách mới"}
        </Button>
        <Button onClick={handleLoadAttendanceStatus} disabled={loadingFetch}>
          {loadingFetch ? "Đang tải..." : "👁️ Hiển thị danh sách đã tạo"}
        </Button>
      </div>

      {showTable && (
        <>
          <Table
            columns={
              editable
                ? ["ID", "Họ và tên", "Trạng thái", "Hành động"]
                : ["ID", "Họ và tên", "Trạng thái"]
            }
            data={students.map((student) => {
              const row = {
                ID: student.id,
                "Họ và tên": student.name,
                "Trạng thái": student.present ? "✅ Có mặt" : "❌ Vắng mặt",
              };
              if (editable) {
                row["Hành động"] = (
                  <Button
                    variant={student.present ? "danger" : "success"}
                    onClick={() => handleStatusChange(student.id)}
                  >
                    {student.present
                      ? "❌ Đánh dấu vắng"
                      : "✅ Đánh dấu có mặt"}
                  </Button>
                );
              }
              return row;
            })}
          />

          <div style={{ marginTop: "16px", display: "flex", gap: "12px" }}>
            <Button variant="outline" onClick={handleCloseAttendance}>
              ❎ Đóng danh sách
            </Button>
            <Button variant="success" onClick={handleSendAttendance}>
              📤 Gửi qua email
            </Button>
          </div>
        </>
      )}
    </div>
  );
};

export default Attendance;