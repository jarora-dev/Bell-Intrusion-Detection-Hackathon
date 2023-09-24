const express = require("express");
const cors = require("cors");
const http = require("http");

const app = express();
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

io.on("connection", (socket) => {
  console.log("User connected");

  socket.on("send-data", (data) => {
    console.log(data);
    io.emit("update-data", data);
  });

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });
});

app.get("/test", (req, res) => {
  res.json({ message: "Hello from the server!" });
});

const PORT = 5000;
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
