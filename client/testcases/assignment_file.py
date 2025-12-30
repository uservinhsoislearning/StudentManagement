import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2  # 🔧 Thay bằng ID lớp muốn upload bài tập

url = f"{BASE_URL}/classes/{class_id}/assignments-file"

# 📝 Nội dung bài tập (nếu backend hỗ trợ text_content)
data = {
    "text_content": "Bài tập chương 6: Vẽ biểu đồ bằng Matplotlib.",
    "deadline": "2025-06-15T23:59:00Z",  # 🔧 Nhớ định dạng chuẩn ISO
    "is_exam": False,
}

# # 📎 File đính kèm (PDF hoặc DOCX)
# files = {
#     "file": open(
#         "student-management-system/Data Visualization-6.pdf", "rb"
#     )  # ✅ Đường dẫn thực tế
# }

response = requests.post(url, data=data)

print("📤 Upload bài tập:")
print("Status:", response.status_code)
try:
    print("Response:", response.json())
except Exception as e:
    print("❌ Lỗi đọc JSON:", e, response.text)
