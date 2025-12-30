import requests
from tabulate import tabulate  # pip install tabulate nếu chưa cài

BASE_URL = "http://127.0.0.1:8000"  # ⚠️ Sửa nếu backend bạn chạy khác
student_id = 1  # 🔁 Thay bằng ID sinh viên cần test

url = f"{BASE_URL}/api/student/{student_id}/schedule"

try:
    res = requests.get(url)
    print("📅 Lấy thời khoá biểu...")
    print("Status:", res.status_code)

    if res.status_code != 200:
        print("❌ Lỗi:", res.text)
    else:
        schedule = res.json()

        if not schedule:
            print("🟡 Sinh viên chưa có thời khoá biểu.")
        else:
            table = [
                [i + 1, s["subject"], s["day"], s["startTime"], s["endTime"]]
                for i, s in enumerate(schedule)
            ]
            print(
                tabulate(
                    table,
                    headers=["#", "Môn học", "Thứ", "Bắt đầu", "Kết thúc"],
                    tablefmt="grid",
                )
            )
except Exception as e:
    print("❌ Exception:", e)
