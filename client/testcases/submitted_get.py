import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2
student_id = 1
assignment_id = 9

url = f"{BASE_URL}/classes/{class_id}/student/{student_id}/assignment/{assignment_id}"

res = requests.get(url)

print("📥 Lấy bài đã nộp:")
print("Status:", res.status_code)
try:
    print("Response:", res.json())
except Exception as e:
    print("❌ Lỗi đọc JSON:", e, res.text)
