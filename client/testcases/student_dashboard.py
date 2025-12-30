import requests

BASE_URL = "http://127.0.0.1:8000/api"


def fetch_student_dashboard(student_id):
    url = f"{BASE_URL}/dashboard/student/{student_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print("📊 Dashboard Học Sinh:")
        print(f"- Số môn đã đăng ký: {data.get('enrolledCourses', 0)}")
        print(f"- Bài kiểm tra sắp tới: {data.get('upcomingExams', 0)}")
        print(f"- Bài tập chưa nộp: {data.get('assignmentsPending', 0)}")

    except requests.exceptions.RequestException as e:
        print("❌ Lỗi khi gọi API:", e)


if __name__ == "__main__":
    student_id = 1  # 👈 sửa ID nếu cần
    fetch_student_dashboard(student_id)
