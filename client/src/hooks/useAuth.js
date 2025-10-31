import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

/**
 * Hook dùng để truy cập và quản lý xác thực người dùng.
 * @returns {Object} Thông tin xác thực và các hàm xử lý đăng nhập, đăng ký, đăng xuất.
 */
const useAuth = () => {
  return useContext(AuthContext);
};

export default useAuth;
