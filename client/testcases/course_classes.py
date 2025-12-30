import requests

BASE_URL = "http://127.0.0.1:8000/api"
url = f"{BASE_URL}/course-classes-both"

res = requests.get(url)
print("📚 Danh sách môn học có lớp và thời khóa biểu:")
print("Status:", res.status_code)

try:
    data = res.json()
    for course in data:
        course_name = course.get("course_name", "Không rõ")
        print(f"\n📘 Môn: {course_name} (Học kỳ {course.get('course_semester')})")

        for cls in course.get("classes", []):
            class_name = cls.get("class_name", "Không rõ")
            print(f"  🏫 Lớp: {class_name} (HK {cls.get('class_semester')})")

            for t in cls.get("timetables", []):
                print(
                    f"    🕒 {t.get('day_of_week')} | {t.get('start_time')} - {t.get('end_time')}"
                )
except Exception as e:
    print("❌ Lỗi khi đọc JSON:", e)
    print("Raw response:", res.text)
