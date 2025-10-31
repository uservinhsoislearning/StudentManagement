import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// ✅ Lấy danh sách tất cả môn học (course-classes)
export const getCourseClasses = async () => {
    const res = await axios.get(`${API_URL}/api/course-classes-both`);
    return res.data;
};

// ✅ Tạo mới môn học
export const createCourseClass = async (data) => {
    const res = await axios.post(`${API_URL}/api/course-classes`, data);
    return res.data;
};

// ✅ Cập nhật môn học
export const updateCourseClass = async (id, data) => {
    const res = await axios.put(`${API_URL}/api/course-classes/${id}`, data);
    return res.data;
};

// ✅ Xoá môn học
export const deleteCourseClass = async (id) => {
    const res = await axios.delete(`${API_URL}/api/course-classes/${id}`);
    return res.data;
};

// ✅ Import môn học từ file Excel
export const importCourseClassesFromExcel = async (formData) => {
    const res = await axios.post(`${API_URL}/api/course-classes/import`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    return res.data;
};