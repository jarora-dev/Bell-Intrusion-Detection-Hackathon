import React from "react";

function Table({ data }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Originating IP</th>
            <th>Protocol</th>
            <th>Service State</th>
            <th>Source Packets</th>
            <th>Source Bytes</th>
            <th>Request Blocked?</th>
            <th>Request Malicious?</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr
              key={index}
              style={{ backgroundColor: row.requestBlocked ? "red" : "" }}
            >
              <td>{row.requestData.sNo}</td>
              <td>{row.requestData.originatingIP}</td>
              <td>{row.requestData.protocol}</td>
              <td>{row.requestData.serviceState}</td>
              <td>{row.requestData.sourcePackets}</td>
              <td>{row.requestData.sourceBytes}</td>
              <td>{row.requestBlocked ? "Yes" : "No"}</td>
              <td>{row.requestMalicious ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
