import requests

BASE_URL = "http://127.0.0.1:8000/api"
class_id = 2  # 🔧 Thay bằng ID lớp bạn muốn xem chi tiết

url = f"{BASE_URL}/classes/{class_id}/details"

response = requests.get(url)

print("📄 Thông tin chi tiết lớp học:")
print("Status:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("❌ Không thể đọc JSON:", e)
    print("Raw response:", response.text)
