import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api/dashboard";

export const fetchAdminDashboard = async () => {
  const response = await axios.get(`${BASE_URL}/admin`);
  return response.data;
};

export const fetchTeacherDashboard = async (teacherId) => {
  const response = await axios.get(`${BASE_URL}/teacher/${teacherId}`);
  return response.data;
};

export const fetchStudentDashboard = async (studentId) => {
  const response = await axios.get(`${BASE_URL}/student/${studentId}`);
  return response.data;
};

export const fetchParentDashboard = async () => {
  const response = await axios.get(`${BASE_URL}/parent`);
  return response.data;
};

export const fetchReports = async () => {
  const response = await axios.get("http://127.0.0.1:8000/api/reports");
  return response.data;
};
