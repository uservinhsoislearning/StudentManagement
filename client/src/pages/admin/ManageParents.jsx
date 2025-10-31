import useParents  from "../../hooks/useParent";
import Table from "../../components/UI/Table";
import Button from "../../components/UI/Button";
import Modal from "../../components/UI/Modal";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import { useState } from "react";

const ManageParents = () => {
  const { parents, setParents } = useParents();
  const [isModalOpen, setModalOpen] = useState(false);
  const [newParent, setNewParent] = useState({ name: "", email: "", phone: "" });

  const handleDelete = (id) => {
    setParents(parents.filter((parent) => parent.id !== id));
  };

  const handleAddParent = (e) => {
    e.preventDefault();
    setParents([...parents, { id: parents.length + 1, ...newParent }]);
    setModalOpen(false);
  };

  return (
    <div>
      <h2>Quản lý Phụ huynh</h2>
      <Button onClick={() => setModalOpen(true)}>Thêm Phụ huynh</Button>
      <Table
        columns={["ID", "Họ và tên", "Email", "Số điện thoại", "Hành động"]}
        data={parents.map((parent) => ({
          ...parent,
          action: <Button onClick={() => handleDelete(parent.id)}>Xóa</Button>,
        }))}
      />

      {/* Modal Thêm Phụ huynh */}
      <Modal isOpen={isModalOpen} onClose={() => setModalOpen(false)} title="Thêm Phụ huynh">
        <Form onSubmit={handleAddParent}>
          <Input label="Họ và tên" value={newParent.name} onChange={(e) => setNewParent({ ...newParent, name: e.target.value })} />
          <Input label="Email" type="email" value={newParent.email} onChange={(e) => setNewParent({ ...newParent, email: e.target.value })} />
          <Input label="Số điện thoại" type="tel" value={newParent.phone} onChange={(e) => setNewParent({ ...newParent, phone: e.target.value })} />
          <Button type="submit">Lưu</Button>
        </Form>
      </Modal>
    </div>
  );
};

export default ManageParents;
