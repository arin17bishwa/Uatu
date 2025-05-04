import React, { useState } from "react";
const API_HOST = "http://localhost:8002";

const ClobDownloader = ({ execId, sequenceNo }) => {
  const [status, setStatus] = useState("idle"); // idle, loading, notfound

  const handleDownload = async () => {
    setStatus("loading");

    const response = await fetch(`${API_HOST}/api/clob/${execId}/${sequenceNo}`);
    console.log(response.status)
    if (!response.ok) {
      if (response.status === 404) {
        setStatus("notfound");
      } else {
        setStatus("error");
      }
      return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${execId}_${sequenceNo}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
    setStatus("idle");
  };

  if (status === "notfound") return <span className="text-red-600">Not found</span>;

  return (
    <button
      className="text-blue-600 underline text-sm"
      onClick={handleDownload}
      disabled={status === "loading"}
    >
      {status === "loading" ? "Checking..." : "Download CLOB"}
    </button>
  );
};

export default ClobDownloader;