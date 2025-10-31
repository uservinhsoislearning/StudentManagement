import requests

BASE_URL = "http://127.0.0.1:8000/api"
SESSION = requests.Session()  # giữ session login (nếu cần)

# 👉 Đăng nhập trước nếu backend yêu cầu session-based
# def login_as_student():
#     payload = {
#         "useremail": "sinhvien@example.com",  # thay bằng email thật
#         "password": "matkhau123",             # thay bằng password thật
#         "usertype": "student",
#     }
#     res = SESSION.post(f"{BASE_URL}/login", json=payload)
#     print("🔑 Login:", res.status_code, res.text)


# 1️⃣ Đăng ký lớp môn học
def register_class(class_id):
    url = f"{BASE_URL}/registrations/{class_id}"
    res = SESSION.post(url)
    print("📌 Đăng ký lớp:")
    print("Status:", res.status_code)
    print("Response:", res.json())


# 2️⃣ Huỷ đăng ký lớp môn học
def unregister_class(class_id):
    url = f"{BASE_URL}/registrations/{class_id}"
    res = SESSION.delete(url)
    print("🗑️ Huỷ đăng ký lớp:")
    print("Status:", res.status_code)
    print("Response:", res.json())


# 3️⃣ Lấy danh sách lớp chưa đăng ký
def get_available_classes():
    url = f"{BASE_URL}/registrations/available"
    res = SESSION.get(url)
    print("📖 Lớp chưa đăng ký:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ JSON decode lỗi:", e, res.text)


# 4️⃣ Lấy danh sách lớp đã đăng ký
def get_registered_classes():
    url = f"{BASE_URL}/registrations/registered"
    res = SESSION.get(url)
    print("✅ Lớp đã đăng ký:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ JSON decode lỗi:", e, res.text)


if __name__ == "__main__":
    # login_as_student()          # Bỏ nếu không cần login bằng session
    register_class(1)  # Thay ID lớp thực tế
    # unregister_class(1)         # Thay ID lớp thực tế
    # get_available_classes()
    # get_registered_classes()
