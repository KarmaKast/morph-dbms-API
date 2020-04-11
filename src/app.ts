import express from "express";
import { Request, Response } from "express";
import * as morphCore from "@karmakast/morph-dbms-core";
import * as morphViz from "@karmakast/morph-dbms-viz";
const app = express();

app.use(express.urlencoded({ extended: true }));

import { config } from "./config";
app.use("/config", config);
const configTest = {
  databasePath: "./data",
};

app.all("/", function (_request: Request, response: Response) {
  response.send("Morph DBMS Server");
});

let vizSession: morphViz.Viz;
app.post("/collection/create", function (req, res) {
  const label = req.body.label;
  console.log("label : ", label);

  vizSession = new morphViz.Viz(label);
  res.send("Success");
});

app.post("/collection/save", function (req, res) {
  vizSession.save(configTest.databasePath);
  res.send("Success");
});

app.post("/collection/load", function (req, res) {
  vizSession = morphViz.load(
    configTest.databasePath,
    req.body.collectionID,
    req.body.label
  );
  res.send("Success");
});

app.get("/collection/get", function (req, res) {
  if (vizSession) {
    res.send(
      morphCore.Collection.condenseCollection(vizSession.sourceCollection)
    );
  } else res.send("collection hasn't been loaded yet");
});

export { app };
