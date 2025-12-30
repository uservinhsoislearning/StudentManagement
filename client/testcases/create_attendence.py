import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2  # Thay bằng ID lớp thật
student_id = 1  # Thay bằng ID sinh viên thật

url = f"{BASE_URL}/classes/{class_id}/student/{student_id}/attendance"

try:
    res = requests.patch(url)
    print("📌 Gửi PATCH điểm danh:")
    print("Status:", res.status_code)
    print("Response:", res.json())
except Exception as e:
    print("❌ Lỗi:", e)
