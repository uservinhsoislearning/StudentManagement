import React from "react";
import styles from "./Select.module.css"; // bạn có thể tạo file CSS riêng nếu muốn

const Select = ({ label, name, value, onChange, options, required }) => {
    return (
        <div className={styles.formGroup}>
            <label className={styles.label}>{label}</label>
            <select
                className={styles.select}
                name={name}
                value={value}
                onChange={onChange}
                required={required}
            >
                {options.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                        {opt.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default Select;