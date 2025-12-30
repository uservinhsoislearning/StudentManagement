import requests

BASE_URL = "http://127.0.0.1:8000/api"
CLASS_ID = 2  # ⚠️ Thay bằng ID lớp thực tế


def get_students_in_class(class_id):
    url = f"{BASE_URL}/classes/{class_id}/get-students"
    res = requests.post(url)

    print(f"📚 Danh sách sinh viên trong lớp ID {class_id}:")
    print("Status code:", res.status_code)

    try:
        data = res.json()
        if isinstance(data, list):
            for i, student in enumerate(data, start=1):
                print(
                    f"{i}. ID: {student.get('student_id')} - {student.get('student_name')} ({student.get('student_email')})"
                )
        else:
            print("⚠️ Response không phải danh sách:", data)
    except Exception as e:
        print("❌ Lỗi khi phân tích JSON:", e)
        print("Response text:", res.text)


if __name__ == "__main__":
    get_students_in_class(CLASS_ID)
