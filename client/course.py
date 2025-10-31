import requests

BASE_URL = "http://127.0.0.1:8000/api/course-classes"


# 1. GET tất cả các môn học
def get_courses():
    res = requests.get(BASE_URL)
    print("📥 GET:", res.status_code)
    print(res.json())


# 2. POST - thêm môn học mới
def create_course():
    data = {
        "course_name": "Computer Networks",
        "course_semester": 1,
        "course_midterm_coeff": 0.4,
        "course_final_coeff": 0.6,
    }
    res = requests.post(BASE_URL, json=data)
    print("🆕 POST:", res.status_code)
    print(res.json())
    return res.json()  # giả sử trả về ID nếu cần


# 3. PUT - cập nhật môn học
def update_course(course_id):
    data = {
        "course_name": "Computer Networks - Updated",
        "course_semester": 2,
        "course_midterm_coeff": 0.5,
        "course_final_coeff": 0.5,
        "course_credit": 1,
    }
    res = requests.put(f"{BASE_URL}/{course_id}", json=data)
    print("✏️ PUT:", res.status_code)
    print(res.json())


# 4. DELETE - xoá môn học
def delete_course(course_id):
    res = requests.delete(f"{BASE_URL}/{course_id}")
    print("🗑️ DELETE:", res.status_code)
    print(res.json())


if __name__ == "__main__":
    # get_courses()
    # create_course()
    update_course(1)  # sửa ID phù hợp
    # delete_course(1)
