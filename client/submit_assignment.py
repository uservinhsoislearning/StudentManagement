import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2
student_id = 1
assignment_id = 2

url = f"{BASE_URL}/classes/{class_id}/student/{student_id}/work/{assignment_id}"
payload = {
    "text_content": "Em đã hoàn thành bài tập. Xem chi tiết ở file đính kèm.",
    "file": None,  # Nếu có upload file, bạn dùng 'files={'file': open('path', 'rb')}' thay thế.
}

res = requests.post(url, json=payload)
print("📤 Nộp bài:")
print("Status:", res.status_code)
try:
    print("Response:", res.json())
except Exception as e:
    print("❌ Lỗi đọc JSON:", e, res.json())
