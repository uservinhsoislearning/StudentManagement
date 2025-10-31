import { useContext } from "react";
import { ParentContext } from "../context/ParentContext";

/**
 * Custom hook dùng để truy cập ParentContext.
 */
const useParents = () => {
  const context = useContext(ParentContext);
  if (!context) {
    throw new Error("useParents must be used within a ParentProvider");
  }
  return context;
};

export default useParents;
