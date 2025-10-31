import { useContext, useEffect, useState } from "react";
import { updateCurrentUser } from "../../api/auth";
import Button from "../../components/UI/Button";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";

const Profile = () => {
    const { user, setUser } = useContext(AuthContext);
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        phone: "",
        address: "",
    });
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (user) {
            setFormData({
                name: user.name || "",
                email: user.email || "",
                phone: user.phone || "",
                address: user.address || "",
            });
        }
    }, [user]);

    const handleChange = (e) => {
        setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const updated = await updateCurrentUser(formData);
            setUser(updated); // cập nhật vào context
            setMessage("Cập nhật thông tin thành công!");
        } catch (err) {
            console.error(err);
            setMessage("Đã xảy ra lỗi khi cập nhật.");
        }
    };

    return (
        <div>
            <h2>Thông tin cá nhân</h2>

            <Form onSubmit={handleSubmit}>
                <Input
                    label="Họ và tên"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                />
                <Input
                    label="Email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                <Input
                    label="Số điện thoại"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                />
                <Input
                    label="Địa chỉ"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                />

                <Button type="submit">Lưu thông tin</Button>

                {message && <p style={{ marginTop: "10px" }}>{message}</p>}
            </Form>
        </div>
    );
};

export default Profile;