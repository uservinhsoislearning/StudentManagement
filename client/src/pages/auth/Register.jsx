import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import logo from "../../assets/bachkhoa-logo.png";
import styles from "./Register.module.css";
import StudentRegisterForm from "./StudentRegisterForm";
import TeacherRegisterForm from "./TeacherRegisterForm";
import { registerUser } from "../../api/auth"; // API của bạn

const Register = () => {
  const navigate = useNavigate();
  
  // State quản lý các bước
  const [step, setStep] = useState(1); // 1: Chọn role, 2: Điền form
  const [role, setRole] = useState("student"); // Mặc định là học sinh
  const [error, setError] = useState("");

  // Hàm xử lý khi nhấn "Tiếp tục" ở bước 1
  const handleNextStep = (e) => {
    e.preventDefault();
    setError("");
    setStep(2);
  };

  // Hàm xử lý đăng ký cuối cùng (Step 2 gọi hàm này)
  const handleFinalSubmit = async (formData) => {
    setError("");
    try {
      // Gọi API, truyền thêm role vào data
      const dataToSend = { ...formData, role: role }; 
      
      console.log("Data sending to API:", dataToSend); // Debug check

      await registerUser(dataToSend); 
      
      alert("Đăng ký thành công! Vui lòng đăng nhập.");
      navigate("/login");
    } catch (err) {
      setError(err.message || "Đăng ký thất bại!");
    }
  };

  return (
    <div className={styles.container}>
      <img src={logo} alt="Bách Khoa" className={styles.logo} />

      <div className={styles.card}>
        <h2 className={styles.title}>Đăng ký tài khoản</h2>
        {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

        {/* --- BƯỚC 1: CHỌN VAI TRÒ --- */}
        {step === 1 && (
          <form onSubmit={handleNextStep}>
            <div className={styles.inputGroup}>
              <label className={styles.label}>Bạn là:</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className={styles.select}
              >
                <option value="student">Học sinh / Sinh viên</option>
                <option value="teacher">Giáo viên / Giảng viên</option>
              </select>
            </div>
            
            <button type="submit" className={styles.button}>
              Tiếp tục
            </button>
            
            <div className={styles.link}>
              <p>Đã có tài khoản? <Link to="/login">Đăng nhập ngay</Link></p>
            </div>
          </form>
        )}

        {/* --- BƯỚC 2: HIỂN THỊ FORM TƯƠNG ỨNG --- */}
        {step === 2 && (
          <>
            {role === "student" ? (
              <StudentRegisterForm 
                onSubmit={handleFinalSubmit} 
                onBack={() => setStep(1)} 
              />
            ) : (
              <TeacherRegisterForm 
                onSubmit={handleFinalSubmit} 
                onBack={() => setStep(1)} 
              />
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Register;