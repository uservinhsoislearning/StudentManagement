import requests

# Cấu hình
base_url = "http://127.0.0.1:8000"
class_id = 2  # 🆔 ID lớp học cần sửa
student_id = 1  # 🆔 ID sinh viên trong lớp đó

# Dữ liệu điểm cần cập nhật
payload = {
    "midterm": 7.5,
    "final": 9.0,
    "grade": round((7.5 + 9.0) / 2, 2),  # Tổng điểm (có thể backend tự tính)
}

# Gửi PUT request
url = f"{base_url}/api/classes/{class_id}/students/{student_id}/grades"
response = requests.put(url, json=payload)

# In kết quả
if response.status_code == 200:
    print("✅ Cập nhật điểm thành công!")
    print("📦 Dữ liệu trả về:", response.json())
else:
    print(f"❌ Lỗi ({response.status_code}): {response.text}")
