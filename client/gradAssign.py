import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Thay bằng ID thực tế
CLASS_ID = 2
STUDENT_ID = 1
ASSIGNMENT_ID = 9


def test_put_grade():
    url = f"{BASE_URL}/classes/{CLASS_ID}/student/{STUDENT_ID}/work/{ASSIGNMENT_ID}"
    payload = {
        "score": 9.5  # Điểm chấm
    }
    response = requests.put(url, json=payload)
    print("📝 PUT - Chấm điểm bài tập")
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("❌ JSON error:", e, response.text)


def test_delete_grade():
    url = f"{BASE_URL}/classes/{CLASS_ID}/student/{STUDENT_ID}/work/{ASSIGNMENT_ID}"
    response = requests.delete(url)
    print("\n❌ DELETE - Xoá điểm bài tập")
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("❌ JSON error:", e, response.text)


if __name__ == "__main__":
    test_put_grade()
    # test_delete_grade()
