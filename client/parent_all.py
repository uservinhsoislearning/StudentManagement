import requests

BASE_URL = "http://127.0.0.1:8000/api"
url = f"{BASE_URL}/parents"

try:
    response = requests.get(url)
    response.raise_for_status()

    parents = response.json()
    print(f"📋 Danh sách phụ huynh:{parents}")
    for parent in parents:
        print(
            f"- ID: {parent.get('id')} | Họ tên: {parent.get('name')} | Email: {parent.get('email')} | SĐT: {parent.get('phone')}"
        )
except requests.exceptions.RequestException as e:
    print("❌ Lỗi khi gọi API:", e)
