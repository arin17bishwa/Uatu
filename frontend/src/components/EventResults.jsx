import React from "react";
import ClobDownloader from "./ClobDownloader";

const EventResults = ({ data }) => {
  return (
    <div className="space-y-4">
      {data.map((group) => (
        <div key={group.exec_id} className="border p-4 rounded bg-gray-50">
          <h3 className="text-lg font-bold mb-2">Exec ID: {group.exec_id}</h3>
          <ul className="space-y-2">
            {group.events
              .sort((a, b) => a.sequence_no - b.sequence_no)
              .map((event, idx) => (
                <li
                  key={idx}
                  className="flex justify-between items-center bg-white p-2 rounded shadow"
                >
                  <div>
                    <div className="text-sm text-gray-600">
                      Seq: {event.sequence_no}
                    </div>
                    <div>{event.message}</div>
                  </div>
                  <ClobDownloader
                    execId={group.exec_id}
                    sequenceNo={event.sequence_no}
                  />
                </li>
              ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default EventResults;
