import { app } from "./app";
import http from "http";
import kill from "kill-port";

const port = 3000;

kill(port, "tcp").then(() => {
  const server = http.createServer(app).listen(port, () => {
    console.log(
      `Started Morph dbms server. Listening at http://localhost:${port}`
    );
  });
});
