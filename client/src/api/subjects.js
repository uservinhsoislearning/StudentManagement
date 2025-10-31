// import axios from "axios";

// // ✅ Lấy danh sách tất cả môn học
// export const getSubjects = async () => {
//     const res = await axios.get("/api/subjects");
//     return res.data;
// };

// // ✅ Tạo mới môn học
// export const createSubject = async (data) => {
//     const res = await axios.post("/api/subjects", data);
//     return res.data;
// };

// // ✅ Cập nhật môn học theo ID
// export const updateSubject = async (id, data) => {
//     const res = await axios.put(`/api/subjects/${id}`, data);
//     return res.data;
// };

// // ✅ Xoá môn học theo ID
// export const deleteSubject = async (id) => {
//     const res = await axios.delete(`/api/subjects/${id}`);
//     return res.data;
// };

// // ✅ Import môn học từ file Excel
// export const importSubjectsFromExcel = async (formData) => {
//     const res = await axios.post("/api/subjects/import", formData, {
//         headers: {
//             "Content-Type": "multipart/form-data",
//         },
//     });
//     return res.data;
// };

// === Dữ liệu môn học giả lập ===
let mockSubjects = [
    { id: 1, name: "Toán cao cấp" },
    { id: 2, name: "Xác suất thống kê" },
    { id: 3, name: "Nhập môn Công nghệ phần mềm" },
];

// ✅ Lấy danh sách tất cả môn học
export const getSubjects = async () => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve([...mockSubjects]);
        }, 300);
    });
};

// ✅ Tạo mới môn học
export const createSubject = async (data) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const newSubject = {
                id: Date.now(),
                ...data,
            };
            mockSubjects.push(newSubject);
            console.log("🧪 Fake createSubject:", newSubject);
            resolve(newSubject);
        }, 300);
    });
};

// ✅ Cập nhật môn học theo ID
export const updateSubject = async (id, data) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            mockSubjects = mockSubjects.map((subject) =>
                subject.id === Number(id) ? { ...subject, ...data } : subject
            );
            console.log("🧪 Fake updateSubject:", id, data);
            resolve({ id, ...data });
        }, 300);
    });
};

// ✅ Xoá môn học theo ID
export const deleteSubject = async (id) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            mockSubjects = mockSubjects.filter((subject) => subject.id !== Number(id));
            console.log("🧪 Fake deleteSubject:", id);
            resolve({ success: true });
        }, 300);
    });
};

// ✅ Import môn học từ file Excel (giả lập)
export const importSubjectsFromExcel = async (formData) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            const imported = [
                { id: Date.now() + 1, name: "Vật lý đại cương" },
                { id: Date.now() + 2, name: "Kỹ thuật lập trình" },
            ];
            mockSubjects = [...mockSubjects, ...imported];
            console.log("🧪 Fake importSubjectsFromExcel:", imported);
            resolve({ imported });
        }, 500);
    });
};