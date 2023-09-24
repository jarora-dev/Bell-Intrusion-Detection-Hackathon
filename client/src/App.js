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

  useEffect(() => {
    setTotalReceived(data.length);
    setTotalBlocked(data.filter((row) => row.requestBlocked).length);
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
        threatLevel="Medium"
        totalBlocked={totalBlocked}
        totalReceived={totalReceived}
        falsePositives={10}
        falseNegatives={5}
      />
      {/* <h1>{data.sNo}</h1> */}
      <Table data={data} />
    </div>
  );
}

export default App;
