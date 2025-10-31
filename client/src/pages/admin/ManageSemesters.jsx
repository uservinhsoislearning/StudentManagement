import { useEffect, useState } from "react";
import {
    createSemester,
    deleteSemester,
    getSemesters,
    toggleSemesterStatus,
    updateSemester,
} from "../../api/semesters";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Modal from "../../components/UI/Modal";
import Table from "../../components/UI/Table";

const ManageSemesters = () => {
    const [semesters, setSemesters] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [isModalOpen, setModalOpen] = useState(false);
    const [editingSemester, setEditingSemester] = useState(null);
    const [formData, setFormData] = useState({
        name: "",
        startDate: "",
        endDate: "",
        isActive: true,
    });

    useEffect(() => {
        fetchSemesters();
    }, []);

    const fetchSemesters = async () => {
        const data = await getSemesters();
        setSemesters(data);
    };

    const handleSearch = (e) => setSearchTerm(e.target.value);

    const filteredSemesters = semesters.filter((s) => {
        const nameMatch = s.name?.toLowerCase().includes(searchTerm.toLowerCase());
        const year = s.startDate?.slice(0, 4);
        const yearMatch = year?.includes(searchTerm);
        return nameMatch || yearMatch;
    });

    const openAddModal = () => {
        setEditingSemester(null);
        setFormData({
            name: "",
            startDate: "",
            endDate: "",
            isActive: true,
        });
        setModalOpen(true);
    };

    const openEditModal = (semester) => {
        setEditingSemester(semester);
        setFormData({
            name: semester.name,
            startDate: semester.startDate,
            endDate: semester.endDate,
            isActive: semester.isActive,
        });
        setModalOpen(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm("Xoá học kỳ này?")) {
            await deleteSemester(id);
            fetchSemesters();
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (editingSemester) {
            await updateSemester(editingSemester.semester_id, formData);
        } else {
            await createSemester(formData);
        }
        fetchSemesters();
        setModalOpen(false);
    };

    const handleToggleStatus = async (id) => {
        await toggleSemesterStatus(id);
        fetchSemesters();
    };

    const tableData = filteredSemesters.map((sem) => ({
        "ID": sem.semester_id,
        "Tên học kỳ": sem.name,
        "Năm": sem.startDate?.slice(0, 4),
        "Từ ngày": sem.startDate,
        "Đến ngày": sem.endDate,
        "Trạng thái": sem.isActive ? "Đang mở" : "Đã đóng",
        "Hành động": (
            <>
                <Button
                    variant="secondary"
                    onClick={() => openEditModal(sem)}
                    style={{ marginRight: "6px" }}
                >
                    Sửa
                </Button>
                <Button
                    variant={sem.isActive ? "warning" : "success"}
                    onClick={() => handleToggleStatus(sem.semester_id)}
                    style={{ marginRight: "6px" }}
                >
                    {sem.isActive ? "Đóng học kỳ" : "Mở học kỳ"}
                </Button>
                <Button variant="danger" onClick={() => handleDelete(sem.semester_id)}>
                    Xoá
                </Button>
            </>
        ),
    }));

    return (
        <>
            <h2>Quản lý Học kỳ</h2>

            <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
                <Input
                    placeholder="Tìm kiếm theo tên hoặc năm"
                    value={searchTerm}
                    onChange={handleSearch}
                />
                <Button onClick={openAddModal}>Thêm học kỳ</Button>
            </div>

            <Table
                columns={["ID", "Tên học kỳ", "Năm", "Từ ngày", "Đến ngày", "Trạng thái", "Hành động"]}
                data={tableData}
            />

            <Modal
                isOpen={isModalOpen}
                onClose={() => setModalOpen(false)}
                title={editingSemester ? "Sửa học kỳ" : "Thêm học kỳ"}
            >
                <Form onSubmit={handleSubmit}>
                    <Input
                        label="Tên học kỳ"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        required
                    />
                    <Input
                        label="Ngày bắt đầu"
                        type="date"
                        value={formData.startDate}
                        onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                        required
                    />
                    <Input
                        label="Ngày kết thúc"
                        type="date"
                        value={formData.endDate}
                        onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
                        required
                    />
                    <Button type="submit">Lưu</Button>
                </Form>
            </Modal>
        </>
    );
};

export default ManageSemesters;