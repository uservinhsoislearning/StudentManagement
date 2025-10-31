import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2  # 🔧 Thay bằng ID lớp
student_id = 1  # 🔧 Thay bằng ID sinh viên
assignment_id = 8  # 🔧 Thay bằng ID bài tập

url = f"{BASE_URL}/classes/{class_id}/student/{student_id}/work/{assignment_id}"

# 🎯 Điểm số cần chấm
payload = {"score": 8.5}

response = requests.put(url, json=payload)

print("📥 CHẤM ĐIỂM:")
print("Status:", response.status_code)
try:
    print("Response:", response.json())
except Exception as e:
    print("❌ Lỗi đọc JSON:", e, response.text)
