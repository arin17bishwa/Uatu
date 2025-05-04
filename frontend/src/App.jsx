import React, { useState, useEffect } from "react";
import SearchForm from "./components/SearchForm";
import EventResults from "./components/EventResults";
const API_HOST = "http://localhost:8002";

function App() {
  const [results, setResults] = useState([]);

  const handleSearch = async (formData) => {
  console.log(formData)
    const response = await fetch(`${API_HOST}/api/splunk`, {      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const data = await response.json();
    console.log(data)
    setResults(data); // assume backend returns grouped data
  };

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold text-center">Splunk Event Search</h1>
      <SearchForm onSearch={handleSearch} />
      <EventResults data={results} />
    </div>
  );
}

export default App;
