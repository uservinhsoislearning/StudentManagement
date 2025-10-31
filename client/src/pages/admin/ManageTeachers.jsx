import { useEffect, useState } from "react";
import {
  createTeacher,
  deleteTeacher,
  updateTeacher,
} from "../../api/admin";
import {
  createClass,
  deleteClass,
  updateClass,
} from "../../api/classes";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Modal from "../../components/UI/Modal";
import useTeachers from "../../hooks/useTeacher";

const ManageTeachers = () => {
  const { teachers, setTeachers, loading } = useTeachers();
  const [isModalOpen, setModalOpen] = useState(false);
  const [editingTeacher, setEditingTeacher] = useState(null);
  const [teacherForm, setTeacherForm] = useState({
    teacher_name: "",
    teacher_email: "",
    teacher_gender: "",
    teacher_classes: "",
    teacher_profession: "",
  });
  const [searchTerm, setSearchTerm] = useState("");
  const [expandedTeacherId, setExpandedTeacherId] = useState(null);
  const [editingClass, setEditingClass] = useState(null);
  const [classForm, setClassForm] = useState({
    class_name: "",
    class_semester: "",
    course: "",
  });
  const [classSearchTerm, setClassSearchTerm] = useState("");

  useEffect(() => {
    setEditingClass(null);
    setClassForm({ class_name: "", class_semester: "", course: "" });
  }, [expandedTeacherId]);

  const openAddModal = () => {
    setEditingTeacher(null);
    setTeacherForm({
      teacher_name: "",
      teacher_email: "",
      teacher_gender: "",
      teacher_classes: "",
      teacher_profession: "",
    });
    setModalOpen(true);
  };

  const openEditModal = (teacher) => {
    setEditingTeacher(teacher);
    setTeacherForm(teacher);
    setModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Bạn có chắc muốn xoá giáo viên này?")) {
      try {
        await deleteTeacher(id);
        setTeachers((prev) => prev.filter((t) => t.teacher_id !== id));
        alert("✅ Đã xoá giáo viên!");
      } catch (err) {
        console.error("❌ Lỗi khi xoá giáo viên:", err);
        alert("❌ Lỗi khi xoá!");
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTeacher) {
        await updateTeacher(editingTeacher.teacher_id, {
          ...teacherForm,
          teacher_id: editingTeacher.teacher_id,
        });
        setTeachers((prev) =>
          prev.map((t) =>
            t.teacher_id === editingTeacher.teacher_id
              ? { ...teacherForm, teacher_id: editingTeacher.teacher_id, classes: t.classes }
              : t
          )
        );
        alert("✅ Đã cập nhật giáo viên!");
      } else {
        const newTeacher = await createTeacher(teacherForm);
        setTeachers((prev) => [...prev, newTeacher]);
        alert("✅ Đã thêm giáo viên!");
      }
      setModalOpen(false);
    } catch (err) {
      console.error("❌ Lỗi khi lưu:", err);
      alert("❌ Lỗi khi lưu giáo viên!");
    }
  };

  const handleAddClass = async (teacherId) => {
    if (!classForm.class_name || !classForm.class_semester || !classForm.course) {
      alert("Vui lòng nhập đầy đủ tên lớp, học kỳ và khoá học!");
      return;
    }
    const payload = {
      class_name: classForm.class_name,
      class_semester: Number(classForm.class_semester),
      class_teacher: teacherId,
      course: Number(classForm.course),
    };
    try {
      await createClass(payload);
      alert("✅ Đã thêm lớp học!");
      setClassForm({ class_name: "", class_semester: "", course: "" });
    } catch (err) {
      console.error("❌ Lỗi khi thêm lớp:", err);
      alert("❌ Lỗi khi thêm lớp học!");
    }
  };

  const handleEditClass = async (classId, teacherId) => {
    const payload = {
      class_id: classId,
      class_name: classForm.class_name,
      class_semester: Number(classForm.class_semester),
      class_teacher: teacherId,
    };
    try {
      await updateClass(classId, payload);
      alert("✅ Đã cập nhật lớp học!");
      const refreshed = await fetch("/api/teachers");
      const data = await refreshed.json();
      setTeachers(data);
      setClassForm({ class_name: "", class_semester: "" });
      setEditingClass(null);
    } catch (err) {
      console.error("❌ Lỗi khi cập nhật lớp:", err);
      alert("❌ Lỗi khi cập nhật lớp học!");
    }
  };

  const handleDeleteClass = async (classId) => {
    if (window.confirm("Bạn có chắc muốn xoá lớp học này?")) {
      try {
        await deleteClass(classId);
        const refreshed = await fetch("/api/teachers");
        const data = await refreshed.json();
        setTeachers(data);
        alert("✅ Đã xoá lớp!");
      } catch (err) {
        console.error("❌ Lỗi khi xoá lớp:", err);
      }
    }
  };

  const filteredTeachers = teachers.filter((t) => {
    const search = searchTerm.toLowerCase();
    return (
      t.teacher_id.toString().includes(search) ||
      t.teacher_name.toLowerCase().includes(search) ||
      t.teacher_email.toLowerCase().includes(search)
    );
  });

  return (
    <div>
      <h2>Quản lý Giáo viên</h2>

      <div style={{ display: "flex", gap: "10px", marginBottom: "16px" }}>
        <Input
          placeholder="Tìm kiếm theo ID, tên hoặc email"
          onChange={(e) => setSearchTerm(e.target.value)}
          value={searchTerm}
        />
        <Button onClick={openAddModal}>➕ Thêm Giáo viên</Button>
      </div>

      {loading ? (
        <p>Đang tải danh sách giáo viên...</p>
      ) : (
        filteredTeachers.map((t) => (
          <div
            key={t.teacher_id}
            style={{ border: "1px solid #ccc", padding: "12px", marginBottom: "12px" }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <strong>{t.teacher_name}</strong> – ID: {t.teacher_id} – {t.teacher_email} ({t.teacher_gender}) – <em>{t.teacher_profession}</em>
              </div>
              <div>
                <Button
                  variant="secondary"
                  onClick={() =>
                    setExpandedTeacherId((prev) =>
                      prev === t.teacher_id ? null : t.teacher_id
                    )
                  }
                  style={{ marginRight: 8 }}
                >
                  {expandedTeacherId === t.teacher_id ? "Ẩn lớp" : "Xem lớp"}
                </Button>
                <Button variant="secondary" onClick={() => openEditModal(t)} style={{ marginRight: 8 }}>
                  Sửa
                </Button>
                <Button variant="danger" onClick={() => handleDelete(t.teacher_id)}>
                  Xoá
                </Button>
              </div>
            </div>

            {expandedTeacherId === t.teacher_id && (
              <div style={{ marginTop: "10px" }}>
                <h4>Lớp giảng dạy:</h4>
                <Input
                  placeholder="Tìm theo học kỳ"
                  value={classSearchTerm}
                  onChange={(e) => setClassSearchTerm(e.target.value)}
                  style={{ width: "200px", marginBottom: "10px" }}
                />
                {(t.classes || [])
                  .filter((cls) =>
                    classSearchTerm === "" ||
                    cls.class_semester?.toString().includes(classSearchTerm)
                  )
                  .map((cls) => (
                    <div
                      key={cls.class_id}
                      style={{
                        padding: "8px",
                        border: "1px solid #eee",
                        marginBottom: "4px",
                      }}
                    >
                      <strong>{cls.class_name}</strong> – ID: {cls.class_id} – Học kỳ: {cls.class_semester}
                      <Button
                        variant="danger"
                        onClick={() => handleDeleteClass(cls.class_id)}
                        style={{ marginLeft: "12px" }}
                      >
                        Xoá lớp
                      </Button>
                      <Button
                        variant="secondary"
                        onClick={() => {
                          setEditingClass(cls.class_id);
                          setClassForm({
                            class_name: cls.class_name,
                            class_semester: cls.class_semester?.toString() || "",
                          });
                        }}
                        style={{ marginLeft: "8px" }}
                      >
                        Sửa
                      </Button>
                    </div>
                  ))}

                <Form
                  onSubmit={(e) => {
                    e.preventDefault();
                    editingClass
                      ? handleEditClass(editingClass, t.teacher_id)
                      : handleAddClass(t.teacher_id);
                  }}
                >
                  <Input
                    label="Khoá học (course ID)"
                    value={classForm.course}
                    onChange={(e) =>
                      setClassForm({ ...classForm, course: e.target.value })
                    }
                    required
                  />
                  <Input
                    label="Tên lớp"
                    value={classForm.class_name}
                    onChange={(e) =>
                      setClassForm({ ...classForm, class_name: e.target.value })
                    }
                    required
                  />
                  <Input
                    label="Học kỳ"
                    value={classForm.class_semester}
                    onChange={(e) =>
                      setClassForm({
                        ...classForm,
                        class_semester: e.target.value,
                      })
                    }
                    required
                  />
                  <Button type="submit">
                    {editingClass ? "Cập nhật lớp" : "➕ Thêm lớp"}
                  </Button>
                </Form>
              </div>
            )}
          </div>
        ))
      )}

      <Modal
        isOpen={isModalOpen}
        onClose={() => setModalOpen(false)}
        title={editingTeacher ? "Sửa Giáo viên" : "Thêm Giáo viên"}
      >
        <Form onSubmit={handleSubmit}>
          <Input
            label="Họ và tên"
            value={teacherForm.teacher_name}
            onChange={(e) =>
              setTeacherForm({ ...teacherForm, teacher_name: e.target.value })
            }
            required
          />
          <Input
            label="Email"
            type="email"
            value={teacherForm.teacher_email}
            onChange={(e) =>
              setTeacherForm({ ...teacherForm, teacher_email: e.target.value })
            }
            required
          />
          <Input
            label="Giới tính"
            value={teacherForm.teacher_gender}
            onChange={(e) =>
              setTeacherForm({ ...teacherForm, teacher_gender: e.target.value })
            }
          />
          <Input
            label="Môn dạy"
            value={teacherForm.teacher_classes}
            onChange={(e) =>
              setTeacherForm({ ...teacherForm, teacher_classes: e.target.value })
            }
          />
          <Input
            label="Chuyên môn"
            value={teacherForm.teacher_profession}
            onChange={(e) =>
              setTeacherForm({
                ...teacherForm,
                teacher_profession: e.target.value,
              })
            }
          />
          <Button type="submit">Lưu</Button>
        </Form>
      </Modal>
    </div>
  );
};

export default ManageTeachers;
