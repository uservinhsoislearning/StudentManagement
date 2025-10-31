import requests

# Cấu hình
base_url = "http://127.0.0.1:8000"
student_id = 1  # 🔁 Thay bằng ID sinh viên bạn muốn test

# Gửi request GET để lấy bảng điểm
url = f"{base_url}/api/student/{student_id}/grades"
response = requests.get(url)
print(response.json())
# Xử lý kết quả
if response.status_code == 200:
    print("✅ Danh sách điểm:")
    for g in response.json():
        print(f"Môn: {g['class_field']}, GK: {g['midterm']}, CK: {g['final']}")
else:
    print(f"❌ Lỗi ({response.status_code}): {response.text}")
