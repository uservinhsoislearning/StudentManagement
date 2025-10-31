import axios from "axios";
const API_URL = "http://127.0.0.1:8000/api";

// Lấy toàn bộ danh sách giáo viên
export const fetchAllTeachers = async () => {
  const res = await fetch(`${API_URL}/teachers`);
  if (!res.ok) throw new Error("Không thể lấy danh sách giáo viên");
  return res.json();
};

// Lấy danh sách lớp của giáo viên dựa vào email
export const fetchTeacherClassesByEmail = async (email) => {
  console.log("📩 Fetch lớp theo email:", email);
  const res = await fetch(`${API_URL}/teachers`);
  const data = await res.json();
  console.log("📚 Danh sách teacher:", data);
  const teacher = data.find((t) => t.teacher_email === email);
  console.log("🎯 Match teacher:", teacher);
  return teacher?.classes || [];
};
export const fetchTeacherByEmail = async (email) => {
  try {
    console.log("📩 Fetch teacher by email:", email);
    const res = await fetch(`${API_URL}/teachers`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const teachers = await res.json();
    console.log("📚 Danh sách teacher:", teachers);

    const teacher = teachers.find(
      (s) => s.teacher_email?.trim().toLowerCase() === email.trim().toLowerCase()
    );
    console.log("🎯 Match teacher:", teacher);
    return teacher;
  } catch (err) {
    console.error("❌ Lỗi khi fetch teacher:", err);
    return null;
  }
};
// Lấy bảng điểm của lớp
export const fetchClassGrades = async (classId) => {
  const res = await fetch(`${API_URL}/classes/${classId}/grades`);
  if (!res.ok) throw new Error("Không thể lấy bảng điểm lớp");
  return res.json();
};

// Cập nhật điểm cho sinh viên
// ✅ Cập nhật điểm sinh viên qua API PUT /api/classes/:classId/students/:studentId/grades
export const updateStudentGrade = async ({ classId, studentId, midterm, final }) => {
  const total = ((Number(midterm) + Number(final)) / 2).toFixed(2);

  const payload = {
    midterm,
    final,
    grade: total, // gửi cả tổng điểm nếu backend không tự tính
  };

  const response = await fetch(`http://127.0.0.1:8000/api/classes/${classId}/students/${studentId}/grades`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error("Không thể cập nhật điểm: " + errorText);
  }

  return response.json(); // Giả sử trả về { updated: { midterm, final, grade } }
};

// Lấy danh sách sinh viên trong lớp
export const fetchStudentsInClass = async (classId) => {
  const res = await fetch(`${API_URL}/classes/${classId}/students`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Không thể lấy danh sách sinh viên");
  return res.json();
};

// Lấy thống kê điểm lớp
export const fetchClassStatistics = async (classId) => {
  const res = await fetch(`${API_URL}/classes/${classId}/statistics`);
  if (!res.ok) throw new Error("Không thể lấy thống kê điểm");
  return res.json();
};
// 🧾 Lấy bài nộp và điểm của sinh viên cho một bài tập
export const getAssignmentSubmission = async ({ classId, studentId, assignmentId }) => {
  const response = await axios.get(
    `${API_URL}/classes/${classId}/student/${studentId}/work/${assignmentId}`
  );
  return response.data;
};



// 🧑‍🏫 Giáo viên chấm điểm bài tập
export const gradeAssignment = async ({ classId, studentId, assignmentId, score }) => {
  const response = await axios.put(
    `${API_URL}/classes/${classId}/student/${studentId}/work/${assignmentId}`,
    { score }
  );
  return response.data;
};

// ❌ Giáo viên xoá điểm (nếu cần)
export const deleteAssignmentGrade = async ({ classId, studentId, assignmentId }) => {
  const response = await axios.delete(
    `${API_URL}/classes/${classId}/student/${studentId}/work/${assignmentId}`
  );
  return response.data;
};
export const fetchAssignments = async (classId) => {
  const res = await fetch(`${API_URL}/classes/${classId}/assignments`);
  if (!res.ok) {
    const err = await res.text();
    throw new Error("Không thể lấy danh sách bài tập: " + err);
  }
  return res.json();
};

export const addAssignment = async (classId, assignment) => {
  const payload = {
    text_content: assignment.text_content || "",
    file: null,
    deadline: assignment.deadline,
    is_exam: assignment.is_exam || false, // ➕ Thêm dòng này
  };

  const res = await fetch(`${API_URL}/classes/${classId}/assignments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error("Không thể thêm bài tập: " + err);
  }

  return res.json();
};
export const createAttendanceList = async (classId) => {
  const res = await fetch(`${API_URL}/classes/${classId}/attendance`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Không thể tạo danh sách điểm danh");
  return res.json();
};
export const sendAttendanceByEmail = async (classId, date, records) => {
  const res = await fetch(`${API_URL}/classes/${classId}/send-attendance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ date, records }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error("Không thể gửi điểm danh: " + err);
  }

  return res.json();
};
export const getAttendanceList = async (classId) => {
  const res = await fetch(`${API_URL}/classes/${classId}/attendance`, {
    method: "GET",
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error("Không thể lấy danh sách điểm danh: " + err);
  }

  return res.json();
};

export const toggleStudentAttendance = async (classId, studentId) => {
  const res = await axios.patch(`${API_URL}/classes/${classId}/students/${studentId}/attendance`);
  return res.data;
};

const BASE_URL = "http://127.0.0.1:8000/api";

export const addAssignmentWithFile = async (classId, assignmentData) => {
  const url = `${BASE_URL}/classes/${classId}/assignments-file`;

  const formData = new FormData();
  formData.append("text_content", assignmentData.text_content);
  formData.append("deadline", assignmentData.deadline);
  formData.append("is_exam", assignmentData.is_exam);
  if (assignmentData.file) formData.append("file", assignmentData.file);

  const response = await axios.post(url, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};
export const fetchAllParents = async () => {
  const response = await axios.get(`${BASE_URL}/parents`);
  return response.data; // Trả về danh sách: [ { id, name, email, phone }, ... ]
};