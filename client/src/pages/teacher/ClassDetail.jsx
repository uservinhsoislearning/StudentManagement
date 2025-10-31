import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import {
    addStudentToClass,
    getClassById,
    getClassStatistics,
    getStudentsInClass,
    removeStudentFromClass,
    updateStudentScore,
} from "../../api/classes";
import { fetchStudents } from "../../api/students";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Modal from "../../components/UI/Modal";
import Table from "../../components/UI/Table";
import { useTeachers } from "../../context/TeacherContext";
import TeacherLayout from "../../layouts/TeacherLayout";

const ClassDetail = () => {
    const { id } = useParams();
    const { teachers } = useTeachers();

    const [classInfo, setClassInfo] = useState(null);
    const [students, setStudents] = useState([]);
    const [allStudents, setAllStudents] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [statistics, setStatistics] = useState(null);

    const [isAddModalOpen, setAddModalOpen] = useState(false);
    const [isScoreModalOpen, setScoreModalOpen] = useState(false);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [score, setScore] = useState("");

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [cls, svList, stats, allSv] = await Promise.all([
                    getClassById(id),
                    getStudentsInClass(id),
                    getClassStatistics(id),
                    fetchStudents(),
                ]);
                setClassInfo(cls);
                setStudents(svList);
                setStatistics(stats);
                setAllStudents(allSv);
            } catch (err) {
                console.error("Lỗi khi tải dữ liệu lớp:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    const handleRemoveStudent = async (studentId) => {
        if (window.confirm("Bạn có chắc muốn xoá sinh viên này khỏi lớp?")) {
            await removeStudentFromClass(id, studentId);
            setStudents(students.filter((sv) => sv.id !== studentId));
        }
    };

    const handleAddStudent = async (e) => {
        e.preventDefault();
        await addStudentToClass(id, selectedStudent);
        const updatedList = await getStudentsInClass(id);
        setStudents(updatedList);
        setAddModalOpen(false);
        setSelectedStudent(null);
    };

    const handleOpenScoreModal = (student) => {
        setSelectedStudent(student);
        setScore(student.averageScore || "");
        setScoreModalOpen(true);
    };

    const handleUpdateScore = async (e) => {
        e.preventDefault();
        await updateStudentScore(id, selectedStudent.id, { score: parseFloat(score) });
        const updatedList = await getStudentsInClass(id);
        setStudents(updatedList);
        setScoreModalOpen(false);
    };

    const getTeacherName = (teacherId) => {
        const teacher = teachers.find((t) => t.id === teacherId);
        return teacher ? teacher.name : "Không xác định";
    };

    const filteredStudents = students.filter(
        (sv) =>
            sv.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            sv.studentCode.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const tableData = filteredStudents.map((sv) => ({
        "Mã SV": sv.studentCode,
        "Họ tên": sv.name,
        "Email": sv.email,
        "Điểm trung bình": sv.averageScore ?? "Chưa có",
        "Hành động": (
            <>
                <Button variant="secondary" onClick={() => handleOpenScoreModal(sv)} style={{ marginRight: "8px" }}>
                    Sửa điểm
                </Button>
                <Button variant="danger" onClick={() => handleRemoveStudent(sv.id)}>
                    Xoá
                </Button>
            </>
        ),
    }));

    const availableStudents = allStudents.filter(
        (s) => !students.some((sv) => sv.id === s.id)
    );

    if (loading) {
        return (
            <TeacherLayout>
                <p>Đang tải dữ liệu lớp học...</p>
            </TeacherLayout>
        );
    }

    return (
        <TeacherLayout>
            <h2>Chi tiết lớp học</h2>

            <div style={{ marginBottom: "20px" }}>
                <p><strong>Tên lớp:</strong> {classInfo.name}</p>
                <p><strong>Môn học:</strong> {classInfo.subject}</p>
                <p><strong>Học kỳ:</strong> {classInfo.semester}</p>
                <p><strong>Giáo viên:</strong> {getTeacherName(classInfo.teacherId)}</p>
                <p><strong>Sĩ số:</strong> {students.length} sinh viên</p>
            </div>

            {statistics && (
                <div style={{ height: 300, marginBottom: 40 }}>
                    <h4>Thống kê điểm lớp</h4>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={[
                            { name: "Điểm TB", value: statistics.averageScore },
                            { name: "Cao nhất", value: statistics.maxScore },
                            { name: "Thấp nhất", value: statistics.minScore },
                        ]}>
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="value" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
                <Input
                    placeholder="Tìm kiếm sinh viên theo tên hoặc mã SV"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button onClick={() => setAddModalOpen(true)}>Thêm sinh viên</Button>
            </div>

            <Table
                columns={["Mã SV", "Họ tên", "Email", "Điểm trung bình", "Hành động"]}
                data={tableData}
            />

            {/* Modal thêm sinh viên */}
            <Modal isOpen={isAddModalOpen} onClose={() => setAddModalOpen(false)} title="Thêm sinh viên vào lớp">
                <Form onSubmit={handleAddStudent}>
                    <label>Chọn sinh viên:</label>
                    <select
                        value={selectedStudent || ""}
                        onChange={(e) => setSelectedStudent(e.target.value)}
                        required
                        style={{ padding: "8px", width: "100%", marginBottom: "15px" }}
                    >
                        <option value="">-- Chọn sinh viên --</option>
                        {availableStudents.map((s) => (
                            <option key={s.id} value={s.id}>
                                {s.name} ({s.studentCode || s.id})
                            </option>
                        ))}
                    </select>
                    <Button type="submit">Thêm vào lớp</Button>
                </Form>
            </Modal>

            {/* Modal sửa điểm */}
            <Modal isOpen={isScoreModalOpen} onClose={() => setScoreModalOpen(false)} title="Cập nhật điểm">
                <Form onSubmit={handleUpdateScore}>
                    <Input
                        label="Điểm trung bình"
                        type="number"
                        value={score}
                        onChange={(e) => setScore(e.target.value)}
                    />
                    <Button type="submit">Lưu điểm</Button>
                </Form>
            </Modal>
        </TeacherLayout>
    );
};

export default ClassDetail;