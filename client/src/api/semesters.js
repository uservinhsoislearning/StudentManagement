import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// ✅ Lấy danh sách tất cả học kỳ
export const getSemesters = async () => {
    const res = await axios.get(`${API_URL}/api/semesters`);
    return res.data;
};

// ✅ Tạo mới học kỳ
export const createSemester = async (data) => {
    const res = await axios.post(`${API_URL}/api/semesters`, data);
    return res.data;
};

// ✅ Cập nhật học kỳ
export const updateSemester = async (id, data) => {
    const res = await axios.put(`${API_URL}/api/semesters/${id}`, data);
    return res.data;
};

// ✅ Xoá học kỳ
export const deleteSemester = async (id) => {
    const res = await axios.delete(`${API_URL}/api/semesters/${id}`);
    return res.data;
};

// ✅ Đóng / Mở học kỳ (toggle isActive)
export const toggleSemesterStatus = async (id) => {
    const res = await axios.patch(`${API_URL}/api/semesters/${id}/toggle-status`);
    return res.data;
};