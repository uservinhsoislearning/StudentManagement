import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const fetchParentDashboard = async (parentId) => {
  const response = await axios.get(`${BASE_URL}/dashboard/parent/${parentId}`);
  return response.data;
};
export const fetchAllParents = async () => {
  const response = await axios.get(`${BASE_URL}/parents`);
  return response.data; // [ { id, name, email, phone }, ... ]
};

export const fetchParentByEmail = async (email) => {
  const parents = await fetchAllParents();
  return parents.find((p) => p.parent_email.toLowerCase() === email.toLowerCase());
};



export const fetchMessages = async () => {
  const response = await axios.get(`${BASE_URL}/messages`);
  return response.data; // Trả về mảng: [ { sender, text }, ... ]
};

export const sendMessage = async (senderId, receiverId, text) => {
  const url = `${BASE_URL}/messages/usr1/${senderId}/usr2/${receiverId}`;
  const payload = { text };

  const response = await axios.post(url, payload);
  return response.data; // Trả về phản hồi từ backend
};
export const fetchStudentProgress = async (semesterId = "") => {
  const url = semesterId
    ? `${BASE_URL}/progress?semesterId=${semesterId}`
    : `${BASE_URL}/progress`;

  const response = await axios.get(url);
  return response.data;
};