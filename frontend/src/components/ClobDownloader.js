import React, { useState } from "react";

const ClobDownloader = ({ execId, sequenceNo }) => {
  const [status, setStatus] = useState("idle"); // idle, loading, notfound

  const handleDownload = async () => {
    setStatus("loading");

    const response = await fetch(
      `/api/clob?exec_id=${execId}&sequence_no=${sequenceNo}`
    );

    if (!response.ok) {
      setStatus("notfound");
      return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${execId}_${sequenceNo}.txt`;
    a.click();
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
