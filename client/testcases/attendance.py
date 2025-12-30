from datetime import datetime

import requests

BASE_URL = "http://127.0.0.1:8000/api"
CLASS_ID = 2  # Thay bằng class_id thật


def create_attendance_list():
    url = f"{BASE_URL}/classes/{CLASS_ID}/attendance"
    res = requests.post(url)

    print("📋 Tạo danh sách điểm danh:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi parse response:", e, res.text)


def send_attendance_email():
    url = f"{BASE_URL}/classes/{CLASS_ID}/send-attendance"
    today = datetime.now().strftime("%Y-%m-%d")

    payload = {
        "date": today,
        "records": [
            {"studentId": 1, "present": True},
            {"studentId": 2, "present": False},
            {"studentId": 3, "present": True},
        ],
    }

    res = requests.post(url, json=payload)

    print("📧 Gửi điểm danh qua email:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi parse response:", e, res.text)


if __name__ == "__main__":
    create_attendance_list()
