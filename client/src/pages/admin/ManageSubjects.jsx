import { useEffect, useState } from "react";
import {
    createSubject,
    deleteSubject,
    getSubjects,
    importSubjectsFromExcel,
    updateSubject,
} from "../../api/subjects";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Modal from "../../components/UI/Modal";
import Table from "../../components/UI/Table";
import styles from "./ManageSubjects.module.css";

import { readExcelFile } from "../../utils/helpers";

const ManageSubjects = () => {
    const [subjects, setSubjects] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [isModalOpen, setModalOpen] = useState(false);
    const [isImporting, setImporting] = useState(false);
    const [editingSubject, setEditingSubject] = useState(null);
    const [previewData, setPreviewData] = useState([]);

    const [formData, setFormData] = useState({
        name: "",
        code: "",
        credits: "",
        description: "",
    });

    useEffect(() => {
        fetchSubjects();
    }, []);

    const fetchSubjects = async () => {
        const data = await getSubjects();
        setSubjects(data);
    };

    const handleSearch = (e) => setSearchTerm(e.target.value);

    const filteredSubjects = subjects.filter(
        (s) =>
            s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const openAddModal = () => {
        setEditingSubject(null);
        setFormData({ name: "", code: "", credits: "", description: "" });
        setModalOpen(true);
    };

    const openEditModal = (subject) => {
        setEditingSubject(subject);
        setFormData(subject);
        setModalOpen(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm("Bạn có chắc chắn muốn xoá môn học này?")) {
            await deleteSubject(id);
            fetchSubjects();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (editingSubject) {
            await updateSubject(editingSubject.id, formData);
        } else {
            await createSubject(formData);
        }
        fetchSubjects();
        setModalOpen(false);
    };

    const handleImport = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        try {
            const preview = await readExcelFile(file);
            setPreviewData(preview);

            if (
                window.confirm(
                    `Bạn có chắc muốn import ${preview.length} môn học từ Excel không?`
                )
            ) {
                const formData = new FormData();
                formData.append("file", file);
                setImporting(true);
                await importSubjectsFromExcel(formData);
                await fetchSubjects();
                alert("Import thành công!");
                setPreviewData([]);
            }
        } catch (err) {
            console.error(err);
            alert("Không thể đọc file Excel. Vui lòng kiểm tra định dạng.");
        } finally {
            setImporting(false);
        }
    };

    const tableData = filteredSubjects.map((sub) => ({
        "Mã môn": sub.code,
        "Tên môn": sub.name,
        "Số tín chỉ": sub.credits,
        "Mô tả": sub.description || "—",
        "Hành động": (
            <>
                <Button
                    variant="secondary"
                    onClick={() => openEditModal(sub)}
                    style={{ marginRight: "6px" }}
                >
                    Sửa
                </Button>
                <Button variant="danger" onClick={() => handleDelete(sub.id)}>
                    Xoá
                </Button>
            </>
        ),
    }));

    return (
        <div className={styles.container}>
            <section className={styles.header}>
                <h2>📘 Quản lý Môn học</h2>
                <p>Theo dõi, thêm, xoá và chỉnh sửa thông tin môn học.</p>
            </section>

            <div className={styles.controls}>
                <Input
                    placeholder="🔍 Tìm kiếm theo tên hoặc mã môn"
                    value={searchTerm}
                    onChange={handleSearch}
                />
                <Button onClick={openAddModal}>➕ Thêm môn học</Button>
                <label>
                    <input
                        type="file"
                        accept=".xlsx,.xls"
                        onChange={handleImport}
                        hidden
                    />
                    <Button variant="outline" disabled={isImporting}>
                        {isImporting ? "⏳ Đang import..." : "📤 Import từ Excel"}
                    </Button>
                </label>
            </div>

            <Table
                columns={["Mã môn", "Tên môn", "Số tín chỉ", "Mô tả", "Hành động"]}
                data={tableData}
            />

            {previewData.length > 0 && (
                <div className={styles.previewSection}>
                    <h4 style={{ marginBottom: "10px" }}>📄 Xem trước nội dung Excel</h4>
                    <Table
                        columns={["name", "code", "credits", "description"]}
                        data={previewData}
                    />
                </div>
            )}

            <Modal
                isOpen={isModalOpen}
                onClose={() => setModalOpen(false)}
                title={editingSubject ? "✏️ Sửa môn học" : "➕ Thêm môn học"}
            >
                <Form onSubmit={handleSubmit}>
                    <Input
                        label="📘 Tên môn"
                        value={formData.name}
                        onChange={(e) =>
                            setFormData({ ...formData, name: e.target.value })
                        }
                        required
                    />
                    <Input
                        label="🧾 Mã môn"
                        value={formData.code}
                        onChange={(e) =>
                            setFormData({ ...formData, code: e.target.value })
                        }
                        required
                    />
                    <Input
                        label="🎯 Số tín chỉ"
                        type="number"
                        value={formData.credits}
                        onChange={(e) =>
                            setFormData({ ...formData, credits: e.target.value })
                        }
                        required
                    />
                    <Input
                        label="📄 Mô tả"
                        value={formData.description}
                        onChange={(e) =>
                            setFormData({ ...formData, description: e.target.value })
                        }
                    />
                    <Button type="submit">💾 Lưu</Button>
                </Form>
            </Modal>
        </div>
    );
};

export default ManageSubjects;