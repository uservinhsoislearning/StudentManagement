import requests

BASE_URL = "http://127.0.0.1:8000"
class_id = 2  # 🔁 thay bằng ID lớp bạn muốn kiểm tra

url = f"{BASE_URL}/api/classes/{class_id}/attendance"

res = requests.get(url)

print("📋 Danh sách điểm danh hôm nay:")
print("Status:", res.status_code)

try:
    print("Response:", res.json())
except Exception as e:
    print("❌ Lỗi đọc JSON:", e, res.text)
