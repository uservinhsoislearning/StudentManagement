import requests

BASE_URL = "http://127.0.0.1:8000/api/semesters"


# 🟢 1. Lấy danh sách tất cả học kỳ
def test_get_semesters():
    res = requests.get(BASE_URL)
    print("GET all semesters:", res.status_code)
    print(res.json())


# 🟢 2. Tạo mới học kỳ
def test_create_semester():
    data = {
        "name": "Học kỳ 2 - 2025",
        "startDate": "2025-06-01",
        "endDate": "2025-11-30",
        "isActive": True,
    }
    res = requests.post(BASE_URL, json=data)
    print("POST create semester:", res.status_code)
    print(res.json())


# 🟢 3. Cập nhật học kỳ (theo ID)
def test_update_semester(semester_id):
    data = {
        "name": "Học kỳ 2 - 2025 (Updated)",
        "startDate": "2025-06-01",
        "endDate": "2025-12-15",
        "isActive": False,
    }
    res = requests.put(f"{BASE_URL}/{semester_id}", json=data)
    print("PUT update semester:", res.status_code)
    print(res.json())


# 🟢 4. Xoá học kỳ (theo ID)
def test_delete_semester(semester_id):
    res = requests.delete(f"{BASE_URL}/{semester_id}")
    print("DELETE semester:", res.status_code)
    try:
        print(res.json())
    except Exception:
        print("Không có nội dung JSON trả về")


# 🟢 5. Toggle trạng thái học kỳ (Mở/Đóng)
def test_toggle_semester_status(semester_id):
    res = requests.patch(f"{BASE_URL}/{semester_id}/toggle-status")
    print("PATCH toggle semester status:", res.status_code)
    print(res.json())


# 👉 Chạy thử các hàm
if __name__ == "__main__":
    test_get_semesters()
    # test_create_semester()
    # test_update_semester(1)
    # test_delete_semester(2)
    # test_toggle_semester_status(1)
