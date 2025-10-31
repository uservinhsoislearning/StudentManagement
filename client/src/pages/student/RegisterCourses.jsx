import { useEffect, useState } from "react";
import {
    getAvailableCourseClasses,
    getRegisteredCourseClasses,
    registerToClass,
    unregisterFromClass,
} from "../../api/registrations";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import Table from "../../components/UI/Table";

const RegisterCourses = () => {
    const [availableClasses, setAvailableClasses] = useState([]);
    const [registeredClasses, setRegisteredClasses] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        fetchAll();
    }, []);

    const fetchAll = async () => {
        const [available, registered] = await Promise.all([
            getAvailableCourseClasses(),
            getRegisteredCourseClasses(),
        ]);
        setAvailableClasses(available);
        setRegisteredClasses(registered);
    };

    const handleSearch = (e) => setSearchTerm(e.target.value);

    const isRegistered = (classId) => {
        return registeredClasses.some((cls) => cls.id === classId);
    };

    const handleRegister = async (classId) => {
        await registerToClass(classId);
        fetchAll();
    };

    const handleUnregister = async (classId) => {
        await unregisterFromClass(classId);
        fetchAll();
    };

    const filteredClasses = availableClasses.filter(
        (cls) =>
            cls.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
            cls.subjectName.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const tableData = filteredClasses.map((cls) => ({
        "Mã lớp": cls.code,
        "Tên môn học": cls.subjectName,
        "Giảng viên": cls.teacher,
        "Lịch học": cls.schedule,
        "Học kỳ": cls.semester,
        "Hành động": isRegistered(cls.id) ? (
            <Button variant="danger" onClick={() => handleUnregister(cls.id)}>
                Huỷ đăng ký
            </Button>
        ) : (
            <Button variant="primary" onClick={() => handleRegister(cls.id)}>
                Đăng ký
            </Button>
        ),
    }));

    return (
        <div style={{ padding: "24px" }}>
            <h2>Đăng ký Lớp môn học</h2>

            <Input
                placeholder="Tìm kiếm theo mã hoặc tên môn học"
                value={searchTerm}
                onChange={handleSearch}
                style={{ marginBottom: "15px" }}
            />

            <Table
                columns={["Mã lớp", "Tên môn học", "Giảng viên", "Lịch học", "Học kỳ", "Hành động"]}
                data={tableData}
            />
        </div>
    );
};

export default RegisterCourses;