// Chuyển đổi chữ cái đầu thành chữ hoa
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";

// 📥 Đọc file Excel và trả về mảng đối tượng
export const readExcelFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        const json = XLSX.utils.sheet_to_json(sheet); // [{name, code, credits, description}]
        resolve(json);
      } catch (err) {
        reject("Không đọc được file Excel.");
      }
    };

    reader.onerror = () => reject("Lỗi khi đọc file.");
    reader.readAsArrayBuffer(file);
  });
};
export const capitalizeFirstLetter = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

// Format ngày theo dạng dd/mm/yyyy
export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
};

// Kiểm tra xem một giá trị có phải là email hợp lệ không
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Tạo ID ngẫu nhiên
export const generateRandomId = () => {
  return Math.floor(Math.random() * 100000);
};

// 📤 Export bảng điểm ra PDF
export const exportGradesToPDF = (grades, fileName = "BangDiem.pdf") => {
  const doc = new jsPDF();

  const tableData = grades.map((g) => [
    g.studentId,
    g.name,
    g.midterm,
    g.final,
    g.total,
  ]);

  autoTable(doc, {
    head: [["Mã SV", "Họ tên", "Điểm giữa kỳ", "Điểm cuối kỳ", "Tổng điểm"]],
    body: tableData,
    margin: { top: 20 },
  });

  doc.save(fileName);
};