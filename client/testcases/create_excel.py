import pandas as pd

# Tạo dữ liệu mẫu
data = {
    "course_name": ["Computer Networks", "Calculus", "Physics"],
    "course_semester": [1, 2, 1],
    "course_midterm_coeff": [0.4, 0.3, 0.5],
    "course_final_coeff": [0.6, 0.7, 0.5],
    "course_credit": [3, 3, 2],
}

# Tạo DataFrame
df = pd.DataFrame(data)

# Lưu thành file Excel
file_path = "sample_course_classes.xlsx"
df.to_excel(file_path, index=False)

file_path
