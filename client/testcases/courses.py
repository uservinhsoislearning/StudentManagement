import requests

BASE_URL = "http://127.0.0.1:8000/api"


# 1️⃣ Lấy tất cả môn học
def get_all_courses():
    url = f"{BASE_URL}/course-classes"
    res = requests.get(url)
    print("📘 Danh sách môn học:")
    print("Status:", res.status_code)
    print("Response:", res.json())


# 2️⃣ Thêm mới môn học
def create_course():
    url = f"{BASE_URL}/course-classes"
    payload = {
        "course_name": "Machine Learning",
        "course_semester": 1,
        "course_midterm_coeff": 0.4,
        "course_final_coeff": 0.6,
    }
    res = requests.post(url, json=payload)
    print("\n🆕 Tạo môn học mới:")
    print("Status:", res.status_code)
    print("Response:", res.json())


# 3️⃣ Cập nhật môn học
def update_course(course_id):
    url = f"{BASE_URL}/course-classes/{course_id}"
    payload = {
        "course_name": "Machine Learning - Updated",
        "course_semester": 2,
        "course_midterm_coeff": 0.5,
        "course_final_coeff": 0.5,
    }
    res = requests.put(url, json=payload)
    print("\n✏️ Cập nhật môn học:")
    print("Status:", res.status_code)
    print("Response:", res.json())


# 4️⃣ Xoá môn học
def delete_course(course_id):
    url = f"{BASE_URL}/course-classes/{course_id}"
    res = requests.delete(url)
    print("\n❌ Xoá môn học:")
    print("Status:", res.status_code)
    print("Response:", res.json())


# 5️⃣ Import nhiều môn học từ danh sách (mock Excel data)
def import_courses():
    url = f"{BASE_URL}/course-classes/import"
    payload = [
        {
            "course_name": "Introduction to SE",
            "course_semester": 2,
            "course_midterm_coeff": 0.5,
            "course_final_coeff": 0.5,
        },
        {
            "course_name": "Calculus 1",
            "course_semester": 1,
            "course_midterm_coeff": 0.5,
            "course_final_coeff": 0.5,
        },
        {
            "course_name": "Calculus 2",
            "course_semester": 2,
            "course_midterm_coeff": 0.5,
            "course_final_coeff": 0.5,
        },
    ]
    res = requests.post(url, json=payload)
    print("\n📥 Import nhiều môn học:")
    print("Status:", res.status_code)
    print("Response:", res.json())


if __name__ == "__main__":
    get_all_courses()
    create_course()
    update_course(course_id=1)  # Thay ID thật từ DB
    delete_course(course_id=2)  # Thay ID thật từ DB
    import_courses()
