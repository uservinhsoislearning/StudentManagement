import { useState } from "react";
import {
    createClass,
    deleteClass,
    getAllClasses,
    getClassById,
    updateClass,
} from "../api/classes"; // 📌 Bạn cần tạo file api/classes.js đúng theo tên hàm

export const useClassManagement = () => {
    const [classes, setClasses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // 🎯 Fetch danh sách lớp
    const fetchClasses = async (filters = {}) => {
        setLoading(true);
        try {
            const data = await getAllClasses(filters);
            setClasses(data);
        } catch (err) {
            console.error("Lỗi khi tải danh sách lớp:", err);
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    // 🎯 Lấy lớp theo ID
    const fetchClassById = async (id) => {
        try {
            const cls = await getClassById(id);
            return cls;
        } catch (err) {
            setError(err);
            return null;
        }
    };

    // 🎯 Thêm lớp mới
    const addClass = async (classData) => {
        try {
            const newClass = await createClass(classData);
            setClasses((prev) => [...prev, newClass]);
            return newClass;
        } catch (err) {
            setError(err);
            throw err;
        }
    };

    // 🎯 Cập nhật lớp
    const editClass = async (id, updatedData) => {
        try {
            const updatedClass = await updateClass(id, updatedData);
            setClasses((prev) =>
                prev.map((cls) => (cls.id === id ? updatedClass : cls))
            );
            return updatedClass;
        } catch (err) {
            setError(err);
            throw err;
        }
    };

    // 🎯 Xóa lớp
    const removeClass = async (id) => {
        try {
            await deleteClass(id);
            setClasses((prev) => prev.filter((cls) => cls.id !== id));
        } catch (err) {
            setError(err);
            throw err;
        }
    };

    return {
        classes,
        loading,
        error,
        fetchClasses,
        fetchClassById,
        addClass,
        editClass,
        removeClass,
    };
};