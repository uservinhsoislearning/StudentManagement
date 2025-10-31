import requests

# URL API login
url = "http://127.0.0.1:8000/api/auth/login"

# Dữ liệu đăng nhập
payload = {
    "useremail": "coung.dovan@sis.hust.edu.vn",  # 🔁 Thay bằng email thật
    "password": "natehiggers",  # 🔁 Thay bằng mật khẩu đúng
    "role": "teacher",  # 🔁 Chọn role: student, teacher, admin...
}

try:
    response = requests.post(url, json=payload)

    # Kiểm tra kết quả
    if response.status_code == 200:
        print("✅ Đăng nhập thành công!")
        print("📦 Dữ liệu trả về:", response.json())
    else:
        print(f"❌ Đăng nhập thất bại ({response.status_code})")
        print("🧾 Chi tiết:", response.text)

except Exception as e:
    print("❌ Lỗi khi gửi request:", e)
