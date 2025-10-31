import requests

API_URL = "http://127.0.0.1:8000/api/auth/register"


def register_user(name, email, password):
    payload = {"name": name, "email": email, "password": password}

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        print("✅ Đăng ký thành công:", response.json())
    except requests.exceptions.HTTPError as http_err:
        print("❌ Lỗi HTTP:", http_err)
        print(
            "Phản hồi từ server (text):", response.json()
        )  # 👈 Xem lỗi backend cụ thể
    except Exception as err:
        print("❌ Lỗi khác:", err)


# Thử gọi
register_user("Admin Test", "admin@example.com", "123456")
