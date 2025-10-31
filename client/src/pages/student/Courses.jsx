import { useEffect, useState } from "react";
import { fetchStudentCourses } from "../../api/students";
import Table from "../../components/UI/Table";

const Courses = () => {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetchStudentCourses().then(setCourses);
  }, []);

  return (
    <div style={{ padding: "24px" }}>
      <h2>Khóa học của bạn</h2>
      <Table
        columns={["Mã khóa học", "Tên khóa học", "Giảng viên", "Trạng thái"]}
        data={courses}
      />
    </div>
  );
};

export default Courses;
