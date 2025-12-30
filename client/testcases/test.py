import requests

# === Bước 1: Đăng nhập để lấy token ===
# login_url = "http://127.0.0.1:8000/api/auth/login"
# login_payload = {
#     "useremail": "ilovekids177103@gmail.com",
#     "password": "ihave2kidsinmybasement",
#     "role": "admin",  # 👈 Đổi role sang 'admin' nếu gọi API dành cho admin
# }

# login_response = requests.post(login_url, json=login_payload)

# print("🔐 Login Status Code:", login_response.status_code)
# print("🔐 Login Raw Response:", login_response.json())

# # === Bước 2: Kiểm tra và trích xuất token ===
# try:
#     login_data = login_response.json()
#     access_token = login_data.get("access_token")  # hoặc "token", tuỳ theo API của bạn
#     if not access_token:
#         raise ValueError("❌ Không tìm thấy access_token trong phản hồi!")
# except Exception as e:
#     print("❌ Lỗi khi parse JSON từ login:", e)
#     exit()

# === Bước 3: Gọi GET /api/classes với Authorization ===
# classes_url = "http://127.0.0.1:8000/api/classes"

# # === Thêm tham số lọc: ví dụ lọc theo giáo viên và học kỳ ===
# params = {
#     # chỉ lấy lớp của giáo viên id = 1
#     "class_semester": 2,  # chỉ lấy lớp ở học kỳ 2
# }

# # === Gửi request có params ===
# classes_response = requests.get(classes_url, params=params)

# print("📦 Status Code:", classes_response.status_code)
# print("📦 Raw JSON:", classes_response.json())

# try:
#     classes_data = classes_response.json()
#     print("📚 Filtered Classes JSON:", classes_data)
# except Exception as e:
#     print("❌ Không thể parse JSON:", e)


# def fetch_students():
#     url = "http://127.0.0.1:8000/api/students"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Ném lỗi nếu HTTP status code là 4xx/5xx
#         data = response.json()
#         print(f"✅ Danh sách sinh viên nhận được:{data}")
#         for student in data:
#             print(
#                 f"ID: {student['student_id']}, Họ tên: {student['student_name']}, Email: {student.get('email', 'N/A')}"
#             )
#     except requests.exceptions.HTTPError as http_err:
#         print(f"❌ Lỗi HTTP: {http_err}")
#     except requests.exceptions.RequestException as err:
#         print(f"❌ Lỗi kết nối hoặc server: {err}")
#     except Exception as e:
#         print(f"❌ Lỗi khác: {e}")


# if __name__ == "__main__":
#     fetch_students()

url = "http://127.0.0.1:8000/api/classes"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(f"Danh sách lớp học:{data}")
    for cls in data:
        print(f"- ID: {cls['class_id']}, Tên: {cls['class_name']}")
except requests.exceptions.RequestException as e:
    print("Lỗi khi gọi API:", e)
