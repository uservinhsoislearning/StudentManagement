import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/students";

// Dashboard dữ liệu (giữ nguyên nếu có API backend)
export const fetchStudentDashboard = async () => {
  const res = await axios.get(`${API_URL}/dashboard`);
  return res.data;
};

export const fetchStudentCourses = async () => {
  const res = await axios.get(`${API_URL}/courses`);
  return res.data;
};

export const fetchStudentSchedule = async () => {
  const res = await axios.get(`${API_URL}/schedule`);
  return res.data;
};

// 🆕 API: Lấy bảng điểm thật của sinh viên theo ID
export const fetchStudentGradesById = async (studentId) => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/student/${studentId}/grades`);
    return res.data;
  } catch (error) {
    console.error("❌ Lỗi khi lấy bảng điểm:", error);
    throw new Error("Không thể lấy bảng điểm");
  }
};

// Lấy danh sách sinh viên
export const fetchStudents = async () => {
  const res = await axios.get(`${API_URL}`);
  return res.data;
};

export const fetchStudentByEmail = async (email) => {
  try {
    console.log("📩 Fetch student by email:", email);
    const res = await fetch(`${API_URL}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const students = await res.json();
    console.log("📚 Danh sách student:", students);

    const student = students.find(
      (s) => s.student_email?.trim().toLowerCase() === email.trim().toLowerCase()
    );
    console.log("🎯 Match student:", student);
    return student;
  } catch (err) {
    console.error("❌ Lỗi khi fetch student:", err);
    return null;
  }
};
const BASE_URL = "http://127.0.0.1:8000/api";

export const submitAssignment = async ({ classId, studentId, assignmentId, submission }) => {
  const url = `${BASE_URL}/classes/${classId}/student/${studentId}/assignment/${assignmentId}`;

  // Nếu có file thì submission là FormData
  if (submission instanceof FormData) {
    return (await axios.post(url, submission));  // KHÔNG cần headers
  }

  // Nếu không có file
  return (await axios.post(url, submission, {
    headers: {
      "Content-Type": "application/json",
    },
  }));
};

export const fetchSubmittedAssignment = async ({ classId, studentId, assignmentId }) => {
  const res = await fetch(
    `${BASE_URL}/classes/${classId}/student/${studentId}/assignment/${assignmentId}`
  );
  if (!res.ok) throw new Error("Không thể tải bài đã nộp.");
  return res.json();
};