import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import { useEffect, useState } from "react";
import * as XLSX from "xlsx";

import { getAllClasses, getStudentsInClass } from "../../api/classes";
import { fetchClassGrades, updateStudentGrade } from "../../api/teachers";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";

const GradesManagement = () => {
    const [classes, setClasses] = useState([]);
    const [selectedClassId, setSelectedClassId] = useState("");
    const [grades, setGrades] = useState([]);
    const [editing, setEditing] = useState({});
    const [searchTerm, setSearchTerm] = useState("");

    // 🟢 Load danh sách lớp
    useEffect(() => {
        getAllClasses().then((data) => {
            setClasses(
                data.map((cls) => ({
                    id: cls.class_id,
                    name: cls.class_name,
                }))
            );
        });
    }, []);

    const handleClassSelect = async (e) => {
        const classId = e.target.value;
        setSelectedClassId(classId);

        const [gradesData, students] = await Promise.all([
            fetchClassGrades(classId),
            getStudentsInClass(classId),
        ]);

        const gradesWithNames = gradesData.map((g) => {
            const student = students.find((s) => s.student_id === g.student);
            return {
                studentId: g.student,
                name: student?.student_name || "Không rõ",
                midterm: g.midterm,
                final: g.final,
                total: g.grade,
            };
        });

        setGrades(gradesWithNames);
        setEditing({});
        setSearchTerm("");
    };

    const handleGradeChange = (studentId, field, value) => {
        setEditing((prev) => ({
            ...prev,
            [studentId]: {
                ...prev[studentId],
                [field]: value,
            },
        }));
    };

    const handleSave = async (studentId) => {
        const grade = editing[studentId];
        if (!grade) return;

        try {
            // Gửi request cập nhật điểm
            await updateStudentGrade({
                classId: selectedClassId,
                studentId,
                midterm: grade.midterm,
                final: grade.final,
            });

            // Gọi lại API để lấy dữ liệu điểm mới nhất
            const [gradesData, students] = await Promise.all([
                fetchClassGrades(selectedClassId),
                getStudentsInClass(selectedClassId),
            ]);

            const gradesWithNames = gradesData.map((g) => {
                const student = students.find((s) => s.student_id === g.student);
                return {
                    studentId: g.student,
                    name: student?.student_name || "Không rõ",
                    midterm: g.midterm,
                    final: g.final,
                    total: g.grade,
                };
            });

            // Cập nhật lại UI
            setGrades(gradesWithNames);
            setEditing((prev) => ({ ...prev, [studentId]: undefined }));
        } catch (error) {
            console.error("❌ Cập nhật điểm thất bại:", error);
            alert("Không thể cập nhật điểm. Vui lòng thử lại.");
        }
    };

    const handleExportExcel = () => {
        const wsData = grades.map((g) => ({
            "Mã SV": g.studentId,
            "Họ tên": g.name,
            "Điểm giữa kỳ": g.midterm,
            "Điểm cuối kỳ": g.final,
            "Tổng điểm": g.total,
        }));

        const worksheet = XLSX.utils.json_to_sheet(wsData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, worksheet, "BangDiem");
        XLSX.writeFile(wb, `BangDiem_${selectedClassId}.xlsx`);
    };

    const handleExportPDF = () => {
        const doc = new jsPDF();
        autoTable(doc, {
            head: [["Mã SV", "Họ tên", "Điểm giữa kỳ", "Điểm cuối kỳ", "Tổng điểm"]],
            body: grades.map((g) => [
                g.studentId,
                g.name,
                g.midterm,
                g.final,
                g.total,
            ]),
        });
        doc.save(`BangDiem_${selectedClassId}.pdf`);
    };

    const filteredGrades = grades.filter(
        (g) =>
            String(g.studentId).toLowerCase().includes(searchTerm.toLowerCase()) ||
            g.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const tableData = filteredGrades.map((g) => {
        const isEditing = editing[g.studentId] !== undefined;
        const edit = editing[g.studentId] || {};
        const midterm = isEditing ? edit.midterm : g.midterm;
        const final = isEditing ? edit.final : g.final;
        const total =
            midterm !== undefined && final !== undefined
                ? ((+midterm + +final) / 2).toFixed(2)
                : g.total;

        return {
            "Mã SV": g.studentId,
            "Họ tên": g.name,
            "Điểm giữa kỳ": isEditing ? (
                <Input
                    type="number"
                    value={midterm}
                    onChange={(e) =>
                        handleGradeChange(g.studentId, "midterm", e.target.value)
                    }
                />
            ) : (
                g.midterm
            ),
            "Điểm cuối kỳ": isEditing ? (
                <Input
                    type="number"
                    value={final}
                    onChange={(e) =>
                        handleGradeChange(g.studentId, "final", e.target.value)
                    }
                />
            ) : (
                g.final
            ),
            "Tổng điểm": total,
            "Hành động": isEditing ? (
                <Button onClick={() => handleSave(g.studentId)}>Lưu</Button>
            ) : (
                <Button
                    variant="secondary"
                    onClick={() =>
                        setEditing((prev) => ({
                            ...prev,
                            [g.studentId]: { midterm: g.midterm, final: g.final },
                        }))
                    }
                >
                    Sửa
                </Button>
            ),
        };
    });

    return (
        <div style={{ padding: "24px" }}>
            <h2>Quản lý điểm sinh viên</h2>

            <div
                style={{
                    marginBottom: "16px",
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "12px",
                    alignItems: "center",
                }}
            >
                <label>Lớp học:</label>
                <select value={selectedClassId} onChange={handleClassSelect}>
                    <option value="">-- Chọn lớp --</option>
                    {classes.map((cls) => (
                        <option key={cls.id} value={cls.id}>
                            {cls.name}
                        </option>
                    ))}
                </select>

                {grades.length > 0 && (
                    <>
                        <Button variant="outline" onClick={handleExportExcel}>
                            Xuất Excel
                        </Button>
                        <Button variant="outline" onClick={handleExportPDF}>
                            Xuất PDF
                        </Button>
                    </>
                )}
            </div>

            {grades.length > 0 && (
                <>
                    <div style={{ maxWidth: "300px", marginBottom: "10px" }}>
                        <Input
                            placeholder="Tìm sinh viên theo mã hoặc tên"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <Table
                        columns={[
                            "Mã SV",
                            "Họ tên",
                            "Điểm giữa kỳ",
                            "Điểm cuối kỳ",
                            "Tổng điểm",
                            "Hành động",
                        ]}
                        data={tableData}
                    />
                </>
            )}
        </div>
    );
};

export default GradesManagement;