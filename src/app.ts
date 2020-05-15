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
  const label = req.body.Label;
  console.log("label : ", label);

  vizSession = new morphViz.Viz(label);
  res.send("Success");
});

app.post("/collection/save", function (req, res) {
  vizSession.save(configTest.databasePath, "reset");
  res.send("Success");
});

app.post("/collection/clear", function (req, res) {
  vizSession.clear();
  res.send("Success");
});

app.post("/collection/load", function (req, res) {
  console.log(req.body);
  vizSession = morphViz.load(
    configTest.databasePath,
    req.body.collectionID,
    req.body.Label
  );
  morphCore.Collection.describe(vizSession.sourceCollection);
  //console.log(vizSession);
  res.send("Success");
});

app.get("/collection/get", function (req, res) {
  if (vizSession) {
    //morphCore.Collection.describe(vizSession.sourceCollection);
    //morphCore.Collection.describe(vizSession.vizCollection);
    const temp: any = morphCore.Collection.condenseCollection(
      vizSession.sourceCollection
    );
    temp.Relations = {};
    vizSession.sourceCollection.Relations.forEach((value, key) => {
      //
      temp.Relations[value.ID] = value.Label;
    });
    //console.log(temp);
    res.send(temp);
  } else res.status(400).send("collection hasn't been loaded yet");
});

app.get("/collection/getRelation", function (req, res) {
  if (vizSession) {
    //morphCore.Collection.describe(vizSession.sourceCollection);
    //morphCore.Collection.describe(vizSession.vizCollection);
    res.send(vizSession.sourceCollection.Relations.get(req.body.relationID));
  } else res.status(400).send("collection hasn't been loaded yet");
});

app.post("/collection/updateRelation", function (req, res) {
  if (vizSession) {
    console.log("updateRelation: ", req.query, req.body);
    const relationID = req.query.relationID as
      | morphCore.Structs.Relation["ID"]
      | undefined;
    const relationLabel = req.body
      .relationLabel as morphCore.Structs.Relation["Label"];
    if (relationID) {
      const relation = {
        ID: relationID,
        Label: relationLabel,
      };
      vizSession.sourceCollection.Relations.set(relationID, relation);
    }
    res.send("success");
  } else res.status(400).send("collection hasn't been loaded yet");
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
  } else res.status(404).send("collection hasn't been loaded yet");
});

app.post("/entity/remove", function (req, res) {
  console.log(req.body);
  if (vizSession) {
    const entityID: string | undefined = req.body.entityID as
      | string
      | undefined;
    let result;

    if (entityID) {
      //morphCore.Collection.describe(vizSession.sourceCollection);
      result = vizSession.removeEntity(entityID);
      //morphCore.Collection.describe(vizSession.sourceCollection);
      res.send({
        msg: "success",
        claimantIDs: result,
      });
    }

    //console.log(vizPropsString, JSON.parse(vizPropsString));
  } else res.status(404).send("collection hasn't been loaded yet");
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
    if (entityID && sourceEntity) {
      //morphCore.Entity.describe(sourceEntity);
      res.send([
        morphCore.Entity.condenseEntity(sourceEntity),
        morphCore.Entity.condenseEntity(vizSession.getVizEntity(entityID)),
      ]);
    } else
      res
        .status(404)
        .send("no entityID provided or entity with ID does not exist");
  } else res.status(404).send("collection hasn't been loaded yet");
});

function cleanUnusedEmptyRel(): void {
  //
}

app.post("/entity/addRelClaim", function (req, res) {
  console.log(req.body);
  if (vizSession) {
    const claimantID: string | undefined = req.body.claimantID as
      | string
      | undefined;
    const targetID: string | undefined = req.body.targetID as
      | string
      | undefined;

    if (claimantID && targetID) {
      const tempRel = morphCore.createRelation("");
      vizSession.sourceCollection.Relations.set(tempRel.ID, tempRel);
      const claimant = vizSession.sourceCollection.Entities.get(claimantID);
      const target = vizSession.sourceCollection.Entities.get(targetID);
      if (claimant && target) {
        morphCore.Entity.claimRelation(
          tempRel,
          morphCore.Direction.SelfToTarget,
          claimant,
          target
        );
        res.send({
          msg: "success",
          relClaim: JSON.stringify({
            Direction: morphCore.Direction.SelfToTarget,
            To: target.ID,
            Relation: tempRel.ID,
          } as morphCore.Structs.RelationClaimDense),
        });
      }
      //morphCore.Collection.describe(vizSession.sourceCollection);
    }
  } else res.status(404).send("collection hasn't been loaded yet");
});

app.post("/entity/updateLabel", function (req, res) {
  if (vizSession) {
    console.log(req.query, req.body);
    const entityID: string | undefined = req.query.entityID as
      | string
      | undefined;
    const sourceEntity = entityID
      ? vizSession.sourceCollection.Entities.get(entityID)
      : undefined;
    if (entityID && sourceEntity) {
      sourceEntity.Label = req.body.Label;
      res.send("success");
    } else
      res
        .status(404)
        .send("no entityID provided or entity with ID does not exist");
  } else res.status(404).send("collection hasn't been loaded yet");
});

app.post("/entity/updateProps", function (req, res) {
  if (vizSession) {
    console.log(req.query, req.body);
    const entityID: string | undefined = req.query.entityID as
      | string
      | undefined;
    const vizEntity = entityID ? vizSession.getVizEntity(entityID) : undefined;
    const props = JSON.parse(req.body.props);
    console.log(props);
    if (entityID && vizEntity) {
      Object.keys(props).forEach((key) => {
        if (vizEntity.Data) {
          console.log("before : ", vizEntity.Data);
          vizEntity.Data.set(key, props[key]);
          console.log("after : ", vizEntity.Data);
        }
      });
      res.send("success");
    } else
      res
        .status(404)
        .send("no entityID provided or entity with ID does not exist");
  } else res.status(404).send("collection hasn't been loaded yet");
});

function sendAndSleep(response: Response, counter: number): void {
  if (counter > 10) {
    response.end();
  } else {
    response.write({ i: counter });
    counter++;
    setTimeout(function () {
      sendAndSleep(response, counter);
    }, 1000);
  }
}

app.get("/stream", function (req, res) {
  //when using text/plain it did not stream
  //without charset=utf-8, it only worked in Chrome, not Firefox
  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "Transfer-Encoding": "chunked",
  });
  //res.setHeader("Transfer-Encoding", "chunked");

  res.write("Thinking...");
  sendAndSleep(res, 1);
});

export { app };
