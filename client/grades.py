import requests

BASE_URL = "http://127.0.0.1:8000/api"

# ⚠️ Thay thế bằng ID thực tế của lớp và sinh viên trong DB
CLASS_ID = 2
STUDENT_ID = 2


# 1️⃣ Lấy bảng điểm của tất cả sinh viên trong lớp
def get_class_grades():
    url = f"{BASE_URL}/classes/{CLASS_ID}/grades"
    res = requests.get(url)
    print("📄 Lấy bảng điểm lớp:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi đọc response:", e, res.text)


# 2️⃣ Cập nhật điểm cho sinh viên
def update_student_grade():
    url = f"{BASE_URL}/classes/{CLASS_ID}/students/{STUDENT_ID}/grades"
    payload = {"midterm": 7.5, "final": 8.2, "grade": round((7.5 + 8.2) / 2, 2)}
    res = requests.put(url, json=payload)
    print("\n📝 Cập nhật điểm sinh viên:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi đọc response:", e, res.text)


if __name__ == "__main__":
    get_class_grades()
    update_student_grade()
