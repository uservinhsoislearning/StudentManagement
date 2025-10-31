import { useEffect, useState } from "react";
import { fetchStudentSchedule } from "../../api/students";
import Table from "../../components/UI/Table";

const Schedule = () => {
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    fetchStudentSchedule().then(setSchedule);
  }, []);

  return (
    <div style={{ padding: "24px" }}>
      <h2>Thời khóa biểu</h2>
      <Table
        columns={["Môn học", "Ngày học", "Giờ bắt đầu", "Giờ kết thúc"]}
        data={schedule}
      />
    </div>
  );
};

export default Schedule;
