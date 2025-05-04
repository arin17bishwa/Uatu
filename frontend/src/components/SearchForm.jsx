import React, { useState } from 'react';

const SearchForm = ({ onSearch }) => {
  const [rawQuery, setRawQuery] = useState('');
  const [earliest, setEarliest] = useState('');
  const [latest, setLatest] = useState('');
  const [source, setSource] = useState('');
  const [environment, setEnvironment] = useState('');
  const [executionId, setExecutionId] = useState('');
  const [kvFilters, setKvFilters] = useState([{ key: '', value: '' }]);

  const handleKvChange = (index, field, value) => {
    const newFilters = [...kvFilters];
    newFilters[index][field] = value;
    setKvFilters(newFilters);
  };

  const addKvFilter = () => {
    setKvFilters([...kvFilters, { key: '', value: '' }]);
  };

  const removeKvFilter = (index) => {
    setKvFilters(kvFilters.filter((_, i) => i !== index));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      raw_query: rawQuery,
      time_range: {
        earliest,
        latest
      },
      source,
      environment,
      execution_id: executionId,
      kv_filters: kvFilters.filter(f => f.key && f.value)
    };
    onSearch(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <textarea placeholder="Raw Splunk Query" value={rawQuery} onChange={(e) => setRawQuery(e.target.value)} className="w-full p-2 border" />
      <input type="text" placeholder="Earliest Time" value={earliest} onChange={(e) => setEarliest(e.target.value)} className="w-full p-2 border" />
      <input type="text" placeholder="Latest Time" value={latest} onChange={(e) => setLatest(e.target.value)} className="w-full p-2 border" />
      <input type="text" placeholder="Source" value={source} onChange={(e) => setSource(e.target.value)} className="w-full p-2 border" />
      <input type="text" placeholder="Environment" value={environment} onChange={(e) => setEnvironment(e.target.value)} className="w-full p-2 border" />
      <input type="text" placeholder="Execution ID" value={executionId} onChange={(e) => setExecutionId(e.target.value)} className="w-full p-2 border" />

      <div>
        <label className="block mb-2">Key-Value Filters</label>
        {kvFilters.map((filter, index) => (
          <div key={index} className="flex space-x-2 mb-2">
            <input
              type="text"
              placeholder="Key"
              value={filter.key}
              onChange={(e) => handleKvChange(index, 'key', e.target.value)}
              className="p-2 border w-1/2"
            />
            <input
              type="text"
              placeholder="Value"
              value={filter.value}
              onChange={(e) => handleKvChange(index, 'value', e.target.value)}
              className="p-2 border w-1/2"
            />
            <button type="button" onClick={() => removeKvFilter(index)} className="text-red-600">Remove</button>
          </div>
        ))}
        <button type="button" onClick={addKvFilter} className="text-blue-600">Add Filter</button>
      </div>

      <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">Search</button>
    </form>
  );
};

export default SearchForm;
