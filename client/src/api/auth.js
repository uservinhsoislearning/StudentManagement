import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/auth"; // 👉 Thay đúng URL backend

// 🟢 Đăng nhập
export const loginUser = async (email, password, role) => {
  console.log("📤 Gửi login request với:", { email, password, role }); // log đầu vào

  try {
    const response = await axios.post(`${API_URL}/login`, {
      useremail: email,
      password,
      role,
    });

    console.log("📥 Kết quả từ API trả về:", response.data); // log đầu ra
    return response.data;
  } catch (error) {
    console.error("❌ API login lỗi:", error);
    throw error.response ? error.response.data : { message: "Lỗi không xác định" };
  }
};

// 🟢 Đăng ký
export const registerUser = async (formData) => {
  try {
    const response = await axios.post(`${API_URL}/register`, formData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: "Lỗi không xác định" };
  }
};

// 🟢 Quên mật khẩu
export const forgotPassword = async (email) => {
  try {
    const response = await axios.post(`${API_URL}/forgot-password`, { email });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: "Lỗi không xác định" };
  }
};

// 🟢 Đăng xuất
// src/api/auth.js

export const logoutUser = async () => {
  // Không cần gọi API nữa
  return Promise.resolve({ message: "Đăng xuất thành công!" });
};

// ✅ Lấy thông tin người dùng hiện tại
export const getCurrentUser = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Không có token");

  const response = await axios.get(`${API_URL}/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

// ✅ Cập nhật thông tin cá nhân
export const updateCurrentUser = async (data) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        ...data, // trả về dữ liệu mới (giả sử update thành công)
        updatedAt: new Date().toISOString(),
      });
    }, 500);
  });
};