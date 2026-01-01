import Papa from "papaparse";
import { useState } from "react";
import { registerUser } from "../../api/auth";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Select from "../../components/UI/Select";
import styles from "./ManageRegister.module.css";

const ManageRegister = () => {
    const [form, setForm] = useState({
        username: "",
        useremail: "",
        password: "",
        usertype: "Student",
        student_name: "",
        student_dob: "",
        student_gender: "",
        student_email: "",
        parent_email: "",
        student_phone_number: "",
        student_specialization: "",
        student_is_active: true,
        teacher_name: "",
        teacher_gender: "",
        teacher_email: "",
        teacher_profession: ""
    });
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [parsedCSV, setParsedCSV] = useState([]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setForm({ ...form, [name]: type === "checkbox" ? checked : value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage("");
        setError("");

        let dataToSend = {
            username: form.username,
            useremail: form.useremail,
            password: form.password,
            usertype: form.usertype,
        };

        if (form.usertype === "Student") {
            dataToSend = {
                ...dataToSend,
                student_name: form.student_name,
                student_dob: form.student_dob,
                student_gender: form.student_gender,
                student_email: form.student_email,
                parent_email: form.parent_email,
                student_phone_number: form.student_phone_number,
                student_specialization: form.student_specialization,
                student_is_active: true,
            };
        } else if (form.usertype === "Teacher") {
            dataToSend = {
                ...dataToSend,
                teacher_name: form.teacher_name,
                teacher_gender: form.teacher_gender,
                teacher_email: form.teacher_email,
                teacher_profession: form.teacher_profession,
            };
        }

        try {
            await registerUser(dataToSend);
            setMessage("✅ Tạo tài khoản thành công!");
        } catch (err) {
            setError(err.message || "❌ Đăng ký thất bại.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleCSVUpload = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        Papa.parse(file, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
                setParsedCSV(results.data);
                alert(`✅ Đã đọc ${results.data.length} dòng từ file CSV. Bấm \"Đẩy file lên hệ thống\" để đăng ký.`);
            },
            error: (error) => {
                alert("❌ Không đọc được file CSV");
            },
        });
    };

    const submitCSVToServer = async () => {
        if (parsedCSV.length === 0) {
            alert("❌ Chưa có dữ liệu nào được upload!");
            return;
        }

        let successCount = 0;
        let failCount = 0;

        for (const row of parsedCSV) {
            try {
                const payload = buildRegisterPayloadFromCSVRow(row);
                await registerUser(payload);
                successCount++;
            } catch (err) {
                failCount++;
            }
        }

        alert(`📊 Hoàn tất:\n✅ Thành công: ${successCount}\n❌ Thất bại: ${failCount}`);
        setParsedCSV([]);
    };

    const buildRegisterPayloadFromCSVRow = (row) => {
        const base = {
            username: row.username,
            useremail: row.useremail,
            password: row.password,
            usertype: row.usertype,
        };

        switch (row.usertype) {
            case "Student":
                return {
                    ...base,
                    student_name: row.student_name,
                    student_dob: row.student_dob,
                    student_gender: row.student_gender,
                    student_email: row.student_email,
                    parent_email: row.parent_email,
                    student_phone_number: row.student_phone_number,
                    student_specialization: row.student_specialization,
                    student_is_active: true,
                };
            case "Teacher":
                return {
                    ...base,
                    teacher_name: row.teacher_name,
                    teacher_gender: row.teacher_gender,
                    teacher_email: row.teacher_email,
                    teacher_profession: row.teacher_profession,
                };
            default:
                throw new Error("Loại người dùng không hợp lệ trong CSV");
        }
    };

    const renderFields = () => {
        switch (form.usertype) {
            case "Student":
                return (
                    <>
                        <Input label="Tên sinh viên" name="student_name" value={form.student_name} onChange={handleChange} required />
                        <Input label="Ngày sinh" name="student_dob" type="date" value={form.student_dob} onChange={handleChange} required />
                        <Input label="Giới tính" name="student_gender" value={form.student_gender} onChange={handleChange} required />
                        <Input label="Email" name="student_email" value={form.student_email} onChange={handleChange} required />
                        <Input label="Email phụ huynh" name="parent_email" value={form.parent_email} onChange={handleChange} required />
                        <Input label="SĐT" name="student_phone_number" value={form.student_phone_number} onChange={handleChange} required />
                        <Input label="Chuyên ngành" name="student_specialization" value={form.student_specialization} onChange={handleChange} required />
                    </>
                );
            case "Teacher":
                return (
                    <>
                        <Input label="Tên giáo viên" name="teacher_name" value={form.teacher_name} onChange={handleChange} required />
                        <Input label="Giới tính" name="teacher_gender" value={form.teacher_gender} onChange={handleChange} required />
                        <Input label="Email" name="teacher_email" value={form.teacher_email} onChange={handleChange} required />
                        <Input label="Chuyên môn" name="teacher_profession" value={form.teacher_profession} onChange={handleChange} required />
                    </>
                );
            default:
                return null;
        }
    };

    return (
        <div className={styles.container}>
            <h2>Tạo tài khoản người dùng</h2>
            <Form onSubmit={handleSubmit}>
                <Select
                    label="Bạn là:"
                    name="usertype"
                    value={form.usertype}
                    onChange={handleChange}
                    options={[
                        { value: "Student", label: "Sinh viên" },
                        { value: "Teacher", label: "Giáo viên" }
                    ]}
                />
                <Input label="Tên đăng nhập" name="username" value={form.username} onChange={handleChange} required />
                <Input label="Email đăng nhập" name="useremail" value={form.useremail} onChange={handleChange} required />
                <Input label="Mật khẩu" name="password" type="password" value={form.password} onChange={handleChange} required />
                {renderFields()}
                <Button type="submit" disabled={isLoading}>{isLoading ? "Đang tạo..." : "Tạo tài khoản"}</Button>
            </Form>

            <hr style={{ margin: "24px 0" }} />
            <h3>📄 Đăng ký hàng loạt qua file CSV</h3>
            <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
                <input type="file" accept=".csv" onChange={handleCSVUpload} />
                <Button onClick={submitCSVToServer} disabled={parsedCSV.length === 0}>
                    Đẩy file lên hệ thống
                </Button>
            </div>

            {message && <p className={styles.success}>{message}</p>}
            {error && <p className={styles.error}>{error}</p>}
        </div>
    );
};

export default ManageRegister;