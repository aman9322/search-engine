import { useEffect, useState } from "react";
import axios from "./api/axios";

export default function Home() {
  const [myData, setMyData] = useState([]);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");

  const getData = async () => {
    try {
      const res = await axios.post("/", JSON.stringify({ query: query }), {
        headers: { "Content-Type": "application/json" },
      });
      const transformedData = res.data.map((obj) => Object.values(obj)[0]); // Transforming data to extract values from each object
      setMyData(transformedData);
    } catch (error) {
      setError(error.message);
      console.error(error);
    }
  };

  useEffect(() => {
    // getData();  // Optionally call on mount
  }, []);

  const onKeyDownHandler = (e) => {
    if (e.keyCode === 13) {
      e.preventDefault();
      getData();
    }
  };

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  return (
    <div className="container mx-auto p-4 bg-emerald-800">
      <form
        className="flex justify-between items-center mb-4"
        onKeyDown={onKeyDownHandler}
        onSubmit={(e) => e.preventDefault()}
      >
        <input
          type="text"
          class="bg-stone-500 shadow-2xl text-gray-50 font-bold py-2 px-4 rounded"
          className="form-input px-4 py-2 border rounded"
          placeholder="Search..."
          value={query}
          onChange={handleInputChange}
        />
        <button
          type="submit"
          className="bg-blue-500 shadow-2xl hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={getData}
        >
          Send
        </button>
      </form>
      <div>
        {myData.length > 0 && (
          <ul className="list-disc space-y-2">
            {myData.map((item, index) => (
              <li key={index} className="bg-stone-500 shadow-2xl p-2 rounded">
                <a
                  href={item.Link}
                  target="_blank"
                  className="text-blue-500 shadow-2xl hover:underline"
                >
                  {item.Title} - Score: {item.Score}
                </a>
              </li>
            ))}
          </ul>
        )}
        {error && <p className="text-red-500">{error}</p>}
      </div>
    </div>
  );
}
