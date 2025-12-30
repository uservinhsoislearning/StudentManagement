import requests

BASE_URL = "http://127.0.0.1:8000/api/dashboard"
teacher_id = 3  # 🔧 Thay bằng ID giáo viên thật

url = f"{BASE_URL}/teacher/{teacher_id}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    print("📊 Tổng quan Giáo viên:")
    print(f"- Số lớp giảng dạy: {data.get('totalClasses', 0)}")
    print(f"- Số bài tập sắp đến hạn: {data.get('assignmentsDue', 0)}")

except requests.exceptions.RequestException as e:
    print("❌ Lỗi khi gọi API:", e)
    if response is not None:
        print("Phản hồi:", response.json())
