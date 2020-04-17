import { app } from "./app";
import http from "http";

const port = 3000;

const server = http.createServer(app).listen(port, () => {
  console.log(
    `Started Morph dbms server. Listening at http://localhost:${port}`
  );
});
