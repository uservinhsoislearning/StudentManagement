import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/classes";

// 🎯 Lấy tất cả lớp môn học (có thể truyền filters như học kỳ, giáo viên...)
export const getAllClasses = async (filters = {}) => {
    const response = await axios.get(API_URL, { params: filters });
    return response.data;
};

// 🎯 Lấy chi tiết 1 lớp theo ID
export const getClassById = async (id) => {
    const response = await axios.get(API_URL);
    const allClasses = response.data;
    const foundClass = allClasses.find(cls => cls.class_id === id);
    if (!foundClass) {
        throw new Error("Không tìm thấy lớp có ID: " + id);
    }
    return foundClass;
};

// 🎯 Tạo lớp mới
export const createClass = async (classData) => {
    const response = await axios.post(API_URL, classData);
    return response.data;
};

// 🎯 Cập nhật lớp học
export const updateClass = async (id, updatedData) => {
    const data = { ...updatedData, class_id: id };
    const response = await axios.put(API_URL, data);
    return response.data;
};

// 🎯 Xóa lớp học
export const deleteClass = async (id) => {
    const response = await axios.delete(`${API_URL}/${id}`);
    return response.data;
};

// ✅ Lấy danh sách sinh viên trong lớp
export const getStudentsInClass = async (classId) => {
    const response = await axios.post(`${API_URL}/${classId}/get-students`);
    return response.data;
};

// ✅ Thêm sinh viên vào lớp
export const addStudentToClass = async (classId, studentId) => {
    const payload = {
        class_field: classId,
        student: Number(studentId),
    };
    const response = await axios.post(`${API_URL}/students`, payload);
    return response.data;
};

// ✅ Xoá sinh viên khỏi lớp
export const removeStudentFromClass = async (classId, studentId) => {
    const response = await axios.delete(`${API_URL}/${classId}/students/${studentId}`);
    return response.data;
};
const BASE_URL = "http://127.0.0.1:8000/api";
export const fetchClassDetails = async (classId) => {
    const response = await axios.get(`${BASE_URL}/classes/${classId}/details`);
    return response.data;
};

// ✅ Cập nhật điểm sinh viên
export const updateStudentScore = async (classId, studentId, scoreData) => {
    const response = await axios.put(`${API_URL}/${classId}/students/${studentId}/score`, scoreData);
    return response.data;
};

// ✅ Xoá điểm sinh viên
export const deleteStudentScore = async (classId, studentId) => {
    const response = await axios.delete(`${API_URL}/${classId}/students/${studentId}/score`);
    return response.data;
};

// ✅ Lấy thống kê điểm của lớp học
export const getClassStatistics = async (classId) => {
    const response = await axios.get(`${API_URL}/${classId}/statistics`);
    return response.data;
};

// // === Dữ liệu giả ===
// let mockClasses = [
//     { id: 1, class_name: "Introduction to SE", class_teacher: 2, class_semester: 2 },
//     { id: 2, class_name: "Calculus 1", class_teacher: 1, class_semester: 1 },
//     { id: 3, class_name: "Probability and Statistics", class_teacher: 1, class_semester: 2 },
// ];

// // 🎯 Lấy tất cả lớp môn học
// export const getAllClasses = async (filters = {}) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             let result = [...mockClasses];
//             // Lọc theo filters nếu có
//             if (filters.class_teacher)
//                 result = result.filter(c => c.class_teacher === Number(filters.class_teacher));
//             if (filters.class_semester)
//                 result = result.filter(c => c.class_semester === Number(filters.class_semester));
//             resolve(result);
//         }, 300);
//     });
// };

// // 🎯 Lấy chi tiết 1 lớp theo ID
// export const getClassById = async (id) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve(mockClasses.find(c => c.id === Number(id)) || null);
//         }, 300);
//     });
// };

// // 🎯 Tạo lớp mới
// export const createClass = async (classData) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             const newClass = { id: Date.now(), ...classData };
//             mockClasses.push(newClass);
//             console.log("🧪 Fake class created:", newClass);
//             resolve(newClass);
//         }, 300);
//     });
// };

// // 🎯 Cập nhật lớp học
// export const updateClass = async (id, updatedData) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             mockClasses = mockClasses.map(c =>
//                 c.id === Number(id) ? { ...c, ...updatedData } : c
//             );
//             resolve({ id, ...updatedData });
//         }, 300);
//     });
// };

// // 🎯 Xóa lớp học
// export const deleteClass = async (id) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             mockClasses = mockClasses.filter(c => c.id !== Number(id));
//             resolve({ success: true });
//         }, 300);
//     });
// };

// // ✅ Lấy danh sách sinh viên trong lớp
// export const getStudentsInClass = async (classId) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve([
//                 { id: 1, name: "Alice" },
//                 { id: 2, name: "Bob" },
//             ]);
//         }, 300);
//     });
// };

// // ✅ Thêm sinh viên vào lớp
// export const addStudentToClass = async (classId, studentId) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve({ classId, studentId });
//         }, 300);
//     });
// };

// // ✅ Xoá sinh viên khỏi lớp
// export const removeStudentFromClass = async (classId, studentId) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve({ classId, studentId });
//         }, 300);
//     });
// };

// // ✅ Cập nhật điểm sinh viên
// export const updateStudentScore = async (classId, studentId, scoreData) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve({ classId, studentId, ...scoreData });
//         }, 300);
//     });
// };

// // ✅ Xoá điểm sinh viên
// export const deleteStudentScore = async (classId, studentId) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve({ classId, studentId, deleted: true });
//         }, 300);
//     });
// };

// // ✅ Thống kê điểm
// export const getClassStatistics = async (classId) => {
//     return new Promise((resolve) => {
//         setTimeout(() => {
//             resolve({
//                 averageScore: 7.5,
//                 maxScore: 9.8,
//                 minScore: 5.2,
//             });
//         }, 300);
//     });
// };