import requests

BASE_URL = "http://127.0.0.1:8000/api/teachers"


# 🟢 Test GET tất cả giáo viên
def test_get_teachers():
    response = requests.get(BASE_URL)
    print("GET all teachers:", response.status_code)
    print(response.json())


# 🟢 Test POST tạo giáo viên mới
def test_post_teacher():
    data = {
        "teacher_name": "Le Thi Thanh",
        "teacher_gender": "Female",
        "teacher_email": "thanh.le@sis.hust.edu.vn",
        "teacher_profession": "Physics",
    }
    response = requests.post(BASE_URL, json=data)
    print("POST create teacher:", response.status_code)
    print(response.json())


# 🟢 Test PUT cập nhật giáo viên
def test_put_teacher():
    data = {
        "teacher_id": 2,  # sửa ID cho đúng người cần cập nhật
        "teacher_name": "Bui Thi Mai Anh",
        "teacher_gender": "Female",
        "teacher_email": "maianh.bui@sis.hust.edu.vn",
        "teacher_profession": "Software Engineering",
    }
    response = requests.put(BASE_URL, json=data)
    print("PUT update teacher:", response.status_code)
    print(response.json())


# 🟢 Test DELETE giáo viên theo ID
def test_delete_teacher(teacher_id):
    response = requests.delete(f"{BASE_URL}/{teacher_id}")
    print("DELETE teacher:", response.status_code)
    print(response.json())


# 👉 Gọi các hàm để test
if __name__ == "__main__":
    test_get_teachers()
    # test_post_teacher()
    # test_put_teacher()
    # test_delete_teacher(4)  # thay bằng ID thật
