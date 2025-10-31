import requests

BASE_URL = "http://127.0.0.1:8000/api"
parent_id = 1  # 🔧 Thay bằng ID phụ huynh bạn muốn test

url = f"{BASE_URL}/dashboard/parent/{parent_id}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(data)
    print("👨‍👩‍👧 Tổng quan Phụ huynh:")
    print(f"- Số tin nhắn: {data.get('messages', 0)}")
    print("- Danh sách con:")
    for child in data.get("children", []):
        print(f"  • {child['name']} - Tiến độ: {child['progress']}%")

except requests.exceptions.RequestException as e:
    print("❌ Lỗi khi gọi API:", e)
