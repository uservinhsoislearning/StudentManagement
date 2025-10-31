// api/teachers.js
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// ✅ Lấy danh sách tất cả giáo viên
export const getAllTeachers = async () => {
    const res = await axios.get(`${API_URL}/api/teachers`);
    return res.data;
};

// ✅ Thêm giáo viên mới
export const createTeacher = async (data) => {
    const res = await axios.post(`${API_URL}/api/teachers`, data);
    return res.data;
};

// ✅ Cập nhật thông tin giáo viên
// ✅ Sửa lại - bỏ id khỏi URL
export const updateTeacher = async (id, data) => {
    const res = await axios.put(`${API_URL}/api/teachers`, {
        ...data,
        teacher_id: id,
    });
    return res.data;
};

// ✅ Xoá giáo viên
export const deleteTeacher = async (id) => {
    const res = await axios.delete(`${API_URL}/api/teachers/${id}`);
    return res.data;
};