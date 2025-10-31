import requests

# Cấu hình thông tin cần thiết
BASE_URL = "http://127.0.0.1:8000"  # Thay đổi nếu API không chạy ở localhost:8000
class_id = 2
student_id = 1

# Gửi PATCH request
url = f"{BASE_URL}/api/classes/{class_id}/students/{student_id}/attendance"
response = requests.patch(url)

# Hiển thị kết quả
print("Status code:", response.status_code)
print("Response:", response.json())
