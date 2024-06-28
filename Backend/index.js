const express = require("express");
const app = express();
const { spawn } = require("child_process");

app.use(express.json());

app.post("/predict", (req, res) => {
  try {
    const { p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13 } = req.body;

    const python = spawn("python", [
      "predict.py",
      p1,
      p2,
      p3,
      p4,
      p5,
      p6,
      p7,
      p8,
      p9,
      p10,
      p11,
      p12,
      p13,
    ]);

    let predictionVal = "";

    python.stdout.on("data", (data) => {
      console.log("python stdout: ", data.toString());
      predictionVal = data.toString().trim();
    });

    python.stderr.on("data", (data) => {
      console.error("python stderr: ", data.toString());
    });

    python.on("close", (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
        res.status(500).json({ message: "Python script error" });
      } else {
        console.log("predictionVal: ", predictionVal);
        console.log(typeof predictionVal);
        if (predictionVal === "1")
          console.log("The person is suffering from Heart Disease");
        else if (predictionVal === "0")
          console.log("The person is not suffering from Heart Disease");
        res.json({ prediction: predictionVal.trim() });
      }
    });
  } catch (error) {
    console.error("Error", error);
    res.status(500).json({ message: "Failed to predict" });
  }
});

app.listen(8080, () => {
  console.log(`Listening to app at PORT 8080`);
});
