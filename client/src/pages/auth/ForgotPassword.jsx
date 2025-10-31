import { useState } from "react";
import { forgotPassword } from "../../api/auth";
import Form from "../../components/UI/Form";
import Input from "../../components/UI/Input";
import Button from "../../components/UI/Button";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await forgotPassword(email);
      setMessage("Kiểm tra email của bạn để đặt lại mật khẩu.");
    } catch (err) {
      setMessage("Lỗi: Không thể đặt lại mật khẩu!");
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <h2>Quên mật khẩu</h2>
      {message && <p style={{ color: "green" }}>{message}</p>}
      <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <Button type="submit">Gửi yêu cầu</Button>
    </Form>
  );
};

export default ForgotPassword;
