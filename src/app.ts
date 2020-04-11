import express from "express";
import { Request, Response } from "express";
const app = express();

app.use(express.urlencoded({ extended: true }));

import { config } from "./config";
app.use("/config", config);

app.all("/", function (_request: Request, response: Response) {
  response.send("Morph DBMS Server");
});

export { app };
