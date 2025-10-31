import { useState } from "react";
import AnimatedPageWrapper from "../components/AnimatedPageWrapper";
import Footer from "../components/Layout/Footer";
import Header from "../components/Layout/Header";
import Sidebar from "../components/Layout/Sidebar";
import styles from "../styles/layout.module.css";

const TeacherLayout = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <div className={`${styles.sidebar} ${collapsed ? styles.collapsed : styles.expanded}`}>
        <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />
      </div>

      {/* Main content */}
      <div
        className={`${styles.mainContent} ${collapsed ? styles.collapsed : styles.expanded}`}
        style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
      >
        <Header />
        <div style={{ flex: 1 }}>
          <AnimatedPageWrapper>{children}</AnimatedPageWrapper>
        </div>
        <Footer />
      </div>
    </div>
  );
};

export default TeacherLayout;