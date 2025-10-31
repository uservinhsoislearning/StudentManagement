import { useState, useEffect } from "react";
import axios from "axios";

/**
 * Hook dùng để fetch dữ liệu từ API.
 * @param {string} url - Endpoint API cần fetch.
 * @returns {Object} { data, loading, error }
 */
const useFetch = (url) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(url);
        setData(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
};

export default useFetch;
