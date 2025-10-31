import axios from "axios";

// ✅ Lấy lớp môn học chưa đăng ký (dành cho sinh viên)
export const getAvailableCourseClasses = async () => {
    const res = await axios.get("/api/registrations/available");
    return res.data;
};

// ✅ Lấy lớp môn học đã đăng ký của sinh viên
export const getRegisteredCourseClasses = async () => {
    const res = await axios.get("/api/registrations/registered");
    return res.data;
};

// ✅ Đăng ký lớp môn học
export const registerToClass = async (classId) => {
    const res = await axios.post(`/api/registrations/${classId}`);
    return res.data;
};

// ✅ Hủy đăng ký lớp môn học
export const unregisterFromClass = async (classId) => {
    const res = await axios.delete(`/api/registrations/${classId}`);
    return res.data;
};