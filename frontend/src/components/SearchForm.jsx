import React, { useState } from "react";

const SearchForm = ({ onSearch }) => {
  const [showQuery, setShowQuery] = useState(false);
  const [rawQuery, setRawQuery] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [filters, setFilters] = useState({
    source: "",
    environment: "",
    exec_id: "",
  });
  const [kvPairs, setKvPairs] = useState([{ key: "", value: "" }]);

  const handleKVChange = (index, field, value) => {
    const updated = [...kvPairs];
    updated[index][field] = value;
    setKvPairs(updated);
  };

  const addKVPair = () => setKvPairs([...kvPairs, { key: "", value: "" }]);

  const handleSearch = () => {
    onSearch({ rawQuery, startTime, endTime, filters, kvPairs });
  };

  return (
    <div className="p-4 bg-white rounded shadow mb-4">
      <button
        className="text-blue-600 underline mb-2"
        onClick={() => setShowQuery(!showQuery)}
      >
        {showQuery ? "Hide Raw Query Editor" : "Show Raw Query Editor"}
      </button>

      {showQuery && (
        <textarea
          className="w-full p-2 border rounded mb-4"
          rows="4"
          value={rawQuery}
          onChange={(e) => setRawQuery(e.target.value)}
          placeholder="Enter raw Splunk SPL query..."
        />
      )}

      <div className="flex gap-4 mb-4">
        <div className="flex flex-col">
          <label>Start Time</label>
          <input
            type="datetime-local"
            className="border p-1 rounded"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
        </div>
        <div className="flex flex-col">
          <label>End Time</label>
          <input
            type="datetime-local"
            className="border p-1 rounded"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-4">
        {["source", "environment", "exec_id"].map((key) => (
          <div key={key} className="flex flex-col">
            <label>{key}</label>
            <input
              className="border p-1 rounded"
              value={filters[key]}
              onChange={(e) =>
                setFilters({ ...filters, [key]: e.target.value })
              }
            />
          </div>
        ))}
      </div>

      <div className="mb-4">
        <label>Key-Value Filters</label>
        {kvPairs.map((pair, idx) => (
          <div key={idx} className="flex gap-2 mb-2">
            <input
              placeholder="Key"
              className="border p-1 rounded w-1/2"
              value={pair.key}
              onChange={(e) => handleKVChange(idx, "key", e.target.value)}
            />
            <input
              placeholder="Value"
              className="border p-1 rounded w-1/2"
              value={pair.value}
              onChange={(e) => handleKVChange(idx, "value", e.target.value)}
            />
          </div>
        ))}
        <button className="text-blue-500 underline" onClick={addKVPair}>
          + Add more
        </button>
      </div>

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleSearch}
      >
        Search
      </button>
    </div>
  );
};

export default SearchForm;
