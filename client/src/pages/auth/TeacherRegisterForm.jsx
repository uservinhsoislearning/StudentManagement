import React, { useState } from "react";
import styles from "./Register.module.css";

const TeacherRegisterForm = ({ onSubmit, onBack }) => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    department: "", // Thêm khoa/viện
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3 className={styles.title}>Thông tin Giáo viên</h3>
      
      <div className={styles.inputGroup}>
        <label className={styles.label}>Họ và tên:</label>
        <input className={styles.input} name="name" required onChange={handleChange} />
      </div>

      <div className={styles.inputGroup}>
        <label className={styles.label}>Khoa / Viện:</label>
        <input className={styles.input} name="department" required onChange={handleChange} />
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

export default TeacherRegisterForm;