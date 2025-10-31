import { useEffect, useState } from "react";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Modal from "../../components/UI/Modal";
import Table from "../../components/UI/Table";

import {
    createCourseClass,
    deleteCourseClass,
    getCourseClasses,
    importCourseClassesFromExcel,
    updateCourseClass,
} from "../../api/courseClasses";

import { readExcelFile } from "../../utils/helpers";

const ManageCourseClasses = () => {
    const [courses, setCourses] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [isModalOpen, setModalOpen] = useState(false);
    const [formData, setFormData] = useState({
        course_name: "",
        course_semester: "",
        course_midterm_coeff: "",
        course_final_coeff: "",
        course_credit: ""
    });
    const [editingCourse, setEditingCourse] = useState(null);
    const [isImporting, setImporting] = useState(false);
    const [previewData, setPreviewData] = useState([]);
    const [expandedCourseId, setExpandedCourseId] = useState(null);

    useEffect(() => {
        loadCourseClasses();
    }, []);

    const loadCourseClasses = async () => {
        const data = await getCourseClasses();
        setCourses(data);
    };

    const handleSearch = (e) => setSearchTerm(e.target.value);

    const openAddModal = () => {
        setFormData({
            course_name: "",
            course_semester: "",
            course_midterm_coeff: "",
            course_final_coeff: "",
            course_credit: ""
        });
        setEditingCourse(null);
        setModalOpen(true);
    };

    const openEditModal = (course) => {
        setFormData({
            course_name: course.course_name,
            course_semester: course.course_semester,
            course_midterm_coeff: course.course_midterm_coeff,
            course_final_coeff: course.course_final_coeff,
            course_credit: course.course_credit
        });
        setEditingCourse(course);
        setModalOpen(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm("Xoá môn học này?")) {
            await deleteCourseClass(id);
            loadCourseClasses();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const payload = {
            ...formData,
            course_semester: Number(formData.course_semester),
            course_midterm_coeff: Number(formData.course_midterm_coeff),
            course_final_coeff: Number(formData.course_final_coeff),
            course_credit: Number(formData.course_credit)
        };
        if (editingCourse) {
            await updateCourseClass(editingCourse.course_id, payload);
        } else {
            await createCourseClass(payload);
        }
        setModalOpen(false);
        loadCourseClasses();
    };

    const handleImport = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        try {
            const preview = await readExcelFile(file);
            setPreviewData(preview);

            if (window.confirm(`Import ${preview.length} môn học từ Excel?`)) {
                const formData = new FormData();
                formData.append("file", file);
                setImporting(true);
                await importCourseClassesFromExcel(formData);
                await loadCourseClasses();
                alert("Import thành công!");
            }
        } catch (err) {
            alert("Lỗi khi đọc file Excel.");
        } finally {
            setImporting(false);
        }
    };

    const filteredCourses = courses.filter((c) =>
        c.course_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div style={{ padding: "24px" }}>
            <h2>Quản lý môn học & lớp học</h2>

            <div style={{ display: "flex", gap: "10px", marginBottom: "16px" }}>
                <Input
                    placeholder="Tìm kiếm theo tên môn học"
                    value={searchTerm}
                    onChange={handleSearch}
                />
                <Button onClick={openAddModal}>Thêm môn học</Button>
                <label>
                    <input
                        type="file"
                        accept=".xlsx,.xls"
                        hidden
                        onChange={handleImport}
                    />
                    <Button variant="outline" disabled={isImporting}>
                        {isImporting ? "Đang import..." : "Import từ Excel"}
                    </Button>
                </label>
            </div>

            <Table
                columns={["ID", "Tên môn học", "Học kỳ", "Hệ số GK", "Hệ số CK", "Số tín chỉ", "Hành động"]}
                data={filteredCourses.map((course) => ({
                    "ID": course.course_id,
                    "Tên môn học": course.course_name,
                    "Học kỳ": course.course_semester,
                    "Hệ số GK": course.course_midterm_coeff,
                    "Hệ số CK": course.course_final_coeff,
                    "Số tín chỉ": course.course_credit,
                    "Hành động": (
                        <div style={{ display: "flex", gap: "6px" }}>
                            <Button variant="outline" onClick={() => openEditModal(course)}>
                                ✏️ Cập nhật
                            </Button>
                            <Button
                                variant="ghost"
                                onClick={() =>
                                    setExpandedCourseId(
                                        expandedCourseId === course.course_id ? null : course.course_id
                                    )
                                }
                            >
                                {expandedCourseId === course.course_id ? "Ẩn lớp" : "Hiện lớp"}
                            </Button>
                            <Button variant="danger" onClick={() => handleDelete(course.course_id)}>
                                🗑️ Xoá
                            </Button>
                        </div>
                    )
                }))}
            />

            {expandedCourseId && (
                <div style={{ marginTop: "12px", marginBottom: "24px" }}>
                    <h4>Danh sách lớp của môn: {courses.find(c => c.course_id === expandedCourseId)?.course_name}</h4>
                    <Table
                        columns={["Tên lớp", "Học kỳ lớp", "Thời khoá biểu"]}
                        data={(courses.find(c => c.course_id === expandedCourseId)?.classes || []).map(cls => ({
                            "Tên lớp": cls.class_name,
                            "Học kỳ lớp": cls.class_semester,
                            "Thời khoá biểu": (cls.timetables || []).map(t => `${t.day_of_week} ${t.start_time}-${t.end_time}`).join(" | ") || "-"
                        }))}
                    />
                </div>
            )}

            <Modal
                isOpen={isModalOpen}
                onClose={() => setModalOpen(false)}
                title={editingCourse ? "Sửa môn học" : "Thêm môn học"}
            >
                <Form onSubmit={handleSubmit}>
                    <Input
                        label="Tên môn học"
                        value={formData.course_name}
                        onChange={(e) => setFormData({ ...formData, course_name: e.target.value })}
                        required
                    />
                    <Input
                        label="Học kỳ"
                        type="number"
                        value={formData.course_semester}
                        onChange={(e) => setFormData({ ...formData, course_semester: e.target.value })}
                        required
                    />
                    <Input
                        label="Hệ số giữa kỳ"
                        type="number"
                        step="0.01"
                        value={formData.course_midterm_coeff}
                        onChange={(e) => setFormData({ ...formData, course_midterm_coeff: e.target.value })}
                        required
                    />
                    <Input
                        label="Hệ số cuối kỳ"
                        type="number"
                        step="0.01"
                        value={formData.course_final_coeff}
                        onChange={(e) => setFormData({ ...formData, course_final_coeff: e.target.value })}
                        required
                    />
                    <Input
                        label="Số tín chỉ"
                        type="number"
                        step="1"
                        value={formData.course_credit}
                        onChange={(e) => setFormData({ ...formData, course_credit: e.target.value })}
                        required
                    />
                    <Button type="submit">Lưu</Button>
                </Form>
            </Modal>

            {previewData.length > 0 && (
                <div style={{ marginTop: "30px" }}>
                    <h4>Xem trước dữ liệu từ Excel</h4>
                    <Table
                        columns={["course_name", "course_semester", "course_midterm_coeff", "course_final_coeff", "course_credit"]}
                        data={previewData}
                    />
                </div>
            )}
        </div>
    );
};

export default ManageCourseClasses;