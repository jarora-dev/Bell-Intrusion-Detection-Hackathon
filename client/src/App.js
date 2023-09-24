import React, { useState, useEffect } from "react";
import Header from "./Header";
import Table from "./Table";
import Dashboard from "./Dashboard";
import "./styles.css";
import socketIOClient from "socket.io-client";

const ENDPOINT = "http://localhost:5000";
const socket = socketIOClient(ENDPOINT);

function App() {
  const [data, setData] = useState([]);
  const [totalReceived, setTotalReceived] = useState(0);
  const [totalBlocked, setTotalBlocked] = useState(0);
  const [threatLevel, setThreatLevel] = useState("");
  const [falsePositives, setFalsePositives] = useState(0);
  const [falseNegatives, setFalseNegatives] = useState(0);

  useEffect(() => {
    setTotalReceived(data.length);
    setTotalBlocked(data.filter((row) => row.requestBlocked).length);
    //Set threat level to high if more than 50% of requests are blocked from the last 100 requests
    if (totalBlocked / totalReceived > 0.5) {
      setThreatLevel("High");
    }
    //Set threat level to medium if more than 25% of requests are blocked from the last 100 requests
    else if (totalBlocked / totalReceived > 0.25) {
      setThreatLevel("Medium");
    }
    //Set threat level to low if less than 25% of requests are blocked from the last 100 requests
    else {
      setThreatLevel("Low");
    }
    // Set False Positives and False Negatives
    setFalsePositives(
      data.filter((row) => row.requestBlocked && !row.requestMalicious).length
    );
    setFalseNegatives(
      data.filter((row) => !row.requestBlocked && row.requestMalicious).length
    );
  }, [data]);

  useEffect(() => {
    const handleUpdateData = (receivedData) => {
      console.log("connected");
      console.log(receivedData);
      setData((prevData) => [...prevData, receivedData]);
    };

    const handleConnectError = (err) => {
      console.log(`connect_error due to ${err.message}`);
    };

    socket.on("update-data", handleUpdateData);
    socket.on("connect_error", handleConnectError);

    return () => {
      socket.off("update-data", handleUpdateData);
      socket.off("connect_error", handleConnectError);
    };
  }, []);

  return (
    <div>
      <Header />

      <Dashboard
        threatLevel={threatLevel}
        totalBlocked={totalBlocked}
        totalReceived={totalReceived}
        falsePositives={falsePositives}
        falseNegatives={falseNegatives}
      />
      {/* <h1>{data.sNo}</h1> */}
      <Table data={data} />
    </div>
  );
}

export default App;
