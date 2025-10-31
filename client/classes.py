import requests

BASE_URL = "http://127.0.0.1:8000/api/classes"


# ✅ 1. Lấy tất cả lớp
def test_get_classes():
    response = requests.get(BASE_URL)
    print("GET all classes:", response.status_code)
    print(response.json())


# ✅ 2. Tạo lớp mới
def test_create_class():
    data = {"class_name": "YOLO", "class_teacher": 2, "class_semester": 1, "course": 1}
    response = requests.post(BASE_URL, json=data)
    print("POST create class:", response.status_code)
    print(response.json())


# ✅ 3. Cập nhật lớp
def test_update_class(class_id):
    data = {
        "class_id": class_id,
        "class_name": "Giải tích 2",
        "class_teacher": 1,
        "class_semester": 3,
        "course": 6,
    }
    response = requests.put(BASE_URL, json=data)
    print("PUT update class:", response.status_code)
    print(response.json())


# ✅ 4. Xoá lớp
def test_delete_class(class_id):
    response = requests.delete(f"{BASE_URL}/{class_id}")
    print("DELETE class:", response.status_code)
    try:
        print(response.json())
    except Exception:
        print("⚠️ Không có JSON trả về")


# 👉 Chạy thử
if __name__ == "__main__":
    # test_create_class()
    # test_update_class(6)  # Thay bằng class_id thật
    # test_delete_class(2)
    test_get_classes()  # Thay bằng class_id thật
