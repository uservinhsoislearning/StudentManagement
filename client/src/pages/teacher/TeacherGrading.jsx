import { useState } from "react";
import { fetchSubmittedAssignment } from "../../api/students";
import { gradeAssignment } from "../../api/teachers";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";

const API_URL = "http://127.0.0.1:8000"; // ⚠️ Cập nhật nếu khác

const TeacherGrading = () => {
    const [form, setForm] = useState({
        classId: "",
        studentId: "",
        assignmentId: "",
        score: "",
    });
    const [submitted, setSubmitted] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleFetch = async () => {
        const { classId, studentId, assignmentId } = form;
        if (!classId || !studentId || !assignmentId) {
            alert("Vui lòng nhập đủ thông tin!");
            return;
        }

        setLoading(true);
        try {
            const data = await fetchSubmittedAssignment({ classId, studentId, assignmentId });

            // Nếu data là mảng → lấy phần tử đầu tiên
            const submission = Array.isArray(data) ? data[0] : data;

            setSubmitted(submission);
            setForm((prev) => ({
                ...prev,
                score: submission?.score?.toString() || "",
            }));
        } catch (err) {
            alert("❌ Lỗi khi lấy bài nộp: " + err.message);
            setSubmitted(null);
        } finally {
            setLoading(false);
        }
    };

    const handleGrade = async () => {
        const { classId, studentId, assignmentId, score } = form;

        if (!score) {
            alert("Vui lòng nhập điểm số.");
            return;
        }

        try {
            await gradeAssignment({ classId, studentId, assignmentId, score: Number(score) });
            alert("✅ Đã chấm điểm thành công!");
        } catch (err) {
            alert("❌ Lỗi khi chấm điểm: " + err.message);
        }
    };

    return (
        <div style={{ padding: "24px", maxWidth: "700px", margin: "0 auto" }}>
            <h2>🧑‍🏫 Chấm điểm bài tập</h2>

            <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", marginBottom: "16px" }}>
                <Input label="Class ID" name="classId" value={form.classId} onChange={handleChange} required />
                <Input label="Student ID" name="studentId" value={form.studentId} onChange={handleChange} required />
                <Input label="Assignment ID" name="assignmentId" value={form.assignmentId} onChange={handleChange} required />
                <Button onClick={handleFetch} disabled={loading}>
                    📥 Xem bài đã nộp
                </Button>
            </div>

            {submitted && (
                <div style={{ marginBottom: "20px" }}>
                    <h4>📄 Nội dung bài nộp:</h4>
                    <div
                        style={{
                            padding: "12px",
                            border: "1px solid #ccc",
                            borderRadius: "8px",
                            background: "#f9f9f9",
                            whiteSpace: "pre-wrap",
                            marginBottom: "10px",
                        }}
                    >
                        {submitted.text_content || "Không có nội dung."}
                    </div>

                    {submitted.file && (
                        <div style={{ marginBottom: "10px" }}>
                            📎{" "}
                            <a
                                href={`${API_URL}${submitted.file}`}
                                target="_blank"
                                rel="noreferrer"
                            >
                                Tải file đính kèm
                            </a>
                        </div>
                    )}
                </div>
            )}

            {submitted && (
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <Input
                        label="Nhập điểm mới"
                        name="score"
                        value={form.score}
                        type="number"
                        onChange={handleChange}
                        style={{ width: "100px" }}
                    />
                    <Button variant="success" onClick={handleGrade}>
                        ✅ Gửi điểm
                    </Button>
                </div>
            )}
        </div>
    );
};

export default TeacherGrading;