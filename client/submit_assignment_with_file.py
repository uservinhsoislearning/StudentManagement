import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2
student_id = 1
assignment_id = 3

url = f"{BASE_URL}/classes/{class_id}/student/{student_id}/work/{assignment_id}"

# 📝 Nội dung bài làm
data = {"text_content": "Em đã hoàn thành bài tập và gửi kèm file."}

# 📎 File đính kèm (PDF hoặc DOCX)
files = {
    "file": open(
        "student-management-system/Data Visualization-6.pdf", "rb"
    )  # ⚠️ Thay 'sample.pdf' bằng đường dẫn file thật
}

# 📤 Gửi POST request
response = requests.post(url, data=data, files=files)

print("📤 Nộp bài:")
print("Status:", response.status_code)
try:
    print("Response:", response.json())
except Exception as e:
    print("❌ Lỗi đọc JSON:", e, response.text)
