import { useEffect, useState } from "react";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Modal from "../../components/UI/Modal";
import Table from "../../components/UI/Table";

import {
    addStudentToClass,
    createClass,
    deleteClass,
    getAllClasses,
    getStudentsInClass,
    removeStudentFromClass,
    updateClass,
} from "../../api/classes";

import { fetchStudents } from "../../api/students";
import styles from "./ManageAllClasses.module.css";

const ManageAllClasses = () => {
    const [allClasses, setAllClasses] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [editingClass, setEditingClass] = useState(null);
    const [expandedRows, setExpandedRows] = useState({});
    const [modalClassId, setModalClassId] = useState(null);
    const [allStudents, setAllStudents] = useState([]);
    const [newStudentId, setNewStudentId] = useState("");

    const [formData, setFormData] = useState({
        class_name: "",
        class_teacher: "",
        class_semester: "",
        course: "",
    });

    useEffect(() => {
        fetchAllClasses();
        fetchStudents().then(setAllStudents);
    }, []);

    const fetchAllClasses = async () => {
        const data = await getAllClasses();
        setAllClasses(data);
    };

    const handleSearch = (e) => setSearchTerm(e.target.value);

    const openEditModal = (cls) => {
        setEditingClass(cls);
        setFormData({
            class_name: cls.class_name || "",
            class_teacher: cls.class_teacher?.toString() || "",
            class_semester: cls.class_semester?.toString() || "",
            course: cls.course?.toString() || "",
        });
    };

    const handleDelete = async (id) => {
        if (window.confirm("Xoá lớp học này?")) {
            try {
                await deleteClass(id);
                fetchAllClasses();
            } catch (err) {
                alert("❌ Không thể xoá lớp học này!");
                console.error(err);
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const payload = {
            ...formData,
            class_teacher: Number(formData.class_teacher),
            class_semester: Number(formData.class_semester),
            course: Number(formData.course),
        };

        try {
            if (editingClass && editingClass.class_id) {
                await updateClass(editingClass.class_id, {
                    ...payload,
                    class_id: editingClass.class_id,
                });
                alert("✅ Đã cập nhật lớp học!");
            } else {
                await createClass(payload);
                alert("✅ Đã tạo lớp học mới!");
            }
            setFormData({ class_name: "", class_teacher: "", class_semester: "", course: "" });
            setEditingClass(null);
            setSearchTerm("");
            await fetchAllClasses();
        } catch (err) {
            alert("❌ Lỗi khi lưu lớp học!");
            console.error(err);
        }
    };

    const toggleStudents = async (classId) => {
        if (expandedRows[classId]) {
            setExpandedRows((prev) => ({ ...prev, [classId]: null }));
        } else {
            const students = await getStudentsInClass(classId);
            setExpandedRows((prev) => ({ ...prev, [classId]: students }));
        }
    };

    const handleAddStudent = async (e) => {
        e.preventDefault();
        if (!modalClassId || !newStudentId) return;
        try {
            await addStudentToClass(modalClassId, newStudentId);
            const updated = await getStudentsInClass(modalClassId);
            setExpandedRows((prev) => ({ ...prev, [modalClassId]: updated }));
            setNewStudentId("");
            setModalClassId(null);
        } catch (err) {
            alert("❌ Lỗi khi thêm sinh viên!");
            console.error(err);
        }
    };

    const filtered = allClasses.filter(
        (c) =>
            c.class_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.class_id?.toString().includes(searchTerm)
    );

    const tableData = filtered.map((c) => ({
        "Mã lớp": c.class_id,
        "Tên lớp học": c.class_name,
        "ID Giảng viên": c.class_teacher,
        "Học kỳ": c.class_semester,
        // "ID Khoá học": c.course,
        "Hành động": (
            <>
                <Button variant="secondary" onClick={() => openEditModal(c)} style={{ marginRight: "6px" }}>
                    Sửa
                </Button>
                <Button variant="danger" onClick={() => handleDelete(c.class_id)} style={{ marginRight: "6px" }}>
                    Xoá
                </Button>
                <Button onClick={() => toggleStudents(c.class_id)}>
                    {expandedRows[c.class_id] ? "Ẩn" : "▼ Sinh viên"}
                </Button>
            </>
        ),
    }));

    return (
        <div className={styles.container}>
            <section className={styles.header}>
                <h2>Quản lý Lớp học</h2>
                <p>Theo dõi, thêm, xoá và chỉnh sửa thông tin lớp học.</p>
            </section>

            <div style={{ margin: "20px 0", border: "1px solid #ccc", padding: "15px" }}>
                <h4>{editingClass ? "Sửa lớp học" : "Tạo lớp học mới"}</h4>
                <Form onSubmit={handleSubmit}>
                    <Input
                        label="Tên lớp học"
                        value={formData.class_name}
                        onChange={(e) => setFormData({ ...formData, class_name: e.target.value })}
                        required
                    />
                    <Input
                        label="ID Giảng viên"
                        value={formData.class_teacher}
                        onChange={(e) => setFormData({ ...formData, class_teacher: e.target.value })}
                        required
                    />
                    <Input
                        label="Học kỳ"
                        value={formData.class_semester}
                        onChange={(e) => setFormData({ ...formData, class_semester: e.target.value })}
                        required
                    />
                    {!editingClass && (
                        <Input
                            label="ID Khoá học"
                            value={formData.course}
                            onChange={(e) => setFormData({ ...formData, course: e.target.value })}
                            required
                        />
                    )}
                    <Button type="submit">{editingClass ? "Cập nhật" : "Tạo lớp"}</Button>
                </Form>
            </div>

            <form onSubmit={(e) => e.preventDefault()} style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
                <Input placeholder="Tìm kiếm theo mã lớp hoặc tên lớp" value={searchTerm} onChange={handleSearch} />
                <Button type="button">Tìm kiếm</Button>
            </form>

            {tableData.length > 0 && (
                <Table columns={["Mã lớp", "Tên lớp học", "ID Giảng viên", "Học kỳ", "Hành động"]} data={tableData} />
            )}

            {Object.entries(expandedRows).map(([classId, students]) =>
                students ? (
                    <div key={classId} style={{ marginTop: "20px", paddingLeft: "10px" }}>
                        <h4>Sinh viên trong lớp {classId}</h4>
                        <Button onClick={() => setModalClassId(Number(classId))}>➕ Thêm sinh viên</Button>
                        <Table
                            columns={["ID", "Tên", "Email", "Hành động"]}
                            data={students.map((s) => ({
                                ID: s.student_id,
                                Tên: s.student_name,
                                Email: s.student_email,
                                "Hành động": (
                                    <Button variant="danger" onClick={async () => {
                                        await removeStudentFromClass(Number(classId), s.student_id);
                                        toggleStudents(Number(classId));
                                    }}>
                                        Xoá
                                    </Button>
                                ),
                            }))}
                        />
                    </div>
                ) : null
            )}

            <Modal isOpen={!!modalClassId} onClose={() => setModalClassId(null)} title="Thêm sinh viên vào lớp">
                <Form onSubmit={handleAddStudent}>
                    <label style={{ fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                        Chọn sinh viên
                    </label>
                    <select
                        value={newStudentId}
                        onChange={(e) => setNewStudentId(e.target.value)}
                        required
                        style={{ width: "100%", padding: "10px", marginBottom: "16px", borderRadius: "5px", border: "1px solid #ccc" }}
                    >
                        <option value="">-- Chọn sinh viên --</option>
                        {allStudents.map((s) => (
                            <option key={s.student_id} value={s.student_id}>
                                {s.student_name} ({s.student_email})
                            </option>
                        ))}
                    </select>
                    <Button type="submit" style={{ width: "100%" }}>➕ Thêm vào lớp</Button>
                </Form>
            </Modal>
        </div>
    );
};

export default ManageAllClasses;