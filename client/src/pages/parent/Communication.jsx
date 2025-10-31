import { useEffect, useState } from "react";
import { fetchMessages, sendMessage } from "../../api/parents";
import Button from "../../components/UI/Button";
import Input from "../../components/UI/Input";
import styles from "./Communication.module.css";
const Communication = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  useEffect(() => {
    fetchMessages().then(setMessages);
  }, []);

  const handleSendMessage = () => {
    if (newMessage.trim() !== "") {
      sendMessage(newMessage);
      setMessages([...messages, { sender: "Phụ huynh", text: newMessage }]);
      setNewMessage("");
    }
  };

  return (
    <div className={styles.container}>
      <h2>Giao tiếp với giáo viên</h2>
      <div style={{ maxWidth: "600px", marginBottom: "20px" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: "10px", padding: "10px", background: "#f4f4f4", borderRadius: "5px" }}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <Input
        label="Tin nhắn"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        placeholder="Nhập tin nhắn..."
      />
      <Button onClick={handleSendMessage}>Gửi</Button>
    </div>
  );
};

export default Communication;
