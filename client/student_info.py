import requests

BASE_URL = "http://127.0.0.1:8000/api"


def fetch_all_students():
    url = f"{BASE_URL}/students"
    try:
        response = requests.get(url)
        response.raise_for_status()
        students = response.json()

        print(f"✅ Lấy {len(students)} sinh viên thành công.\n")
        for student in students:
            print(
                f"🎓 {student['student_id']} | Email: {student['student_email']} | Lớp tốt nghiệp: {student['student_graduating_class']}"
            )
    except requests.exceptions.RequestException as e:
        print("❌ Lỗi khi gọi API:", e)


if __name__ == "__main__":
    fetch_all_students()
