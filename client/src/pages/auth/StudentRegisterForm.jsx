import React, { useState } from "react";
import styles from "./Register.module.css"; // Dùng chung style

const StudentRegisterForm = ({ onSubmit, onBack }) => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    studentId: "", // Thêm mã số sinh viên
    className: "", // Thêm lớp
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData); // Gửi data ra component cha
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3 className={styles.title}>Thông tin Học sinh</h3>
      
      <div className={styles.inputGroup}>
        <label className={styles.label}>Họ và tên:</label>
        <input className={styles.input} name="name" required onChange={handleChange} />
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label}>MSSV:</label>
        <input className={styles.input} name="studentId" required onChange={handleChange} />
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label}>Lớp:</label>
        <input className={styles.input} name="className" required onChange={handleChange} />
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label}>Email:</label>
        <input className={styles.input} type="email" name="email" required onChange={handleChange} />
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label}>Mật khẩu:</label>
        <input className={styles.input} type="password" name="password" required onChange={handleChange} />
      </div>

      <button type="submit" className={styles.button}>Hoàn tất đăng ký</button>
      <button type="button" onClick={onBack} className={styles.secondaryButton}>Quay lại</button>
    </form>
  );
};

export default StudentRegisterForm;