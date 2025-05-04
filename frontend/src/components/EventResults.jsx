import React, { useState } from 'react';

const EventResults = ({ data }) => {
  return (
    <div className="space-y-4">
      {data && data.map((group, idx) => (
        <EventGroup key={idx} execId={group.exec_id} events={group.events} />
      ))}
    </div>
  );
};

const EventGroup = ({ execId, events }) => {
  return (
    <div className="border rounded p-4 shadow">
      <h2 className="text-lg font-semibold mb-2">Execution ID: {execId}</h2>
      {events
        .sort((a, b) => a.sequence_no - b.sequence_no)
        .map((event, idx) => (
          <CollapsibleEvent key={idx} event={event} />
        ))}
    </div>
  );
};

const CollapsibleEvent = ({ event }) => {
  const [expanded, setExpanded] = useState(false);

  const toggle = () => setExpanded((prev) => !prev);

  return (
    <div className="mb-2 border rounded">
      <div
        className="cursor-pointer bg-gray-100 px-4 py-2 flex justify-between items-center"
        onClick={toggle}
      >
        <span>Sequence No: {event.sequence_no}</span>
        <span>{expanded ? '▲' : '▼'}</span>
      </div>

      {expanded && (
        <div className="bg-white px-4 py-2 text-sm">
          <div className="mb-2 text-gray-600">Timestamp: {new Date(event.timestamp).toLocaleString()}</div>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b">
                <th className="pr-4">Key</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(event.data).map(([key, value], idx) => (
                <tr key={idx} className="border-b">
                  <td className="pr-4 font-medium">{key}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {event.has_clob && (
            <div className="mt-2">
              <a
                href={`/api/clob?exec_id=${event.exec_id}&sequence_no=${event.sequence_no}`}
                className="text-blue-600 underline"
              >
                Download CLOB
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EventResults;
