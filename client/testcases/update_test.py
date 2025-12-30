import requests

# URL API (bạn thay bằng localhost hoặc domain thật nếu có)
API_URL = "http://localhost:8000/api/classes/1"  # 123 là id của lớp cần update

# Dữ liệu cần cập nhật
data = {"class_name": "Lớp A cập nhật", "class_teacher": 2, "class_semester": 1}

# Gửi PUT request
response = requests.put(API_URL, json=data)

# In kết quả
print("Status Code:", response.status_code)
print("Response:", response.json())
