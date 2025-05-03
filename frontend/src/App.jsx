import React, { useState } from "react";
import SearchForm from "./components/SearchForm";
import EventResults from "./components/EventResults";

function App() {
  const [results, setResults] = useState([]);

  const handleSearch = async (formData) => {
    const response = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const data = await response.json();
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
