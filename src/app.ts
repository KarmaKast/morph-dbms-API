import express from "express";
import { Request, Response } from "express";
import * as morphCore from "@karmakast/morph-dbms-core";
import * as morphViz from "@karmakast/morph-dbms-viz";
import cors from "cors";
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(cors());

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
  vizSession.save(configTest.databasePath, "reset");
  res.send("Success");
});

app.post("/collection/load", function (req, res) {
  console.log(req.body);
  vizSession = morphViz.load(
    configTest.databasePath,
    req.body.collectionID,
    req.body.Label
  );
  //console.log(vizSession);
  res.send("Success");
});

app.get("/collection/get", function (req, res) {
  if (vizSession) {
    res.send(
      morphCore.Collection.condenseCollection(vizSession.sourceCollection)
    );
  } else res.status(404).send("collection hasn't been loaded yet");
});

app.post("/entity/create", function (req, res) {
  console.log(req.body);
  if (vizSession) {
    const vizPropsString = req.body.vizProps;
    //console.log(vizPropsString, JSON.parse(vizPropsString));
    if (vizPropsString && typeof vizPropsString === "string")
      res.send({
        entityID: vizSession.createEntity(JSON.parse(vizPropsString)),
      });
    else
      res.send({
        entityID: vizSession.createEntity(),
      });
  } else res.status(404).send("collection hasn't been loaded yet or no entityID provided or entity with ID does not exist");
});

app.get("/entity/get", function (req, res) {
  console.log(req.params);
  console.log(req.query);
  if (vizSession) {
    const entityID: string | undefined = req.query.entityID as
      | string
      | undefined;
    const sourceEntity = entityID
      ? vizSession.sourceCollection.Entities.get(entityID)
      : undefined;
    if (entityID && sourceEntity)
      res.send([
        morphCore.Entity.condenseEntity(sourceEntity),
        morphCore.Entity.condenseEntity(vizSession.getVizEntity(entityID)),
      ]);
    else
      res
        .status(404)
        .send("no entityID provided or entity with ID does not exist");
  } else res.status(404).send("collection hasn't been loaded yet");
});

app.post("/entity/updateLabel", function (req, res) {
  if (vizSession) {
    const entityID: string | undefined = req.params.entityID;
    const sourceEntity = entityID
      ? vizSession.sourceCollection.Entities.get(entityID)
      : undefined;
    if (entityID && sourceEntity) {
      sourceEntity.Label = req.body.Label;
      res.send("success");
    }
  } else res.status(404).send("collection hasn't been loaded yet or no entityID provided or entity with ID does not exist");
});

export { app };
