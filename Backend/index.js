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

const fs = require("fs");
const PDFParser = require("pdf-parse");

/* // Function to read and parse PDF file
function extractDataFromPDF(pdfPath) {
  return new Promise((resolve, reject) => {
    fs.readFile(pdfPath, (err, data) => {
      if (err) {
        reject(err);
        return;
      }

      // Using pdf-parse to extract text from PDF
      PDFParser(data)
        .then((pdf) => {
          const text = pdf.text; // Extracted text from PDF
          console.log("Extracted text:", text);

          // Example: Parsing extracted text to find specific data
          const ageRegex = /Age:\s*(\d+)/i;
          const sexRegex = /Sex:\s*(\d+)/i;
          const chestRegex = /Chest pain type:\s*(\d+)/i;

          const ageMatch = text.match(ageRegex);
          const sexMatch = text.match(sexRegex);
          const chestMatch = text.match(chestRegex);

          const extractedData = {
            age: ageMatch ? parseInt(ageMatch[1]) : null,
            /*  sex: sexMatch ? sexMatch[1] : null,
            chest: chestMatch ? parseInt(chestMatch[1]) : null, 
            // Add more fields as needed
          };

          resolve(extractedData);
        })
        .catch((error) => {
          reject(error);
        });
    });
  });
}

// Usage: Replace 'example.pdf' with your actual PDF file path
extractDataFromPDF("HeartDiseaseReport.pdf")
  .then((data) => {
    console.log("Extracted data:", data);
    // Pass 'data' to your machine learning model or further processing
  })
  .catch((error) => {
    console.error("Error extracting data from PDF:", error);
  });
 */
app.listen(8080, () => {
  console.log(`Listening to app at PORT 8080`);
});
