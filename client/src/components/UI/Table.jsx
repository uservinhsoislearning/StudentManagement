const Table = ({ columns = [], data = [] }) => {
  return (
    <div style={{ overflowX: "auto", animation: "fadeIn 0.3s ease" }}>
      <table
        style={{
          width: "100%",
          borderCollapse: "separate",
          borderSpacing: "0",
          borderRadius: "8px",
          overflow: "hidden",
          marginTop: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
        }}
      >
        <thead>
          <tr>
            {columns.map((col, index) => (
              <th
                key={index}
                style={{
                  padding: "12px",
                  backgroundColor: "#2563eb",
                  color: "white",
                  fontWeight: "600",
                  textAlign: "left",
                }}
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr
              key={rowIndex}
              style={{
                backgroundColor: rowIndex % 2 === 0 ? "#f9fafb" : "white",
                transition: "background-color 0.3s",
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = "#e0f2fe"}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = rowIndex % 2 === 0 ? "#f9fafb" : "white"}
            >
              {columns.map((col, colIndex) => (
                <td
                  key={colIndex}
                  style={{
                    padding: "12px",
                    borderBottom: "1px solid #e5e7eb",
                  }}
                >
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

export default Table;