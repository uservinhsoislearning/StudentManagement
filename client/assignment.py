import requests

BASE_URL = "http://127.0.0.1:8000/api"
CLASS_ID = 2  # ✅ Thay bằng ID lớp bạn muốn test


# 1️⃣ Lấy danh sách bài tập của lớp
def get_assignments():
    url = f"{BASE_URL}/classes/{CLASS_ID}/assignments"
    res = requests.get(url)
    print("📄 Danh sách bài tập:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi đọc JSON:", e, res.text)


# 2️⃣ Tạo bài tập mới (text_content)
def create_assignment():
    url = f"{BASE_URL}/classes/{CLASS_ID}/assignments"
    payload = {
        "text_content": "Lập trình thuật toán quay lui N-Queens",
        "file": None,
        "deadline": "2026-05-13T00:00:00Z",
    }
    res = requests.post(url, json=payload)
    print("\n➕ Thêm bài tập mới:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi đọc JSON:", e, res.text)


# 3️⃣ (Tuỳ chọn) Upload bài tập dạng file
def create_assignment_with_file():
    url = f"{BASE_URL}/classes/{CLASS_ID}/assignments"
    files = {
        "file": open("example.pdf", "rb")  # 👈 Thay bằng file thật
    }
    data = {"text_content": "", "deadline": "2026-05-13T00:00:00Z"}
    res = requests.post(url, data=data, files=files)
    print("\n📎 Upload bài tập dạng file:")
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except Exception as e:
        print("❌ Lỗi đọc JSON:", e, res.text)


# 🏁 Chạy test
if __name__ == "__main__":
    get_assignments()
    # create_assignment()
    # create_assignment_with_file()  # Bỏ comment nếu muốn test file upload
