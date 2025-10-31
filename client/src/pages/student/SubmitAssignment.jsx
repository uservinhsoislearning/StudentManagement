import { useEffect, useState } from "react";
import {
    fetchStudentByEmail,
    fetchSubmittedAssignment,
    submitAssignment,
} from "../../api/students";
import { fetchAssignments } from "../../api/teachers";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import { useAuth } from "../../context/AuthContext";

const SubmitAssignment = () => {
    const { user } = useAuth();
    const [studentId, setStudentId] = useState(null);
    const [classId, setClassId] = useState("");
    const [assignments, setAssignments] = useState([]);
    const [submittedMap, setSubmittedMap] = useState({});
    const [textContent, setTextContent] = useState("");
    const [file, setFile] = useState(null);
    const [selectedAssignment, setSelectedAssignment] = useState(null);
    const [loading, setLoading] = useState(false);

    // Tìm student theo email
    useEffect(() => {
        const resolveStudent = async () => {
            if (!user?.email) return;
            try {
                const student = await fetchStudentByEmail(user.email);
                if (student) {
                    console.log("🎯 Tìm thấy student:", student);
                    setStudentId(student.student_id);
                } else {
                    console.warn("❌ Không tìm thấy student với email:", user.email);
                }
            } catch (err) {
                console.error("❌ Lỗi khi fetch student:", err);
            }
        };
        resolveStudent();
    }, [user]);

    const handleLoadAssignments = async () => {
        if (!classId) return alert("Vui lòng nhập mã lớp!");
        try {
            const list = await fetchAssignments(classId);
            setAssignments(list);

            const map = {};
            for (let assignment of list) {
                try {
                    const res = await fetchSubmittedAssignment({
                        classId,
                        studentId,
                        assignmentId: assignment.assignment_id,
                    });
                    if (res.length > 0) map[assignment.assignment_id] = res[0];
                } catch {
                    console.warn("⚠️ Không tìm thấy bài nộp:", assignment.assignment_id);
                }
            }
            setSubmittedMap(map);
        } catch (err) {
            console.error("❌ Không thể tải bài tập:", err);
            alert("❌ Lỗi khi tải bài tập.");
        }
    };

    const handleSubmit = async () => {
        if (!selectedAssignment) return alert("Vui lòng chọn bài tập!");
        if (!studentId) return alert("❌ studentId bị thiếu!");
        if (!textContent && !file) return alert("Vui lòng nhập nội dung hoặc file!");

        console.log("📤 Nộp bài với studentId:", studentId);

        let submission;
        let headers = {};

        if (file) {
            submission = new FormData();
            submission.append("text_content", textContent);
            submission.append("file", file);
            // axios sẽ tự gán Content-Type là multipart/form-data
        } else {
            submission = {
                text_content: textContent,
                file: null
            };
            headers["Content-Type"] = "application/json";
        }

        setLoading(true);
        try {
            await submitAssignment({
                classId,
                studentId,
                assignmentId: selectedAssignment.assignment_id,
                submission,
                headers,
            });
            alert("✅ Nộp bài thành công!");
            setFile(null);
            setSubmittedMap((prev) => ({
                ...prev,
                [selectedAssignment.assignment_id]: {
                    text_content: textContent,
                    file: file?.name || null,
                },
            }));
        } catch (err) {
            console.error("❌ Lỗi khi nộp bài:", err);
            alert("❌ Không thể nộp bài.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "24px" }}>
            <h2>Nộp bài tập theo Lớp</h2>

            <div style={{ display: "flex", gap: "12px", marginBottom: "16px" }}>
                <Input
                    placeholder="Nhập mã lớp (classId)..."
                    value={classId}
                    onChange={(e) => setClassId(e.target.value)}
                />
                <Button onClick={handleLoadAssignments}>🔍 Tải bài tập</Button>
            </div>

            {assignments.map((a) => (
                <div
                    key={a.assignment_id}
                    style={{
                        border: "1px solid #ccc",
                        padding: "12px",
                        borderRadius: "8px",
                        marginBottom: "12px",
                        background: selectedAssignment?.assignment_id === a.assignment_id ? "#f0f8ff" : "#fff",
                        cursor: "pointer",
                    }}
                    onClick={() => {
                        setSelectedAssignment(a);
                        setTextContent(submittedMap[a.assignment_id]?.text_content || "");
                        setFile(null);
                    }}
                >
                    <p><strong>Bài tập:</strong> {a.text_content}</p>
                    <p><strong>Hạn:</strong> {new Date(a.deadline).toLocaleString("vi-VN")}</p>
                    <p>
                        <strong>Đã nộp:</strong>{" "}
                        {submittedMap[a.assignment_id]
                            ? `✅ ${submittedMap[a.assignment_id].text_content || "—"}`
                            : "❌ Chưa nộp"}
                    </p>
                </div>
            ))}

            {selectedAssignment && (
                <div style={{ marginTop: "24px" }}>
                    <h3>Nộp bài cho: {selectedAssignment.text_content}</h3>

                    <Input
                        label="Nội dung bài làm"
                        placeholder="Nhập nội dung..."
                        value={textContent}
                        onChange={(e) => setTextContent(e.target.value)}
                        type="textarea"
                    />

                    <div style={{ marginTop: "12px" }}>
                        <label>Chọn file:</label>
                        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
                    </div>

                    <div style={{ marginTop: "16px" }}>
                        <Button onClick={handleSubmit} disabled={loading || !studentId}>
                            {loading
                                ? "Đang nộp..."
                                : submittedMap[selectedAssignment.assignment_id]
                                    ? "📤 Cập nhật bài"
                                    : "📤 Nộp bài"}
                        </Button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SubmitAssignment;