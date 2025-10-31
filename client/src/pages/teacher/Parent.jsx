import { useEffect, useState } from "react";
import { fetchAllParents } from "../../api/teachers";

const ParentList = () => {
    const [parents, setParents] = useState([]);

    useEffect(() => {
        const loadParents = async () => {
            try {
                const data = await fetchAllParents();
                setParents(data);
            } catch (err) {
                console.error("❌ Lỗi khi tải danh sách phụ huynh:", err);
            }
        };
        loadParents();
    }, []);

    return (
        <div>
            <h2>Danh sách phụ huynh</h2>
            <ul>
                {parents.map((p) => (
                    <li key={p.id}>
                        {p.name} - {p.email} - {p.phone}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ParentList;